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

> **Note**: For detailed Desktop Edition information, see [README_DESKTOP.md](README_DESKTOP.md)

## Installation

### For ComfyUI Desktop (Recommended)

See [README_DESKTOP.md](README_DESKTOP.md) for detailed Desktop Edition installation instructions.

**Quick Start:**
```bash
cd C:\ComfyUIData\custom_nodes
git clone --recursive https://github.com/[YOUR-USERNAME]/comfyui-chord-desktop.git ComfyUI-Chord
C:\ComfyUIData\.venv\Scripts\python.exe -m pip install -r ComfyUI-Chord\requirements.txt
```

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