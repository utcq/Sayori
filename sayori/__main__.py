from sayo import *
import inspect
from sys import argv
import utils
from types import ModuleType
import sayuu,generator

def main()->None:
    if len(argv)<2: raise Exception("Missing file argument")
    modname=argv[1].replace(".py", "").replace("./", "").replace(".\\", "").strip().replace("\\", "/").replace("/", ".")
    mod=utils.dynamic_import(modname)
    modinfo=generator.ModInfo(mod, mod.__name__)
    sayuu.analyze(modinfo)
    modinfo.writer.close()

if __name__ == "__main__":
    main()