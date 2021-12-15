from Execute import *

def Decode_J_TYPE(instruction):
    instruction = instruction[::-1]
    imm = ['0']*32
    for i in range(31, 19, -1):
        imm[i] = instruction[31]

    for i in range(19, 11, -1):
        imm[i] = instruction[i]
    imm[11] = instruction[20]
    for i in range(30, 20, -1):
        imm[i-20] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += x
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[7:12], 2)

def Decode_U_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 11, -1):
        imm[i] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += x
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[7:12], 2)

def Decode_I_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 10, -1):
        imm[i] = instruction[31]
    for i in range(30, 19, -1):
        imm[i-20] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += x
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[15:20], 2), int(instruction[12:15], 2), int(instruction[7:12], 2)

def Decode_S_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 10, -1):
        imm[i] = instruction[31]
    for i in range(30, 24, -1):
        imm[i-20] = instruction[i]
    for i in range(11, 6, -1):
        imm[i-7] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += x
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[20:25], 2), int(instruction[15:20], 2), int(instruction[12:15], 2), int(instruction[7:12], 2)


def Decode_B_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 11, -1):
        imm[i] = instruction[31]
    imm[11] = instruction[7]
    for i in range(30, 24, -1):
        imm[i - 20] = instruction[i]
    for i in range(11, 7, -1):
        imm[i - 7] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += x
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[20:25], 2), int(instruction[15:20], 2), int(instruction[12:15], 2)

def Decode_R_TYPE(instruction):
    instruction = instruction[::-1]
    return int(instruction[25:32], 2), int(instruction[20:25], 2), int(instruction[15:20], 2), int(instruction[12:15], 2), int(instruction[7:12], 2)

def Instruction_Decode(instruction):
    instruction = instruction.hex()
    instruction = bin(int(instruction, 16))[2:].zfill(32)

    opcode = instruction[-7:]
    print(opcode)

    if opcode == "0110111":
        imm, rd = Decode_U_TYPE(instruction)
        return rd, imm, LUI

    if opcode == "0010111":
        imm, rd =  Decode_U_TYPE(instruction)
        return rd, imm, AUIPC

    if opcode == "1101111":
        imm, rd = Decode_J_TYPE(instruction)
        return rd, imm, JAL

    if opcode == "0110011":
        funct7, rs2, rs1,funct3, rd = Decode_R_TYPE(instruction)
        if funct3 == 0x0 and funct7 == 0x00:
            return rd, reg[rs2], reg[rs1], ADD

        if funct3 == 0x0 and funct7 == 0x20:
            return rd, reg[rs1], reg[rs2], SUB

        if funct3 == 0x4 and funct7 == 0x00:
            return rd, reg[rs1], reg[rs2], XOR

        if funct3 == 0x6 and funct7 == 0x00:
            return rd, reg[rs1], reg[rs2], OR

        if funct3 == 0x7 and funct7 == 0x00:
            return rd, reg[rs1], reg[rs2], AND