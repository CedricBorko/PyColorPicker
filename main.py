import sys

from PySide6.QtWidgets import QApplication

from color_window import ColorWindow


def main():
    app = QApplication(sys.argv)
    window = ColorWindow()
    window.show()
    sys.exit((app.exec_()))


if __name__ == "__main__":
    main()