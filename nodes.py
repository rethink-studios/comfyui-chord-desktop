import os
import sys
import torch
from omegaconf import OmegaConf
from torchvision.transforms import v2

# Add the current directory and chord subdirectory to path for imports
current_dir = os.path.dirname(os.path.abspath(__file__))
chord_dir = os.path.join(current_dir, "chord")
if current_dir not in sys.path:
    sys.path.insert(0, current_dir)
if chord_dir not in sys.path:
    sys.path.insert(0, chord_dir)

from normal_to_height import normal_to_height

# Modules from ComfyUI
import folder_paths
import comfy.model_management
from comfy.utils import load_torch_file
from comfy.model_patcher import ModelPatcher

# Modules from ComfyUI-Chord
from chord import ChordModel

def apply_padding(model, mode):
    for layer in [layer for _, layer in model.named_modules() if isinstance(layer, torch.nn.Conv2d)]:
        layer.padding_mode = mode

def apply_circular_padding(model):
    if hasattr(model, 'sd'):
        apply_padding(model.sd.vae, 'circular')
        apply_padding(model.sd.unet, 'circular')
    else:
        apply_padding(model, 'circular')

class ChordLoadModel:
    """Node to load Chord Model"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "ckpt_name": (folder_paths.get_filename_list("checkpoints"), ),
            }
        }
    
    RETURN_TYPES = ("CHORD_MODEL",)
    RETURN_NAMES = ("chord_model",)
    FUNCTION = "load_model"
    CATEGORY = "Chord"

    def load_model(self, ckpt_name):
        try:
            if type(ckpt_name) is list:
                ckpt_name = ckpt_name[0]
            ckpt_path = folder_paths.get_full_path("checkpoints", ckpt_name)
            if not os.path.exists(ckpt_path):
                raise FileNotFoundError(f"Model file not found: {ckpt_path}\nPlease ensure chord_v1.safetensors is in the checkpoints folder.")
            config_path = os.path.join(os.path.dirname(__file__), "chord/config/chord.yaml")
            if not os.path.exists(config_path):
                raise FileNotFoundError(f"Config file not found: {config_path}")
            config = OmegaConf.load(config_path)
            model = ChordModel(config)
            sd = load_torch_file(ckpt_path, safe_load=True)
            try:
                model.load_state_dict(sd)
            except RuntimeError as e:
                raise RuntimeError('Failed to load model, check if the checkpoint file is correct.\n{}'.format(repr(e)))
            model.eval()
            model_patcher = ModelPatcher(model,
                                         comfy.model_management.get_torch_device(),
                                         comfy.model_management.unet_offload_device())
            return (model_patcher,)
        except Exception as e:
            print(f"[ComfyUI-Chord] Error in ChordLoadModel.load_model: {e}")
            import traceback
            traceback.print_exc()
            raise

class ChordMaterialEstimation:
    """Chord Material Estimation Node"""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "chord_model": ("CHORD_MODEL",),
                "image": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE", "IMAGE", "IMAGE", "IMAGE")
    RETURN_NAMES = ("basecolor", "normal", "roughness", "metalness")
    FUNCTION = "estimate_material"
    CATEGORY = "Chord"

    def estimate_material(self, chord_model, image):
        try:
            comfy.model_management.load_models_gpu([chord_model])
            model = chord_model.model
            device = next(model.parameters()).device
            apply_circular_padding(model)
            image = image.permute(0,3,1,2).to(device)
            ori_h, ori_w = image.shape[-2:]
            x = v2.Resize(size=(1024, 1024), antialias=True)(image)
            with torch.no_grad() as no_grad, torch.autocast(device_type=device.type) as amp:
                output = model(x)
            for key in output.keys():
                output[key] = v2.Resize(size=(ori_h, ori_w), antialias=True)(output[key])
                if output[key].ndim == 4:
                    output[key] = output[key].permute(0,2,3,1)
            return (output['basecolor'], output['normal'], output['roughness'], output['metalness'])
        except Exception as e:
            print(f"[ComfyUI-Chord] Error in ChordMaterialEstimation.estimate_material: {e}")
            import traceback
            traceback.print_exc()
            raise
    
class ChordNormalToHeight:
    """Integrate normal map to height map using Poisson solver with overlapping subregions."""

    @classmethod
    def INPUT_TYPES(cls):
        return {
            "required": {
                "normal": ("IMAGE",),
            }
        }
    
    RETURN_TYPES = ("IMAGE",)
    RETURN_NAMES = ("height",)
    FUNCTION = "convert_to_height"
    CATEGORY = "Chord"

    def convert_to_height(self, normal):
        try:
            normal = normal.permute(0,3,1,2)
            height_var_threshold = 5e-4
            ori_h, ori_w = normal.shape[-2:]
            x = v2.Resize(size=(1024, 1024), antialias=True)(normal)
            height_maps = []
            for i in range(x.shape[0]): # to support batch processing
                height = normal_to_height(x[i])[None, None].squeeze(1)
                if height.var() < height_var_threshold and height.var() > 0:
                    height = normal_to_height(x[i], skip_normalize_normal=True)[None, None].squeeze(1)
                height_maps.append(height)
            height = torch.cat(height_maps, dim=0)
            height = v2.Resize(size=(ori_h, ori_w), antialias=True)(height)
            return (height,)
        except Exception as e:
            print(f"[ComfyUI-Chord] Error in ChordNormalToHeight.convert_to_height: {e}")
            import traceback
            traceback.print_exc()
            raise

# Node class mappings
print(f"[ComfyUI-Chord] Debug: Defining NODE_CLASS_MAPPINGS")
print(f"[ComfyUI-Chord] Debug: ChordLoadModel = {ChordLoadModel}")
print(f"[ComfyUI-Chord] Debug: ChordMaterialEstimation = {ChordMaterialEstimation}")
print(f"[ComfyUI-Chord] Debug: ChordNormalToHeight = {ChordNormalToHeight}")

NODE_CLASS_MAPPINGS = {
    "ChordLoadModel": ChordLoadModel,
    "ChordMaterialEstimation": ChordMaterialEstimation,
    "ChordNormalToHeight": ChordNormalToHeight,
}

NODE_DISPLAY_NAME_MAPPINGS = {
    "ChordLoadModel": "Chord - Load Model",
    "ChordMaterialEstimation": "Chord - Material Estimation",
    "ChordNormalToHeight": "Chord - Normal to Height",
}

print(f"[ComfyUI-Chord] Debug: NODE_CLASS_MAPPINGS defined with {len(NODE_CLASS_MAPPINGS)} nodes: {list(NODE_CLASS_MAPPINGS.keys())}")
