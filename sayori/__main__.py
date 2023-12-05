from sayo import *
import inspect
from sys import argv
import utils
import os
from types import ModuleType
import sayuu,generator

def compile(out:str)->None:
    to_compile:list[str]=[]
    for path,fd,files in os.walk("sayo_build/"):
        for file in files:
            if (file.endswith(".c")):
                to_compile.append(path+file)
    os.system(f"gcc {' '.join(to_compile)} -o sayo_build/{out}")



def main()->None:
    if len(argv)<2: raise Exception("Missing file argument")
    modname=argv[1].replace(".py", "").replace("./", "").replace(".\\", "").strip().replace("\\", "/").replace("/", ".")
    mod=utils.dynamic_import(modname)
    modinfo=generator.ModInfo(mod, mod.__name__)
    sayuu.analyze(modinfo)
    modinfo.writer.close()

    compile(mod.__name__)

if __name__ == "__main__":
    main()