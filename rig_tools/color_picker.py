try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    # Fall back to PySide2 if PySide6 is not available
    from PySide2 import QtCore, QtWidgets, QtGui

import maya.cmds as mc
from rig_tools import utils
from importlib import reload
reload(utils)


class ColorLabel(QtWidgets.QLabel):
    def __init__(self, color):
        super().__init__()
        self.color = color
        self.setFixedSize(30, 30)
        self.setAutoFillBackground(True)
        self.update_color()

    def update_color(self):
        palette = self.palette()
        palette.setColor(QtGui.QPalette.Window, self.color)
        self.setPalette(palette)
        self.setFrameStyle(QtWidgets.QFrame.Box | QtWidgets.QFrame.Plain)
        self.setLineWidth(1)

    def highlight(self, highlight):
        if highlight:
            self.setLineWidth(3)
        else:
            self.setLineWidth(1)
        self.update()


class ColorPalette(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.colors = [
            QtGui.QColor('red'),
            QtGui.QColor('green'),
            QtGui.QColor('blue'),
            QtGui.QColor('yellow'),
            QtGui.QColor('magenta'),
            QtGui.QColor('cyan'),
            QtGui.QColor('orange'),
            QtGui.QColor('purple'),
            QtGui.QColor('brown'),
            QtGui.QColor('lightblue'),
            QtGui.QColor('pink'),
            QtGui.QColor('darkgreen'),
            QtGui.QColor('lightgreen'),
            QtGui.QColor('darkblue'),
            QtGui.QColor('gold'),
            QtGui.QColor('silver'),
            QtGui.QColor('black'),
            QtGui.QColor('white'),
            QtGui.QColor('gray'),
        ]

        self.color_palette_grid_layout = QtWidgets.QGridLayout()
        self.setLayout(self.color_palette_grid_layout)

        self.labels = []
        for i, color in enumerate(self.colors):
            label = ColorLabel(color)
            label.mousePressEvent = self.make_click_handler(label)
            self.color_palette_grid_layout.addWidget(label, i // 5, i % 5)
            self.labels.append(label)

        self.selected_label = None

    def make_click_handler(self, label):
        def handler(event):
            if self.selected_label:
                self.selected_label.highlight(False)
            self.selected_label = label
            self.selected_label.highlight(True)

            # Get the RGB values of the selected color
            color = self.selected_label.color
            r = color.red() / 255.0
            g = color.green() / 255.0
            b = color.blue() / 255.0

            selected_node_list = mc.ls(sl=True)
            for node in selected_node_list:
                node_shape = (mc.listRelatives(node, s=True))[0]
                utils.set_rgb_override_color(node_shape, (r, g, b))

        return handler
