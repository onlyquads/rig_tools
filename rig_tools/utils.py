import maya.cmds as mc


def set_rgb_override_color(node_shape, color=(1, 1, 1)):
    '''
    Set the color of the shape controller in viewport. Use only on anim CTLs
    '''
    def apply_override_color(node_shape, color):
        ''' Helper function to set override color for a given node '''
        rgb = ("R", "G", "B")
        mc.setAttr(f"{node_shape}.overrideEnabled", 1)
        mc.setAttr(f"{node_shape}.overrideRGBColors", 1)
        for channel, value in zip(rgb, color):
            mc.setAttr(f"{node_shape}.overrideColor{channel}", value)

    # Set the color for the main node
    apply_override_color(node_shape, color)


def get_rgb_override_color(node):
    '''
    Get the color of the shape controller in viewport. Use only on anim
    CTLs
    '''

    rgb = ("R", "G", "B")
    current_color = []

    if not mc.getAttr(f'{node}Shape.overrideRGBColors'):
        mc.setAttr(f'{node}Shape.overrideRGBColors', 1)

    # Get the current color values for each channel
    for channel in rgb:
        current_color.append(mc.getAttr(f'{node}Shape.overrideColor{channel}'))
    return tuple(current_color)
