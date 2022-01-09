import sys
import InstructionDecode as ID
import Execute as EX
import InstructionFetch as IF
import Memory

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
        Memory.RAM[poz] = bytes.fromhex(acm[1])

Introdu_In_Memorie()

while 1:
    instruction = IF.Instruction_Fetch()
    if instruction == b'\x00\x00\x00\x00':
        continue
    print(f"Instructiunea este {bin(int(str(instruction.hex()), 16))[2:].zfill(32)} PC este {hex(Memory.PC - 4)}")
    decoded = ID.Instruction_Decode(instruction)
    print(decoded)
    EX.Execute(decoded)