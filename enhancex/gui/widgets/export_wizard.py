try:
    from PyQt6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QFileDialog, QSpinBox
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QDialog, QVBoxLayout, QFormLayout, QComboBox, QLineEdit, QPushButton, QFileDialog, QSpinBox
        HAS_QT = True
    except ImportError:
        HAS_QT = False


if HAS_QT:
    class ExportWizardDialog(QDialog):
        """Export Configuration Wizard Dialog."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.setWindowTitle("EnhanceX Export Wizard")
            self.resize(500, 300)

            layout = QVBoxLayout(self)
            form = QFormLayout()

            # Output Format
            self.combo_format = QComboBox(self)
            self.combo_format.addItems(["MP4 (H.264)", "MOV (ProRes)", "PNG Sequence", "JPG Image"])
            form.addRow("Target Output Format:", self.combo_format)

            # Target Scale
            self.spin_scale = QSpinBox(self)
            self.spin_scale.setRange(1, 8)
            self.spin_scale.setValue(2)
            form.addRow("Target Upscale Factor:", self.spin_scale)

            # Target FPS
            self.spin_fps = QSpinBox(self)
            self.spin_fps.setRange(15, 240)
            self.spin_fps.setValue(60)
            form.addRow("Target Frame Rate (FPS):", self.spin_fps)

            # Output Directory
            self.edit_dir = QLineEdit(self)
            self.btn_browse = QPushButton("Browse...", self)
            self.btn_browse.clicked.connect(self.browse_dir)
            form.addRow("Destination Directory:", self.edit_dir)

            layout.addLayout(form)

            # Process Button
            self.btn_export = QPushButton("🚀 Export Media", self)
            self.btn_export.setStyleSheet("background-color: #3B82F6; color: white; font-weight: bold; padding: 10px; border-radius: 6px;")
            self.btn_export.clicked.connect(self.accept)
            layout.addWidget(self.btn_export)

        def browse_dir(self):
            path = QFileDialog.getExistingDirectory(self, "Select Export Directory")
            if path:
                self.edit_dir.setText(path)
else:
    class ExportWizardDialog:
        def __init__(self, *args, **kwargs):
            pass
