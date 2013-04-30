import ctypes
import os
import types
from platform_utils import paths

def load_library(libname):
 libfile = os.path.join(paths.module_path(), 'lib', libname)
 return ctypes.windll[libfile]

def get_output_classes():
 import outputs
 module_type = types.ModuleType
 classes = [m.output_class for m in outputs.__dict__.itervalues() if type(m) == module_type and hasattr(m, 'output_class')]
 return sorted(classes, key=lambda c: c.priority)
