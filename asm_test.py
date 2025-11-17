from colorama import Fore, Back, Style
from asm import compile_code

TESTS = [
    (
        [
            "   @ Test comment",
            "   ADDi R1 R0 4",
            "   SUB R7 R0 R1",
            "   AND R1 R2 R3",
            "   or:"
            " "
            "   OR R1 R2 R3",
            "   XOR R1 R2 R3",
            "   JNEQ R2 R4 sl",
            "   @ Test comment",
            "   sl: SL R1 R2 R3",
            "   SR R1 R2 R3",
            "   MUL R1 R2 R3",
            "   JMP or"
        ], [
            "00000100 10000000 00000000 01000000",
            "00001011 10000010 00000000 00000000",
            "00010000 10100110 00000000 00000000",
            "00011000 10100110 00000000 00000000",
            "00100000 10100110 00000000 00000000",
            "11010010 10000000 00000000 11000000",
            "00101000 10100110 00000000 00000000",
            "00110000 10100110 00000000 00000000",
            "00111000 10100110 00000000 00000000",
            "11000000 00000000 00011000 00000000",
        ]
    ),
    ( ["JEQU R0 R0 label"], None ),
    (
        [
            "LD R0 R4",
            "label:    ST R2 R7"
        ],
        [
            "01000000 10000000 00000000 00000000",
            "01001010 11100000 00000000 00000000"
        ]
    )
]


def main():
    test_index = 0
    for (INPUT, OUTPUT) in TESTS:
        test_index += 1
        print(Style.RESET_ALL)
        print(f"> TEST {test_index} : ")
        try:
            compiled_code = compile_code(INPUT)

            if OUTPUT is None:
                print(Fore.RED, end="")
                print(f"[-] FAILED")
                print("Should have returned an error, but returned")
                print(compiled_code)
                continue

            txt_output = ""
            for out_line in OUTPUT:
                txt_output += out_line[::-1] + "\n"
            txt_output = txt_output.removesuffix("\n")

            n = len(compiled_code.split('\n'))
            m = len(txt_output.split('\n'))
            if n != m:
                print(Fore.RED, end="")
                print(f"[-] FAILED : Different lengths ({n} vs {m})")
                print(compiled_code)
                print("vs")
                print(txt_output)
                continue
            
            isError = False
            for i in range(0, n):
                a = compiled_code.split("\n")[i]
                b = txt_output.split("\n")[i]
                if a != b:
                    print(Fore.RED, end="")
                    print(f"[-] FAILED : At line {i+1}")
                    print("Expected : " + b)
                    print("Got      : " + a)
                    
                    isError = True
                    break

            if isError: continue
            
            print(Fore.LIGHTGREEN_EX, end="")
            print(f"[+] SUCCESS")
        except SystemExit:
            if OUTPUT is None:
                print(Fore.LIGHTGREEN_EX, end="")
                print(f"[+] SUCCESS")
                continue
            else:
                print(Fore.RED, end="")
                print(f"[-] FAILED")
                print("Assembler returned an error")
                continue
    print(Style.RESET_ALL)


if __name__ == "__main__":
    main()
