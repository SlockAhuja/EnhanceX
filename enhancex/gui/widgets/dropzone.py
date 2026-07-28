import os
try:
    from PyQt6.QtWidgets import QFrame, QVBoxLayout, QLabel
    from PyQt6.QtCore import Qt, pyqtSignal
    from PyQt6.QtGui import QDragEnterEvent, QDropEvent
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QFrame, QVBoxLayout, QLabel
        from PySide6.QtCore import Qt, Signal as pyqtSignal
        from PySide6.QtGui import QDragEnterEvent, QDropEvent
        HAS_QT = True
    except ImportError:
        HAS_QT = False


if HAS_QT:
    class DropZoneWidget(QFrame):
        """Drag & Drop file upload dropzone widget."""
        filesDropped = pyqtSignal(list)

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setAcceptDrops(True)
            self.setObjectName("DropZoneWidget")
            self.setStyleSheet("""
                QFrame#DropZoneWidget {
                    border: 2px dashed #3B82F6;
                    border-radius: 12px;
                    background-color: #1E293B;
                    padding: 30px;
                }
                QFrame#DropZoneWidget:hover {
                    background-color: #334155;
                    border-color: #60A5FA;
                }
                QLabel {
                    color: #F8FAFC;
                    font-size: 15px;
                    font-weight: bold;
                }
            """)

            layout = QVBoxLayout(self)
            layout.setAlignment(Qt.AlignmentFlag.AlignCenter)

            self.icon_label = QLabel("📁 Drag & Drop Images or Videos Here", self)
            self.icon_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.icon_label)

            self.sub_label = QLabel("Supports MP4, AVI, MOV, PNG, JPG, WEBP", self)
            self.sub_label.setStyleSheet("color: #94A3B8; font-size: 12px; font-weight: normal;")
            self.sub_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
            layout.addWidget(self.sub_label)

        def dragEnterEvent(self, event: QDragEnterEvent):
            if event.mimeData().hasUrls():
                event.acceptProposedAction()

        def dropEvent(self, event: QDropEvent):
            paths = []
            for url in event.mimeData().urls():
                filepath = url.toLocalFile()
                if os.path.exists(filepath):
                    paths.append(filepath)
            if paths:
                self.filesDropped.emit(paths)
else:
    class DropZoneWidget:
        def __init__(self, *args, **kwargs):
            pass
