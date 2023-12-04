import importlib
from types import ModuleType
from sys import path as _path

def dynamic_import(module_name:str)->ModuleType:
    tmz= module_name.split(".")
    if (len(tmz)>1):
        _path.append('/'.join(tmz[:-1]))
    try:
        module = importlib.import_module(tmz[-1])
        return module
    except ImportError as e:
        raise Exception(f"Error importing module {module_name}: {e}")