from PyQt6.QtWidgets import (QWidget, QVBoxLayout, QPushButton, QLabel,
                             QFileDialog, QMessageBox)
from pydub import AudioSegment
import numpy as np
import os

# Funciones de compresion/descompresion simplificadas con RLE para audio
def compress_audio_rle(samples):
    if len(samples) == 0:
        return []
    compressed = []
    count = 1
    for i in range(1, len(samples)):
        if samples[i] == samples[i - 1]:
            count += 1
        else:
            compressed.append((samples[i - 1], count))
            count = 1
    compressed.append((samples[-1], count))
    return compressed

def decompress_audio_rle(compressed):
    decompressed = []
    for value, count in compressed:
        decompressed.extend([value] * count)
    return np.array(decompressed, dtype=np.int16)


class AudioCompressionWindow(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Compresión de Audio - WAV RLE")
        self.setGeometry(350, 250, 450, 300)

        # Variables internas
        self.audio_path = None
        self.audio_data = None
        self.compressed_data = None
        self.frame_rate = 44100  # valor por defecto
        self.channels = 1

        # Layout principal
        layout = QVBoxLayout()

        # Etiqueta de informacion
        self.label_info = QLabel("Seleccione un archivo de audio (.wav) para comprimir")
        layout.addWidget(self.label_info)

        # Botones
        self.btn_load = QPushButton("Cargar audio")
        self.btn_compress = QPushButton("Comprimir")
        self.btn_decompress = QPushButton("Descomprimir")
        self.btn_back = QPushButton("Volver al menú principal")

        layout.addWidget(self.btn_load)
        layout.addWidget(self.btn_compress)
        layout.addWidget(self.btn_decompress)
        layout.addWidget(self.btn_back)

        # Desactivar botones de compresion/descompresion al inicio
        self.btn_compress.setEnabled(False)
        self.btn_decompress.setEnabled(False)

        self.setLayout(layout)

        # Conectar botones
        self.btn_load.clicked.connect(self.load_audio)
        self.btn_compress.clicked.connect(self.compress_audio)
        self.btn_decompress.clicked.connect(self.decompress_audio)
        self.btn_back.clicked.connect(self.close)

    # Cargar archivo de audio
    def load_audio(self):
        path, _ = QFileDialog.getOpenFileName(self, "Seleccionar archivo de audio", "", "Audio Files (*.wav)")
        if path:
            self.audio_path = path
            audio = AudioSegment.from_wav(path)
            self.frame_rate = audio.frame_rate
            self.channels = audio.channels
            samples = np.array(audio.get_array_of_samples(), dtype=np.int16)
            self.audio_data = samples
            self.label_info.setText(f"Audio cargado: {os.path.basename(path)}\nDuración: {len(audio)/1000:.2f} segundos")
            self.btn_compress.setEnabled(True)

    # Comprimir audio
    def compress_audio(self):
        if self.audio_data is None:
            QMessageBox.warning(self, "Error", "Primero carga un archivo de audio.")
            return

        self.compressed_data = compress_audio_rle(self.audio_data)
        compressed_path = self.audio_path.rsplit(".", 1)[0] + "_comprimido.rle"
        # Guardar en formato simple (texto)
        with open(compressed_path, "w") as f:
            for value, count in self.compressed_data:
                f.write(f"{value},{count} ")
        self.btn_decompress.setEnabled(True)

        original_size = os.path.getsize(self.audio_path)
        compressed_size = os.path.getsize(compressed_path)
        QMessageBox.information(
            self, "Compresión completa",
            f"Audio comprimido guardado como:\n{compressed_path}\n\n"
            f"Tamaño original: {original_size} bytes\n"
            f"Tamaño comprimido: {compressed_size} bytes"
        )

    # Descomprimir audio
    def decompress_audio(self):
        if self.compressed_data is None:
            QMessageBox.warning(self, "Error", "Primero comprime el audio.")
            return

        decompressed_samples = decompress_audio_rle(self.compressed_data)
        decompressed_path = self.audio_path.rsplit(".", 1)[0] + "_descomprimido.wav"

        # Reconstruir audio con pydub
        audio_segment = AudioSegment(
            decompressed_samples.tobytes(),
            frame_rate=self.frame_rate,
            sample_width=decompressed_samples.dtype.itemsize,
            channels=self.channels
        )
        audio_segment.export(decompressed_path, format="wav")
        QMessageBox.information(
            self, "Descompresión completa",
            f"Audio descomprimido guardado como:\n{decompressed_path}"
        )
