from types import ModuleType
from os import path,mkdir

class Writer:
    def __init__(self, modname:str):
        if (not path.exists("sayo_build/")): mkdir("sayo_build/")
        self.header=open(f"sayo_build/{modname}.h", "w")
        self.source=open(f"sayo_build/{modname}.c", "w")
        
        self.hwrite(f"#ifndef {modname.upper()}_H\n#define {modname.upper()}_H\n")
        self.swrite(f'#include "{modname}.h"\n')
        
    def hwrite(self, value:str)->None:
        self.header.write(value)
    
    def swrite(self, value:str)->None:
        self.source.write(value)
        
    def close(self)->None:
        self.hwrite("\n#endif")
        
        self.source.close()
        self.header.close()

class ModInfo:
    def __init__(self, mod:ModuleType, modname:str):
        self.mod=mod
        self.modname=modname
        self.writer=Writer(self.modname)