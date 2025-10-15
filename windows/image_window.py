from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox)
from PyQt6.QtGui import QPixmap
from .rle import compress_rle, decompress_rle, image_to_string, string_to_image
import os


class ImageCompressionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compresión de Imágenes - RLE")
        self.setGeometry(350, 250, 600, 500)

        # Variables para la imagen y la compresión
        self.img_path = None
        self.bit_string = None
        self.compressed_data = None
        self.width = 0
        self.height = 0

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de información
        self.label_info = QLabel("Seleccione una imagen (.png o .bmp) para comprimir")
        layout.addWidget(self.label_info)

        # Vista previa de la imagen
        self.image_preview = QLabel()
        self.image_preview.setScaledContents(True)
        self.image_preview.setFixedHeight(250)
        layout.addWidget(self.image_preview)

        # Botones
        self.btn_load = QPushButton("Cargar imagen")
        self.btn_compress = QPushButton("Comprimir")
        self.btn_decompress = QPushButton("Descomprimir")
        self.btn_back = QPushButton("Volver al menú principal")

        # Agregar botones al layout
        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_compress)
        layout.addWidget(self.btn_decompress)
        layout.addWidget(self.btn_back)

        # Desactivar botones al inicio
        self.btn_compress.setEnabled(False)
        self.btn_decompress.setEnabled(False)

        self.setLayout(layout)

        # Conectar botones con funciones
        self.btn_load.clicked.connect(self.load_image)
        self.btn_compress.clicked.connect(self.compress_image)
        self.btn_decompress.clicked.connect(self.decompress_image)
        self.btn_back.clicked.connect(self.close)

    # Cargar imagen
    def load_image(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar imagen", "", "Images (*.png *.bmp)")
        if path:
            self.img_path = path
            # Convertir imagen a cadena binaria
            self.bit_string, self.width, self.height = image_to_string(path)
            # Mostrar vista previa
            self.image_preview.setPixmap(QPixmap(path))
            self.label_info.setText(f"Imagen cargada: {os.path.basename(path)}")
            self.btn_compress.setEnabled(True)

    # Comprimir imagen con RLE
    def compress_image(self):
        if not self.bit_string:
            QMessageBox.warning(self, "Error", "Primero carga una imagen.")
            return

        # Comprimir
        self.compressed_data = compress_rle(self.bit_string)

        # Guardar archivo comprimido
        compressed_path = self.img_path.rsplit(".", 1)[0] + "_comprimido.rle"
        with open(compressed_path, "w") as f:
            f.write(self.compressed_data)

        # Obtener tamaños
        original_size = os.path.getsize(self.img_path)
        compressed_size = os.path.getsize(compressed_path)

        # Habilitar descompresión
        self.btn_decompress.setEnabled(True)

        # Mensaje al usuario
        QMessageBox.information(
            self, "Compresión completa",
            f"Imagen comprimida guardada como:\n{compressed_path}\n\n"
            f"Tamaño original: {original_size} bytes\n"
            f"Tamaño comprimido: {compressed_size} bytes"
        )

    # Descomprimir imagen
    def decompress_image(self):
        if not self.compressed_data:
            QMessageBox.warning(self, "Error", "Primero comprime una imagen.")
            return

        # Descomprimir cadena
        decompressed_bits = decompress_rle(self.compressed_data)

        # Guardar imagen reconstruida
        decompressed_path = self.img_path.rsplit(".", 1)[0] + "_descomprimida.png"
        string_to_image(decompressed_bits, self.width, self.height, decompressed_path)

        # Mostrar vista previa de la imagen descomprimida
        self.image_preview.setPixmap(QPixmap(decompressed_path))

        # Mensaje al usuario
        QMessageBox.information(
            self, "Descompresión completa",
            f"Imagen descomprimida guardada como:\n{decompressed_path}"
        )
