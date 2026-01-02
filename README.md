<h1 align="center"> 'copy' command </h1>

<h3 align="center">A very simple, safe, and cross-platform command-line tool to copy text **from files or stdin** directly to your system clipboard.</h3>

`copycmd` is designed to behave like a real UNIX utility:

* Works with pipes (`|`)
* Handles encodings safely
* Avoids copying binary data by default
* Supports Linux (X11 & Wayland), macOS, and Windows

---

## ✨ Features

* 📋 Copy file contents to clipboard
* 🔗 Read from **stdin** (pipes)
* 🛡️ Binary detection to prevent accidental garbage copies
* ⚙️ Encoding fallback (`utf-8`, `latin-1`, etc.)
* 🐧 Linux-aware clipboard verification (X11 & Wayland)
* 🖥 Works on Windows, macOS, and Linux
* 🧩 Minimal dependencies (`pyperclip` only)

---

## 📦 Repository Structure

```
copycmd/
├── copy_command.py   # Main CLI tool
├── installer.py      # Installer script
└── README.md
```

---

## 🔧 Requirements

* Python **3.6+**
* `pyperclip`

### Linux clipboard dependencies

Depending on your environment:

* **X11**:

  ```bash
  sudo apt install xclip
  ```

* **Wayland**:

  ```bash
  sudo apt install wl-clipboard
  ```

Optional pip extras:

```bash
pip install 'pyperclip[xclip]'
```

---

## 🚀 Installation

Clone the repository:

```bash
git clone https://github.com/URDev4ever/copycmd.git
cd copycmd
```

Install the command:

```bash
python installer.py
```

The installer will:

* Copy `copy_command.py` to an appropriate directory
* Create a `copy` wrapper command
* Warn you if the directory is not in your `PATH`

---

## 🧪 Usage

### Copy from a file

```bash
copy file.txt
```

### Copy from stdin (pipes)

```bash
cat file.txt | copy
echo "hello world" | copy
ls -la | copy
```

### Combine multiple files

```bash
cat *.txt | copy
```

### Verbose output

```bash
copy file.txt -v
cat file.txt | copy -v
```

### Force copy binary-like content (not recommended)

```bash
copy suspicious.bin -f
```

This copies a **preview**, not the full binary file.

---

## ⚠️ Notes

* If **stdin is present**, it always takes priority over file arguments:

  ```bash
  echo test | copy file.txt  # copies 'test', ignores file.txt
  ```

* On **Linux Wayland**, clipboard verification may be limited due to compositor restrictions.

* Large files (>10MB) are rejected by default.

---

## 🧠 Exit Codes

| Code | Meaning            |
| ---: | ------------------ |
|    0 | Success            |
|    1 | Error              |
|  130 | Cancelled (Ctrl+C) |

---

## 🛠️ Development

Run directly without installing (NOT recommended):

```bash
python copy_command.py file.txt
```

---
## ⭐ Contributing

Pull requests are welcome if they improve the command by:
- Adding useful CLI flags or quality-of-life options
- Improving clipboard detection or compatibility across platforms
- Making the code simpler, safer, or more robust

Please report any bugs you encounter, thx ;)
If you like this project, feel free to ⭐ the repository!

---
Made with <3 by URDev

