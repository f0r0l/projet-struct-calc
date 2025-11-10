import sys

def open_asm_file(path):
    try:
        with open(path, 'r') as asm_file:
            return asm_file.read()
    except:
        print("ERR : ASM file not found at path " + path)
        exit(1)


def main():
    path = "code.asm" # Default path
    if len(sys.argv) == 2:
        path = sys.argv[1]
    
    asm_code = open_asm_file(path)
    return


if __name__ == "__main__":
    main()
