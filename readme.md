


## About
Set of tools used for rigging in maya.

For now it shows a set of shape controllers, you can easily change rotate them 90° X, Y, Z and set their color.
- Simply select an existing controller you want to change the shape and select one from the library.
- You can also simply create a controller by having no selection in maya and choose one controller from the library.

More options will probably be added in the future.


## Installation:

1. Copy the `spring_tool` folder into your Maya scripts directory. This directory is typically located at:

    | os       | path                                          |
    | ------   | ------                                        |
    | linux    | ~/< username >/maya                           |
    | windows  | \Users\\%username%\Documents\maya              |
    | mac os x | ~<username>/Library/Preferences/Autodesk/maya |

2. Launch Maya and run the following Python code in the Maya Script Editor
or Python console to open the tool without presets functions:
```python
from rig_tools import main
main.show()
```