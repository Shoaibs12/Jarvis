from PyQt6.QtWidgets import QWidget, QLabel
from PyQt6.QtGui import QMovie, QFont
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, QByteArray

class JarvisUI(QWidget):
    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_animation()

    # --------------------------------------------------
    # UI LAYOUT
    # --------------------------------------------------
    def init_ui(self):
        self.setWindowTitle("JARVIS")
        self.setGeometry(100, 100, 400, 430)
        self.setStyleSheet("background-color: black;")

        # Arc Reactor GIF
        self.arc_label = QLabel(self)
        self.arc_label.setGeometry(25, 10, 350, 350)
        self.arc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.movie = QMovie("resources/arc.gif")
        self.movie.setScaledSize(QSize(350, 350))
        self.arc_label.setMovie(self.movie)
        self.movie.start()

        # Status text
        self.status_label = QLabel("", self)
        self.status_label.setGeometry(0, 365, 400, 50)
        self.status_label.setStyleSheet("color: cyan;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Arial", 12))

    # --------------------------------------------------
    # FADE-IN TEXT ANIMATION
    # --------------------------------------------------
    def init_animation(self):
        self.anim = QPropertyAnimation(self.status_label, b"windowOpacity")
        self.anim.setDuration(350)

    # --------------------------------------------------
    # STATUS UPDATE FUNCTION
    # --------------------------------------------------
    def set_status(self, text: str):
        self.status_label.setText(text)
        self.status_label.repaint()

        # Fade-in animation
        self.anim.stop()
        self.status_label.setWindowOpacity(0.0)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

    # Alias for compatibility (main.py uses both)
    def show_status(self, text: str):
        self.set_status(text)

    # --------------------------------------------------
    # UI-SIDE SPEAK DISPLAY (optional)
    # --------------------------------------------------
    def speak_text(self, text: str):
        """Show what Jarvis is speaking in the UI"""
        self.set_status(f"Jarvis: {text}")
