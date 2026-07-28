try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox
    from PyQt6.QtCore import Qt
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QListWidget, QListWidgetItem, QPushButton, QHBoxLayout, QLabel, QMessageBox
        from PySide6.QtCore import Qt
        HAS_QT = True
    except ImportError:
        HAS_QT = False

from enhancex.ai.model_loader import ModelLoader


if HAS_QT:
    class ModelManagerWidget(QWidget):
        """Model Manager Widget for downloading and selecting AI neural weights."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.model_loader = ModelLoader()

            layout = QVBoxLayout(self)

            title = QLabel("🧠 Neural Model Manager", self)
            title.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: bold;")
            layout.addWidget(title)

            self.list_widget = QListWidget(self)
            self.list_widget.setStyleSheet("""
                QListWidget {
                    background-color: #1E293B;
                    color: #F8FAFC;
                    border-radius: 8px;
                    padding: 8px;
                }
                QListWidget::item {
                    padding: 10px;
                    border-bottom: 1px solid #334155;
                }
                QListWidget::item:selected {
                    background-color: #3B82F6;
                    border-radius: 4px;
                }
            """)
            layout.addWidget(self.list_widget)

            btn_layout = QHBoxLayout()
            self.btn_download = QPushButton("⬇️ Download Selected Weights", self)
            self.btn_download.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
            self.btn_download.clicked.connect(self.download_selected)

            btn_layout.addWidget(self.btn_download)
            layout.addLayout(btn_layout)

            self.refresh_list()

        def refresh_list(self):
            self.list_widget.clear()
            for model_name in self.model_loader.MODEL_REGISTRY.keys():
                path = self.model_loader.get_model_path(model_name, auto_download=False)
                is_cached = " (Cached locally)" if path and os.path.exists(path) else " (Not Downloaded)"
                item = QListWidgetItem(f"{model_name.upper()}{is_cached}")
                item.setData(Qt.ItemDataRole.UserRole, model_name)
                self.list_widget.addItem(item)

        def download_selected(self):
            curr_item = self.list_widget.currentItem()
            if not curr_item:
                return
            model_name = curr_item.data(Qt.ItemDataRole.UserRole)
            try:
                self.model_loader.download_model(model_name)
                QMessageBox.information(self, "Download Complete", f"Successfully downloaded pre-trained weights for {model_name}.")
                self.refresh_list()
            except Exception as e:
                QMessageBox.warning(self, "Download Failed", f"Failed to download {model_name}: {e}")
else:
    class ModelManagerWidget:
        def __init__(self, *args, **kwargs):
            pass
