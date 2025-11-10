# Projet structure des calculateurs
Ben GAUDRY, Daniel CAILLE, Kevin BERTAUX, Wail BENSALEM

## Encodage

| CATEGORIE | INST | CODE CATEGORIE | CODE INST |
|-----------|------|----------------|-----------|
| UAL       | ADD  | 00             | 000       |
| UAL       | SUB  | 00             | 001       |
| UAL       | AND  | 00             | 010       |
| UAL       | OR   | 00             | 011       |
| UAL       | XOR  | 00             | 100       |
| UAL       | SL   | 00             | 101       |
| UAL       | SR   | 00             | 110       |
| UAL       | MUL  | 00             | 111       |
|-----------|------|----------------|-----------|
| MEM       | LD   | 01             | 000       |
| MEM       | ST   | 01             | 001       |
|-----------|------|----------------|-----------|
| CTRL      | JMP  | 11             | 000       |
| CTRL      | JEQU | 11             | 001       |
| CTRL      | JNEQ | 11             | 010       |
| CTRL      | JSUP | 11             | 011       |
| CTRL      | JINF | 11             | 100       |
| CTRL      | CALL | 11             | 101       |
| CTRL      | RET  | 11             | 110       |


## Utilisation assembleur

```sh
python asm.py [asm_file_path]
```
