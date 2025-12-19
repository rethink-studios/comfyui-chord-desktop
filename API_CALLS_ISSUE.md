# ComfyUI Desktop API Calls Issue

## Problem Identified

The ComfyUI-Chord nodes use Hugging Face API calls to download Stable Diffusion 2.1 components, which may not work in ComfyUI Desktop due to:

1. **Network restrictions** - ComfyUI Desktop may block network requests
2. **Security policies** - Desktop apps often have stricter security
3. **Missing internet access** - Desktop version might run in isolated environment
4. **Different diffusers behavior** - The `diffusers` library may behave differently in Desktop

## Where the API Calls Happen

**File:** `chord/chord/module/stable_diffusion.py`

**Lines 51-66:** These methods download from Hugging Face:
- `UNet2DConditionModel.load_config()` - Downloads UNet config
- `UNet2DConditionModel.from_config()` - Downloads UNet weights  
- `AutoencoderKL.load_config()` - Downloads VAE config
- `AutoencoderKL.from_config()` - Downloads VAE weights
- `CLIPTextConfig.from_pretrained()` - Downloads CLIP config
- `CLIPTokenizer.from_pretrained()` - Downloads tokenizer (requires vocab download)
- `DDIMScheduler.load_config()` - Downloads scheduler config

**Current setting:** `local_files_only = False` (line 35) - Allows downloads

## Solution Implemented

**Desktop Edition uses:** `local_files_only = True` by default

This ensures:
- ✅ No API calls to HuggingFace during runtime
- ✅ Works offline once model is cached
- ✅ Reliable in ComfyUI Desktop's Electron environment

**User Setup:**
- Users run `download_sd21.bat` to pre-download Stable Diffusion 2.1
- Model is cached locally (~5GB)
- Chord nodes work offline after initial setup


