from interpretor import *

def LUI(rd, imm):
    return rd, imm

def AUIPC(rd, imm):
    return rd, PC + imm

def JAL(rd, imm):
    math = PC + 4
    PC += imm
    return rd, math

def ADD(rd, val1, val2):
    return rd, val1+val2

def SUB(rd, val1, val2):
    return rd, val1 - val2

def XOR(rd, val1, val2):
    return rd, val1 ^ val2

def OR(rd, val1, val2):
    return rd, val1 | val2

def AND(rd, val1, val2):
    return rd, val1 & val2