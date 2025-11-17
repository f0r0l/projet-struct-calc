@ Test file
main:
        XOR R1 R1 R1
        XOR R2 R2 R2  @ hello
while:  JNEQ R1 R2 endwh
        ADDi R1 R1 5
        JMP while
endwh:  SUBi R1 R1 4

