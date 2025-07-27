import os
import types
from accessible_output3.utils import load_library


def get_output_classes():
    from . import outputs

    module_type = types.ModuleType
    classes = [
        m.output_class
        for m in outputs.__dict__.values()
        if isinstance(m, module_type) and hasattr(m, "output_class")
    ]
    return sorted(classes, key=lambda c: c.priority)


def find_datafiles():
    import platform
    from glob import glob
    import accessible_output3

    if platform.system() != "Windows":
        return []
    path = os.path.join(accessible_output3.__path__[0], "lib", "*.dll")
    results = glob(path)
    dest_dir = os.path.join("accessible_output3", "lib")
    return [(dest_dir, results)]
