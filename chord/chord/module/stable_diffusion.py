import torch
from torchvision.transforms import v2

from diffusers import UNet2DConditionModel, AutoencoderKL, DDIMScheduler
from transformers import CLIPTextModel, CLIPTextConfig, CLIPTokenizer

from . import register
from .base import Base


def apply_padding(model, mode):
    for layer in [layer for _, layer in model.named_modules() if isinstance(layer, torch.nn.Conv2d)]:
        if mode == 'circular':
            layer.padding_mode = 'circular'
        else:
            layer.padding_mode = 'zeros'
    return model

def freeze(model):
    model = model.eval()
    for param in model.parameters():
        param.requires_grad = False
    return model

@register("stable_diffusion")
class StableDiffusion(Base):
    def setup(self):
        hf_key = self.config.get("hf_key", None)
        self.device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        fp16 = self.config.get("fp16", True)
        self.dtype = torch.bfloat16 if fp16 else torch.float32
        vae_padding = self.config.get("vae_padding", "zeros")

        self.sd_version = self.config.get("version", 2.1)
        # Force local files only for ComfyUI Desktop compatibility
        # This prevents API calls that may be blocked in Desktop
        local_files_only = True
        if hf_key is not None:
            print(f"[ComfyUI-Chord] Using hugging face custom model key: {hf_key}")
            model_key = hf_key
        elif str(self.sd_version) == "2.1":
            # model_key = "stabilityai/stable-diffusion-2-1"
            # StabilityAI deleted the original 2.1 model from HF, use a community version
            model_key = "RedbeardNZ/stable-diffusion-2-1-base"
            print(f"[ComfyUI-Chord] Loading Stable Diffusion 2.1 from local cache only")
            print(f"[ComfyUI-Chord] Model key: {model_key}")
            
            # Check if model is cached
            import os
            cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
            model_cache_name = f"models--{model_key.replace('/', '--')}"
            model_cache_path = os.path.join(cache_dir, model_cache_name)
            
            if not os.path.exists(model_cache_path):
                error_msg = f"\n[ComfyUI-Chord] ⚠️  Stable Diffusion 2.1 is NOT cached locally.\n"
                error_msg += f"Cache path: {model_cache_path}\n\n"
                error_msg += f"📥 SOLUTION: Download Stable Diffusion 2.1 first (requires internet):\n"
                error_msg += f"   1. Run ComfyUI Portable once - it will automatically cache the model\n"
                error_msg += f"   2. Or use Hugging Face CLI:\n"
                error_msg += f"      huggingface-cli download {model_key}\n"
                error_msg += f"   3. Or manually download from:\n"
                error_msg += f"      https://huggingface.co/{model_key}\n\n"
                error_msg += f"After downloading, restart ComfyUI Desktop and it will work offline.\n"
                print(error_msg)
                raise FileNotFoundError(error_msg)
            else:
                print(f"[ComfyUI-Chord] ✓ Model cache found at: {model_cache_path}")
        else:
            raise ValueError(
                f"Stable-diffusion version {self.sd_version} not supported."
            )

        # Load components separately to avoid download unnecessary weights
        # All loads use local_files_only=True to prevent API calls in ComfyUI Desktop
        # Note: load_config() doesn't support local_files_only, so we need to catch network errors
        import os
        from huggingface_hub import snapshot_download
        
        # Check if model is cached
        cache_dir = os.path.expanduser("~/.cache/huggingface/hub")
        model_cache_name = f"models--{model_key.replace('/', '--')}"
        model_cache_path = os.path.join(cache_dir, model_cache_name)
        
        if local_files_only and not os.path.exists(model_cache_path):
            error_msg = f"[ComfyUI-Chord] ERROR: Stable Diffusion 2.1 is not cached locally.\n"
            error_msg += f"Cache path checked: {model_cache_path}\n\n"
            error_msg += f"SOLUTION: You need to download Stable Diffusion 2.1 first.\n"
            error_msg += f"Option 1: Run ComfyUI Portable once - it will automatically cache the model.\n"
            error_msg += f"Option 2: Use Hugging Face CLI:\n"
            error_msg += f"  huggingface-cli download {model_key} --local-dir {model_cache_path}\n"
            error_msg += f"Option 3: Manually download from: https://huggingface.co/{model_key}\n"
            print(error_msg)
            raise RuntimeError(error_msg)
        
        try:
            # 1. UNet (diffusion backbone)
            print(f"[ComfyUI-Chord] Loading UNet config...")
            try:
                unet_config = UNet2DConditionModel.load_config(model_key, subfolder="unet", local_files_only=local_files_only)
            except TypeError:
                # load_config doesn't support local_files_only, but will use cache if available
                unet_config = UNet2DConditionModel.load_config(model_key, subfolder="unet")
            self.unet = UNet2DConditionModel.from_config(unet_config, local_files_only=local_files_only)
            self.unet.to(self.device, dtype=self.dtype).eval()
            print(f"[ComfyUI-Chord] UNet loaded successfully")
            
            # 2. VAE (image autoencoder)
            print(f"[ComfyUI-Chord] Loading VAE config...")
            try:
                vae_config = AutoencoderKL.load_config(model_key, subfolder="vae", local_files_only=local_files_only)
            except TypeError:
                vae_config = AutoencoderKL.load_config(model_key, subfolder="vae")
            self.vae = AutoencoderKL.from_config(vae_config, local_files_only=local_files_only)
            self.vae.to(self.device, dtype=self.dtype).eval()
            self.vae = apply_padding(freeze(self.vae), vae_padding)
            print(f"[ComfyUI-Chord] VAE loaded successfully")
            
            # 3. Text encoder (CLIP)
            print(f"[ComfyUI-Chord] Loading CLIP text encoder config...")
            text_encoder_config = CLIPTextConfig.from_pretrained(model_key, subfolder="text_encoder", local_files_only=local_files_only)
            self.text_encoder = CLIPTextModel(text_encoder_config)
            self.text_encoder.to(self.device, dtype=self.dtype).eval()
            print(f"[ComfyUI-Chord] CLIP text encoder loaded successfully")
            
            # 4. Tokenizer (CLIP tokenizer, this one has vocab so from_pretrained is needed)
            print(f"[ComfyUI-Chord] Loading CLIP tokenizer...")
            self.tokenizer = CLIPTokenizer.from_pretrained(model_key, subfolder="tokenizer", local_files_only=local_files_only)
            print(f"[ComfyUI-Chord] CLIP tokenizer loaded successfully")
            
            # 5. Scheduler
            print(f"[ComfyUI-Chord] Loading scheduler config...")
            try:
                scheduler_config = DDIMScheduler.load_config(model_key, subfolder="scheduler", local_files_only=local_files_only)
            except TypeError:
                scheduler_config = DDIMScheduler.load_config(model_key, subfolder="scheduler")
            scheduler_config["prediction_type"] = "v_prediction"
            scheduler_config["timestep_spacing"] = "trailing"
            scheduler_config["rescale_betas_zero_snr"] = True
            self.scheduler = DDIMScheduler.from_config(scheduler_config)
            print(f"[ComfyUI-Chord] Scheduler loaded successfully")
            print(f"[ComfyUI-Chord] Stable Diffusion 2.1 components loaded successfully from local cache")
        except Exception as e:
            # Check if it's a network/connection error
            error_str = str(e).lower()
            if "couldn't connect" in error_str or "connection" in error_str or "network" in error_str:
                error_msg = f"[ComfyUI-Chord] ERROR: Cannot connect to Hugging Face and model not cached.\n"
                error_msg += f"Error: {str(e)}\n\n"
                error_msg += f"SOLUTION: You need to download Stable Diffusion 2.1 first (requires internet).\n"
                error_msg += f"Option 1: Run ComfyUI Portable once with internet - it will cache the model.\n"
                error_msg += f"Option 2: Use Hugging Face CLI (requires internet):\n"
                error_msg += f"  huggingface-cli download {model_key}\n"
                error_msg += f"Option 3: Manually download from: https://huggingface.co/{model_key}\n"
                error_msg += f"Cache location: {model_cache_path}\n"
                error_msg += f"\nAfter downloading, restart ComfyUI Desktop and it will work offline.\n"
            else:
                error_msg = f"[ComfyUI-Chord] ERROR: Failed to load Stable Diffusion 2.1 components.\n"
                error_msg += f"Error: {str(e)}\n"
            print(error_msg)
            raise RuntimeError(error_msg) from e

    def encode_text(self, prompt, padding_mode="do_not_pad"):
        # prompt: [str]
        inputs = self.tokenizer(
            prompt,
            padding=padding_mode,
            max_length=self.tokenizer.model_max_length,
            return_tensors="pt",
        )
        embeddings = self.text_encoder(inputs.input_ids.to(self.device))[0]
        return embeddings    

    def decode_latents(self, latents):
        latents = 1 / self.vae.config.scaling_factor * latents
        imgs = self.vae.decode(latents).sample
        imgs = (imgs / 2 + 0.5).clamp(0, 1)
        return imgs

    def encode_imgs(self, imgs):
        if imgs.shape[1] == 1: # for grayscale maps
            imgs = v2.functional.grayscale_to_rgb(imgs)
        imgs = 2 * imgs - 1
        posterior = self.vae.encode(imgs).latent_dist
        latents = posterior.sample() * self.vae.config.scaling_factor
        return latents
    
    def encode_imgs_deterministic(self, imgs):
        if imgs.shape[1] == 1: # for grayscale maps
            imgs = v2.functional.grayscale_to_rgb(imgs)
        imgs = 2 * imgs - 1
        h = self.vae.encoder(imgs)
        moments = self.vae.quant_conv(h)
        mean, logvar = torch.chunk(moments, 2, dim=1)
        latents = mean * self.vae.config.scaling_factor
        return latents