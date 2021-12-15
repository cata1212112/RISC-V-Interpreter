import sys
import InstructionDecode as ID
import Execute as EX
import InstructionFetch as IF

RAM = []
reg = [0] * 31
PC = 0

offset = 0x80000000
machine_code = open(sys.argv[1])

def Introdu_In_Memorie():
    ignore = iter(machine_code)
    next(ignore)
    for line in machine_code:
        if '<' in line:
            continue
        line = line.replace(':', ' ')
        acm = line.split()
        RAM.append(bytes.fromhex(acm[1]))

Introdu_In_Memorie()
