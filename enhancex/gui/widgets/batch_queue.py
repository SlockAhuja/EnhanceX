try:
    from PyQt6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView
    from PyQt6.QtCore import Qt
    HAS_QT = True
except ImportError:
    try:
        from PySide6.QtWidgets import QWidget, QVBoxLayout, QTableWidget, QTableWidgetItem, QPushButton, QHBoxLayout, QHeaderView
        from PySide6.QtCore import Qt
        HAS_QT = True
    except ImportError:
        HAS_QT = False


if HAS_QT:
    class BatchQueueWidget(QWidget):
        """Batch Processing Queue Manager Widget."""

        def __init__(self, parent=None):
            super().__init__(parent)
            layout = QVBoxLayout(self)

            # Table for batch queue items
            self.table = QTableWidget(0, 4, self)
            self.table.setHorizontalHeaderLabels(["Input File", "Algorithm", "Status", "Progress"])
            self.table.horizontalHeader().setSectionResizeMode(QHeaderView.ResizeMode.Stretch)
            self.table.setStyleSheet("""
                QTableWidget {
                    background-color: #1E293B;
                    gridline-color: #334155;
                    color: #F8FAFC;
                    border-radius: 6px;
                }
                QHeaderView::section {
                    background-color: #0F172A;
                    color: #38BDF8;
                    font-weight: bold;
                    padding: 6px;
                    border: none;
                }
            """)
            layout.addWidget(self.table)

            # Control buttons
            btn_layout = QHBoxLayout()
            self.btn_run = QPushButton("▶ Start Batch Queue", self)
            self.btn_run.setStyleSheet("background-color: #10B981; color: white; font-weight: bold; padding: 8px 16px; border-radius: 6px;")

            self.btn_clear = QPushButton("🗑️ Clear Queue", self)
            self.btn_clear.setStyleSheet("background-color: #EF4444; color: white; font-weight: bold; padding: 8px 16px; border-radius: 6px;")
            self.btn_clear.clicked.connect(self.clear_queue)

            btn_layout.addWidget(self.btn_run)
            btn_layout.addWidget(self.btn_clear)
            layout.addLayout(btn_layout)

        def add_item(self, filepath: str, algorithm: str):
            row = self.table.rowCount()
            self.table.insertRow(row)
            self.table.setItem(row, 0, QTableWidgetItem(filepath))
            self.table.setItem(row, 1, QTableWidgetItem(algorithm))
            self.table.setItem(row, 2, QTableWidgetItem("Queued"))
            self.table.setItem(row, 3, QTableWidgetItem("0%"))

        def clear_queue(self):
            self.table.setRowCount(0)
else:
    class BatchQueueWidget:
        def __init__(self, *args, **kwargs):
            pass
