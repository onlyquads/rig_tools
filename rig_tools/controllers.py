import maya.cmds as mc
from rig_tools import controllers_shapes_library
from importlib import reload
reload(controllers_shapes_library)


def draw_curve(curve, curve_name='curve1'):
    '''
    This function is used to create curve controllers. It can create circles
    or create curves from the controller shapes library
    '''
    # Exception for Circle shape.
    if curve == 'circle':
        mc.circle(d=3, r=2, nr=[0, 1, 0], ch=False)
        mc.rename('nurbsCircle1', 'curve1')
    else:
        mc.curve(d=1, p=controllers_shapes_library.CV_TUPLE_DICT[curve])
    mc.rename('curve1', curve_name)


def create_controller_curve_from_ui(control_curve_name):
    '''
    Create a curve controller from the UI icon clicked.
    Requires a controller to be selected in the viewport. It replaces
    the selected controller with a new curve from the controller shapes
    library.
    '''
    mc.undoInfo(ock=True)
    # Check selection
    selection = mc.ls(sl=True)

    if not selection:
        return mc.warning("Please select a controller to replace.")
    if len(selection) > 1:
        return mc.warning("Please select only one controller at the time")

    selected_controller = selection[0]

    # Draw the new curve
    new_curve_name = f"{control_curve_name}_temp"
    draw_curve(control_curve_name, curve_name=new_curve_name)

    # Replace selected controller's shape with the new curve's shape
    shapes = mc.listRelatives(new_curve_name, shapes=True)
    if not shapes:
        mc.warning(f"No shapes found on the new curve {new_curve_name}")
        return

    # Delete old shapes on the selected controller
    old_shapes = mc.listRelatives(selected_controller, shapes=True) or []
    if old_shapes:
        mc.delete(old_shapes)

    # Parent new shapes to the selected controller
    n = 0
    for shape in shapes:
        new_name = f"{selection[0]}Shape"
        if len(shapes) > 1:
            n += 1
            new_name = f"{new_name}_{n}"
        mc.parent(shape, selected_controller, shape=True, relative=True)
        mc.rename(shape, new_name)

    # Delete temporary transform node
    mc.delete(new_curve_name)

    mc.select(selected_controller)
    mc.undoInfo(ock=True)


def orient_controller_shape_90_degrees(x=False, y=False, z=False):
    '''
    Orient the selected controller shape 90° according the the given arg
    '''
    mc.undoInfo(ock=True)
    selection = mc.ls(sl=True)
    if len(selection) == 0:
        return
    for curve in selection:
        try:
            form = mc.getAttr(f'{curve}.form')
            deg = mc.getAttr(f'{curve}.degree')
            spans = mc.getAttr(f'{curve}.spans')
            if form != 2:
                spans += deg
            mc.select(f'{curve}.cv[0:%s]' % spans)
            if x:
                mc.rotate(90, 0, 0, r=1, os=1)
            elif y:
                mc.rotate(0, 90, 0, r=1, os=1)
            elif z:
                mc.rotate(0, 0, 90, r=1, os=1)
        except Exception:
            pass
    mc.select(selection)
    mc.undoInfo(cck=True)


def select_all_cvs(nurbs_node):
    '''
    Select all the cvs of the given nurbs shape
    '''
    if not mc.objectType(nurbs_node) == 'nurbsCurve':
        return
    # Get the number of CVs in the NURBS curve:
    all_cvs = mc.getAttr(
        f'{nurbs_node}.span') + mc.getAttr(f'{nurbs_node}.degree')
    cvs = [
        f'{nurbs_node}.cv[{i}]' for i in range(all_cvs)
        ]
    return mc.select(cvs)
