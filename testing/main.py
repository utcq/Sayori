#################################################
from sys import path as _path
from os import name as _name
_path[0] = ("\\" if _name == "nt" else "/").join(_path[0].split(("\\" if _name == "nt" else "/"))[:-1])
#################################################

from sayori import *

stdio = Include("stdio.h")


def main() -> OPointer(int):
    username:str = "UnityTheCoder"; # ANNOTAZIONE
    myname = "UwU" # SENZA
    printf("%s\n", username);
    return 0

# Original python source