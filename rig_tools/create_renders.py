'''
This script is used to create snapshot of the viewport. Mainly to get
illustrations for the controllers shapes
'''

import maya.cmds as mc
from rig_tools.controllers import draw_curve
from rig_tools.controllers_shapes_library import CV_TUPLE_DICT

import os

WIDTH = 256


def capture_viewport(camera_name, file_name):
    # Create a new model panel
    # Find or create a model panel and set the camera
    model_panel = mc.getPanel(withFocus=True)
    if not model_panel or 'modelPanel' not in model_panel:
        model_panel = mc.modelPanel(cam=camera_name, label='MyModelPanel')
    else:
        mc.modelPanel(model_panel, edit=True, camera=camera_name)

    mc.viewFit()

    mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", True)
    mc.setAttr("hardwareRenderingGlobals.multiSampleCount", 8)

    # Set the render resolution
    width = WIDTH
    height = WIDTH

    # Get the path to the desktop
    desktop_path = os.path.join(os.path.expanduser("~"), "renders")

    # Construct the full file path
    file_path = os.path.join(desktop_path, file_name)

    # Set the viewport settings
    mc.modelEditor(
        model_panel,
        edit=True,
        displayAppearance='smoothShaded',
        displayTextures=True
        )

    # Take the snapshot
    mc.playblast(
        completeFilename=file_path,
        forceOverwrite=True,
        format='image',
        width=width,
        height=height,
        showOrnaments=False,
        startTime=1,
        endTime=1,
        viewer=False,
        framePadding=0,
        percent=100
        )

    # Convert the output image to PNG format (if necessary)
    if not file_path.lower().endswith('.png'):
        base, ext = os.path.splitext(file_path)
        new_file_path = base + '.png'
        mc.sysFile(file_path, rename=new_file_path)
        file_path = new_file_path

    print("Saved image to:", file_path)
    if mc.modelPanel(model_panel, exists=True):
        mc.deleteUI(model_panel)


def create_controller_shape_render():

    for shape, points in CV_TUPLE_DICT.items():
        shape_name = shape.replace(' ', '_')
        draw_curve(shape)
        shape.replace(' ', '_')
        capture_viewport("shotcam", f'{shape_name}_render.png')
        if mc.objExists('nurbsCircle1'):
            mc.delete('nurbsCircle1')
        if mc.objExists('curve1'):
            mc.delete('curve1')


if __name__ == "__main__":
    create_controller_shape_render()