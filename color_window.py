from PySide6.QtCore import Qt, QEvent
from PySide6.QtGui import QCursor, QMouseEvent, QEnterEvent, QIcon, QKeyEvent, QPixmap
from PySide6.QtWidgets import QMainWindow, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QPushButton

from color_picker import PyColorPicker


class ColorWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setFixedSize(400, 675)
        self.setWindowFlags(Qt.FramelessWindowHint | Qt.Window)
        self.setAttribute(Qt.WA_TranslucentBackground)
        self.statusBar().setSizeGripEnabled(False)
        self.statusBar().hide()

        self.setStyleSheet(
            "QFrame#central{background: #292929}"
            "QLabel{color: white}"
            "QFrame#title_bar{border: none; border-bottom: 1px solid white}"
            "QFrame#title_bar QPushButton{background: transparent; border: none; border-radius: 4px}"
            "QFrame#title_bar QPushButton:hover{background: #4c4c4c}"
            "QFrame#title_bar QPushButton:hover#exit_btn{background: #DC143C}"
            "QFrame#title_bar QLabel{padding-left: 10px}"
            "QFrame{background: #292929; border: none; color: white}"
            "QPushButton{background: transparent; border: none}"
            "QSpinBox{background: #292929; border: none; color: white; font: 12pt Times New Roman}"
            "QLineEdit{background: #292929; border: none; color: white; font: 12pt Times New Roman}"
            "QSlider:add-page{background: #8A8A8A}"
            "QSlider:sub-page{background: #6495ED}"
            "QSlider:groove:horizontal{height: 8px; background: #6495ED; border: none}"
            "QSlider:handle:horizontal{background: white; width: 10px; height: 10px;"
            "margin: -5px 0px -5px 0px; border-radius: 5px; border: none}"
        )

        self.central_frame = QFrame(self)
        self.central_frame.setObjectName("central")
        self.setCentralWidget(self.central_frame)

        self.title_bar = ColorTitleBar(self)
        self.color_picker = PyColorPicker(self)

        self.central_layout = QVBoxLayout(self.central_frame)
        self.central_layout.setContentsMargins(0, 0, 0, 0)
        self.central_layout.setSpacing(20)
        self.central_layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.central_layout.addWidget(self.title_bar)
        self.central_layout.addWidget(self.color_picker)

    def keyPressEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_F12:
            print("t")
            pm = self.grab()
            pm.save("img.png")


class ColorTitleBar(QFrame):
    def __init__(self, window: QMainWindow, height: int = 40, button_height: float = 0.8):
        super().__init__()

        # VARIABLES
        # ------------------------------------------------------------------------------------------

        self.last_mouse_position = None
        self.window = window
        self.maximized = False

        window.statusBar().setSizeGripEnabled(True)

        # STYLE
        # ------------------------------------------------------------------------------------------

        # SETUP
        # ------------------------------------------------------------------------------------------

        self.setFixedHeight(height)
        self.setMouseTracking(True)
        self.setObjectName("title_bar")

        # WIDGETS
        # ------------------------------------------------------------------------------------------

        self.title_label = QLabel("Color Picker", self)
        self.title_label.setObjectName("title_label")

        self.minimize_btn = TitleButton(self, int(height * button_height))
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setFixedSize(int(height * button_height), int(height * button_height))
        self.minimize_btn.setToolTip("Minimize")
        self.minimize_btn.setIcon(QIcon("icons/minimize.svg"))

        self.exit_btn = TitleButton(self, int(height * button_height))
        self.exit_btn.setObjectName("exit_btn")
        self.exit_btn.setFixedSize(int(height * button_height), int(height * button_height))
        self.exit_btn.setToolTip("Exit")
        self.exit_btn.setIcon(QIcon("icons/x.svg"))

        # CONNECTIONS
        # ------------------------------------------------------------------------------------------

        self.minimize_btn.clicked.connect(self.window.showMinimized)
        self.exit_btn.clicked.connect(self.window.close)

        # LAYOUTS
        # ------------------------------------------------------------------------------------------

        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)
        self.layout_.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # FILL LAYOUTS
        # ------------------------------------------------------------------------------------------

        self.layout_.addWidget(self.title_label)
        self.layout_.addStretch()
        self.layout_.addWidget(self.minimize_btn)
        self.layout_.addWidget(self.exit_btn)

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.last_mouse_position = event.pos()
            self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.window.move(self.window.pos() + (
                event.pos() - self.last_mouse_position))

    def mouseDoubleClickEvent(self, event: QMouseEvent):
        if self.window.isFullScreen():
            return

        if event.buttons() == Qt.LeftButton:
            if self.maximized:
                self.restore()
            else:
                self.maximize()


class TitleButton(QPushButton):
    def __init__(self, parent: ColorTitleBar, height: int):
        super().__init__(parent)

        self.setFixedSize(height, height)

    def enterEvent(self, event: QEnterEvent) -> None:
        self.setCursor(QCursor(Qt.PointingHandCursor))

    def leaveEvent(self, event: QEvent) -> None:
        self.setCursor(QCursor(Qt.ArrowCursor))