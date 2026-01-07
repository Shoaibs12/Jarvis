from PyQt6.QtCore import Qt, QTimer, QPointF
from PyQt6.QtGui import QPainter, QBrush, QColor, QPen
from PyQt6.QtWidgets import QWidget
import math

class ArcReactorWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.angle = 0
        self.pulse = 0
        self.pulse_dir = 1

        # Animation timers
        self.timer = QTimer()
        self.timer.timeout.connect(self.animate)
        self.timer.start(16)  # ~60 FPS

    def animate(self):
        self.angle += 2
        if self.angle >= 360:
            self.angle = 0

        # Pulse glow
        self.pulse += 0.02 * self.pulse_dir
        if self.pulse > 1 or self.pulse < 0:
            self.pulse_dir *= -1

        self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setRenderHint(QPainter.RenderHint.Antialiasing)

        w = self.width()
        h = self.height()
        r = min(w, h) / 2 - 10
        center = QPointF(w / 2, h / 2)

        # Background
        painter.setBrush(QBrush(QColor(10, 15, 30)))
        painter.drawEllipse(center, r, r)

        # Glowing core
        glow_strength = 180 + int(self.pulse * 75)
        painter.setBrush(QBrush(QColor(0, 200, 255, glow_strength)))
        painter.setPen(Qt.PenStyle.NoPen)
        painter.drawEllipse(center, r * 0.40, r * 0.40)

        # Rotating blades
        painter.setPen(QPen(QColor(0, 255, 255), 4))
        for i in range(6):
            angle = math.radians(self.angle + i * 60)
            x1 = center.x() + math.cos(angle) * (r * 0.45)
            y1 = center.y() + math.sin(angle) * (r * 0.45)
            x2 = center.x() + math.cos(angle) * (r * 0.90)
            y2 = center.y() + math.sin(angle) * (r * 0.90)
            painter.drawLine(int(x1), int(y1), int(x2), int(y2))
