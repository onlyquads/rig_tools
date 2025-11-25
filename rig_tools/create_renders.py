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
    # Create a temporary window + modelPanel to guarantee validity
    win = mc.window(title="TmpViewportWin", widthHeight=(WIDTH, WIDTH))
    form = mc.formLayout()
    model_panel = mc.modelPanel()
    mc.formLayout(
        form,
        edit=True,
        attachForm=[(model_panel, 'top', 0),
                    (model_panel, 'left', 0),
                    (model_panel, 'right', 0),
                    (model_panel, 'bottom', 0)])
    mc.showWindow(win)

    # Assign the camera
    mc.modelPanel(model_panel, edit=True, camera=camera_name)

    # Fit view
    mc.setFocus(model_panel)
    mc.viewFit()

    # Render settings
    mc.setAttr("hardwareRenderingGlobals.multiSampleEnable", 1)
    mc.setAttr("hardwareRenderingGlobals.multiSampleCount", 8)

    width = height = WIDTH

    # Build file path
    desktop_path = os.path.join(os.path.expanduser("~"), "renders")
    if not os.path.exists(desktop_path):
        os.makedirs(desktop_path)

    file_path = os.path.join(desktop_path, file_name)

    # Ensure correct drawing style
    mc.modelEditor(model_panel, edit=True,
                   displayAppearance='smoothShaded',
                   displayTextures=True)

    # Snapshot
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

    # Convert to PNG if needed
    if not file_path.lower().endswith('.png'):
        base, ext = os.path.splitext(file_path)
        new_file_path = base + '.png'
        mc.sysFile(file_path, rename=new_file_path)
        file_path = new_file_path

    print("Saved image to:", file_path)

    if mc.window(win, exists=True):
        mc.deleteUI(win)


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
