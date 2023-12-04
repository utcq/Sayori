#################################################
from sys import path as _path
from os import name as _name
sep = ("\\" if _name == "nt" else "/")
_path[0] = sep.join(_path[0].split(sep)[:-1])
#################################################

from sayori import *


magic = Define(0x8f23e)

n1: uint8_t = TReference(uint8_t(10))

def main(x:int) -> OPointer(int):
    num: uint16_t = 0x90
    return 0
