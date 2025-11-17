        XOR R0 R0 R0
        ADDi R0 R0 5

        XOR R1 R1 R1

wh:     JSUP R1 R0 ewh      @ loop 5 times

        ADDi R1 R1 1
        JMP wh

ewh:    XOR R0 R0 R0
