from Memory import *

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def get_32_bits(val):
    return val&0xffffffff

def sx(val):
    m = 1<<31
    val = val&((1<<32) - 1)
    return (val^m) - m

def ux(value):
    ok = 0
    if (value & (1<<31)) != 0:
        ok = 1
    value = value&0x7fffffff + (1<<32) * ok
    return value

def get8(val):
    return val&0x000000ff

def get16(val):
    return val&0x0000ffff

def get32(val):
    return val&0xffffffff

def LUI(rd, imm): #VERIFICAT
    reg[rd] = twos_comp(imm,32)

def AUIPC(rd, imm):
    reg[rd] = PC + twos_comp(imm,32)

def JAL(rd, imm):
    reg[rd] = PC + 4
    PC += twos_comp(imm,32)

def ADD(rd, val1, val2):
    reg[rd] = twos_comp(get_32_bits(sx(val1)+sx(val2)), 32)

def SUB(rd, val1, val2):
    reg[rd] = twos_comp(sx(val1) - sx(val2), 32)

def XOR(rd, val1, val2):
    reg[rd] = twos_comp(ux(val1) ^ ux(val2), 32)

def OR(rd, val1, val2):
    return rd, twos_comp(ux(val1) | ux(val2), 32)

def AND(rd, val1, val2):
    return rd, twos_comp(ux(val1) & ux(val2), 32)

def SLL(rd, val1, val2):
    reg[rd] = twos_comp(get_32_bits(ux(val1)<<val2), 32)

def SRL(rd, val1, val2):
    reg[rd] = twos_comp(ux(val1)>>val2, 32)

def SRA(rd, val1, val2):
    reg[rd] = twos_comp(sx(val1)>>val2, 32)

def SLT(rd, val1, val2):
    if sx(val1) < sx(val2):
        reg[rd] = 1
    else:
        reg[rd] = 0

def SLTU(rd, val1, val2):
    if ux(val1) < ux(val2):
        reg[rd] = 1
    else:
        reg[rd] = 0

def ADDI(rd, val1, imm):
    reg[rd] = val1 + sx(imm)

def XORI(rd, val1, imm):
    reg[rd] = ux(val1)^ux(imm)

def ORI(rd, val1, imm):
    reg[rd] = ux(val1) | ux(imm)

def ANDI(rd, val1, imm):
    reg[rd] = ux(val1) & ux(imm)

def SLTI(rd, val1, imm):
    if sx(val1) < sx(imm):
        reg[rd] = 1
    else:
        reg[rd] = 0

def SLTIU(rd, val1, imm):
    if ux(val1) < ux(imm):
        reg[rd] = 1
    else:
        reg[rd] = 0

def SLLI(rd, val1, imm):
    reg[rd] = twos_comp(get_32_bits(ux(val1)<<ux(imm)), 32)

def SRLI(rd, val1, imm):
    reg[rd] = twos_comp(get_32_bits(ux(val1)>>ux(imm)), 32)

def SRAI(rd, val1, imm):
    reg[rd] = twos_comp(get_32_bits(sx(val1)>>ux(imm)), 32)

def LB(rd, val1, imm):
    reg[rd] = sx(get8(RAM[val1 + imm]))

def LH(rd, val1, imm):
    reg[rd] = sx(get16(RAM[val1 + imm]))

def LW(rd, val1, imm):
    reg[rd] = sx(get32(RAM[val1 + imm]))

def LBU(rd, val1, imm):
    reg[rd] = ux(get8(RAM[val1 + imm]))
    return rd, ux(get8(RAM[val1 + imm]))

def LHU(rd, val1, imm):
    return rd, ux(get16(RAM[val1 + imm]))

def SB(val1, val2, imm):
    return val1+twos_comp(imm,32), get8(val2)

def SB(val1, val2, imm):
    return val1+twos_comp(imm,32), get16(val2)

def SB(val1, val2, imm):
    return val1+twos_comp(imm,32), get32(val2)

def BEQ(val1, val2, imm):
    math = 0
    if val1 == val2:
        math = PC + twos_comp(imm,32)
    return math

def BEQ(val1, val2, imm):
    math = 0
    if val1 != val2:
        math = PC + twos_comp(imm,32)
    return math

def BLT(val1, val2, imm):
    math = 0
    if val1 < val2:
        math = PC + twos_comp(imm,32)
    return math

def BGE(val1, val2, imm):
    math = 0
    if val1 >= val2:
        math = PC + twos_comp(imm,32)
    return math

def BLTU(val1, val2, imm):
    math = 0
    if ux(val1) < ux(val2):
        math = PC + twos_comp(imm,32)
    return math

def BGEU(val1, val2, imm):
    math = 0
    if ux(val1) >= ux(val2):
        math = PC + twos_comp(imm,32)
    return math