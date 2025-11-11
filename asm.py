import sys

INSTRUCTION_SIZE = 32
CONSTANT_SIZE = 16

ARITHMETIC_OPERATIONS = ["ADD", "SUB", "AND", "OR", "XOR", "SL", "SR", "MUL"]
MEM_OPERATIONS = ["LD", "ST"]
CTRL_OPERATIONS = ["JMP", "JEQU", "JNEQ", "JSUP", "JINF", "CALL", "RET"]


def open_asm_file():
    path = "asm/code.asm" # Default path
    if len(sys.argv) >= 2:
        path = sys.argv[1]
        
    try:
        with open(path, 'r') as asm_file:
            return asm_file.readlines()
    except:
        print("ERR : ASM file not found at path " + path)
        exit(1)


def write_bin_file(bin_lines):
    path = "out.bin" # Default path
    if len(sys.argv) >= 3:
        path = sys.argv[2]

    try:
        with open(path, 'w+') as out_file:
            out_file.write(bin_lines)
    except:
        print("ERR : ASM file not found at path " + path)
        exit(1)


def to_bin(nb: int, size: int):
    bin_nb = bin(nb)
    bin_nb = bin_nb.removeprefix("0b")
    n = len(bin_nb)
    if n > size:
        print(nb + " could not be converted to a " + size + " long binary nb")
        exit(1)
    return (size-n) * "0" + bin_nb


def fill_with_zeros(bin: str, size: int):
    n = len(bin)
    if n >= size: return bin
    return bin + (size-n) * "0"


def is_operation_immediate(op: str):
    if not op.endswith("i"): return False
    return op.removesuffix("i") in ARITHMETIC_OPERATIONS


def get_operation_code(op: str):
    match op:
        case "ADD" | "ADDi" | "LD" | "JMP":
            return "000"
        case "SUB" | "SUBi" | "ST" | "JEQU":
            return "001"
        case "AND" | "ANDi" | "JNEQ":
            return "010"
        case "OR" | "ORi" | "JSUP":
            return "011"
        case "XOR" | "XORi" | "JINF":
            return "100"
        case "SL" | "SLi" | "CALL":
            return "101"
        case "SR" | "SRi" | "RET":
            return "110"
        case "MUL" | "MULi":
            return "111"
        case _:
            print("ERR : Unknown operation " + op)
            exit(1)


def get_operation_category(op: str):
    if (op in ARITHMETIC_OPERATIONS
        or (op.endswith("i") and (op.removesuffix("i") in ARITHMETIC_OPERATIONS))):
        return "00"
    
    if op in MEM_OPERATIONS: return "01"
    if op in CTRL_OPERATIONS: return "11"

    print("ERR : Unknown operation " + op)
    exit(1)


def get_register_binary(reg: str | None):
    if reg is None or not reg.startswith("R"):
        print("Invalid register " + reg)
        exit(1)
    
    try:
        reg_nb = int(reg.removeprefix("R"))
        return to_bin(reg_nb, 3)
    except:
        print("Invalid register " + reg)
        exit(1)


def process_line(line: str):
    line = line.strip()
    if line.startswith("@"): # Ignore comments
        return None
    
    keys = line.split(" ")
    op = keys[0]
    if op is None: return None

    category = get_operation_category(op)
    code = get_operation_code(op)
    bin_code = category + code

    if category == "00": # If arithmetic operation
        is_immediate = is_operation_immediate(op)
        bin_code += "1" if is_immediate else "0"
        bin_code += get_register_binary(keys[1])
        bin_code += get_register_binary(keys[2])
        if is_immediate:
            bin_code += to_bin(int(keys[3]), CONSTANT_SIZE)
        else:
            bin_code += get_register_binary(keys[3])
        
    return fill_with_zeros(bin_code, INSTRUCTION_SIZE)


def compile_code(code_lines):
    bin_lines = ""
    for line in code_lines:
        bin_code = process_line(line)
        if bin_code is None: continue # Ignore comments
        bin_lines += bin_code[::-1] + "\n"
    return bin_lines.removesuffix("\n")


def main():
    code_lines = open_asm_file()
    bin_lines = compile_code(code_lines)
    print(bin_lines)
    write_bin_file(bin_lines)


if __name__ == "__main__":
    main()
