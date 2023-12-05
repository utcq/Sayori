from types import ModuleType
from os import path,mkdir

class Writer:
    def __init__(self, modname:str):
        if (not path.exists("sayo_build/")): mkdir("sayo_build/")
        self.modname = modname
        self.header=open(f"sayo_build/{modname}.h", "w+")
        self.source=open(f"sayo_build/{modname}.c", "w+")
        self.tabs=0
        
        self.hwrite(f"#include <stdint.h>\n#ifndef {modname.upper()}_H\n#define {modname.upper()}_H\n\n")
        self.swrite(f'#include <stdint.h>\n#include "{modname}.h"\n\n')
        
    def hwrite(self, value:str)->None:
        self.header.write(("\t"*self.tabs)+value)
    
    def swrite(self, value:str)->None:
        self.source.write(("\t"*self.tabs)+value)

    def stwrite(self, value:str)->None:
        source = self.source.read()
        self.swrite(value)
        self.swrite(source)
        
    def close(self)->None:
        self.hwrite("\n#endif")
        
        self.source.close()
        self.header.close()

class ModInfo:
    def __init__(self, mod:ModuleType, modname:str):
        self.mod=mod
        self.modname=modname
        self.source = open(mod.__file__, "r").read()
        self.writer=Writer(self.modname)