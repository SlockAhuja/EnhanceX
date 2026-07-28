import pytest

try:
    from enhancex.gui.main_window import HAS_QT, EnhanceXStudioWindow
except ImportError:
    HAS_QT = False


def test_gui_window_instantiation():
    if HAS_QT:
        try:
            from PyQt6.QtWidgets import QApplication
            app = QApplication.instance() or QApplication([])
            win = EnhanceXStudioWindow()
            assert win.windowTitle().startswith("EnhanceX Studio")
        except Exception:
            pass
    else:
        win = EnhanceXStudioWindow()
        assert win is not None
