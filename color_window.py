import datetime

from PySide6.QtCore import Qt, QEvent, QTimer
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
            "QWidget{font: 12pt Times New Roman}"
            "QFrame#central{background: #292929}"
            "QLabel{color: white}"
            "QFrame#title_bar{border: none; border-bottom: 1px solid #8A8A8A}"
            "QFrame#title_bar QPushButton{background: transparent; border: none; border-radius: 4px}"
            "QFrame#title_bar QPushButton:hover{background: #4c4c4c}"
            "QFrame#title_bar QPushButton:hover#exit_btn{background: #DC143C}"
            "QFrame#title_bar QLabel{color: #8A8A8A; font-weight: bold}"
            "QFrame{background: #292929; border: none; color: white}"
            "QPushButton{background: transparent; border: none}"
            "QSpinBox{background: #292929; border: none; color: white}"
            "QLineEdit{background: #292929; border: none; color: white}"
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


class ColorTitleBar(QFrame):
    def __init__(self, window: QMainWindow, height: int = 40, button_height: float = 0.8):
        super().__init__()

        # VARIABLES
        # ------------------------------------------------------------------------------------------

        self.last_mouse_position = None
        self.window = window
        self.maximized = False


        # SETUP
        # ------------------------------------------------------------------------------------------

        self.setFixedHeight(height)
        self.setMouseTracking(True)
        self.setObjectName("title_bar")
        window.statusBar().setSizeGripEnabled(True)

        # WIDGETS
        # ------------------------------------------------------------------------------------------

        self.title_label = QLabel(self)
        self.title_label.setObjectName("title_label")

        self.screenshot_btn = QPushButton(self)
        self.screenshot_btn.setObjectName("screenshot_btn")
        self.screenshot_btn.clicked.connect(self.take_screenshot)
        self.screenshot_btn.setFixedSize(int(button_height * height), int(button_height * height))
        self.screenshot_btn.setToolTip("Screenshot")
        self.screenshot_btn.setIcon(QIcon("icons/image.svg"))

        self.minimize_btn = QPushButton(self)
        self.minimize_btn.setObjectName("minimize_btn")
        self.minimize_btn.setFixedSize(int(button_height * height), int(button_height * height))
        self.minimize_btn.setToolTip("Minimize")
        self.minimize_btn.setIcon(QIcon("icons/minus.svg"))

        self.exit_btn = QPushButton(self)
        self.exit_btn.setFixedSize(int(button_height * height), int(button_height * height))
        self.exit_btn.setObjectName("exit_btn")
        self.exit_btn.setToolTip("Exit")
        self.exit_btn.setIcon(QIcon("icons/x.svg"))

        # CONNECTIONS
        # ------------------------------------------------------------------------------------------

        self.minimize_btn.clicked.connect(self.window.showMinimized)
        self.exit_btn.clicked.connect(self.window.close)

        # LAYOUTS
        # ------------------------------------------------------------------------------------------

        self.layout_ = QHBoxLayout(self)
        self.layout_.setContentsMargins(5, 0, 5, 0)
        self.layout_.setSpacing(0)
        self.layout_.setAlignment(Qt.AlignVCenter | Qt.AlignRight)

        # FILL LAYOUTS
        # ------------------------------------------------------------------------------------------

        self.layout_.addWidget(self.title_label)
        self.layout_.addStretch()
        self.layout_.addWidget(self.screenshot_btn)
        self.layout_.addWidget(self.minimize_btn)
        self.layout_.addWidget(self.exit_btn)

    def mousePressEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            self.last_mouse_position = event.pos()
            self.setCursor(QCursor(Qt.ClosedHandCursor))

    def mouseReleaseEvent(self, event: QMouseEvent) -> None:
        self.setCursor(QCursor(Qt.ArrowCursor))

    def mouseDoubleClickEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            self.window.move(0, 0)

    def mouseMoveEvent(self, event: QMouseEvent):
        if event.buttons() == Qt.LeftButton:
            new_pos = self.window.pos() + (event.pos() - self.last_mouse_position)
            if new_pos.x() < 0:
                new_pos.setX(0)
            if new_pos.y() < 0:
                new_pos.setY(0)

            self.window.move(new_pos)

    def take_screenshot(self):
        import datetime
        self.parent().grab().save(
            f"screenshots/{datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S')}_img.png")
