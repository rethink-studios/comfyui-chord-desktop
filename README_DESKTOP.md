# ComfyUI-Chord - Desktop Edition

**Version 1.0.0** | December 19, 2025

A ComfyUI Desktop-compatible fork of ComfyUI-Chord with enhanced compatibility and desktop-specific fixes.

**Based on the work of:**
- **[Ubisoft LaForge](https://github.com/ubisoft)** - [Original ComfyUI-Chord](https://github.com/ubisoft/ComfyUI-Chord) ⭐

---

## What's New in This Desktop Edition?

This fork adds **ComfyUI Desktop compatibility** with the following enhancements:

### Desktop Compatibility Features ✅
- ✅ **Desktop App Support**: Works seamlessly in ComfyUI Desktop's Electron environment
- 🔧 **Fixed Import Paths**: Resolved path resolution issues specific to ComfyUI Desktop
- 🔍 **Enhanced Logging**: Better debugging support with detailed error messages
- 📝 **Desktop Setup Guide**: Comprehensive documentation for Desktop users
- 🔄 **Update Script**: Easy Windows update script (`UPDATE.bat`)

### Technical Improvements
- **Fixed Internal Package Imports**: Changed absolute imports to relative imports within the chord package for better compatibility
- **Improved Path Setup**: Enhanced `sys.path` handling for ComfyUI Desktop's different path resolution order
- **Better Error Handling**: More informative error messages and traceback logging

---

## Installation

### For ComfyUI Desktop

1. Navigate to your ComfyUI custom nodes directory:
   ```
   C:\ComfyUIData\custom_nodes\
   ```

2. Clone this repository **with the `--recursive` flag** (required for the chord submodule):
   ```bash
   cd C:\ComfyUIData\custom_nodes
   git clone --recursive https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord
   ```

3. Install dependencies:
   ```bash
   # Using ComfyUI Desktop's Python environment
   C:\ComfyUIData\.venv\Scripts\python.exe -m pip install -r C:\ComfyUIData\custom_nodes\ComfyUI-Chord\requirements.txt
   ```

4. Download the pretrained model:
   - Download **chord_v1.safetensors** from [Hugging Face](https://huggingface.co/Ubisoft/ubisoft-laforge-chord)
   - Place it in: `C:\ComfyUIData\models\checkpoints\`

5. **Important**: Pre-cache Stable Diffusion 2.1 (see [Desktop Setup Guide](COMFYUI_DESKTOP_SETUP.md))

6. Restart ComfyUI Desktop

### Updating to Latest Version

**Quick Update (Windows):**
1. Double-click `UPDATE.bat` in the ComfyUI-Chord folder
2. Wait for the update to complete
3. Restart ComfyUI Desktop

**Manual Update:**
```bash
cd C:\ComfyUIData\custom_nodes\ComfyUI-Chord
git pull origin main
git submodule update --init --recursive
```

---

## Prerequisites

### Required Model Files

1. **Chord Model**: `chord_v1.safetensors`
   - Download from: https://huggingface.co/Ubisoft/ubisoft-laforge-chord
   - Place in: `C:\ComfyUIData\models\checkpoints\`

2. **Stable Diffusion 2.1** (must be cached locally)
   - See [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md) for detailed instructions
   - Cache location: `C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base`

### Python Dependencies

Install via:
```bash
C:\ComfyUIData\.venv\Scripts\python.exe -m pip install -r requirements.txt
```

Required packages:
- `huggingface_hub[hf_xet]`
- `diffusers`
- `omegaconf`
- `imageio`

---

## Available Nodes

This Desktop Edition provides three custom nodes:

1. **Chord - Load Model**: Load the Chord model checkpoint
2. **Chord - Material Estimation**: Estimate PBR materials from texture images
3. **Chord - Normal to Height**: Convert normal maps to height maps

---

## Troubleshooting

### Nodes Show "X" Icons

1. Check ComfyUI Desktop console/logs for error messages
2. Verify `chord_v1.safetensors` is in your checkpoints folder
3. Ensure Stable Diffusion 2.1 is cached locally (see [Desktop Setup Guide](COMFYUI_DESKTOP_SETUP.md))
4. Check that all dependencies are installed

### Import Errors

If you see import errors:
1. Verify the `chord` submodule is initialized:
   ```bash
   cd C:\ComfyUIData\custom_nodes\ComfyUI-Chord
   git submodule update --init --recursive
   ```
2. Check the console logs for detailed error messages (they start with `[ComfyUI-Chord]`)

### Stable Diffusion Loading Issues

- Ensure Stable Diffusion 2.1 is fully cached before using Chord nodes
- See [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md) for caching instructions
- Check logs for "Loading Stable Diffusion 2.1 from local cache" messages

---

## Differences from Original

### What Changed

- **Import Path Fixes**: Modified internal imports to use relative imports for better Desktop compatibility
- **Path Handling**: Enhanced `sys.path` setup to work with ComfyUI Desktop's environment
- **Error Logging**: Added comprehensive debug logging for troubleshooting
- **Documentation**: Added Desktop-specific setup guides and troubleshooting

### What Stayed the Same

- All core functionality remains identical to the original
- Same model files and dependencies
- Same node interfaces and behavior
- Same license (Ubisoft Machine Learning License)

---

## License

This project is released under the **Ubisoft Machine Learning License (Research-Only - Copyleft)**. See the full terms in the [LICENSE](LICENSE) file.

**Important**: This Desktop Edition maintains the same license as the original work. All modifications are clearly marked, and attribution to Ubisoft is retained.

---

## Citation

If you use this work, please cite the original paper:

```
@inproceedings{ying2025chord,
    author = {Ying, Zhi and Rong, Boxiang and Wang, Jingyu and Xu, Maoyuan},
    title = {Chord: Chain of Rendering Decomposition for PBR Material Estimation from Generated Texture Images},
    year = {2025},
    isbn = {9798400721373},
    publisher = {Association for Computing Machinery},
    address = {New York, NY, USA},
    url = {https://doi.org/10.1145/3757377.3763848},
    doi = {10.1145/3757377.3763848},
    booktitle = {Proceedings of the SIGGRAPH Asia 2025 Conference Papers},
    articleno = {164},
    numpages = {11},
    keywords = {Appearance Modeling, Material Generation, Texture Synthesis, SVBRDF, Image-conditional Diffusion Models},
    series = {SA Conference Papers '25}
}
```

---

## Credits

- **Ubisoft LaForge** - Original ComfyUI-Chord implementation
- **RETHINK Studios** - Desktop Edition compatibility fixes and enhancements

---

## Support

If you encounter any issues:

1. Check the [Desktop Setup Guide](COMFYUI_DESKTOP_SETUP.md)
2. Review the [Fixes Documentation](FIXES_FOR_COMFYUI_DESKTOP.md)
3. Check ComfyUI Desktop logs for `[ComfyUI-Chord]` messages
4. Open an issue on GitHub with:
   - ComfyUI Desktop version
   - Error messages from logs
   - Steps to reproduce

---

© [2025] Ubisoft Entertainment. All Rights Reserved.  
Desktop Edition modifications © [2025] RETHINK Studios.

