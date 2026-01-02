#!/usr/bin/env python3
"""
copy - Copy file contents or stdin to clipboard
"""

import sys
import os
import platform
import argparse

try:
    import pyperclip
except ImportError:
    print("Error: pyperclip not installed.")
    print("Install with: pip install pyperclip")
    sys.exit(1)


def verify_clipboard_linux(test_text="clipboard_test"):
    """Linux clipboard verification with readback check."""
    try:
        import time
        pyperclip.copy(test_text)
        time.sleep(0.1)
        
        try:
            pasted = pyperclip.paste()
            if pasted.strip() != test_text.strip():
                return False, "Clipboard verification failed"
        except Exception:
            pass  # Some systems don't allow paste()
        
        return True, None
    except Exception as e:
        return False, f"Clipboard error: {e}"


def check_clipboard_access():
    """Verify clipboard functionality."""
    system = platform.system()
    
    if system == "Linux":
        success, msg = verify_clipboard_linux()
        if not success:
            print(f"Clipboard issue: {msg}")
            print("\nLinux clipboard setup:")
            print("X11:      sudo apt install xclip")
            print("Wayland:  sudo apt install wl-clipboard")
            print("\nPip extras: pip install 'pyperclip[xclip]'")
            return False
        return True
    
    try:
        pyperclip.copy("test")
        return True
    except Exception as e:
        print(f"Clipboard error: {e}")
        return False


def detect_binary(content):
    """Check if content appears to be binary."""
    if not content:
        return False
    
    if '\x00' in content:
        return True
    
    if len(content) > 1000:
        sample = content[:1000]
        printable = sum(1 for c in sample if 32 <= ord(c) <= 126 or c in '\n\r\t')
        if printable / len(sample) < 0.7:
            return True
    
    return False


def read_file_safely(filepath):
    """Read file with encoding fallback."""
    if not os.path.exists(filepath):
        return None, f"File not found: {filepath}"
    
    if not os.path.isfile(filepath):
        return None, f"Not a file: {filepath}"
    
    filesize = os.path.getsize(filepath)
    if filesize > 10 * 1024 * 1024:
        return None, f"File too large (>10MB): {filesize:,} bytes"
    
    if filesize == 0:
        return "", None
    
    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
    
    for encoding in encodings:
        try:
            with open(filepath, 'r', encoding=encoding) as f:
                content = f.read()
                if detect_binary(content):
                    return None, "File appears to be binary"
                return content, None
        except UnicodeDecodeError:
            continue
        except PermissionError:
            return None, f"Permission denied: {filepath}"
        except Exception as e:
            return None, f"Read error: {e}"
    
    return None, "Cannot decode file"


def copy_to_clipboard(content):
    """Copy content to clipboard."""
    try:
        pyperclip.copy(content)
        return True, None
    except pyperclip.PyperclipException as e:
        return False, f"Clipboard error: {e}"
    except Exception as e:
        return False, f"Unexpected error: {e}"


def main():
    parser = argparse.ArgumentParser(
        description='Copy file contents or stdin to clipboard',
        epilog='Examples:\n  copy file.txt\n  cat file.txt | copy\n  echo "text" | copy'
    )
    parser.add_argument(
        'file',
        nargs='?',
        help='File to copy (omit to read from stdin)'
    )
    parser.add_argument(
        '-v', '--verbose',
        action='store_true',
        help='Show detailed information'
    )
    parser.add_argument(
        '-f', '--force',
        action='store_true',
        help='Force copy even if content appears binary'
    )
    
    args = parser.parse_args()
    
    if not check_clipboard_access():
        sys.exit(1)
    
    content = None
    source_name = "stdin"
    
    # Read from stdin if pipe detected or no file provided
    if not sys.stdin.isatty():
        content = sys.stdin.read()
        if not content and args.file:
            # stdin empty but file specified
            pass
    elif args.file:
        # Read from file
        content, error = read_file_safely(args.file)
        if error:
            if "binary" in error and args.force:
                try:
                    with open(args.file, 'rb') as f:
                        raw = f.read(1000)
                        content = str(raw[:100]) + "..." if len(raw) > 100 else str(raw)
                except:
                    print(error)
                    sys.exit(1)
            else:
                print(error)
                sys.exit(1)
        source_name = os.path.basename(args.file)
    else:
        # No stdin and no file
        parser.print_help()
        print("\nError: No input provided")
        print("Use: copy <file>  or  pipe data to copy")
        sys.exit(1)
    
    if content is None:
        print("Error: No content to copy")
        sys.exit(1)
    
    if content == "":
        print("Empty input")
        copy_to_clipboard("")
        sys.exit(0)
    
    if detect_binary(content) and not args.force:
        print("Warning: Input appears to be binary")
        print("Use -f to force copy")
        sys.exit(1)
    
    success, error = copy_to_clipboard(content)
    if not success:
        print(error)
        sys.exit(1)
    
    # Calculate statistics
    chars = len(content)
    lines = content.count('\n')
    lines = lines + 1 if content and not content.endswith('\n') else lines
    
    if source_name == "stdin":
        print(f"✓ Copied stdin to clipboard")
    else:
        print(f"✓ Copied '{source_name}' to clipboard")
    
    if args.verbose:
        if args.file:
            print(f"  Path: {os.path.abspath(args.file)}")
            print(f"  Size: {os.path.getsize(args.file):,} bytes")
        print(f"  Lines: {lines:,}")
        print(f"  Characters: {chars:,}")
        
        if platform.system() == "Linux":
            print("  Note: Clipboard verification may be limited on Wayland")
    else:
        print(f"  ({chars:,} chars, {lines:,} lines)")


if __name__ == "__main__":
    try:
        main()
    except KeyboardInterrupt:
        print("\nCancelled")
        sys.exit(130)
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)
