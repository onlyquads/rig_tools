import sys

try:
    from PySide6 import QtCore, QtWidgets
except ImportError:
    from PySide2 import QtCore, QtWidgets

from rig_tools import controllers_ui, color_picker
from importlib import reload

reload(controllers_ui)
reload(color_picker)

window = None


def maya_main_window():
    '''Return Maya's main window'''
    for obj in QtWidgets.QApplication.topLevelWidgets():
        if obj.objectName() == 'MayaWindow':
            return obj
    raise RuntimeError('Could not find MayaWindow instance')


class RigToolUi(QtWidgets.QMainWindow):
    def __init__(self, parent=None):
        parent = parent or maya_main_window()
        super(RigToolUi, self).__init__(parent)
        self.setWindowFlags(QtCore.Qt.Tool)
        self.setWindowTitle('Rig Tools')

        central_widget = QtWidgets.QWidget(self)  # Create a central widget
        self.main_layout = QtWidgets.QVBoxLayout(central_widget)
        controllers_ui_widget = controllers_ui.RigControllerShapes()
        self.main_layout.addWidget(controllers_ui_widget)

        self.setCentralWidget(central_widget)


def show():
    global window
    if window is not None:
        window.close()
    window = RigToolUi(parent=maya_main_window())
    window.show()


if __name__ == '__main__':

    if not QtWidgets.QApplication.instance():
        app = QtWidgets.QApplication(sys.argv)
    else:
        app = QtWidgets.QApplication.instance()

    window = RigToolUi()
    window.show()
    app.exec_()
