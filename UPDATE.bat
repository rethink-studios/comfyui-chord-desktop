@echo off
echo ==========================================
echo  ComfyUI-Chord Desktop Edition - Update Script
echo ==========================================
echo.

cd /d "%~dp0"

echo Current directory: %CD%
echo.

echo Checking for updates from GitHub...
echo.

git fetch origin
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to fetch from GitHub!
    echo Check your internet connection.
    pause
    exit /b 1
)

echo.
echo Pulling latest changes...
echo.

git pull origin main
if errorlevel 1 (
    echo.
    echo [ERROR] Failed to pull changes!
    echo You may have local modifications.
    echo.
    echo To force update (WARNING: loses local changes):
    echo   git reset --hard origin/main
    pause
    exit /b 1
)

echo.
echo Updating submodules...
echo.

git submodule update --init --recursive
if errorlevel 1 (
    echo.
    echo [WARNING] Failed to update submodules!
    echo You may need to update manually.
)

echo.
echo ==========================================
echo  Update Complete! ✓
echo ==========================================
echo.
echo Changes applied successfully.
echo Restart ComfyUI Desktop to load updates.
echo.

pause

