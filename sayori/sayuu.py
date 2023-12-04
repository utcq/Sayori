from types import ModuleType, NoneType, FunctionType
import inspect
import ast
import sayo, generator


def type_parse(dtype:any, info:str="")->str:
    if (dtype==str): return "char* "
    elif (dtype==int): return "int"
    elif (dtype==inspect._empty): raise Exception(f"Not declared type. {info}")
    elif (type(dtype).__name__==sayo.TPointer.__name__):
        return f"*{type_parse(dtype.val, f'TypePointer: {info}')}"
    elif (type(dtype).__name__==sayo.TReference.__name__):
        return f"&{type_parse(dtype.val, f'TypeReference: {info}')}"
    elif (type(dtype).__name__==sayo.OPointer.__name__):
        return f"{type_parse(dtype.val, f'ObjectPointer: {info}')}*"
    elif (type(dtype).__name__==sayo.OReference.__name__):
        return f"{type_parse(dtype.val, f'ObjectReference: {info}')}&"
    else: 
        try: return dtype.__name__
        except Exception as e: raise Exception(f"Unkown type {dtype}. {info}\n\n{e}")

def fn_parse(name:str, obj:FunctionType, modinfo: generator.ModInfo):
    _fn_name:str=name
    _fn_type:any = type_parse(inspect.signature(obj).return_annotation, f"Function Declaration: {name}, missing type annotation")
    _fn_params: list[(str, any)] = []
    for param in inspect.signature(obj).parameters.values():
        _fn_params.append((param.name, type_parse(param.annotation, f"Function Declaration: {name}, on param {param.name}")))
        
        
    _parparse:list[str]=[]
    for param in _fn_params: _parparse.append(f"{param[1]} {param[0]}")
    
    _fn_dec=f"{_fn_type} {_fn_name}({', '.join(_parparse)})"
    
    print(_fn_dec)

def parse(name:str, obj: any, modinfo: generator.ModInfo):
    otype = type(obj)
    if (otype == FunctionType):
        fn_parse(name,obj, modinfo)


def _var_finder(mod: ModuleType)->list[(str, any, any)]:
    return [
        (it, type(obj), obj)
        for it, obj in ((it, mod.__getattribute__(it)) for it in set(dir(mod)) - set(dir(sayo)) if not it.startswith("_"))
        if not (inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismodule(obj))
    ] # Some magic, just pray it works


def analyze(modinfo: generator.ModInfo)->None:
    _glob_vars:list[(str,any,any)] = _var_finder(modinfo.mod)
    print(_glob_vars)
    
    for name, obj in inspect.getmembers(modinfo.mod)[1:]:
        if (type(obj) == ModuleType):
            if (obj.__name__.split(".")[0]=="sayori"): continue
        elif (type(obj) == type):
            if (obj.__module__.split(".")[0]=="sayori"): continue
        elif (type(obj)==NoneType): continue
        elif ("_frozen_importlib_external.SourceFileLoade" in str(type(obj))): continue
        elif ("_frozen_importlib.ModuleSpec" in str(type(obj))): continue
        
        # Temp skip for list
        elif (type(obj) == list): continue
        
        parse(name, obj, modinfo)