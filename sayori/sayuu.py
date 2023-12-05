from types import ModuleType, NoneType, FunctionType
import inspect
import ast
import generator
from sayo import *
import sayo


def type_parse(dtype:any, info:str="")->str:
    if (dtype==str): return "char*"
    elif (dtype==int): return "int"
    elif (dtype=="int"): return "int"
    elif (dtype=="str"): return "char*"
    elif (type(dtype)==str): return "char*"
    elif (dtype==inspect._empty): raise Exception(f"Not declared type. {info}")
    elif (type(dtype).__name__==TPointer.__name__):
        return f"*{type_parse(dtype.val, f'TypePointer: {info}')}"
    elif (type(dtype).__name__==TReference.__name__):
        return f"&{type_parse(dtype.val, f'TypeReference: {info}')}"
    elif (type(dtype).__name__==OPointer.__name__):
        return f"{type_parse(dtype.val, f'ObjectPointer: {info}')}*"
    elif (type(dtype).__name__==OReference.__name__):
        return f"{type_parse(dtype.val, f'ObjectReference: {info}')}&"
    elif isinstance(dtype, TPointer):
        return f"*{type_parse(dtype.val, f'TypePointer: {info}')}"
    else: 
        if type(dtype).__name__ != "type":
            return type(dtype).__name__
        else:
            try: return dtype.__name__
            except Exception as e: raise Exception(f"Unkown type {dtype}. {info}\n\n{e}")

def op_parse(value:any)->str:
    if isinstance(value, ast.Add):
        return "+"
    elif isinstance(value, ast.Sub):
        return "-"
    elif isinstance(value, ast.Mult):
        return "*"
    elif isinstance(value, ast.Div):
        return "/"
    elif isinstance(value, ast.Mod):
        return "%"
    elif isinstance(value, ast.BitXor):
        return "^"
    elif isinstance(value, ast.BitOr):
        return "&"
    elif isinstance(value, ast.BitAnd):
        return "|"
    elif isinstance(value, ast.RShift):
        return ">>"
    elif isinstance(value, ast.LShift):
        return "<<"

def exp_parse(value: any) -> str:
    if isinstance(value, ast.BinOp):
        left_exp = exp_parse(value.left)
        right_exp = exp_parse(value.right)
        return f"({left_exp}{op_parse(value.op)}{right_exp})"
    elif isinstance(value, ast.Expr):
        return exp_parse(value.value)
    else:
        return value_parse(value)

def str_to_type(dtype:any)->any:
    rtype = sayo.__dict__.get(dtype)
    if (not rtype):
        try: rtype = sayo.__dict__.get(dtype.__name__)
        except: pass
    if (not rtype):
        temp = sayo.__dict__.get(type(dtype).__name__)
        if temp: rtype = dtype
        rtype = dtype
    if (not rtype):
        try: rtype = eval(dtype)
        except: rtype = type(dtype)
    return rtype

def try_cast(dtype:any)->any:
    try: return str_to_type(dtype)
    except Exception as e: print(e); return str(dtype)

def type_conv(node:ast.AST)->any:
    if (isinstance(node, ast.Call)):
        args:list[str]=[]
        for arg in node.args:
            args.append(type_conv(arg.id))
        rztype = eval(f"{node.func.id}({', '.join(args)})")
        return rztype
    elif (isinstance(node, str)):
        return str(node)
    elif (isinstance(node, ast.Name)):
        return try_cast(node.id)
    
def literal_parse(value: any)->str:
    if isinstance(value, str):
        return f'"{value}"'.replace("\n", "\\n")
    elif isinstance(value, char):
        return f"'{value}'".replace("\n", "\\n")
    elif isinstance(value, str):
        return f'"{value}"'.replace("\n", "\\n")
    elif isinstance(value, int):
        return str(value)
    elif (type(value).__name__ == int8_t.__name__):
        return str(value)
    elif (type(value).__name__ == int16_t.__name__):
        return str(value)
    elif (type(value).__name__ == int32_t.__name__):
        return str(value)
    elif (type(value).__name__ == int64_t.__name__):
        return str(value)
    elif (type(value).__name__ == uint8_t.__name__):
        return str(value)
    elif (type(value).__name__ == uint16_t.__name__):
        return str(value)
    elif (type(value).__name__ == uint32_t.__name__):
        return str(value)
    elif (type(value).__name__ == uint64_t.__name__):
        return str(value)
    elif isinstance(value, void):
        return "void"
    elif isinstance(value, NoneType):
        return "NULL"
    else:
        return str(value)

def call_parse(node:ast.AST)->str:
    _c_name = node.func.id
    _c_args:list[str]=[]
    for arg in node.args:
        _c_args.append(exp_parse(arg))
    return f"{_c_name}({', '.join(_c_args)})"

def value_parse(node:any)->str:
    if isinstance(node, ast.Constant):
        return literal_parse(node.value)
    elif isinstance(node, ast.Name):
        return str(node.id)
    elif isinstance(node, ast.Call):
        return str(call_parse(node))
    
    elif (type(node).__name__ == TReference.__name__):
        return f"&{exp_parse(node.val)}"
    elif (type(node).__name__ == OReference.__name__):
        return f"&{exp_parse(node.val)}"
    elif (type(node).__name__ == TPointer.__name__):
        return f"*{exp_parse(node.val)}"
    elif (type(node).__name__ == OPointer.__name__):
        return f"*{exp_parse(node.val)}"

def is_expr(node):
    return isinstance(node, (ast.Expr, ast.BinOp, ast.UnaryOp, ast.BoolOp, ast.Compare))

def block_parse(source:str, modinfo: generator.ModInfo):
    tree = ast.parse(source)
    for node in ast.iter_child_nodes(tree):
        if isinstance(node, ast.Return):
            exp = exp_parse(node.value)
            modinfo.writer.swrite(f"return {exp};\n")
        elif isinstance(node, ast.AnnAssign): # Annotated Assign
            _v_name:str = node.target.id
            _v_type:any = type_parse(type_conv(node.annotation))
            _v_value:any = exp_parse(node.value)
            modinfo.writer.swrite(f"{_v_type} {_v_name} = {_v_value};\n")
        elif isinstance(node, ast.Expr):
            if isinstance(node.value, ast.Call):
                _cstr = call_parse(node.value)
                modinfo.writer.swrite(f"{_cstr};\n")

def fn_parse(name:str, obj:FunctionType, modinfo: generator.ModInfo):
    _fn_name:str=name
    _fn_type:any = type_parse(inspect.signature(obj).return_annotation, f"Function Declaration: {name}, missing type annotation")
    if (_fn_type == "NoneType"): _fn_type="void"
    _fn_params: list[(str, any)] = []
    for param in inspect.signature(obj).parameters.values():
        _fn_params.append((param.name, type_parse(param.annotation, f"Function Declaration: {name}, on param {param.name}")))
        
        
    _parparse:list[str]=[]
    for param in _fn_params: _parparse.append(f"{param[1]} {param[0]}")
    
    _fn_dec=f"{_fn_type} {_fn_name}({', '.join(_parparse)})"
    
    modinfo.writer.hwrite(_fn_dec+";\n")
    modinfo.writer.swrite(_fn_dec+" {\n")
    modinfo.writer.tabs+=1

    _fn_block = inspect.getsourcelines(obj)[0][1:]
    for _statement in _fn_block:
        _statement=_statement.strip()
        block_parse(_statement, modinfo)

    modinfo.writer.tabs-=1
    modinfo.writer.swrite("}\n\n")

def parse(name:str, obj: any, modinfo: generator.ModInfo):
    otype = type(obj)
    if (otype == FunctionType):
        if (obj.__module__.split(".")[-1] == "cstdlib"): return
        fn_parse(name,obj, modinfo)


def _var_finder(mod: ModuleType)->list[(str, any, any)]:
    return [
        (it, obj, obj)
        for it, obj in ((it, mod.__getattribute__(it)) for it in set(dir(mod)) - set(dir(sayo)) if not it.startswith("_"))
        if not (inspect.isfunction(obj) or inspect.isclass(obj) or inspect.ismodule(obj))
    ] # Some magic, just pray it works


def _def_finder(modinfo: ModuleType, _gvars: list[(str,any,any)])->None:
    for variable in _gvars:
        if (type(variable[1]).__name__==sayo.Define.__name__):
            modinfo.writer.hwrite(f"#define {variable[0]} {variable[2].value}\n")
        elif (type(variable[1]).__name__==sayo.Include.__name__):
            modinfo.writer.stwrite(f"#include <{variable[2].value}>\n")
        elif (type(variable[1]).__name__==sayo.IncludeLocal.__name__):
            modinfo.writer.stwrite(f'#include "{variable[2].value}"\n')
    tree= ast.parse(open(modinfo.mod.__file__, "r").read())
    for node in ast.walk(tree):
        if isinstance(node, ast.AnnAssign):
            _v_name:str = node.target.id
            if (modinfo.mod.__dict__.get(_v_name)):
                _v_type:any = type_parse(try_cast(node.annotation.id))
                _v_value:any = exp_parse(node.value)
                modinfo.writer.swrite(f"{_v_type} {_v_name} = {_v_value};\n\n")
            elif (exp_parse(node.value) == "NULL"):
                _v_type:any = type_parse(try_cast(node.annotation.id))
                modinfo.writer.swrite(f"{_v_type} {_v_name};\n\n")

        elif isinstance(node, ast.Assign):
            if isinstance(node.targets[0], ast.Name):
                _v_name:str = node.targets[0].id
            else:
                _v_name:str = node.targets[0].value.id
            if not (modinfo.mod.__dict__.get(_v_name)): continue
            try: 
                if (_v_name).startswith("_"): continue
            except: pass
            if isinstance(node.value, ast.Call):
                try: 
                    if (node.value.func.id == "Define"): continue
                    if (node.value.func.id == "Include"): continue
                    if (node.value.func.id == "IncludeLocal"): continue
                except: pass
            raise Exception(f"Cannot use globals without annotations, '{node.targets[0].id}' [line {node.lineno}]")
        elif isinstance(node, ast.Call):
            try:
                if (node.func.id == "Include"):
                    try: file = node.func.args[0]
                    except: raise Exception(f"Missing argument in Include [Line {node.lineno}]")
                    modinfo.writer.stwrite(f"#include <{file}>\n")
                if (node.func.id == "IncludeLocal"):
                    try: file = node.func.args[0]
                    except: raise Exception(f"Missing argument in IncludeLocal [Line {node.lineno}]")
                    modinfo.writer.stwrite(f'#include "{file}"\n')
            except: pass
def analyze(modinfo: generator.ModInfo)->None:
    _glob_vars:list[(str,any,any)] = _var_finder(modinfo.mod)
    _def_finder(modinfo, _glob_vars)
    
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