<h1 align="center"> comando 'copy' </h1>
<p align="center">
  🇺🇸 <a href="README.md"><b>English</b></a> |
  🇪🇸 <b>Español</b>
</p>
<h3 align="center">Una herramienta de línea de comandos muy simple, segura y multiplataforma para copiar texto desde archivos o stdin directamente al portapapeles del sistema.</h3>

`copycmd` está diseñado para comportarse como una verdadera utilidad UNIX:

* Funciona con pipes (`|`)
* Maneja codificaciones de forma segura
* Evita copiar datos binarios por defecto
* Soporta Linux (X11 y Wayland), macOS y Windows

---

## ✨ Características

* 📋 Copia el contenido de archivos al portapapeles
* 🔗 Lee desde **stdin** (pipes)
* 🛡️ Detección de binarios para evitar copiar basura accidentalmente
* ⚙️ Fallback de codificación (`utf-8`, `latin-1`, etc.)
* 🐧 Verificación del portapapeles consciente de Linux (X11 y Wayland)
* 🖥 Funciona en Windows, macOS y Linux
* 🧩 Dependencias mínimas (solo `pyperclip`)

---

## 📦 Estructura del repositorio

```
copycmd/
├── copy_command.py   # Herramienta CLI principal
├── installer.py      # Script de instalación
├── README.md
└── README_ES.md
```

---

## 🔧 Requisitos

* Python **3.6+**
* `pyperclip`

### Dependencias del portapapeles en Linux

Según tu entorno:

* **X11**:

  ```bash
  sudo apt install xclip
  ```

* **Wayland**:

  ```bash
  sudo apt install wl-clipboard
  ```

Extras opcionales vía pip:

```bash
pip install 'pyperclip[xclip]'
```

---

## 🚀 Instalación

Clona el repositorio:

```bash
git clone https://github.com/URDev4ever/copycmd.git
cd copycmd
```

Instala el comando:

```bash
python installer.py
```

El instalador hará lo siguiente:

* Copiará `copy_command.py` a un directorio apropiado
* Creará un comando wrapper `copy`
* Te advertirá si el directorio no está en tu `PATH`

---

## 🧪 Uso

### Copiar desde un archivo

```bash
copy file.txt
```

### Copiar desde stdin (pipes)

```bash
cat file.txt | copy
echo "hello world" | copy
ls -la | copy
```

### Combinar múltiples archivos

```bash
cat *.txt | copy
```

### Salida detallada (verbose)

```bash
copy file.txt -v
cat file.txt | copy -v
```

### Forzar copia de contenido tipo binario (no recomendado)

```bash
copy suspicious.bin -f
```

Esto copia una **vista previa**, no el archivo binario completo.

---

## ⚠️ Notas

* Si **stdin está presente**, siempre tiene prioridad sobre los archivos:

  ```bash
  echo test | copy file.txt  # copia 'test', ignora file.txt
  ```

* En **Linux Wayland**, la verificación del portapapeles puede ser limitada debido a restricciones del compositor.

* Archivos grandes (>10MB) se rechazan por defecto.

---

## 🧠 Códigos de salida

| Código | Significado        |
| -----: | ------------------ |
|      0 | Éxito              |
|      1 | Error              |
|    130 | Cancelado (Ctrl+C) |

---

## 🛠️ Desarrollo

Ejecutar directamente sin instalar (NO recomendado):

```bash
python copy_command.py file.txt
```

---

## ⭐ Contribuir

Los pull requests son bienvenidos si mejoran el comando mediante:

* Agregar flags útiles u opciones de calidad de vida
* Mejorar la detección del portapapeles o la compatibilidad entre plataformas
* Hacer el código más simple, seguro o robusto

Por favor reporta cualquier bug que encuentres, ¡gracias ;)
Si te gusta este proyecto, ¡no dudes en darle ⭐ al repositorio!

---

Hecho con <3 por URDev
