# GitHub Repository Setup Instructions

## Repository Name
`comfyui-chord-desktop`

## GitHub Organization
`rethink-studios`

## Steps to Create and Push

### 1. Create GitHub Repository

1. Go to: https://github.com/organizations/rethink-studios/repositories/new
2. Repository name: `comfyui-chord-desktop`
3. Description: `ComfyUI Desktop-compatible fork of ComfyUI-Chord with enhanced compatibility and desktop-specific fixes`
4. Visibility: **Public** (to match Model Linker Desktop Edition)
5. **DO NOT** initialize with README, .gitignore, or license (we already have these)
6. Click "Create repository"

### 2. Update Remote and Push

```bash
cd C:\ComfyUIData\custom_nodes\ComfyUI-Chord

# Remove old remote (pointing to Ubisoft)
git remote remove origin

# Add new remote (rethink-studios)
git remote add origin https://github.com/rethink-studios/comfyui-chord-desktop.git

# Commit all Desktop Edition changes
git commit -m "Desktop Edition v1.0.0: ComfyUI Desktop compatibility fixes

- Fixed import paths for Desktop environment
- Enhanced logging and error handling
- Added Desktop setup documentation
- Added Windows update script
- Improved path resolution for Electron environment

Based on: https://github.com/ubisoft/ComfyUI-Chord"

# Push to new repository
git push -u origin main
```

### 3. Handle Submodule Changes

The `chord` submodule has Desktop-specific modifications. You have two options:

#### Option A: Include as Regular Directory (Recommended)
Since we've modified the submodule for Desktop compatibility, we can include it directly:

```bash
# Remove submodule reference
git rm --cached chord
rm -rf .git/modules/chord

# Add chord directory as regular files
git add chord/

# Commit
git commit -m "Include chord directory directly (Desktop Edition modifications)"
git push origin main
```

#### Option B: Keep as Submodule (Requires Forking Chord)
If you want to keep it as a submodule, you'll need to:
1. Fork the original chord repository
2. Push Desktop Edition changes to your fork
3. Update submodule URL to point to your fork

### 4. Update README URLs

After pushing, update the README.md and README_DESKTOP.md to replace `[YOUR-USERNAME]` with `rethink-studios`:

- Search for: `[YOUR-USERNAME]`
- Replace with: `rethink-studios`

### 5. Add Repository Topics

On GitHub, add these topics:
- `comfyui`
- `comfyui-desktop`
- `comfyui-custom-node`
- `chord`
- `material-estimation`
- `pbr`
- `desktop-edition`

### 6. Create Release

1. Go to Releases → Create a new release
2. Tag: `v1.0.0`
3. Title: `Desktop Edition v1.0.0`
4. Description:
```markdown
## Desktop Edition v1.0.0

First release of ComfyUI-Chord Desktop Edition with full ComfyUI Desktop compatibility.

### Features
- ✅ Desktop App Support
- 🔧 Fixed Import Paths
- 🔍 Enhanced Logging
- 📝 Desktop Setup Guide
- 🔄 Windows Update Script

### Installation
```bash
cd C:\ComfyUIData\custom_nodes
git clone --recursive https://github.com/rethink-studios/comfyui-chord-desktop.git ComfyUI-Chord
```

Based on: https://github.com/ubisoft/ComfyUI-Chord
```

---

## Verification Checklist

- [ ] Repository created at `rethink-studios/comfyui-chord-desktop`
- [ ] All files committed and pushed
- [ ] README URLs updated
- [ ] Repository topics added
- [ ] Release v1.0.0 created
- [ ] Test clone: `git clone --recursive https://github.com/rethink-studios/comfyui-chord-desktop.git`

