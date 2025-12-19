# Fixes for ComfyUI Desktop Compatibility

## Problem
The ComfyUI-Chord custom node works with ComfyUI Portable but fails with ComfyUI Desktop due to import path issues.

## Root Cause
The chord package uses absolute imports (`from chord.module import ...`) internally, which can fail in ComfyUI Desktop due to different Python path handling compared to ComfyUI Portable.

## Changes Made

### 1. Fixed Internal Package Imports
Changed absolute imports to relative imports within the chord package:

**File: `chord/chord/__init__.py`**
- Changed: `from chord.module import make` → `from .module import make`
- Changed: `from chord.module.chord import post_decoder` → `from .module.chord import post_decoder`

**File: `chord/chord/module/chord.py`**
- Changed: `from chord.util import ...` → `from ..util import ...`

### 2. Improved Path Setup
**File: `__init__.py`**
- Changed `sys.path.append()` to `sys.path.insert(0, ...)` to ensure the chord directory is checked first
- This helps with ComfyUI Desktop's different path resolution order

## Testing
After these changes, the node should work in both ComfyUI Portable and ComfyUI Desktop. The relative imports ensure that the package can find its internal modules regardless of how Python's import system resolves paths.

## Notes
- The standalone scripts (`demo_gradio.py`, `test.py`) still use absolute imports, which is fine since they're meant to be run from the `chord` directory
- The main `nodes.py` file already uses `sys.path.insert(0, ...)` which is optimal


