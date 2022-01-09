import Memory

def Instruction_Fetch():
    old_PC = Memory.PC
    Memory.PC += 4
    return Memory.RAM[old_PC - Memory.offset]