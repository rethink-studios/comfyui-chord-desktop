@echo off
REM ===================================================================
REM  Stable Diffusion 2.1 Downloader for ComfyUI-Chord Desktop Edition
REM  With Progress Bars
REM ===================================================================

setlocal enabledelayedexpansion

echo ===================================================================
echo  Stable Diffusion 2.1 Downloader for ComfyUI-Chord
echo ===================================================================
echo.

REM Set cache directory
set CACHE_DIR=%USERPROFILE%\.cache\huggingface\hub\models--RedbeardNZ--stable-diffusion-2-1-base
set REPO_ID=RedbeardNZ/stable-diffusion-2-1-base

echo Checking for existing installation...
if exist "%CACHE_DIR%\snapshots" (
    echo [OK] Stable Diffusion 2.1 is already cached
    echo Location: %CACHE_DIR%
    echo.
    echo You can now use ComfyUI-Chord nodes!
    echo.
    pause
    exit /b 0
)

echo [INFO] Stable Diffusion 2.1 not found in cache
echo.

REM Check if Python is available
echo Checking for Python...
python --version >nul 2>&1
if errorlevel 1 (
    echo [ERROR] Python not found!
    echo.
    echo Please install Python or use ComfyUI Desktop's Python:
    echo   C:\ComfyUIData\.venv\Scripts\python.exe
    echo.
    pause
    exit /b 1
)
echo [OK] Python found
echo.

REM Check if huggingface_hub is installed
echo Checking for huggingface_hub...
python -c "import huggingface_hub" >nul 2>&1
if errorlevel 1 (
    echo [INFO] huggingface_hub not installed, installing...
    echo.
    python -m pip install huggingface_hub --quiet
    if errorlevel 1 (
        echo [ERROR] Failed to install huggingface_hub
        echo.
        echo Try installing manually:
        echo   pip install huggingface_hub
        echo.
        pause
        exit /b 1
    )
    echo [OK] huggingface_hub installed
) else (
    echo [OK] huggingface_hub found
)
echo.

REM Check for tqdm (progress bars)
python -c "import tqdm" >nul 2>&1
if errorlevel 1 (
    echo [INFO] Installing tqdm for progress bars...
    python -m pip install tqdm --quiet >nul 2>&1
)

REM Download the model with progress
echo ===================================================================
echo  Starting Download
echo ===================================================================
echo.
echo Repository: %REPO_ID%
echo Destination: %CACHE_DIR%
echo.
echo Download size: ~5GB
echo Estimated time: 5-15 minutes
echo.
echo Progress bars will appear below...
echo.

python -c "from huggingface_hub import snapshot_download; from tqdm import tqdm; snapshot_download(repo_id='%REPO_ID%', repo_type='model', local_dir_use_symlinks=False, resume_download=True, tqdm_class=tqdm)"

if errorlevel 1 (
    echo.
    echo ===================================================================
    echo [ERROR] Download failed!
    echo ===================================================================
    echo.
    echo Possible issues:
    echo 1. No internet connection
    echo 2. HuggingFace is down
    echo 3. Need to accept license at:
    echo    https://huggingface.co/%REPO_ID%
    echo.
    echo Try:
    echo 1. Check your internet connection
    echo 2. Visit the model page and accept terms
    echo 3. Run this script again (downloads resume automatically)
    echo.
    pause
    exit /b 1
)

echo.
echo ===================================================================
echo [SUCCESS] Download Complete!
echo ===================================================================
echo.
echo Stable Diffusion 2.1 is now cached at:
echo %CACHE_DIR%
echo.
echo You can now use ComfyUI-Chord nodes in ComfyUI Desktop!
echo.
echo Next steps:
echo 1. Restart ComfyUI Desktop if it's running
echo 2. Use the Chord nodes in your workflows
echo.
pause
