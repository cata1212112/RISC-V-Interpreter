import sys
import InstructionDecode as ID
import Execute as EX
import InstructionFetch as IF
from Memory import *

offset = 0x80000000
str_offset = "0x80000000"
machine_code = open(sys.argv[1])

def Introdu_In_Memorie():
    ignore = iter(machine_code)
    next(ignore)
    for line in machine_code:
        if '<' in line:
            continue
        line = line.replace(':', ' ')
        acm = line.split()
        poz = int(acm[0], 16) - int(str_offset, 16)
        RAM[poz] = bytes.fromhex(acm[1])

Introdu_In_Memorie()

