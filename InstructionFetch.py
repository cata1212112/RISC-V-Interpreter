from interpretor import *

def Instruction_Fetch(program_counter):
    old_PC = program_counter
    program_counter += 4
    return RAM[old_PC - offset]