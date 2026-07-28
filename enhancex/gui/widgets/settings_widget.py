try:
    from PyQt6.QtWidgets import QWidget, QFormLayout, QComboBox, QSpinBox, QCheckBox, QLabel, QPushButton, QVBoxLayout
    from PyQt6.QtCore import Qt
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QWidget, QFormLayout, QComboBox, QSpinBox, QCheckBox, QLabel, QPushButton, QVBoxLayout
        from PySide6.QtCore import Qt
        HAS_QT = True
    except ImportError:
        HAS_QT = False

from enhancex.core.config import ConfigManager


if HAS_QT:
    class SettingsWidget(QWidget):
        """EnhanceX Framework Global Settings Page."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.config = ConfigManager.get_instance()

            layout = QVBoxLayout(self)

            title = QLabel("⚙️ EnhanceX System Settings", self)
            title.setStyleSheet("color: #38BDF8; font-size: 16px; font-weight: bold;")
            layout.addWidget(title)

            form = QFormLayout()

            # Hardware Device Selection
            self.combo_device = QComboBox(self)
            self.combo_device.addItems(["auto", "cuda", "cpu"])
            form.addRow("Hardware Acceleration Device:", self.combo_device)

            # Inference Backend Selection
            self.combo_backend = QComboBox(self)
            self.combo_backend.addItems(["onnx", "torch", "tensorrt"])
            form.addRow("Inference Engine Backend:", self.combo_backend)

            # Tile Size for Super Resolution
            self.spin_tile = QSpinBox(self)
            self.spin_tile.setRange(128, 2048)
            self.spin_tile.setValue(512)
            self.spin_tile.setSingleStep(128)
            form.addRow("Tile Inference Size (PX):", self.spin_tile)

            # Thread Pool Size
            self.spin_threads = QSpinBox(self)
            self.spin_threads.setRange(1, 32)
            self.spin_threads.setValue(4)
            form.addRow("Worker Threads:", self.spin_threads)

            layout.addLayout(form)

            # Save Button
            self.btn_save = QPushButton("💾 Save Settings", self)
            self.btn_save.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
            self.btn_save.clicked.connect(self.save_settings)
            layout.addWidget(self.btn_save)

        def save_settings(self):
            self.config.set("system.device", self.combo_device.currentText())
            self.config.set("system.backend", self.combo_backend.currentText())
            self.config.set("ai.super_resolution.tile_size", self.spin_tile.value())
            self.config.set("system.threads", self.spin_threads.value())
else:
    class SettingsWidget:
        def __init__(self, *args, **kwargs):
            pass
