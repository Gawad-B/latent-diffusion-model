#!/usr/bin/env python3
"""
Setup verification script for Medical Image Generator
Checks if all requirements are met before running the application
"""

import sys
from pathlib import Path
import importlib


def print_header(text):
    """Print a formatted header"""
    print("\n" + "="*60)
    print(f"  {text}")
    print("="*60)


def check_python_version():
    """Check if Python version is adequate"""
    print("\n📋 Checking Python version...")
    version = sys.version_info
    if version.major == 3 and version.minor >= 8:
        print(f"   ✅ Python {version.major}.{version.minor}.{version.micro}")
        return True
    else:
        print(f"   ❌ Python {version.major}.{version.minor}.{version.micro}")
        print(f"   Required: Python 3.8 or higher")
        return False


def check_dependencies():
    """Check if required packages are installed"""
    print("\n📦 Checking dependencies...")
    
    required = {
        'flask': 'Flask',
        'torch': 'PyTorch',
        'torchvision': 'TorchVision',
        'diffusers': 'Diffusers',
        'transformers': 'Transformers',
        'PIL': 'Pillow',
        'numpy': 'NumPy',
        'tqdm': 'tqdm'
    }
    
    all_installed = True
    for module, name in required.items():
        try:
            importlib.import_module(module)
            print(f"   ✅ {name}")
        except ImportError:
            print(f"   ❌ {name} - NOT INSTALLED")
            all_installed = False
    
    return all_installed


def check_cuda():
    """Check CUDA availability"""
    print("\n🎮 Checking GPU/CUDA...")
    try:
        import torch
        if torch.cuda.is_available():
            print(f"   ✅ CUDA available")
            print(f"   GPU: {torch.cuda.get_device_name(0)}")
            return True
        else:
            print(f"   ⚠️  CUDA not available - will use CPU")
            print(f"   Note: Generation will be slower on CPU")
            return True
    except:
        print(f"   ❌ Cannot check CUDA")
        return False


def check_directories():
    """Check if required directories exist"""
    print("\n📁 Checking directories...")
    
    required_dirs = [
        'checkpoints',
        'static/generated',
        'static/assets',
        'templates'
    ]
    
    all_exist = True
    for dir_path in required_dirs:
        path = Path(dir_path)
        if path.exists():
            print(f"   ✅ {dir_path}/")
        else:
            print(f"   ❌ {dir_path}/ - NOT FOUND")
            all_exist = False
    
    return all_exist


def check_model_checkpoint():
    """Check if model checkpoint exists"""
    print("\n🤖 Checking model checkpoint...")
    
    checkpoint_path = Path('checkpoints/final_unet_model.pth')
    
    if checkpoint_path.exists():
        size_mb = checkpoint_path.stat().st_size / (1024 * 1024)
        print(f"   ✅ final_unet_model.pth ({size_mb:.1f} MB)")
        
        if size_mb < 100:
            print(f"   ⚠️  Warning: File seems small, may not be complete")
            return False
        
        return True
    else:
        print(f"   ❌ final_unet_model.pth - NOT FOUND")
        print(f"   ")
        print(f"   You need to download this from your Colab notebook!")
        print(f"   See MODEL_DOWNLOAD_GUIDE.md for instructions.")
        return False


def check_files():
    """Check if required files exist"""
    print("\n📄 Checking required files...")
    
    required_files = [
        'server.py',
        'model_inference.py',
        'requirements.txt',
        'templates/index.html',
        'static/assets/js/main.js'
    ]
    
    all_exist = True
    for file_path in required_files:
        path = Path(file_path)
        if path.exists():
            print(f"   ✅ {file_path}")
        else:
            print(f"   ❌ {file_path} - NOT FOUND")
            all_exist = False
    
    return all_exist


def print_summary(checks):
    """Print summary of checks"""
    print_header("VERIFICATION SUMMARY")
    
    total = len(checks)
    passed = sum(checks.values())
    
    print(f"\nPassed: {passed}/{total} checks")
    
    if all(checks.values()):
        print("\n🎉 ALL CHECKS PASSED!")
        print("\nYou're ready to run the application!")
        print("\nNext steps:")
        print("  1. Run: python server.py")
        print("  2. Open: http://127.0.0.1:5000")
        print("  3. Navigate to 'Generate Images' section")
        print("  4. Select disease and generate!")
    else:
        print("\n⚠️  SOME CHECKS FAILED")
        print("\nPlease fix the issues above before running.")
        
        if not checks['model']:
            print("\n❗ CRITICAL: Model checkpoint missing!")
            print("   See MODEL_DOWNLOAD_GUIDE.md for instructions")
        
        if not checks['dependencies']:
            print("\n❗ Install dependencies:")
            print("   pip install -r requirements.txt")


def main():
    """Run all checks"""
    print_header("MEDICAL IMAGE GENERATOR - SETUP VERIFICATION")
    print("\nThis script will verify that your setup is complete.")
    
    checks = {
        'python': check_python_version(),
        'dependencies': check_dependencies(),
        'cuda': check_cuda(),
        'directories': check_directories(),
        'files': check_files(),
        'model': check_model_checkpoint()
    }
    
    print_summary(checks)
    
    return 0 if all(checks.values()) else 1


if __name__ == "__main__":
    sys.exit(main())
