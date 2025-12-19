# ComfyUI Desktop Setup Guide

## Changes Made for Desktop Compatibility

### 1. Fixed Import Paths
- Changed absolute imports to relative imports within the chord package
- Improved path setup to work with ComfyUI Desktop's different path handling

### 2. Disabled API Calls (Option 1 Implementation)
- Set `local_files_only = True` by default in `stable_diffusion.py`
- Prevents Hugging Face API calls that may be blocked in ComfyUI Desktop
- All model loading now uses local cache only

## Prerequisites

Before using Chord nodes in ComfyUI Desktop, you need to have Stable Diffusion 2.1 cached locally.

### Option 1: Pre-cache via ComfyUI Portable (Easiest)

1. Install and run ComfyUI Portable
2. Load any workflow that uses Stable Diffusion 2.1
3. ComfyUI Portable will automatically download and cache the model
4. The cache will be located at: `C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base`
5. This cache is shared between Portable and Desktop versions

### Option 2: Manual Download

1. Visit: https://huggingface.co/RedbeardNZ/stable-diffusion-2-1-base
2. Accept the license terms
3. Download all required files:
   - `unet/config.json` and weights
   - `vae/config.json` and weights  
   - `text_encoder/config.json` and weights
   - `tokenizer/vocab.json`, `merges.txt`, `tokenizer_config.json`
   - `scheduler/scheduler_config.json`
4. Place them in: `C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base`

### Option 3: Use Hugging Face CLI

```bash
# Install huggingface-cli if needed
pip install huggingface_hub

# Login (required for gated models)
huggingface-cli login

# Download the model
huggingface-cli download RedbeardNZ/stable-diffusion-2-1-base --local-dir C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base
```

## Verification

After caching the model, restart ComfyUI Desktop. When you use a Chord node, you should see:

```
[ComfyUI-Chord] Loading Stable Diffusion 2.1 from local cache only
[ComfyUI-Chord] Loading UNet config...
[ComfyUI-Chord] UNet loaded successfully
[ComfyUI-Chord] Loading VAE config...
[ComfyUI-Chord] VAE loaded successfully
...
[ComfyUI-Chord] Stable Diffusion 2.1 components loaded successfully from local cache
```

If you see an error about missing files, follow the prerequisites above to cache the model.

## Troubleshooting

### Error: "Failed to load Stable Diffusion 2.1 components from local cache"

**Solution:** The model files are not cached. Follow one of the options above to download them.

### Error: "Connection error" or network-related errors

**Solution:** This shouldn't happen anymore with `local_files_only=True`, but if it does, ensure the model is fully cached locally.

### Nodes show "X" icons

**Solution:** 
1. Check console for error messages
2. Ensure `chord_v1.safetensors` is in your checkpoints folder
3. Ensure Stable Diffusion 2.1 is cached (see prerequisites)

## Notes

- The cache location is shared between ComfyUI Portable and Desktop
- Once cached, the model works offline
- No internet connection is required after initial caching
- The cache persists across ComfyUI updates


