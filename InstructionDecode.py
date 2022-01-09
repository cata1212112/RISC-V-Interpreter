import Memory

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
        imm_str += str(x)
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[11:6:-1], 2)

def Decode_U_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 11, -1):
        imm[i] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += str(x)
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[11:6:-1], 2)

def Decode_I_TYPE(instruction):
    instruction = instruction[::-1]
    imm = [0] * 32
    for i in range(31, 10, -1):
        imm[i] = instruction[31]
    for i in range(30, 19, -1):
        imm[i-20] = instruction[i]

    imm_str = ""
    for x in imm:
        imm_str += str(x)
    func7 = imm_str[5:12]
    special_funct7 = imm_str[0:5]
    imm_str = imm_str[::-1]
    func7 = func7[::-1]
    special_funct7 = special_funct7[::-1]
    # print(int(imm_str, 2), int(instruction[19:14:-1], 2), int(instruction[14:11:-1], 2), int(instruction[11:6:-1], 2))
    # print(f"rs1 {int(instruction[24:19:-1], 2)} in rs1 {Memory.reg[int(instruction[24:19:-1], 2)]}")
    return int(imm_str, 2), int(instruction[19:14:-1], 2), int(instruction[14:11:-1], 2), int(instruction[11:6:-1], 2), int(func7, 2), int(special_funct7, 2)

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
        imm_str += str(x)
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[24:19:-1], 2), int(instruction[19:14:-1], 2), int(instruction[14:11:-1], 2), int(instruction[11:6:-1], 2)


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
        imm_str += str(x)
    imm_str = imm_str[::-1]
    return int(imm_str, 2), int(instruction[24:19:-1], 2), int(instruction[19:14:-1], 2), int(instruction[14:11:-1], 2)

def Decode_R_TYPE(instruction):
    instruction = instruction[::-1]
    return int(instruction[31:24:-1], 2), int(instruction[24:19:-1], 2), int(instruction[19:14:-1], 2), int(instruction[14:11:-1], 2), int(instruction[11:6:-1], 2)

def Instruction_Decode(instruction):
    instruction = instruction.hex()
    instruction = bin(int(str(instruction), 16))[2:].zfill(32)

    opcode = instruction[-7:]

    if opcode == "0110111":
        imm, rd = Decode_U_TYPE(instruction)
        return rd, imm, "LUI"

    if opcode == "0010111":
        imm, rd =  Decode_U_TYPE(instruction)
        return rd, imm, "AUIPC"

    if opcode == "1101111":
        imm, rd = Decode_J_TYPE(instruction)
        return rd, imm, "JAL"

    if opcode == "0110011":
        funct7, rs2, rs1,funct3, rd = Decode_R_TYPE(instruction)
        if funct3 == 0x0 and funct7 == 0x00:
            return rd, Memory.reg[rs2], Memory.reg[rs1], "ADD"

        if funct3 == 0x0 and funct7 == 0x20:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SUB"

        if funct3 == 0x4 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "XOR"

        if funct3 == 0x6 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "OR"

        if funct3 == 0x7 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "AND"

        if funct3 == 0x1 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SLL"

        if funct3 == 0x5 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SRL"

        if funct3 == 0x5 and funct7 == 0x20:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SRA"

        if funct3 == 0x2 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SLT"

        if funct3 == 0x3 and funct7 == 0x00:
            return rd, Memory.reg[rs1], Memory.reg[rs2], "SLTU"

    if opcode == "0010011":
        imm, rs1, funct3, rd, funct7, speacial_funct7 = Decode_I_TYPE(instruction)

        if funct3 == 0x0:
            return rd, Memory.reg[rs1], imm, "ADDI"
        if funct3 == 0x4:
            return rd, Memory.reg[rs1], imm, "XORI"
        if funct3 == 0x6:
            return rd, Memory.reg[rs1], imm, "ORI"
        if funct3 == 0x7:
            return rd, Memory.reg[rs1], imm, "ANDI"
        if funct3 == 0x1 and funct7 == 0x00:
            return rd, Memory.reg[rs1], speacial_funct7, "SLLI"
        if funct3 == 0x5 and funct7 == 0x00:
            return rd, Memory.reg[rs1], speacial_funct7, "SRLI"
        if funct3 == 0x5 and funct7 == 0x20:
            return rd, Memory.reg[rs1], speacial_funct7, "SRAI"
        if funct3 == 0x2:
            return rd, Memory.reg[rs1], imm, "SLTI"
        if funct3 == 0x3:
            return rd, Memory.reg[rs1], imm, "SLTIU"

    if opcode == "0000011":
        imm, rs1, funct3, rd, funct7, speacial_funct7 = Decode_I_TYPE(instruction)

        if funct3 == 0x0:
            return rd, Memory.reg[rs1], imm, "LB"
        if funct3 == 0x1:
            return rd, Memory.reg[rs1], imm, "LH"
        if funct3 == 0x2:
            return rd, Memory.reg[rs1], imm, "LW"
        if funct3 == 0x4:
            return rd, Memory.reg[rs1], imm, "LBU"
        if funct3 == 0x5:
            return rd, Memory.reg[rs1], imm, "LHU"


    if opcode == "0100011":
        imm ,rs2, rs1, funct3, rd = Decode_S_TYPE(instruction)

        if funct3 == 0x0:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "SB"
        if funct3 == 0x1:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "SH"
        if funct3 == 0x2:
            return Memory.reg[rs1],Memory.reg[rs2], imm, "SW"

    if opcode == "1100011":
        imm ,rs2, rs1, funct3 = Decode_B_TYPE(instruction)

        if funct3 == 0x0:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "BEQ"
        if funct3 == 0x1:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "BNE"
        if funct3 == 0x4:
            return Memory.reg[rs1],Memory.reg[rs2], imm, "BLT"
        if funct3 == 0x5:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "BGE"
        if funct3 == 0x6:
            return Memory.reg[rs1],Memory.reg[rs2],imm,  "BLTU"
        if funct3 == 0x7:
            return Memory.reg[rs1],Memory.reg[rs2], imm, "BGEU"

