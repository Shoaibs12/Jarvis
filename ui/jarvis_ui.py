from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout
from PyQt6.QtGui import QMovie, QFont, QColor, QPalette
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
        self.setWindowTitle("JARVIS AI OS")
        self.setGeometry(100, 100, 800, 600)
        self.setStyleSheet("background-color: #050510;")

        # Main Layout
        main_layout = QHBoxLayout(self)

        # Left Panel (Arc Reactor & Status)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Arc Reactor GIF
        self.arc_label = QLabel()
        self.arc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("resources/arc.gif")
        self.movie.setScaledSize(QSize(300, 300))
        self.arc_label.setMovie(self.movie)
        self.movie.start()
        left_layout.addWidget(self.arc_label)

        # Status text
        self.status_label = QLabel("")
        self.status_label.setStyleSheet("color: #00e5ff; margin-top: 10px;")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Consolas", 14, QFont.Weight.Bold))
        left_layout.addWidget(self.status_label)

        main_layout.addWidget(left_panel, stretch=1)

        # Right Panel (Agent Reasoning & Execution Log)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        log_title = QLabel("AUTONOMOUS REASONING & EXECUTION LOG")
        log_title.setStyleSheet("color: #00e5ff; letter-spacing: 2px;")
        log_title.setFont(QFont("Consolas", 10, QFont.Weight.Bold))
        right_layout.addWidget(log_title)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("""
            QTextEdit {
                background-color: rgba(10, 15, 30, 0.7);
                color: #a0c0ff;
                border: 1px solid #0055ff;
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas;
                font-size: 11px;
            }
        """)
        right_layout.addWidget(self.log_console)

        main_layout.addWidget(right_panel, stretch=2)

    def append_log(self, text: str):
        """Adds a line to the execution log safely."""
        self.log_console.append(text)
        # Scroll to bottom
        scrollbar = self.log_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

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
