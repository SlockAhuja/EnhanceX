try:
    from PyQt6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QWidget, QHBoxLayout, QLabel, QSlider
        from PySide6.QtCore import Qt, Signal as pyqtSignal
        from PySide6.QtGui import QImage, QPixmap, QPainter, QPen, QColor
        HAS_QT = True
    except ImportError:
        HAS_QT = False


if HAS_QT:
    class SplitComparisonWidget(QWidget):
        """Interactive Before / After Split View Comparison Widget."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.split_pos = 0.5  # Split ratio (0.0 to 1.0)
            self.pixmap_before = None
            self.pixmap_after = None

            self.setMinimumSize(400, 300)
            self.setStyleSheet("background-color: #0F172A; border-radius: 8px;")

        def set_images(self, pixmap_before: QPixmap, pixmap_after: QPixmap):
            self.pixmap_before = pixmap_before
            self.pixmap_after = pixmap_after
            self.update()

        def set_split_position(self, pos: float):
            self.split_pos = max(0.0, min(1.0, pos))
            self.update()

        def paintEvent(self, event):
            painter = QPainter(self)
            painter.setRenderHint(QPainter.RenderHint.Antialiasing)

            w = self.width()
            h = self.height()

            if not self.pixmap_before or not self.pixmap_after:
                painter.setPen(QColor("#64748B"))
                painter.drawText(self.rect(), Qt.AlignmentFlag.AlignCenter, "No Media Loaded for Comparison")
                return

            split_x = int(w * self.split_pos)

            # Draw Before Image on Left
            scaled_before = self.pixmap_before.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
            painter.setClipRect(0, 0, split_x, h)
            painter.drawPixmap(0, 0, scaled_before)

            # Draw After Image on Right
            scaled_after = self.pixmap_after.scaled(w, h, Qt.AspectRatioMode.KeepAspectRatio)
            painter.setClipRect(split_x, 0, w - split_x, h)
            painter.drawPixmap(0, 0, scaled_after)

            # Reset Clip & Draw Divider Line
            painter.setClipping(False)
            painter.setPen(QPen(QColor("#38BDF8"), 3))
            painter.drawLine(split_x, 0, split_x, h)

            # Draw Labels
            painter.setPen(QColor("#FFFFFF"))
            painter.drawText(10, 25, "BEFORE")
            painter.drawText(w - 70, 25, "AFTER")

        def mouseMoveEvent(self, event):
            if event.buttons() & Qt.MouseButton.LeftButton:
                self.set_split_position(event.position().x() / self.width())
else:
    class SplitComparisonWidget:
        def __init__(self, *args, **kwargs):
            pass
