"""
FONCTIONNEMENT :
1) "Supprime" les commentaires
2) Analyse les labels et les mets dans l'objet label avec 
   en clé le label et en valeur la ligne à laquelle il pointe
3) Convertit la ligne de code en un tableau de keywords
4) Convertit chacun de ces keywords en code binaire correspondant

-> Si une erreur est détectée tout s'arrête
"""

import sys

INSTRUCTION_SIZE = 32
CONSTANT_SIZE = 16

NB_OF_REGISTERS = 8

ARITHMETIC_OPERATIONS = ["ADD", "SUB", "AND", "OR", "XOR", "SL", "SR", "MUL"]
MEM_OPERATIONS = ["LD", "ST"]
CTRL_OPERATIONS = ["JMP", "JEQU", "JNEQ", "JSUP", "JINF", "CALL", "RET"]

labels = {}
current_line_index = 0


def open_asm_file():
    path = "asm/code.asm" # Default path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        
    try:
        with open(path, 'r') as asm_file:
            return asm_file.readlines()
    except:
        print("ERR : ASM file not found at path " + path)
        sys.exit(1)    


def write_bin_file(bin_lines):
    path = "out.bin" # Default path
    if len(sys.argv) >= 3:
        path = sys.argv[2]

    try:
        with open(path, 'w+') as out_file:
            out_file.write(bin_lines)
    except:
        print("ERR : ASM file not found at path " + path)
        sys.exit(1)


def write_hex_file(hex_lines):
    path = "out.hex" # Default path
    if len(sys.argv) >= 3:
        path = sys.argv[2]

    try:
        with open(path, 'w+') as out_file:
            out_file.write(hex_lines)
    except:
        print("ERR : ASM file not found at path " + path)
        sys.exit(1)


def print_error(msg: str):
    global current_line_index
    print("Error at line " + str(current_line_index) + " :")
    print(msg)
    sys.exit(1)


def to_bin(nb: int, size: int):
    """
    converts a decimal number to a binary number in a string
    of size provided in arguments
    """
    bin_nb = bin(nb)
    bin_nb = bin_nb.removeprefix("0b")
    n = len(bin_nb)
    if n > size:
        print_error(nb + " could not be converted to a " + size + " long binary nb")
    return (size-n) * "0" + bin_nb


def bin_to_hex(bin: str):
    """Converts a 32-bits long number in a 8 bits hexadecimal string"""
    hex_nb = hex(int(bin, 2))
    hex_nb = hex_nb.removeprefix("0x").upper()
    n = len(hex_nb)
    if n > 8:
        print_error(bin + " could not be converted to a 8 long hexadecimal nb")
    return (8-n) * "0" + hex_nb


def label_encoding(label: str, bin_size = 16):
    global labels
    
    if label not in labels:
        print_error("Label '" + label + "' does not exist")

    return to_bin(labels[label], bin_size)[::-1] # reverse for Logisim


def fill_with_zeros(bin: str, size: int):
    n = len(bin)
    if n >= size: return bin
    return bin + (size-n) * "0"


def is_register_valid(reg: str | None):
    if reg == "":
        return False
    
    if reg[0] != 'R':
        return False
    
    x = int(reg[1:])
    return x >= 0 and x <= NB_OF_REGISTERS-1


def is_operation_immediate(op: str):
    if not op.endswith("i"): return False
    return op.removesuffix("i") in ARITHMETIC_OPERATIONS


def get_operation_code(op: str):
    if is_operation_immediate(op):
        return get_operation_code(op.removesuffix("i"))

    match op:
        case "ADD" | "LD" | "JMP":
            return "000"
        case "SUB" | "ST" | "JEQU":
            return "001"
        case "AND" | "JNEQ":
            return "010"
        case "OR" | "JSUP":
            return "011"
        case "XOR" | "JINF":
            return "100"
        case "SL" | "CALL":
            return "101"
        case "SR" | "RET":
            return "110"
        case "MUL":
            return "111"
        case _:
            print_error("Unknown operation " + op)


def get_operation_category(op: str):
    if (op in ARITHMETIC_OPERATIONS or is_operation_immediate(op)):
        return "00"
    
    if op in MEM_OPERATIONS: return "01"
    if op in CTRL_OPERATIONS: return "11"

    print_error("Unknown operation '" + op + "'")


def get_register_binary(reg: str | None) -> str:
    if not is_register_valid(reg):
        print_error("Invalid register '" + reg + "'")
    
    try:
        reg_nb = int(reg.removeprefix("R"))
        return to_bin(reg_nb, 3)[::-1] # reverse for Logisim
    except:
        print_error("Invalid register '" + reg + "'")


def process_line(keys: list[str]):
    global current_line_index
    current_line_index += 1 # use for printing errors

    if len(keys) == 0: return None

    op = keys[0]

    category = get_operation_category(op)
    code = get_operation_code(op)
    bin_code = category + code

    if category == "00": # arithmetic operation
        is_immediate = is_operation_immediate(op)
        bin_code += "1" if is_immediate else "0"
        bin_code += get_register_binary(keys[1])
        bin_code += get_register_binary(keys[2])
        if is_immediate:
            bin_code += to_bin(int(keys[3]), CONSTANT_SIZE)[::-1] # reverse constant for Logisim
        else:
            bin_code += get_register_binary(keys[3])

    if category == "11": # CTRL operation
        if op == 'JMP': # no registers for JMP instruction, only label
            bin_code += label_encoding(keys[1])
        else:
            bin_code += get_register_binary(keys[1])
            bin_code += get_register_binary(keys[2])
            bin_code += label_encoding(keys[3])

    if category == "01": # MEM operation
        bin_code += "0" # unused bit
        bin_code += get_register_binary(keys[1])
        bin_code += get_register_binary(keys[2])
        
    return fill_with_zeros(bin_code, INSTRUCTION_SIZE) # make instruction 32 bits long


def compile_code(code_lines):
    code_keys = analyse_labels(code_lines)
    bin_code = "" # the string containing the final code 
    hex_code = ""
    for keys in code_keys:
        bin_line = process_line(keys)
        if bin_line is None: continue

        reversed_line = bin_line[::-1] # reverse line for Logisim
        # separate line in groups of 8 bits for importing in Logisim
        splitted_line = reversed_line[:8] + " " + reversed_line[8:16] + " " + reversed_line[16:24] + " " + reversed_line[24:32]
        hex_code += bin_to_hex(reversed_line) + "\n"
        bin_code += splitted_line + "\n"

    return (bin_code.removesuffix("\n"), hex_code.removesuffix("\n"))


def analyse_labels(code_lines):
    # The array that will be returned containing only useful keys
    # (without comments or labels)
    code_keys = [] 
    i = 0
    for line in code_lines:
        code_keys.append([]) # empty line in case the line is not code
        line = line.strip()
        if line.startswith("@"): # ignore comments
            continue
        
        keys = line.split(" ")
        keys = [key for key in keys if key != '' and key != ' ']
        
        if len(keys) == 0: continue

        if keys[0].endswith(":"): # starts with a label
            labels[keys[0].removesuffix(":")] = i # store label in global labels obj
            keys = keys[1:]

        if len(keys) == 0: continue
        if keys[0].startswith("@"): # the line is a label + a comment : ignore it
            continue

        code_keys[i] = keys
        i += 1

    return code_keys


def main():
    code_lines = open_asm_file()
    (bin_lines, hex_lines) = compile_code(code_lines)
    print(hex_lines)
    write_hex_file(hex_lines)
    write_bin_file(bin_lines)


if __name__ == "__main__":
    main()
