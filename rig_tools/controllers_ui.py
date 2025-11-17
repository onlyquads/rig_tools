try:
    from PySide6 import QtCore, QtWidgets, QtGui
except ImportError:
    # Fall back to PySide2 if PySide6 is not available
    from PySide2 import QtCore, QtWidgets, QtGui

import os
from rig_tools import controllers
from rig_tools.color_picker import ColorPalette
from functools import partial
from importlib import reload


CURRENT_DIR = os.path.dirname(__file__)
IMAGES_DIR = os.path.join(
    os.path.dirname(CURRENT_DIR), 'rig_tools', 'controllers_renders')


class RigControllerShapes(QtWidgets.QWidget):
    def __init__(self):
        super().__init__()

        self.controllers_layout = QtWidgets.QVBoxLayout(self)
        self.controllers_layout.setAlignment(QtCore.Qt.AlignTop)

        self.load_controller_tab_ui()
        self.load_colors_and_orientation()

    def load_controller_tab_ui(self):
        # Create a scroll area to contain the grid layout
        self.scroll_area = QtWidgets.QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.controllers_layout.addWidget(self.scroll_area)

        # Create a group box that contains the grid layout with shapes
        self.rig_ctl_grid_group_box = QtWidgets.QGroupBox()
        self.rig_ctl_grid_layout = QtWidgets.QGridLayout()
        self.rig_ctl_grid_group_box.setLayout(self.rig_ctl_grid_layout)
        self.scroll_area.setWidget(self.rig_ctl_grid_group_box)

        self.populate_grid(os.path.normpath(IMAGES_DIR))

    def populate_grid(self, folder_path):
        image_extensions = ('.png', '.jpg', '.jpeg', '.bmp')
        images = [
            file_name for file_name in os.listdir(folder_path)
            if file_name.lower().endswith(image_extensions)
        ]
        images.reverse()
        row = 0
        col = 0
        for image_file in images:
            thumbnail = self.create_thumbnail(
                os.path.join(folder_path, image_file))
            button = QtWidgets.QPushButton()
            button.setIcon(QtGui.QIcon(thumbnail))
            button.setIconSize(QtCore.QSize(60, 60))
            button.setSizePolicy(
                QtWidgets.QSizePolicy.Fixed, QtWidgets.QSizePolicy.Fixed)
            button.clicked.connect(
                partial(self.controller_image_clicked, image_file))
            self.rig_ctl_grid_layout.addWidget(button, row, col)
            col += 1
            if col > 5:  # Set the number of columns here, adjust as needed
                col = 0
                row += 1

    def create_thumbnail(self, image_path):
        pixmap = QtGui.QPixmap(image_path)
        return pixmap

    def controller_image_clicked(self, image_file):
        print(f"Clicked on image: {image_file}")
        controller_name = image_file.replace('_render.png', '')
        controllers.create_controller_curve_from_ui(controller_name)

    def load_colors_and_orientation(self):
        color_and_orientation_layout = QtWidgets.QHBoxLayout()
        color_picker_layout = QtWidgets.QVBoxLayout()
        orient_buttons_layout = QtWidgets.QVBoxLayout()
        self.color_palette = ColorPalette()
        color_picker_layout.addWidget(self.color_palette)

        self.rotate_x_button = QtWidgets.QPushButton('Rotate X')
        self.rotate_y_button = QtWidgets.QPushButton('Rotate Y')
        self.rotate_z_button = QtWidgets.QPushButton('Rotate Z')

        self.rotate_x_button.clicked.connect(
            partial(controllers.orient_controller_shape_90_degrees, x=True))
        self.rotate_y_button.clicked.connect(
            partial(controllers.orient_controller_shape_90_degrees, y=True))
        self.rotate_z_button.clicked.connect(
            partial(controllers.orient_controller_shape_90_degrees, z=True))

        orient_buttons_layout.addWidget(self.rotate_x_button)
        orient_buttons_layout.addWidget(self.rotate_y_button)
        orient_buttons_layout.addWidget(self.rotate_z_button)
        orient_buttons_layout.addStretch()

        color_and_orientation_layout.addLayout(color_picker_layout)
        color_and_orientation_layout.addLayout(orient_buttons_layout)
        self.controllers_layout.addLayout(color_and_orientation_layout)

    def refresh(self):
        print('Refreshing controllers_tab.py. Nothing in function yet')
