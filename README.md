# Proyecto de Compresión de Datos

## Descripción
Este proyecto es una aplicación de escritorio desarrollada en **Python** con **PyQt6**, que permite al usuario comprimir y descomprimir **texto, imágenes y audio** utilizando distintos algoritmos de compresión.

La aplicación cuenta con una interfaz gráfica intuitiva y uniforme para las tres secciones, permitiendo cargar archivos, ejecutar la compresión, visualizar el tamaño original vs comprimido y descomprimir los archivos fácilmente.

---

## Funcionalidades

### 1. Compresión de Texto
- **Algoritmo:** Huffman
- **Entrada:** Archivo `.txt`
- **Salida:** Archivo comprimido `.bin` y opción de descomprimirlo a `.txt`
- **Descripción:**  
  Se realiza la compresión Huffman de los caracteres del archivo de texto. La aplicación muestra el tamaño original y el tamaño comprimido, y permite descomprimir el archivo a su contenido original.

### 2. Compresión de Imágenes
- **Algoritmo:** Run Length Encoding (RLE) aplicado píxel por píxel
- **Entrada:** Imagen `.png` o `.bmp`
- **Salida:** Archivo comprimido `.rle` y opción de reconstruir la imagen original
- **Descripción:**  
  Convierte la imagen a escala de grises y codifica los píxeles usando RLE. La aplicación muestra la previsualización de la imagen y permite descomprimirla para obtener el archivo original en `.png`.

### 3. Compresión de Audio
- **Algoritmo:** RLE sobre muestras de audio WAV
- **Entrada:** Archivo `.wav`
- **Salida:** Archivo comprimido `.rle` y opción de reconstruir el audio original `.wav`
- **Descripción:**  
  Se comprimen los datos del audio usando RLE. Este método es educativo y funciona mejor con audio simple (mono, pocas variaciones). Se puede reproducir el audio descomprimido.

---

## Estructura del Proyecto

```text
Proyecto compresión de datos/
│
├─ main.py
├─ main_window.py
├─ windows/
│   ├─ text_window.py
│   ├─ image_window.py
│   ├─ audio_window.py
│   ├─ huffman.py
│   └─ rle.py
└─ README.md

## Requisitos
- **Python 3.8 o superior**
- **Librerias necesarias:**
  - pip install PyQt6
  - pip install Pillow
  - pip install numpy
  - pip install pydub
