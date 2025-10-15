from PyQt6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QPushButton
from PyQt6.QtCore import Qt
from windows.text_window import TextCompressionWindow
from windows.image_window import ImageCompressionWindow
from windows.audio_window import AudioCompressionWindow

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Compresor de datos")
        self.setGeometry(200, 200, 400, 300)

        # Widget central
        central_widget = QWidget()
        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignmentFlag.AlignCenter)
        layout.setSpacing(10)  # menor espacio entre botones

        # Botones del menú principal
        self.text_button = QPushButton("Comprimir texto")
        self.image_button = QPushButton("Comprimir imágenes")
        self.audio_button = QPushButton("Comprimir audio")

        # "CSS"
        for btn in [self.text_button, self.image_button, self.audio_button]:
            btn.setFixedWidth(200)
            btn.setFixedHeight(40)
            btn.setStyleSheet("""
                QPushButton {
                    font-size: 14px;
                    border-radius: 8px;
                    background-color: #3498db;
                    color: white;
                    padding: 6px;
                }
                QPushButton:hover {
                    background-color: #2980b9;
                }
            """)

        # Conectar botones
        self.text_button.clicked.connect(self.open_text_window)
        self.image_button.clicked.connect(self.open_image_window)
        self.audio_button.clicked.connect(self.open_audio_window)

        # Agregar botones al layout
        layout.addWidget(self.text_button)
        layout.addWidget(self.image_button)
        layout.addWidget(self.audio_button)
        central_widget.setLayout(layout)

        self.setCentralWidget(central_widget)

    def open_text_window(self):
        self.text_window = TextCompressionWindow()
        self.text_window.show()

    def open_image_window(self):
        self.image_window = ImageCompressionWindow()
        self.image_window.show()

    def open_audio_window(self):
        self.audio_window = AudioCompressionWindow()
        self.audio_window.show()