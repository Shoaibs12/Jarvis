from PyQt6.QtWidgets import QWidget, QLabel, QTextEdit, QVBoxLayout, QHBoxLayout, QLineEdit, QPushButton, QGraphicsDropShadowEffect
from PyQt6.QtGui import QMovie, QFont, QColor
from PyQt6.QtCore import Qt, QSize, QPropertyAnimation, pyqtSignal

class JarvisUI(QWidget):
    manual_activation_triggered = pyqtSignal()
    text_input_submitted = pyqtSignal(str)

    def __init__(self):
        super().__init__()
        self.init_ui()
        self.init_animation()

    def init_ui(self):
        # Frameless, transparent, futuristic window overlay style
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setGeometry(100, 100, 1000, 700)

        # Main background widget to simulate glassmorphism
        self.bg_widget = QWidget(self)
        self.bg_widget.setGeometry(0, 0, 1000, 700)
        self.bg_widget.setStyleSheet("""
            QWidget {
                background-color: rgba(5, 10, 20, 0.85);
                border: 2px solid rgba(0, 229, 255, 0.4);
                border-radius: 20px;
            }
        """)

        # Add Neon Glow to main widget
        glow = QGraphicsDropShadowEffect(self)
        glow.setBlurRadius(40)
        glow.setColor(QColor(0, 229, 255, 150))
        glow.setOffset(0, 0)
        self.bg_widget.setGraphicsEffect(glow)

        main_layout = QHBoxLayout(self.bg_widget)
        main_layout.setContentsMargins(30, 30, 30, 30)

        # Left Panel (Arc Reactor & System Status)
        left_panel = QWidget()
        left_layout = QVBoxLayout(left_panel)
        left_layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # AI Core (Arc Reactor)
        self.arc_label = QLabel()
        self.arc_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.movie = QMovie("resources/arc.gif")
        self.movie.setScaledSize(QSize(350, 350))
        self.arc_label.setMovie(self.movie)
        self.movie.start()

        # Core Glow Effect
        core_glow = QGraphicsDropShadowEffect(self)
        core_glow.setBlurRadius(60)
        core_glow.setColor(QColor(0, 255, 255, 200))
        core_glow.setOffset(0, 0)
        self.arc_label.setGraphicsEffect(core_glow)

        left_layout.addWidget(self.arc_label)

        # Dynamic AI Status text (e.g. LISTENING, REASONING)
        self.status_label = QLabel("STANDBY")
        self.status_label.setStyleSheet("""
            color: #00e5ff;
            margin-top: 20px;
            letter-spacing: 5px;
        """)
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.status_label.setFont(QFont("Consolas", 18, QFont.Weight.Bold))
        left_layout.addWidget(self.status_label)

        main_layout.addWidget(left_panel, stretch=1)

        # Right Panel (Live Terminal HUD & Memory Stream)
        right_panel = QWidget()
        right_layout = QVBoxLayout(right_panel)

        log_title = QLabel("SYSTEM METRICS & REASONING LOG")
        log_title.setStyleSheet("color: #00ffff; letter-spacing: 2px;")
        log_title.setFont(QFont("Consolas", 12, QFont.Weight.Bold))
        right_layout.addWidget(log_title)

        self.log_console = QTextEdit()
        self.log_console.setReadOnly(True)
        self.log_console.setStyleSheet("""
            QTextEdit {
                background-color: rgba(0, 15, 30, 0.6);
                color: #00ffcc;
                border: 1px solid rgba(0, 255, 255, 0.3);
                border-radius: 10px;
                padding: 15px;
                font-family: Consolas;
                font-size: 12px;
            }
        """)

        # Terminal Glow
        term_glow = QGraphicsDropShadowEffect(self)
        term_glow.setBlurRadius(20)
        term_glow.setColor(QColor(0, 255, 255, 50))
        term_glow.setOffset(0, 0)
        self.log_console.setGraphicsEffect(term_glow)

        right_layout.addWidget(self.log_console)

        # Bottom controls (Manual Activation & Text Mode Fallback)
        bottom_controls = QHBoxLayout()

        self.activate_btn = QPushButton("OVERRIDE")
        self.activate_btn.setStyleSheet("""
            QPushButton {
                background-color: rgba(0, 229, 255, 0.1);
                color: #00e5ff;
                border: 1px solid #00e5ff;
                border-radius: 5px;
                padding: 10px;
                font-weight: bold;
                letter-spacing: 2px;
            }
            QPushButton:hover {
                background-color: rgba(0, 229, 255, 0.4);
                color: white;
                box-shadow: 0 0 15px #00e5ff;
            }
        """)
        self.activate_btn.clicked.connect(self._on_activate_clicked)
        bottom_controls.addWidget(self.activate_btn)

        self.text_input = QLineEdit()
        self.text_input.setPlaceholderText("Input command override sequence...")
        self.text_input.setStyleSheet("""
            QLineEdit {
                background-color: rgba(0, 20, 40, 0.8);
                color: #00ffcc;
                border: 1px solid rgba(0, 255, 255, 0.5);
                border-radius: 5px;
                padding: 10px;
                font-family: Consolas;
            }
            QLineEdit:focus {
                border: 1px solid #00ffff;
            }
        """)
        self.text_input.returnPressed.connect(self._on_text_submitted)
        bottom_controls.addWidget(self.text_input)

        right_layout.addLayout(bottom_controls)
        main_layout.addWidget(right_panel, stretch=2)

    def _on_activate_clicked(self):
        self.manual_activation_triggered.emit()

    def _on_text_submitted(self):
        text = self.text_input.text().strip()
        if text:
            self.text_input_submitted.emit(text)
            self.text_input.clear()

    def append_log(self, text: str):
        self.log_console.append(text)
        scrollbar = self.log_console.verticalScrollBar()
        scrollbar.setValue(scrollbar.maximum())

    def init_animation(self):
        self.anim = QPropertyAnimation(self.status_label, b"windowOpacity")
        self.anim.setDuration(350)

    def set_status(self, text: str):
        self.status_label.setText(text)
        self.status_label.repaint()
        self.anim.stop()
        self.status_label.setWindowOpacity(0.0)
        self.anim.setStartValue(0.0)
        self.anim.setEndValue(1.0)
        self.anim.start()

    def show_status(self, text: str):
        self.set_status(text)

    # Allows dragging the frameless window
    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.oldPos = event.globalPosition().toPoint()

    def mouseMoveEvent(self, event):
        if hasattr(self, 'oldPos'):
            delta = event.globalPosition().toPoint() - self.oldPos
            self.move(self.x() + delta.x(), self.y() + delta.y())
            self.oldPos = event.globalPosition().toPoint()

    def mouseReleaseEvent(self, event):
        if hasattr(self, 'oldPos'):
            del self.oldPos
