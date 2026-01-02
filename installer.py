#!/usr/bin/env python3
"""
Installer for 'copy' command
"""

import os
import sys
import platform
import shutil

def get_install_dir():
    """Get appropriate installation directory."""
    system = platform.system()
    
    if system == "Windows":
        python_dir = os.path.dirname(sys.executable)
        scripts_dir = os.path.join(python_dir, "Scripts")
        if os.path.exists(scripts_dir):
            return scripts_dir
        home = os.path.expanduser("~")
        return os.path.join(home, "bin")
    
    else:
        if os.access("/usr/local/bin", os.W_OK):
            return "/usr/local/bin"
        home = os.path.expanduser("~")
        local_bin = os.path.join(home, ".local", "bin")
        os.makedirs(local_bin, exist_ok=True)
        return local_bin


def check_in_path(directory):
    """Check if directory is in PATH."""
    path_env = os.environ.get("PATH", "")
    path_dirs = path_env.split(os.pathsep)
    return directory in path_dirs


def create_wrapper(install_dir, script_path):
    """Create platform-specific wrapper."""
    system = platform.system()
    
    if system == "Windows":
        wrapper = os.path.join(install_dir, "copy.bat")
        content = f'''@echo off
"{sys.executable}" "{script_path}" %*
'''
        with open(wrapper, "w") as f:
            f.write(content)
        return wrapper
    
    else:
        wrapper = os.path.join(install_dir, "copy")
        content = f'''#!/bin/sh
"{sys.executable}" "{script_path}" "$@"
'''
        with open(wrapper, "w") as f:
            f.write(content)
        os.chmod(wrapper, 0o755)
        return wrapper


def check_dependencies():
    """Check for pyperclip."""
    try:
        import pyperclip
        print("✓ pyperclip is installed")
        return True
    except ImportError:
        print("✗ pyperclip not found")
        print(f"\nInstall: {sys.executable} -m pip install pyperclip")
        
        if platform.system() == "Linux":
            print("\nLinux clipboard tools:")
            print("  X11:      sudo apt install xclip")
            print("  Wayland:  sudo apt install wl-clipboard")
        
        return False


def main():
    print("Installing 'copy' command...")
    
    if sys.version_info < (3, 6):
        print("Error: Python 3.6+ required")
        sys.exit(1)
    
    if not check_dependencies():
        print("\nInstall dependencies first.")
        sys.exit(1)
    
    script_dir = os.path.dirname(os.path.abspath(__file__))
    main_script = os.path.join(script_dir, "copy_command.py")
    
    if not os.path.exists(main_script):
        print(f"Error: copy_command.py not found")
        sys.exit(1)
    
    install_dir = get_install_dir()
    os.makedirs(install_dir, exist_ok=True)
    
    dest_script = os.path.join(install_dir, "copy_command.py")
    try:
        shutil.copy2(main_script, dest_script)
        print(f"✓ Script copied to {dest_script}")
    except PermissionError:
        print(f"Permission denied: {install_dir}")
        print("Try: sudo python install_copy.py")
        sys.exit(1)
    
    wrapper = create_wrapper(install_dir, dest_script)
    print(f"✓ Wrapper created: {wrapper}")
    
    if not check_in_path(install_dir):
        print(f"\n⚠️  {install_dir} is not in PATH")
        
        system = platform.system()
        if system == "Windows":
            print(f'Add to PATH: {install_dir}')
        elif system == "Darwin":
            rc_file = "~/.zshrc" if "zsh" in os.environ.get("SHELL", "") else "~/.bash_profile"
            print(f'Add to {rc_file}:')
            print(f'  export PATH="{install_dir}:$PATH"')
        else:
            rc_file = "~/.bashrc" if "bash" in os.environ.get("SHELL", "") else "~/.zshrc"
            print(f'Add to {rc_file}:')
            print(f'  export PATH="{install_dir}:$PATH"')
    else:
        print(f"\n✅ Installation complete!")
        print("Test: copy --help")


if __name__ == "__main__":
    main()
