try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
    from PyQt6.QtCore import QTimer, Qt
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QHBoxLayout, QLabel, QProgressBar
        from PySide6.QtCore import QTimer, Qt
        HAS_QT = True
    except ImportError:
        HAS_QT = False

from enhancex.gpu.manager import GPUManager


if HAS_QT:
    class GPUMonitorWidget(QWidget):
        """Real-time GPU & Hardware Performance Monitor Widget."""

        def __init__(self, parent=None):
            super().__init__(parent)
            self.gpu_mgr = GPUManager.get_instance()

            layout = QVBoxLayout(self)
            layout.setContentsMargins(10, 10, 10, 10)

            # Title
            title = QLabel("⚡ Hardware Performance Monitor", self)
            title.setStyleSheet("color: #38BDF8; font-weight: bold; font-size: 14px;")
            layout.addWidget(title)

            # Device Info Label
            self.device_label = QLabel("Device: Initializing...", self)
            self.device_label.setStyleSheet("color: #F8FAFC; font-size: 12px;")
            layout.addWidget(self.device_label)

            # Memory Progress Bar
            mem_layout = QHBoxLayout()
            mem_title = QLabel("VRAM / RAM:", self)
            mem_title.setStyleSheet("color: #94A3B8; font-size: 11px;")
            self.mem_bar = QProgressBar(self)
            self.mem_bar.setRange(0, 100)
            self.mem_bar.setValue(25)
            self.mem_bar.setStyleSheet("""
                QProgressBar {
                    background-color: #1E293B;
                    border-radius: 4px;
                    text-align: center;
                    color: #FFFFFF;
                }
                QProgressBar::chunk {
                    background-color: #10B981;
                    border-radius: 4px;
                }
            """)
            mem_layout.addWidget(mem_title)
            mem_layout.addWidget(self.mem_bar)
            layout.addLayout(mem_layout)

            # Refresh Timer (1 second)
            self.timer = QTimer(self)
            self.timer.timeout.connect(self.update_stats)
            self.timer.start(1000)
            self.update_stats()

        def update_stats(self):
            info = self.gpu_mgr.get_device_info()
            dev_name = info.get("name", "CPU Engine")
            is_cuda = info.get("is_cuda", False)

            self.device_label.setText(f"Active Backend: {dev_name} ({'CUDA Accelerated' if is_cuda else 'CPU Fallback'})")

            if is_cuda and "memory_allocated_mb" in info and "memory_total_mb" in info:
                used = info["memory_allocated_mb"]
                total = max(1.0, info["memory_total_mb"])
                pct = int((used / total) * 100)
                self.mem_bar.setValue(pct)
                self.mem_bar.setFormat(f"{pct}% ({used:.0f}MB / {total:.0f}MB)")
            else:
                self.mem_bar.setValue(15)
                self.mem_bar.setFormat("CPU Multi-threaded Mode")
else:
    class GPUMonitorWidget:
        def __init__(self, *args, **kwargs):
            pass
