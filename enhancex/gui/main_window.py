import os
import sys
try:
    from PyQt6.QtWidgets import (
        QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
        QPushButton, QLabel, QSplitter, QFileDialog, QMessageBox, QSlider
    )
    from PyQt6.QtCore import Qt, QUrl
    from PyQt6.QtGui import QIcon, QPixmap
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import (
            QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QTabWidget,
            QPushButton, QLabel, QSplitter, QFileDialog, QMessageBox, QSlider
        )
        from PySide6.QtCore import Qt, QUrl
        from PySide6.QtGui import QIcon, QPixmap
        HAS_QT = True
    except ImportError:
        HAS_QT = False

from enhancex.api.high_level import VideoEnhancer, ImageEnhancer
from enhancex.gui.widgets.dropzone import DropZoneWidget
from enhancex.gui.widgets.split_comparison import SplitComparisonWidget
from enhancex.gui.widgets.gpu_monitor import GPUMonitorWidget
from enhancex.gui.widgets.batch_queue import BatchQueueWidget
from enhancex.gui.widgets.model_manager_widget import ModelManagerWidget
from enhancex.gui.widgets.settings_widget import SettingsWidget
from enhancex.gui.widgets.export_wizard import ExportWizardDialog


if HAS_QT:
    class EnhanceXStudioWindow(QMainWindow):
        """EnhanceX Studio Desktop Application Main Window."""

        def __init__(self):
            super().__init__()
            self.setWindowTitle("EnhanceX Studio - AI Image & Video Enhancement Suite")
            self.resize(1280, 800)

            self.image_enhancer = ImageEnhancer()
            self.video_enhancer = VideoEnhancer()
            self.current_filepath = None

            self.apply_theme()
            self.init_ui()

        def apply_theme(self):
            self.setStyleSheet("""
                QMainWindow {
                    background-color: #0F172A;
                }
                QTabWidget::pane {
                    border: 1px solid #334155;
                    background-color: #1E293B;
                    border-radius: 8px;
                }
                QTabBar::tab {
                    background-color: #0F172A;
                    color: #94A3B8;
                    padding: 10px 20px;
                    font-weight: bold;
                    border-top-left-radius: 6px;
                    border-top-right-radius: 6px;
                }
                QTabBar::tab:selected {
                    background-color: #1E293B;
                    color: #38BDF8;
                    border-bottom: 2px solid #38BDF8;
                }
                QPushButton {
                    background-color: #3B82F6;
                    color: white;
                    border-radius: 6px;
                    padding: 8px 16px;
                    font-weight: bold;
                }
                QPushButton:hover {
                    background-color: #2563EB;
                }
            """)

        def init_ui(self):
            main_widget = QWidget(self)
            self.setCentralWidget(main_widget)
            main_layout = QHBoxLayout(main_widget)

            # Left Sidebar Tabs
            self.tabs = QTabWidget(self)
            
            # Tab 1: Studio Workspace
            workspace_tab = QWidget()
            ws_layout = QVBoxLayout(workspace_tab)

            # Dropzone
            self.dropzone = DropZoneWidget(self)
            self.dropzone.filesDropped.connect(self.load_media_files)
            ws_layout.addWidget(self.dropzone)

            # Split Comparison Player
            self.split_player = SplitComparisonWidget(self)
            ws_layout.addWidget(self.split_player, stretch=1)

            # Timeline Slider
            timeline_layout = QHBoxLayout()
            timeline_layout.addWidget(QLabel("Timeline:", self))
            self.timeline_slider = QSlider(Qt.Orientation.Horizontal, self)
            timeline_layout.addWidget(self.timeline_slider)
            ws_layout.addLayout(timeline_layout)

            # Action Bar
            action_layout = QHBoxLayout()
            self.btn_enhance = QPushButton("✨ Enhance Media", self)
            self.btn_enhance.clicked.connect(self.process_current_media)
            self.btn_export_wizard = QPushButton("⚙️ Export Wizard...", self)
            self.btn_export_wizard.clicked.connect(self.open_export_wizard)

            action_layout.addWidget(self.btn_enhance)
            action_layout.addWidget(self.btn_export_wizard)
            ws_layout.addLayout(action_layout)

            self.tabs.addTab(workspace_tab, "🎨 Workspace")

            # Tab 2: Batch Queue
            self.batch_widget = BatchQueueWidget(self)
            self.tabs.addTab(self.batch_widget, "📋 Batch Queue")

            # Tab 3: Model Manager
            self.model_widget = ModelManagerWidget(self)
            self.tabs.addTab(self.model_widget, "🧠 Model Hub")

            # Tab 4: System Settings
            self.settings_widget = SettingsWidget(self)
            self.tabs.addTab(self.settings_widget, "⚙️ Settings")

            main_layout.addWidget(self.tabs, stretch=3)

            # Right Panel: Hardware Performance Monitor
            right_panel = QVBoxLayout()
            self.gpu_monitor = GPUMonitorWidget(self)
            right_panel.addWidget(self.gpu_monitor)
            right_panel.addStretch()

            main_layout.addLayout(right_panel, stretch=1)

        def load_media_files(self, filepaths: list):
            if not filepaths:
                return
            self.current_filepath = filepaths[0]
            if self.current_filepath.lower().endswith(('.png', '.jpg', '.jpeg', '.bmp', '.webp')):
                pixmap = QPixmap(self.current_filepath)
                self.split_player.set_images(pixmap, pixmap)
            self.batch_widget.add_item(self.current_filepath, "AI Super Resolution 4x")

        def process_current_media(self):
            if not self.current_filepath:
                QMessageBox.warning(self, "No Media", "Please drag and drop an image or video first.")
                return

            ext = self.current_filepath.split(".")[-1].lower()
            if ext in ["jpg", "jpeg", "png", "bmp", "webp"]:
                out_img = self.image_enhancer.enhance(self.current_filepath, sharpen=1.5, clahe=True)
                # Convert enhanced image to QPixmap for split view after comparison
                h, w, c = out_img.shape
                bytes_per_line = c * w
                qimg_after = QImage(out_img.data, w, h, bytes_per_line, QImage.Format.Format_BGR888)
                pixmap_before = QPixmap(self.current_filepath)
                pixmap_after = QPixmap.fromImage(qimg_after)
                self.split_player.set_images(pixmap_before, pixmap_after)
                QMessageBox.information(self, "Enhancement Complete", "Image enhancement finished! View comparison slider.")

        def open_export_wizard(self):
            dialog = ExportWizardDialog(self)
            dialog.exec()

        def show_about_dialog(self):
            QMessageBox.about(
                self,
                "About EnhanceX Studio v2.0.0",
                "<h2>EnhanceX v2.0.0</h2>"
                "<p>Universal AI-Powered Image & Video Enhancement Suite</p>"
                "<p><b>Created by:</b> Slock Ahuja</p>"
                "<p><b>GitHub:</b> <a href='https://github.com/SlockAhuja/EnhanceX'>https://github.com/SlockAhuja/EnhanceX</a></p>"
            )
else:
    class EnhanceXStudioWindow:
        def __init__(self, *args, **kwargs):
            pass
