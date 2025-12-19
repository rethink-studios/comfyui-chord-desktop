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

## Solutions

### Option 1: Force Local Files Only (Recommended for Desktop)
**Change:** Set `local_files_only = True` by default

**Pros:**
- No API calls needed
- Works offline
- More reliable in Desktop

**Cons:**
- Requires Stable Diffusion 2.1 to be pre-downloaded/cached
- First-time users need to download manually or via ComfyUI Portable first

### Option 2: Use ComfyUI's Model Loading System
**Change:** Replace diffusers loading with ComfyUI's native model loading

**Pros:**
- Uses ComfyUI's existing model infrastructure
- No external API calls
- Better integration with ComfyUI Desktop

**Cons:**
- Requires significant code refactoring
- Need to adapt Chord's Stable Diffusion usage to ComfyUI's format

### Option 3: Hybrid Approach
**Change:** Try local files first, fall back to download only if explicitly enabled

**Pros:**
- Works offline if files exist
- Can still download if needed (with user permission)

**Cons:**
- More complex code
- Still may fail in Desktop if downloads are blocked

## Recommendation

**For ComfyUI Desktop:** Use **Option 1** - Force `local_files_only = True`

The Stable Diffusion 2.1 model will need to be cached first (can be done via ComfyUI Portable or manual download), but then it will work reliably in Desktop without any API calls.

## Next Steps

1. Modify `stable_diffusion.py` to use `local_files_only = True`
2. Add better error messages if files aren't found
3. Provide instructions for pre-downloading SD 2.1 via ComfyUI Portable or manual download


