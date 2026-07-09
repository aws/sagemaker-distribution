from __future__ import absolute_import

import pathlib
import sys

# make the utils modules accessible to modules from within the tornado_server folder
utils_path = pathlib.Path(__file__).parent.parent / "utils"
sys.path.insert(0, str(utils_path.resolve()))

# make the tornado_server modules accessible to each other
tornado_module_path = pathlib.Path(__file__).parent
sys.path.insert(0, str(tornado_module_path.resolve()))
