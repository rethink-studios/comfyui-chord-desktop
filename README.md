# ComfyUI-Chord - Desktop Edition

**Version 1.0.0** | December 19, 2025

A ComfyUI Desktop-compatible fork that works seamlessly in ComfyUI Desktop's Electron environment.

<a href="https://arxiv.org/abs/2509.09952"><img src="https://img.shields.io/badge/arXiv-2509.09952-B31B1B?logo=arxiv&logoColor=white&style=flat-square" alt="arXiv"></a>
<a href="https://ubisoft-laforge.github.io/world/chord/"><img src="https://img.shields.io/badge/Project-Page-brightgreen?logo=ubisoft&logoColor=white&style=flat-square" alt="Project Page"></a>
<a href="https://github.com/ubisoft/ubisoft-laforge-chord"><img src="https://img.shields.io/badge/Github-Code-blue?logo=github&logoColor=white&style=flat-square" alt="Code"></a>

**Based on the work of:** [Ubisoft LaForge](https://github.com/ubisoft/ComfyUI-Chord) ⭐

ComfyUI custom node for the paper: **Chord: Chain of Rendering Decomposition for PBR Material Estimation from Generated Texture Images**

## 🆕 Desktop Edition Features

- ✅ **Desktop App Support**: Works seamlessly in ComfyUI Desktop's Electron environment
- 🔧 **Fixed Import Paths**: Resolved path resolution issues specific to ComfyUI Desktop
- 🔍 **Enhanced Logging**: Better debugging support with detailed error messages
- 📝 **Desktop Setup Guide**: Comprehensive documentation for Desktop users
- 🔄 **Update Script**: Easy Windows update script (`UPDATE.bat`)
- ⬇️ **Auto-Download Script**: One-click Stable Diffusion 2.1 downloader (`download_sd21.bat`)

> **Note**: For detailed Desktop Edition information, see [README_DESKTOP.md](README_DESKTOP.md)

## Installation

### For ComfyUI Desktop (Recommended)

See [README_DESKTOP.md](README_DESKTOP.md) for detailed Desktop Edition installation instructions.

**Quick Start:**
```bash
cd C:\ComfyUIData\custom_nodes
git clone https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord
C:\ComfyUIData\.venv\Scripts\python.exe -m pip install -r ComfyUI-Chord\requirements.txt
```

**Download Stable Diffusion 2.1 (Required):**

ComfyUI-Chord requires Stable Diffusion 2.1 to be cached locally. Use our automated downloader:

1. Double-click `download_sd21.bat` in the ComfyUI-Chord folder
2. Wait for download to complete (~5GB, 5-15 minutes)
3. Restart ComfyUI Desktop

Or see [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md) for manual installation options.

### For Standard ComfyUI

1. Download and install ComfyUI. If you are new to ComfyUI, refer to the original [repository](https://github.com/comfyanonymous/ComfyUI) to get started. **Make sure you have the latest version.**

2. Download the pretrained model **chord_v1.safetensors** from [Hugging Face](https://huggingface.co/Ubisoft/ubisoft-laforge-chord) and place it in the folder **./ComfyUI/models/checkpoints**.

3. Install the custom nodes by manually cloning this repository in the custom nodes folder, **with the argument `--recursive`**:

> Note the ComfyUI-Manager does not support cloning with `--recursive` dependencies. The nodes have to be cloned manually for the moment.

```shell
# Clone the repository
cd ./ComfyUI/custom_nodes
git clone --recursive https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord

# Install dependencies
## For Python version
pip install -r .\ComfyUI-Chord\requirements.txt

## Or for Windows portable version
..\..\python_embeded\python.exe -s -m pip install -r .\ComfyUI-Chord\requirements.txt
```

4. When running the nodes for the first time, they will download the model **Stable Diffusion 2.1** from this repository on the Hugging Face hub: [RedbeardNZ/stable-diffusion-2-1-base](https://huggingface.co/RedbeardNZ/stable-diffusion-2-1-base). The download will be placed in the Hugging Face cache folder `C:\Users\[your-username]\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base`. We are working on simplifying this dependency to have all models centralized in the ComfyUI models folder.

> **Desktop Users**: See [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md) for Stable Diffusion 2.1 caching instructions.

## Differences from Original Version

### What Changed in Desktop Edition

This Desktop Edition includes several modifications to ensure compatibility with ComfyUI Desktop's Electron environment:

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
- **Requirement**: Users must pre-cache Stable Diffusion 2.1 (see [COMFYUI_DESKTOP_SETUP.md](COMFYUI_DESKTOP_SETUP.md))

#### 5. **Documentation**
- Added Desktop-specific setup guides:
  - `README_DESKTOP.md` - Comprehensive Desktop Edition guide
  - `COMFYUI_DESKTOP_SETUP.md` - Model caching instructions
  - `FIXES_FOR_COMFYUI_DESKTOP.md` - Technical details of changes
  - `API_CALLS_ISSUE.md` - HuggingFace API handling
- Added `UPDATE.bat` for easy Windows updates
- Added `CHANGELOG.md` for version tracking

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

## Example Workflow

You can load this workflow using the JSON file `example_workflows/chord_image_to_material.json` or by dropping the image in ComfyUI.

![Example workflow](chord_image_to_material.png)

## License

This project is released under the **Ubisoft Machine Learning License (Research-Only - Copyleft)**. See the full terms in the [LICENSE](LICENSE) file.

## Citation

If you find our work useful, please consider citing:

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

© [2025] Ubisoft Entertainment. All Rights Reserved.