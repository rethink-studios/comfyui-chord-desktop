# ComfyUI-Chord - Desktop Edition

**Version 1.0.0** | December 19, 2025

A ComfyUI Desktop-compatible fork that works seamlessly in ComfyUI Desktop's Electron environment.

<a href="https://arxiv.org/abs/2509.09952"><img src="https://img.shields.io/badge/arXiv-2509.09952-B31B1B?logo=arxiv&logoColor=white&style=flat-square" alt="arXiv"></a>
<a href="https://ubisoft-laforge.github.io/world/chord/"><img src="https://img.shields.io/badge/Project-Page-brightgreen?logo=ubisoft&logoColor=white&style=flat-square" alt="Project Page"></a>
<a href="https://github.com/ubisoft/ubisoft-laforge-chord"><img src="https://img.shields.io/badge/Github-Code-blue?logo=github&logoColor=white&style=flat-square" alt="Code"></a>

**Based on the work of:** [Ubisoft LaForge](https://github.com/ubisoft/ComfyUI-Chord) ⭐

ComfyUI custom node for the paper: **Chord: Chain of Rendering Decomposition for PBR Material Estimation from Generated Texture Images**

---

## 🆕 What's New in Desktop Edition

The original Chord implementation didn't work with ComfyUI Desktop, so we built a Desktop-compatible version!

**Desktop Edition Features:**
- ✅ **Desktop App Support**: Works seamlessly in ComfyUI Desktop's Electron environment
- 🔧 **Fixed Import Paths**: Resolved path resolution issues specific to ComfyUI Desktop
- 🔍 **Enhanced Logging**: Better debugging support with detailed error messages
- ⬇️ **Auto-Download Script**: One-click Stable Diffusion 2.1 downloader (`download_sd21.bat`)
- 🔄 **Update Script**: Easy Windows update script (`UPDATE.bat`)
- 📝 **Desktop Setup Guide**: Comprehensive documentation for Desktop users

---

## Installation

### For ComfyUI Desktop (Recommended)

**Quick Start:**
```bash
cd C:\ComfyUIData\custom_nodes
git clone https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord
C:\ComfyUIData\.venv\Scripts\python.exe -m pip install -r ComfyUI-Chord\requirements.txt
```

**Download Stable Diffusion 2.1 (Required):**

ComfyUI-Chord requires Stable Diffusion 2.1 to be cached locally. Use our automated downloader:

1. Navigate to `C:\ComfyUIData\custom_nodes\ComfyUI-Chord`
2. Double-click `download_sd21.bat`
3. Wait for download to complete (~5GB, shows progress bars)
4. Restart ComfyUI Desktop

**That's it!** You're ready to use Chord nodes.

### For Standard ComfyUI

1. Download and install ComfyUI from the [original repository](https://github.com/comfyanonymous/ComfyUI)

2. Clone this repository:
```bash
cd ./ComfyUI/custom_nodes
git clone https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord
```

3. Install dependencies:
```bash
# For Python version
pip install -r ComfyUI-Chord/requirements.txt

# Or for Windows portable version
..\..\python_embeded\python.exe -s -m pip install ComfyUI-Chord\requirements.txt
```

4. Download **chord_v1.safetensors** from [Hugging Face](https://huggingface.co/Ubisoft/ubisoft-laforge-chord) and place in `./ComfyUI/models/checkpoints`

5. Download Stable Diffusion 2.1 - it will be cached automatically on first run

### Updating to Latest Version

**Windows (Quick):**
```bash
# Double-click this file in the ComfyUI-Chord folder
UPDATE.bat
```

**Manual:**
```bash
cd C:\ComfyUIData\custom_nodes\ComfyUI-Chord
git pull origin main
```

---

## Available Nodes

This Desktop Edition provides three custom nodes:

1. **Chord - Load Model**: Load the Chord model checkpoint
2. **Chord - Material Estimation**: Estimate PBR materials from texture images
3. **Chord - Normal to Height**: Convert normal maps to height maps

---

## Differences from Original Version

### What Changed in Desktop Edition

This Desktop Edition includes modifications to ensure compatibility with ComfyUI Desktop's Electron environment:

#### 1. **Import Path Fixes**
- **Original**: Used absolute imports (`from chord.module import ...`)
- **Desktop Edition**: Changed to relative imports (`from .module import ...`)
- **Why**: ComfyUI Desktop has different Python path handling; relative imports ensure the chord package can always find its internal modules
- **Files modified**: 
  - `chord/chord/__init__.py`
  - `chord/chord/module/chord.py`
  - `chord/chord/module/stable_diffusion.py`

#### 2. **Enhanced Node Loading**
- **Original**: Simple module import in `__init__.py`
- **Desktop Edition**: Uses `importlib` with explicit path resolution and comprehensive error logging
- **Why**: More reliable module loading across different ComfyUI environments
- **Features added**:
  - Debug logging with `[ComfyUI-Chord]` prefix
  - Detailed error messages with traceback
  - Path verification before import
  - Better error isolation

#### 3. **Path Setup Priority**
- **Original**: Used `sys.path.append()`
- **Desktop Edition**: Uses `sys.path.insert(0, ...)` 
- **Why**: Ensures chord directory is checked first, preventing conflicts with other packages

#### 4. **Local-Only Model Loading**
- **Original**: May attempt HuggingFace API calls for Stable Diffusion 2.1
- **Desktop Edition**: Set `local_files_only=True` by default in `stable_diffusion.py`
- **Why**: ComfyUI Desktop may block network requests; all models must be pre-cached locally
- **Solution**: Users run `download_sd21.bat` to pre-cache SD 2.1

#### 5. **Automated Setup**
- **Added**: `download_sd21.bat` - One-click SD 2.1 downloader with progress bars
- **Added**: `UPDATE.bat` - Easy update script for Windows
- **Added**: Comprehensive Desktop-specific documentation

#### 6. **Installation Differences**
- **Original**: Install to `ComfyUI/custom_nodes/`
- **Desktop Edition**: Install to `C:\ComfyUIData\custom_nodes\`
- **Original**: Uses portable Python or system Python
- **Desktop Edition**: Uses `C:\ComfyUIData\.venv\Scripts\python.exe`

### What Stayed the Same

- ✅ All core functionality is identical
- ✅ Same model files (chord_v1.safetensors)
- ✅ Same node interfaces and behavior
- ✅ Same output quality and capabilities
- ✅ Same license (Ubisoft Machine Learning License)
- ✅ Same dependencies (omegaconf, diffusers, imageio, etc.)

### Should You Use Desktop Edition?

- **Use Desktop Edition** if you're running ComfyUI Desktop (Electron app)
- **Use Original** if you're running standard ComfyUI Portable/Python
- **Both work** but Desktop Edition has specific fixes for the Desktop environment

---

## Example Workflow

You can load this workflow using the JSON file `example_workflows/chord_image_to_material.json` or by dropping the image in ComfyUI.

![Example workflow](chord_image_to_material.png)

---

## Troubleshooting

### Nodes Show "X" Icons

1. Check ComfyUI Desktop console/logs for error messages (look for `[ComfyUI-Chord]`)
2. Verify `chord_v1.safetensors` is in your checkpoints folder
3. Ensure Stable Diffusion 2.1 is cached - run `download_sd21.bat` if not
4. Check that all dependencies are installed

### Import Errors

If you see import errors:
1. Check the console logs for detailed error messages
2. Verify all dependencies are installed: `pip install -r requirements.txt`

### Stable Diffusion Loading Issues

- Ensure Stable Diffusion 2.1 is cached before using Chord nodes
- Run `download_sd21.bat` to download automatically
- Check logs for "Loading Stable Diffusion 2.1 from local cache" messages

For more troubleshooting help, see [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md)

---

## Documentation

- [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md) - Manual setup options
- [FIXES_FOR_COMFYUI_DESKTOP.md](FIXES_FOR_COMFYUI_DESKTOP.md) - Technical details of changes
- [API_CALLS_ISSUE.md](API_CALLS_ISSUE.md) - HuggingFace API handling
- [CHANGELOG.md](CHANGELOG.md) - Version history

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

1. Check the [Troubleshooting](#troubleshooting) section above
2. Review [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md)
3. Check ComfyUI Desktop logs for `[ComfyUI-Chord]` messages
4. Open an issue on GitHub with:
   - ComfyUI Desktop version
   - Error messages from logs
   - Steps to reproduce

---

© [2025] Ubisoft Entertainment. All Rights Reserved.  
Desktop Edition modifications © [2025] RETHINK Studios.
