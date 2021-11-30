import sys

from PySide6.QtGui import QIcon, QAction, QDesktopServices
from PySide6.QtWidgets import QApplication, QSystemTrayIcon, QMenu

from color_window import ColorWindow


def main():
    app = QApplication(sys.argv)
    app.setQuitOnLastWindowClosed(False)

    icon = QIcon("icons/tray_icon.png")

    tray = QSystemTrayIcon()
    tray.setIcon(icon)
    tray.setVisible(True)

    menu = QMenu()
    window = ColorWindow()

    close_action = QAction("Schließen")
    close_action.triggered.connect(app.quit)

    open_action = QAction("Fenster öffnen")
    open_action.triggered.connect(window.show)

    google_color_picker_action = QAction("Color Picker Google")
    google_color_picker_action.triggered.connect(
        QDesktopServices.openUrl(
            "https://imagecolorpicker.com/color-code/0051ff"
        )
    )

    menu.addAction(close_action)
    menu.addAction(open_action)
    menu.addAction(google_color_picker_action)

    tray.setContextMenu(menu)
    sys.exit((app.exec_()))


if __name__ == "__main__":
    main()
