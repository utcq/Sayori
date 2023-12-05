#################################################
from sys import path as _path
from os import name as _name
_path[0] = ("\\" if _name == "nt" else "/").join(_path[0].split(("\\" if _name == "nt" else "/"))[:-1])
#################################################

from sayori import *

stdio = Include("stdio.h")

magic = Define(0x8f23e)

n1: uint16_t = None

def add(x:int, y:int)->int:
    return (x-1)+y


def main() -> OPointer(int):
    greet: str = "Hello"
    num: int = add(1+0x50, 0x20);
    printf("%s\n",greet)
    return 0
