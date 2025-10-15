from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
    QFileDialog, QMessageBox
)
import os
from .huffman import encode, decode


class TextCompressionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compresión de Texto - Huffman")
        self.setGeometry(350, 250, 450, 320)

        # Variables para guardar la informacion del archivo
        self.file_path = None
        self.codes = None
        self.bit_string = None

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de informacion
        self.label_info = QLabel("Seleccione un archivo .txt para comprimir")
        layout.addWidget(self.label_info)

        # Botones
        self.btn_load = QPushButton("Cargar archivo")
        self.btn_compress = QPushButton("Comprimir")
        self.btn_decompress = QPushButton("Descomprimir")
        self.btn_back = QPushButton("Volver al menú principal")

        # Agregar los botones al layout
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_compress)
        layout.addWidget(self.btn_decompress)
        layout.addWidget(self.btn_back)

        # Desactivar los botones de compresion/descompresion al inicio
        self.btn_compress.setEnabled(False)
        self.btn_decompress.setEnabled(False)

        self.setLayout(layout)

        # Conectar los botones a sus funciones
        self.btn_load.clicked.connect(self.load_file)
        self.btn_compress.clicked.connect(self.compress_file)
        self.btn_decompress.clicked.connect(self.decompress_file)
        self.btn_back.clicked.connect(self.close)

    # Cargar archivo de texto
    def load_file(self):
        file_name, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de texto", "", "Text Files (*.txt)")
        if file_name:
            self.file_path = file_name
            file_size = os.path.getsize(file_name)
            self.label_info.setText(f"Archivo cargado: {os.path.basename(file_name)}\nTamaño original: {file_size} bytes")
            self.btn_compress.setEnabled(True)

    # Comprimir archivo
    def compress_file(self):
        # Leer el texto original
        with open(self.file_path, 'r', encoding='utf-8') as f:
            text = f.read()

        # Codificar con Huffman
        bit_string, codes = encode(text)
        self.codes = codes
        self.bit_string = bit_string

        # Convertir la cadena de bits a bytes para guardarla
        padding = 8 - len(bit_string) % 8
        bit_string += "0" * padding
        b = bytearray()
        b.append(padding)
        for i in range(0, len(bit_string), 8):
            byte = bit_string[i:i + 8]
            b.append(int(byte, 2))

        # Guardar el archivo comprimido
        compressed_path = self.file_path.replace(".txt", "_comprimido.bin")
        with open(compressed_path, 'wb') as f:
            f.write(b)

        # Obtener los tamaños
        original_size = os.path.getsize(self.file_path)
        compressed_size = os.path.getsize(compressed_path)

        # Habilitar boton de descompresión
        self.btn_decompress.setEnabled(True)

        # Mostrar mensaje al usuario
        QMessageBox.information(
            self, "Compresión completa",
            f"Archivo comprimido guardado como:\n{compressed_path}\n\n"
            f"Tamaño original: {original_size} bytes\n"
            f"Tamaño comprimido: {compressed_size} bytes"
        )

    # Descomprimir archivo
    def decompress_file(self):
        # Verificar si hay datos para descomprimir
        if not self.bit_string or not self.codes:
            QMessageBox.warning(self, "Error", "No hay datos para descomprimir.")
            return

        # Decodificar el texto
        decoded_text = decode(self.bit_string, self.codes)
        decompressed_path = self.file_path.replace(".txt", "_descomprimido.txt")

        # Guardar el texto descomprimido
        with open(decompressed_path, 'w', encoding='utf-8') as f:
            f.write(decoded_text)

        # Mostrar mensaje al usuario
        QMessageBox.information(
            self, "Descompresión completa",
            f"Archivo descomprimido guardado como:\n{decompressed_path}"
        )
