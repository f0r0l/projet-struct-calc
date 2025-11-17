        XOR R0 R0 R0
        JMP noadd
        ADDi R0 R0 5
noadd:  ADDi R0 R0 1

@ R0 should be 1 at the end
