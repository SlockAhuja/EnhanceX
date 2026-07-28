import sys
from enhancex.core.logger import get_logger

logger = get_logger("EnhanceX.Studio")


def launch_studio():
    """Launches EnhanceX Studio Qt6 Desktop Application."""
    try:
        from PyQt6.QtWidgets import QApplication
        from enhancex.gui.main_window import EnhanceXStudioWindow
    except ImportError:
        try:
            from PySide6.QtWidgets import QApplication
            from enhancex.gui.main_window import EnhanceXStudioWindow
        except ImportError:
            logger.error("PyQt6 or PySide6 is required to launch EnhanceX Studio. Install via: pip install PyQt6")
            print("\nError: PyQt6 / PySide6 GUI framework is missing. Please install with:\n  pip install PyQt6\n")
            sys.exit(1)

    app = QApplication(sys.argv)
    window = EnhanceXStudioWindow()
    window.show()
    sys.exit(app.exec())


if __name__ == "__main__":
    launch_studio()
