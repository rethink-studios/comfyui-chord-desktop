# ComfyUI Desktop Setup Guide

## Quick Setup (Recommended)

**Use the automated downloader:**

1. Navigate to the ComfyUI-Chord folder
2. Double-click `download_sd21.bat`
3. Wait for download to complete (~5GB, shows progress bars)
4. Restart ComfyUI Desktop

**That's it!** The script handles everything automatically.

---

## What the Desktop Edition Does

### 1. Fixed Import Paths
- Changed absolute imports to relative imports within the chord package
- Improved path setup to work with ComfyUI Desktop's different path handling

### 2. Disabled API Calls
- Set `local_files_only = True` by default in `stable_diffusion.py`
- Prevents Hugging Face API calls that may be blocked in ComfyUI Desktop
- All model loading now uses local cache only

### 3. Automated Download Script
- `download_sd21.bat` downloads Stable Diffusion 2.1 automatically
- Progress bars show download status
- Handles all caching and setup

---

## Manual Setup (Advanced Users Only)

If you prefer manual installation or the automated script doesn't work:

### Option 1: Use Hugging Face CLI

```bash
# Install huggingface_hub
pip install huggingface_hub

# Download the model
python -c "from huggingface_hub import snapshot_download; snapshot_download(repo_id='RedbeardNZ/stable-diffusion-2-1-base', repo_type='model')"
```

### Option 2: Pre-cache via ComfyUI Portable

1. Install and run ComfyUI Portable
2. Load any workflow that uses Stable Diffusion 2.1
3. ComfyUI Portable will automatically download and cache the model
4. Cache location: `C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base`
5. This cache is shared between Portable and Desktop versions

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


