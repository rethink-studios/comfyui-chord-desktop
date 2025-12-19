#!/usr/bin/env python3
"""
Stable Diffusion 2.1 Downloader with Progress Bars
For ComfyUI-Chord Desktop Edition
"""

import os
import sys
from pathlib import Path

def main():
    repo_id = "RedbeardNZ/stable-diffusion-2-1-base"
    cache_dir = Path.home() / ".cache" / "huggingface" / "hub" / "models--RedbeardNZ--stable-diffusion-2-1-base"
    
    print("=" * 70)
    print(" Stable Diffusion 2.1 Downloader for ComfyUI-Chord")
    print("=" * 70)
    print()
    
    # Check if already downloaded
    if cache_dir.exists() and (cache_dir / "snapshots").exists():
        print("[OK] Stable Diffusion 2.1 is already cached")
        print(f"Location: {cache_dir}")
        print()
        print("You can now use ComfyUI-Chord nodes!")
        input("\nPress Enter to exit...")
        return 0
    
    print(f"Repository: {repo_id}")
    print(f"Destination: {cache_dir}")
    print()
    print("Download size: ~5GB")
    print("Estimated time: 5-15 minutes")
    print()
    print("-" * 70)
    print("Starting download with progress bars...")
    print("-" * 70)
    print()
    
    try:
        # Import with progress support
        from huggingface_hub import snapshot_download
        
        # Try to use tqdm for progress bars
        try:
            from tqdm import tqdm
            use_tqdm = True
        except ImportError:
            print("Note: Install 'tqdm' for better progress bars")
            print("  pip install tqdm")
            print()
            use_tqdm = False
        
        # Download with progress
        if use_tqdm:
            snapshot_download(
                repo_id=repo_id,
                repo_type="model",
                local_dir_use_symlinks=False,
                resume_download=True,
                tqdm_class=tqdm
            )
        else:
            # Fallback without tqdm
            snapshot_download(
                repo_id=repo_id,
                repo_type="model",
                local_dir_use_symlinks=False,
                resume_download=True
            )
        
        print()
        print("=" * 70)
        print("[SUCCESS] Download Complete!")
        print("=" * 70)
        print()
        print(f"Stable Diffusion 2.1 cached at:")
        print(f"{cache_dir}")
        print()
        print("Next steps:")
        print("1. Restart ComfyUI Desktop if running")
        print("2. Use Chord nodes in your workflows")
        print()
        input("Press Enter to exit...")
        
        return 0
        
    except KeyboardInterrupt:
        print()
        print()
        print("[CANCELLED] Download cancelled by user")
        print("Run this script again to resume from where it stopped")
        input("\nPress Enter to exit...")
        return 1
        
    except Exception as e:
        print()
        print("=" * 70)
        print("[ERROR] Download Failed!")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Possible issues:")
        print("1. No internet connection")
        print("2. HuggingFace is down")
        print("3. Need to accept license at:")
        print(f"   https://huggingface.co/{repo_id}")
        print()
        print("Solutions:")
        print("1. Check your internet connection")
        print("2. Visit the model page and accept terms")
        print("3. Run this script again (downloads resume automatically)")
        print()
        input("Press Enter to exit...")
        
        return 1

if __name__ == "__main__":
    try:
        sys.exit(main())
    except Exception as e:
        print(f"\nUnexpected error: {e}")
        input("\nPress Enter to exit...")
        sys.exit(1)

