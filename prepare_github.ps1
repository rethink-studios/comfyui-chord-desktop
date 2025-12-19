# PowerShell script to prepare ComfyUI-Chord Desktop Edition for GitHub upload
# Run this script after creating the GitHub repository

Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "ComfyUI-Chord Desktop Edition - GitHub Setup" -ForegroundColor Cyan
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""

$repoPath = "C:\ComfyUIData\custom_nodes\ComfyUI-Chord"
Set-Location $repoPath

Write-Host "Current directory: $repoPath" -ForegroundColor Yellow
Write-Host ""

# Check if we're in a git repository
if (-not (Test-Path ".git")) {
    Write-Host "[ERROR] Not a git repository!" -ForegroundColor Red
    exit 1
}

# Show current status
Write-Host "Current git status:" -ForegroundColor Yellow
git status --short
Write-Host ""

# Check current remote
Write-Host "Current remote:" -ForegroundColor Yellow
git remote -v
Write-Host ""

# Ask for confirmation
Write-Host "This script will:" -ForegroundColor Yellow
Write-Host "1. Remove the old remote (Ubisoft)" -ForegroundColor White
Write-Host "2. Add new remote: rethink-studios/comfyui-chord-desktop" -ForegroundColor White
Write-Host "3. Commit all Desktop Edition changes" -ForegroundColor White
Write-Host "4. Prepare for push (you'll need to create the GitHub repo first)" -ForegroundColor White
Write-Host ""

$confirm = Read-Host "Continue? (y/n)"
if ($confirm -ne "y") {
    Write-Host "Cancelled." -ForegroundColor Yellow
    exit 0
}

Write-Host ""
Write-Host "Step 1: Removing old remote..." -ForegroundColor Cyan
git remote remove origin 2>$null
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Old remote removed" -ForegroundColor Green
} else {
    Write-Host "[INFO] No old remote to remove" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "Step 2: Adding new remote..." -ForegroundColor Cyan
git remote add origin https://github.com/rethink-studios/comfyui-chord-desktop.git
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] New remote added" -ForegroundColor Green
} else {
    Write-Host "[ERROR] Failed to add remote" -ForegroundColor Red
    exit 1
}

Write-Host ""
Write-Host "Step 3: Committing changes..." -ForegroundColor Cyan
$commitMessage = @"
Desktop Edition v1.0.0: ComfyUI Desktop compatibility fixes

- Fixed import paths for Desktop environment
- Enhanced logging and error handling
- Added Desktop setup documentation
- Added Windows update script
- Improved path resolution for Electron environment

Based on: https://github.com/ubisoft/ComfyUI-Chord
"@

git commit -m $commitMessage
if ($LASTEXITCODE -eq 0) {
    Write-Host "[OK] Changes committed" -ForegroundColor Green
} else {
    Write-Host "[WARNING] Commit may have failed or nothing to commit" -ForegroundColor Yellow
}

Write-Host ""
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host "Setup Complete!" -ForegroundColor Green
Write-Host "==========================================" -ForegroundColor Cyan
Write-Host ""
Write-Host "Next steps:" -ForegroundColor Yellow
Write-Host "1. Create the GitHub repository:" -ForegroundColor White
Write-Host "   https://github.com/organizations/rethink-studios/repositories/new" -ForegroundColor Gray
Write-Host "   Name: comfyui-chord-desktop" -ForegroundColor Gray
Write-Host "   Visibility: Public" -ForegroundColor Gray
Write-Host ""
Write-Host "2. Push to GitHub:" -ForegroundColor White
Write-Host "   git push -u origin main" -ForegroundColor Gray
Write-Host ""
Write-Host "3. Handle chord submodule (see GITHUB_SETUP.md for options)" -ForegroundColor White
Write-Host ""

