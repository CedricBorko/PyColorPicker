import math
import re

from PySide6.QtCore import Qt, QPoint, Signal, QSize, QRect
from PySide6.QtGui import QPaintEvent, QPainter, QPen, QColor, QBrush, QConicalGradient, \
    QMouseEvent, QClipboard, QIcon, QResizeEvent, QCursor, QWheelEvent, QKeyEvent, \
    QFont, QImage
from PySide6.QtWidgets import QWidget, QVBoxLayout, QFrame, QLabel, QHBoxLayout, QLineEdit, \
    QPushButton, QGraphicsDropShadowEffect

from slider import PyIconSlider


class PyColorPicker(QFrame):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        self.setObjectName("py_color_picker")
        self.setStyleSheet("QFrame#py_color_picker{background: #292929}")

        self.setFixedSize(400, 600)

        self.color = QColor(255, 0, 0)

        self.hex_group = DisplayGroup("HEX", self)
        self.hex_group.edit.setText("#FF0000")

        self.rgb_group = DisplayGroup("RGB", self)
        self.rgb_group.edit.setText("255, 0, 0")

        self.cmyk_group = DisplayGroup("CMYK", self)
        self.cmyk_group.edit.setText("0, 100, 100, 0")

        self.wheel = PyColorWheel(self)
        self.wheel.angle_changed.connect(self.set_color)

        self.saturation = PyIconSlider(self, QIcon("icons/droplet.svg"), Qt.Horizontal)
        self.saturation.slider.setRange(0, 100)
        self.saturation.slider.setValue(100)
        self.saturation.slider.valueChanged.connect(self.set_color)

        self.saturation.value_edit.setValue(100)
        self.saturation.icon_label.setToolTip("Saturation")

        self.luminance = PyIconSlider(self, QIcon("icons/sun.svg"), Qt.Horizontal)
        self.luminance.slider.setRange(0, 100)
        self.luminance.slider.setValue(50)

        self.luminance.slider.valueChanged.connect(self.set_color)
        self.luminance.value_edit.setValue(50)
        self.luminance.icon_label.setToolTip("Luminance")

        self.layout_ = QVBoxLayout(self)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(0)

        self.layout_.addWidget(self.hex_group)
        self.layout_.addWidget(self.rgb_group)
        self.layout_.addWidget(self.cmyk_group)

        self.layout_.addWidget(self.wheel)
        self.layout_.addWidget(self.saturation)
        self.layout_.addWidget(self.luminance)

    def set_color_by_hex(self):
        if not re.search(r'^#(?:[0-9a-fA-F]{3}){1,2}$', self.hex_group.edit.text()):
            return
        else:
            self.color = QColor(self.hex_group.edit.text())

            self.saturation.slider.blockSignals(True)
            self.luminance.slider.blockSignals(True)
            self.wheel.blockSignals(True)

            self.saturation.slider.setValue(int(self.color.hslSaturation() / 255 * 100))
            self.saturation.value_edit.setValue(int(self.color.hslSaturation() / 255 * 100))

            self.luminance.slider.setValue(int(self.color.lightness() / 255 * 100))
            self.luminance.value_edit.setValue(int(self.color.lightness() / 255 * 100))

            self.wheel.set_angle()

            self.saturation.slider.blockSignals(False)
            self.luminance.slider.blockSignals(False)
            self.wheel.blockSignals(False)

            self.cmyk_group.edit.setText(
                f"{round(self.color.cyanF() * 100)},"
                f" {round(self.color.magentaF() * 100)},"
                f" {round(self.color.yellowF() * 100)},"
                f" {round(self.color.blackF() * 100)}"
            )

            self.rgb_group.edit.setText(
                f"{self.color.red()}, {self.color.green()}, {self.color.blue()}"
            )

            self.update()

    def set_color_by_rgb(self):
        if not re.search(r"\d{1,3},\s*\d{1,3},\s*\d{1,3}", self.rgb_group.edit.text()):
            return
        else:

            if self.rgb_group.edit.text().count(",") > 2:
                return

            r, g, b = self.rgb_group.edit.text().strip().split(",")
            self.color = QColor(int(r), int(g), int(b))

            self.saturation.slider.blockSignals(True)
            self.luminance.slider.blockSignals(True)
            self.wheel.blockSignals(True)

            self.saturation.slider.setValue(self.color.hslSaturation() / 255 * 100)
            self.saturation.value_edit.setValue(int(self.color.hslSaturation() / 255 * 100))

            self.luminance.slider.setValue(int(self.color.lightness() / 255 * 100))
            self.luminance.value_edit.setValue(int(self.color.lightness() / 255 * 100))

            self.wheel.set_angle()

            self.saturation.slider.blockSignals(False)
            self.luminance.slider.blockSignals(False)
            self.wheel.blockSignals(False)

            self.hex_group.edit.setText(self.color.name(QColor.HexRgb).upper())
            self.cmyk_group.edit.setText(
                f"{round(self.color.cyanF() * 100)},"
                f" {round(self.color.magentaF() * 100)},"
                f" {round(self.color.yellowF() * 100)},"
                f" {round(self.color.blackF() * 100)}"
            )

            self.update()

    def set_color_by_cmyk(self):
        if not re.search(r"\d{1,3},\s*\d{1,3},\s*\d{1,3},\s*\d{1,3}", self.cmyk_group.edit.text()):
            return
        else:

            if self.cmyk_group.edit.text().count(",") > 3:
                return

            c, m, y, k = self.cmyk_group.edit.text().strip().split(",")
            self.color = QColor.fromCmyk(int(c), int(m), int(y), int(k))

            self.saturation.slider.blockSignals(True)
            self.luminance.slider.blockSignals(True)
            self.wheel.blockSignals(True)

            self.saturation.slider.setValue(int(self.color.hslSaturation() / 255 * 100))
            self.saturation.value_edit.setValue(int(self.color.hslSaturation() / 255 * 100))

            self.luminance.slider.setValue(int(self.color.lightness() / 255 * 100))
            self.luminance.value_edit.setValue(int(self.color.lightness() / 255 * 100))

            self.wheel.set_angle()

            self.saturation.slider.blockSignals(False)
            self.luminance.slider.blockSignals(False)
            self.wheel.blockSignals(False)

            self.hex_group.edit.setText(self.color.name(QColor.HexRgb).upper())
            self.rgb_group.edit.setText(
                f"{self.color.red()}, {self.color.green()}, {self.color.blue()}"
            )

            self.update()

    def set_color(self):
        self.saturation.value_edit.setValue(self.saturation.slider.value())
        self.luminance.value_edit.setValue(self.luminance.slider.value())

        self.color = QColor.fromHsl(
            (360 - self.wheel.angle) % 360,
            round(self.saturation.slider.value() / 100 * 255),
            round(self.luminance.slider.value() / 100 * 255),
            a=255
        )

        self.hex_group.edit.blockSignals(True)
        self.rgb_group.edit.blockSignals(True)
        self.cmyk_group.edit.blockSignals(True)

        self.hex_group.edit.setText(self.color.name(QColor.HexRgb).upper())
        self.rgb_group.edit.setText(
            f"{self.color.red()},"
            f" {self.color.green()},"
            f" {self.color.blue()}")

        self.cmyk_group.edit.setText(
            f"{round(self.color.cyanF() * 100)},"
            f" {round(self.color.magentaF() * 100)},"
            f" {round(self.color.yellowF() * 100)},"
            f" {round(self.color.blackF() * 100)}"
        )

        self.hex_group.edit.blockSignals(False)
        self.rgb_group.edit.blockSignals(False)
        self.cmyk_group.edit.blockSignals(False)

        self.update()

    def get_hex(self):
        QClipboard().setText(str(self.color.name(QColor.HexRgb).upper()))

    def get_rgb(self):
        QClipboard().setText(f"{self.color.red()}, {self.color.green()}, {self.color.blue()}")

    def get_cmyk(self):
        QClipboard().setText(
            f"{int(self.color.cyanF() * 100)},"
            f" {int(self.color.magentaF() * 100)},"
            f" {int(self.color.yellowF() * 100)},"
            f" {int(self.color.blackF() * 100)}"
        )


class PyColorWheel(QWidget):
    angle_changed = Signal()

    def __init__(self, parent: QWidget, arc_width: int = 50, margin: int = 10):
        super().__init__(parent)

        self.setMinimumSize(400, 400)

        self.ctrl_pressed = False

        self.angle = 0
        self.arc_width = arc_width
        self.margin = margin

        self.size = self.width() // 2

        self.radius = self.size - self.margin - self.arc_width // 2
        self.indicator_pos = self.indicator_pos = QPoint(
            int(self.size + self.radius * math.sin(math.radians(self.angle + 180))),
            int(self.size + self.radius * math.cos(math.radians(self.angle + 180))),
        )

        self.gradient = QConicalGradient()
        self.gradient.setAngle(90)
        self.gradient.setColorAt(0, QColor(255, 0, 0, 255))
        self.gradient.setColorAt(1.0 / 6, QColor(255, 0, 255, 255))
        self.gradient.setColorAt(2.0 / 6, QColor(0, 0, 255, 255))
        self.gradient.setColorAt(3.0 / 6, QColor(0, 255, 255, 255))
        self.gradient.setColorAt(4.0 / 6, QColor(0, 255, 0, 255))
        self.gradient.setColorAt(5.0 / 6, QColor(255, 255, 0, 255))
        self.gradient.setColorAt(1, QColor(255, 0, 0, 255))

    def resizeEvent(self, event: QResizeEvent) -> None:
        self.size = self.width() // 2

        self.radius = self.size - self.margin - self.arc_width // 2
        self.gradient.setCenter(self.rect().center())

        self.indicator_pos = self.indicator_pos = QPoint(
            int(self.size + self.radius * math.sin(math.radians(self.angle + 180))),
            int(self.size + self.radius * math.cos(math.radians(self.angle + 180))),
        )

    def paintEvent(self, event: QPaintEvent) -> None:
        painter = QPainter(self)
        painter.setRenderHint(QPainter.Antialiasing)

        painter.fillRect(self.rect(), QColor("#292929"))

        painter.setPen(QPen(QBrush(self.gradient), self.arc_width))
        painter.drawArc(self.margin + self.arc_width // 2,
                        self.margin + self.arc_width // 2,
                        self.radius * 2,
                        self.radius * 2,
                        0 * 16,
                        360 * 16)

        painter.setPen(QPen(QColor("#FFF"), 3.0))
        painter.drawEllipse(self.indicator_pos, self.arc_width // 2 - 1, self.arc_width // 2 - 1)

        painter.setPen(QPen(self.parent().color, self.arc_width * 0.6))
        painter.drawArc(
            self.size - self.arc_width,
            self.size - self.arc_width,
            self.size // 2, self.size // 2,
            0 * 16, 360 * 16
        )



        painter.setPen(QPen(QColor("#FFF"), 3.0))
        painter.setFont(QFont("Times New Roman", 12))
        painter.drawText(self.rect(), Qt.AlignHCenter | Qt.AlignVCenter,
                         f"{(360 - self.angle) % 360}")

    def mouseMoveEvent(self, event: QMouseEvent) -> None:
        if event.buttons() == Qt.LeftButton:
            radians = math.atan2(event.pos().y() - self.size, event.pos().x() - self.size)
            degrees = -(math.degrees(radians) + 90) % 360

            self.indicator_pos = QPoint(
                int(self.size + self.radius * math.sin(math.radians(degrees + 180))),
                int(self.size + self.radius * math.cos(math.radians(degrees + 180))),
            )

            self.angle = int(degrees)
            self.angle_changed.emit()

            self.update()

    def mousePressEvent(self, event: QMouseEvent) -> None:
        self.setFocus()

    def keyPressEvent(self, event: QKeyEvent) -> None:
        self.ctrl_pressed = event.key() == Qt.Key_Control

    def keyReleaseEvent(self, event: QKeyEvent) -> None:
        if event.key() == Qt.Key_Control:
            self.ctrl_pressed = False

    def wheelEvent(self, event: QWheelEvent) -> None:
        self.setFocus()
        increment = 10 if self.ctrl_pressed else 1
        self.angle += increment if event.angleDelta().y() < 0 else - increment
        self.angle %= 360

        self.indicator_pos = QPoint(
            int(self.size + self.radius * math.sin(math.radians(self.angle + 180))),
            int(self.size + self.radius * math.cos(math.radians(self.angle + 180))),
        )
        self.angle_changed.emit()
        self.update()

    def set_angle(self):
        self.angle = 360 - self.parent().color.hue()
        if self.angle == -1:
            self.angle = 0

        self.indicator_pos = QPoint(
            int(self.size + self.radius * math.sin(math.radians(self.angle + 180))),
            int(self.size + self.radius * math.cos(math.radians(self.angle + 180))),
        )

        self.update()


class DisplayGroup(QFrame):
    def __init__(self, title: str, parent: QWidget = None):
        super().__init__(parent)

        self.label = QLabel(f"{title}:")
        self.label.setAlignment(Qt.AlignRight | Qt.AlignVCenter)
        self.label.setFixedSize(80, 40)

        self.edit = QLineEdit()
        self.edit.setAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
        self.edit.setFixedSize(150, 40)

        self.copy_btn = QPushButton()
        self.copy_btn.setToolTip(f"Copy {title}")
        self.copy_btn.setFixedSize(40, 40)
        self.copy_btn.setCursor(QCursor(Qt.PointingHandCursor))
        self.copy_btn.setIcon(QIcon("icons/copy.svg"))
        self.copy_btn.setIconSize(QSize(24, 24))

        self.layout_ = QHBoxLayout(self)
        self.layout_.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.layout_.setContentsMargins(0, 0, 0, 0)
        self.layout_.setSpacing(40)

        self.layout_.addWidget(self.label)
        self.layout_.addWidget(self.edit)
        self.layout_.addWidget(self.copy_btn)

        self.edit.textEdited.connect(getattr(self.parent(), "set_color_by_" + title.lower()))
        self.copy_btn.clicked.connect(getattr(self.parent(), "get_" + title.lower()))
