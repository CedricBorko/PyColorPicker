from PySide6.QtCore import Qt
from PySide6.QtGui import QIcon, QPixmap, QIntValidator, QColor
from PySide6.QtWidgets import QSlider, QWidget, QLabel, QLineEdit, QHBoxLayout, QFrame, QSpinBox


class PyIconSlider(QFrame):
    def __init__(self, parent: QWidget, icon: QIcon, orientation: Qt.Orientation = Qt.Horizontal):
        super().__init__(parent)

        self.setFixedHeight(40)

        self.slider = QSlider(orientation)
        self.icon_label = QLabel(self)
        self.value_edit = QSpinBox(self)

        self.layout_h = QHBoxLayout(self)
        self.layout_h.setContentsMargins(0, 0, 0, 0)
        self.layout_h.setSpacing(5)

        self.layout_h.addWidget(self.icon_label)
        self.layout_h.addWidget(self.slider)
        self.layout_h.addWidget(self.value_edit)

        self.icon_label.setFixedSize(40, 40)
        self.icon_label.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)
        self.icon_label.setPixmap(icon.pixmap(24, 24))

        self.value_edit.setFixedSize(40, 40)
        self.value_edit.setButtonSymbols(QSpinBox.NoButtons)
        self.value_edit.valueChanged.connect(self.set_slider)
        self.value_edit.setRange(0, 100)
        self.value_edit.setAlignment(Qt.AlignVCenter | Qt.AlignHCenter)


    def set_slider(self):
        self.slider.setValue(int(self.value_edit.text()))

