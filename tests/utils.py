import importlib
import sys


def reload_importlib_module(module_str):
    module = importlib.import_module(module_str)

    try:  # >=py3.4
        importlib.reload(module)
    except AttributeError:
        if sys.version_info[0] == 3:  # >=py3.1
            import imp
            imp.reload(module)
        else:
            reload(module)  # noqa
