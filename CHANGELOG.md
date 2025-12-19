# Changelog

All notable changes to the ComfyUI-Chord Desktop Edition will be documented in this file.

## [1.0.0] - 2025-12-19

### Added
- Desktop Edition compatibility for ComfyUI Desktop
- Enhanced logging with detailed debug messages
- Desktop-specific setup documentation (COMFYUI_DESKTOP_SETUP.md)
- Windows update script (UPDATE.bat)
- Comprehensive troubleshooting guides

### Fixed
- Import path issues specific to ComfyUI Desktop
- Internal package imports changed from absolute to relative
- Path resolution order improved for Desktop environment
- Better error handling and traceback logging

### Changed
- Modified `__init__.py` to use `importlib` for more reliable module loading
- Enhanced `sys.path` setup with `insert(0, ...)` for priority
- Updated README with Desktop Edition branding and instructions

### Documentation
- Added README_DESKTOP.md with comprehensive Desktop Edition guide
- Added FIXES_FOR_COMFYUI_DESKTOP.md documenting technical changes
- Added API_CALLS_ISSUE.md for HuggingFace API handling

---

**Based on:** [Ubisoft ComfyUI-Chord](https://github.com/ubisoft/ComfyUI-Chord)

