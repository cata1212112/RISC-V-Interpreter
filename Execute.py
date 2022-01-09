import Memory

def twos_comp(val, bits):
    if (val & (1 << (bits - 1))) != 0:
        val = val - (1 << bits)
    return val

def get_32_bits(val):
    return val&0xffffffff

def sx(val):
    m = 1<<31
    return (val&(m-1)) - (val^m)

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

def LUI(rd, imm):
    Memory.reg[rd] = twos_comp(imm,32)

def AUIPC(rd, imm):
    Memory.reg[rd] = Memory.PC + twos_comp(imm,32)

def JAL(rd, imm):
    Memory.reg[rd] = Memory.PC
    Memory.PC = Memory.PC + twos_comp(imm,32) - 4

def ADD(rd, val1, val2):
    Memory.reg[rd] = twos_comp(get_32_bits(sx(val1)+sx(val2)), 32)

def SUB(rd, val1, val2):
    Memory.reg[rd] = twos_comp(sx(val1) - sx(val2), 32)

def XOR(rd, val1, val2):
    Memory.reg[rd] = twos_comp(ux(val1) ^ ux(val2), 32)

def OR(rd, val1, val2):
    Memory.reg[rd] = twos_comp(ux(val1) | ux(val2), 32)

def AND(rd, val1, val2):
    Memory.reg[rd] = twos_comp(ux(val1) & ux(val2), 32)

def SLL(rd, val1, val2):
    Memory.reg[rd] = twos_comp(get_32_bits(ux(val1)<<val2), 32)

def SRL(rd, val1, val2):
    Memory.reg[rd] = twos_comp(ux(val1)>>val2, 32)

def SRA(rd, val1, val2):
    Memory.reg[rd] = twos_comp(sx(val1)>>val2, 32)

def SLT(rd, val1, val2):
    if sx(val1) < sx(val2):
        Memory.reg[rd] = 1
    else:
        Memory.reg[rd] = 0

def SLTU(rd, val1, val2):
    if ux(val1) < ux(val2):
        Memory.reg[rd] = 1
    else:
        Memory.reg[rd] = 0

def ADDI(rd, val1, imm):
    Memory.reg[rd] = twos_comp(get32(twos_comp(val1, 32) + twos_comp((imm), 32)),32)

def XORI(rd, val1, imm):
    Memory.reg[rd] = ux(val1)^ux(imm)

def ORI(rd, val1, imm):
    Memory.reg[rd] = ux(val1) | imm

def ANDI(rd, val1, imm):
    Memory.reg[rd] = ux(val1) & ux(imm)

def SLTI(rd, val1, imm):
    if sx(val1) < sx(imm):
        Memory.reg[rd] = 1
    else:
        Memory.reg[rd] = 0

def SLTIU(rd, val1, imm):
    if ux(val1) < ux(imm):
        Memory.reg[rd] = 1
    else:
        Memory.reg[rd] = 0

def SLLI(rd, val1, imm):
    Memory.reg[rd] = twos_comp(get_32_bits(ux(val1)<<ux(imm)), 32)

def SRLI(rd, val1, imm):
    Memory.reg[rd] = twos_comp(get_32_bits(ux(val1)>>ux(imm)), 32)

def SRAI(rd, val1, imm):
    Memory.reg[rd] = twos_comp(get_32_bits(sx(val1)>>ux(imm)), 32)

def LB(rd, val1, imm):
    Memory.reg[rd] = sx(get8(Memory.RAM[val1 + imm]))

def LH(rd, val1, imm):
    Memory.reg[rd] = sx(get16(Memory.RAM[val1 + imm]))

def LW(rd, val1, imm):
    Memory.reg[rd] = sx(get32(Memory.RAM[val1 + imm]))

def LBU(rd, val1, imm):
    Memory.reg[rd] = ux(get8(Memory.RAM[val1 + imm]))

def LHU(rd, val1, imm):
    Memory.reg[rd] = ux(get16(Memory.RAM[val1 + imm]))

def SB(val1, val2, imm):
    Memory.RAM[val1+twos_comp(imm,32)] = 0xffffff00&Memory.RAM[val1+twos_comp(imm,32)] + 0x000000ff&get8(val2)

def SH(val1, val2, imm):
    Memory.RAM[val1 + twos_comp(imm, 32)] = 0xffffff00 & Memory.RAM[val1 + twos_comp(imm, 32)] + 0x0000ffff & get16(val2)

def SW(val1, val2, imm):
    Memory.RAM[val1 + twos_comp(imm, 32)] = get32(val2)

def BEQ(val1, val2, imm):
    if val1 == val2:
        Memory.PC += twos_comp(imm,32) - 4

def BNE(val1, val2, imm):
    if val1 != val2:
        Memory.PC += twos_comp(imm,32) - 4

def BLT(val1, val2, imm):
    if val1 < val2:
        Memory.PC += twos_comp(imm,32)

def BGE(val1, val2, imm):
    if val1 >= val2:
        Memory.PC += twos_comp(imm,32)

def BLTU(val1, val2, imm):
    if ux(val1) < ux(val2):
        Memory.PC += twos_comp(imm,32)

def BGEU(val1, val2, imm):
    if ux(val1) >= ux(val2):
        Memory.PC += twos_comp(imm,32)

def ECALL():
    print(Memory.reg)
    if Memory.reg[10] == 1:
        Memory.running = 0

def Execute(decoded):
    funct = decoded[-1]
    if funct == "LUI":
        LUI(decoded[0], decoded[1])
    elif funct == "AUIPC":
        AUIPC(decoded[0], decoded[1])
    elif funct == "JAL":
        JAL(decoded[0], decoded[1])
    elif funct == "ADD":
        ADD(decoded[0], decoded[1], decoded[2])
    elif funct == "SUB":
        SUB(decoded[0], decoded[1], decoded[2])
    elif funct == "XOR":
        XOR(decoded[0], decoded[1], decoded[2])
    elif funct == "OR":
        OR(decoded[0], decoded[1], decoded[2])
    elif funct == "AND":
        AND(decoded[0], decoded[1], decoded[2])
    elif funct == "SLL":
        SLL(decoded[0], decoded[1], decoded[2])
    elif funct == "SRL":
        SRL(decoded[0], decoded[1], decoded[2])
    elif funct == "SRA":
        SRA(decoded[0], decoded[1], decoded[2])
    elif funct == "SLT":
        SLT(decoded[0], decoded[1], decoded[2])
    elif funct == "SLTU":
        SLTU(decoded[0], decoded[1], decoded[2])
    elif funct == "ADDI":
        ADDI(decoded[0], decoded[1], decoded[2])
    elif funct == "XORI":
        XORI(decoded[0], decoded[1], decoded[2])
    elif funct == "ORI":
        ORI(decoded[0], decoded[1], decoded[2])
    elif funct == "ANDI":
        ANDI(decoded[0], decoded[1], decoded[2])
    elif funct == "SLLI":
        SLLI(decoded[0], decoded[1], decoded[2])
    elif funct == "SRLI":
        SRLI(decoded[0], decoded[1], decoded[2])
    elif funct == "SRAI":
        SRAI(decoded[0], decoded[1], decoded[2])
    elif funct == "SLTI":
        SLTI(decoded[0], decoded[1], decoded[2])
    elif funct == "SLTIU":
        SLTIU(decoded[0], decoded[1], decoded[2])
    elif funct == "LB":
        LB(decoded[0], decoded[1], decoded[2])
    elif funct == "LH":
        LH(decoded[0], decoded[1], decoded[2])
    elif funct == "LW":
        LW(decoded[0], decoded[1], decoded[2])
    elif funct == "LBU":
        LBU(decoded[0], decoded[1], decoded[2])
    elif funct == "LHU":
        LHU(decoded[0], decoded[1], decoded[2])
    elif funct == "SB":
        SB(decoded[0], decoded[1], decoded[2])
    elif funct == "SH":
        SH(decoded[0], decoded[1], decoded[2])
    elif funct == "SW":
        SW(decoded[0], decoded[1], decoded[2])
    elif funct == "BEQ":
        BEQ(decoded[0], decoded[1], decoded[2])
    elif funct == "BNE":
        BNE(decoded[0], decoded[1], decoded[2])
    elif funct == "BLT":
        BLT(decoded[0], decoded[1], decoded[2])
    elif funct == "BGE":
        BGE(decoded[0], decoded[1], decoded[2])
    elif funct == "BLTU":
        BLTU(decoded[0], decoded[1], decoded[2])
    elif funct == "BGEU":
        BGEU(decoded[0], decoded[1], decoded[2])

    Memory.reg[0] = 0