import re


def hexadecimal_a_decimal(hexadecimal):
    try:
        decimal = hexadecimal
        # Elimina "#" o "x" si están presentes en la cadena

        if hexadecimal.startswith("#") or hexadecimal.startswith("x"):
            hexadecimal = hexadecimal[1:]

            # Convierte el valor hexadecimal a decimal
            decimal = int(hexadecimal, 16)
        
        if decimal <= 255:
            return decimal
        else:
            return hexadecimal
    except:
        return hexadecimal
    
def binario_a_decimal(binario):
    try:
        decimal = binario
        # Elimina el prefijo "b" si está presente en la cadena
        if binario.startswith("b"):
            binario = binario[1:]

            # Convierte el valor binario a decimal
            decimal = 0
            longitud = len(binario)

            for i, digito in enumerate(binario[::-1]):
                if digito == '1':
                    decimal += 2**i
        if decimal <= 255:
            return decimal
        else:
            return binario
    except:
        return decimal

mem = r'\((.*?)\)'

file_name = input("Nombre del archivo: ")
file = open(file_name, "r")

labels = []
lineaux = []
lines = []
for line in file:
    lineaux.append(line.strip())
    line = line.strip()
    line = re.split(r'[ ,]', line)
    line = [elemento for elemento in line if elemento]
    for i in range(len(line)):
        dir = re.search(mem, line[i])
        if dir:
            line[i] = str(f"({hexadecimal_a_decimal(dir.group(1))})")
            dir = re.search(mem, line[i])
            line[i] = str(f"({binario_a_decimal(dir.group(1))})")
        line[i] = str(hexadecimal_a_decimal(line[i]))
        line[i] = str(binario_a_decimal(line[i]))
    lines.append(line)


    
for line in lines:
    if len(line) == 1 and line[0][-1] == ":": #Label
        if line[0].strip(":") not in labels:
            labels.append(line[0].strip(":"))
        else:
            print(f"Label {line.strip(':')} definido anteriormente")

count = 0
for line in lines:
    try:
        dir1 = re.search(mem, line[1])
    except:
        pass
    try:
        dir2 = re.search(mem, line[2])
    except:
        pass
    if len(line) == 1 and line[0][-1] == ":": #Label
        pass
    elif line[0] == "MOV":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #MOV A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #MOV A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #MOV A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #MOV A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #MOV B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #MOV B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #MOV B, (Dir)
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1) == "B": #MOV B, (B)
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #MOV (Dir), A
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #MOV (Dir), B
            pass
        elif len(line) == 3 and dir1 and dir1.group(1) == "B" and line[2] == "A": #MOV (B), A
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "ADD":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #ADD A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #ADD A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #ADD A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #ADD A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #ADD B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #ADD B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #ADD B, (Dir)
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and len(line) == 2: #ADD (Dir)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "SUB":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #SUB A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #SUB A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #SUB A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #SUB A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SUB B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #SUB B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #SUB B, (Dir)
            pass
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #SUB (Dir)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "AND":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #AND A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #AND A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #AND A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #AND A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #AND B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #AND B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #AND B, (Dir)
            pass
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #AND (Dir)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "OR":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #OR A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #OR A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #OR A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #OR A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #OR B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #OR B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #OR B, (Dir)
            pass
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #OR (Dir)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "NOT":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #NOT A, A
            pass
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #NOT A, B
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #NOT B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #NOT B, B
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #NOT (Dir), A
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #NOT (Dir), B
            pass
        elif len(line) == 3 and dir1 and dir1.group(1) == "B" and len(line) == 2: #NOT (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "XOR":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #XOR A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #XOR A, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #XOR A, (Dir)
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #XOR A, (B)
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #XOR B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #XOR B, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #XOR B, (Dir)
            pass
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #XOR (Dir)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "SHL":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHL A, A
            pass
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHL A, B
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHL B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHL B, B
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHL (Dir), A
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHL (Dir), B
            pass
        elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHL (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "SHR":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHR A, A
            pass
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHR A, B
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHR B, A
            pass
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHR B, B
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHR (Dir), A
            pass
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHR (Dir), B
            pass
        elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHR (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "INC":
        if len(line) == 2 and line[1] == "B": #INC B
            pass
        elif len(line) == 2 and dir1 and dir1.group(1).isdigit(): #INC (Dir)
            pass
        elif len(line) == 2 and dir1 and dir1.group(1) == "B": #INC (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "RST":
        if len(line) == 2 and dir1 and dir1.group(1).isdigit(): #INC (Dir)
            pass
        elif len(line) == 2 and dir1 and dir1.group(1) == "B": #INC (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif line[0] == "CMP":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #CMP A, B
            pass
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #CMP A, Lit
            pass
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #CMP B, Lit
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #CMP A, Dir
            pass
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #CMP B, Dir
            pass
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #CMP A, (B)
            pass
        else:
            print(f"La función '{lineaux[count]}' no existe")
    elif len(line) == 2 and line[0] == "JMP" and ((line[1] in labels) or line[1].isdigit()): #JMP Dir
        pass
    elif len(line) == 2 and line[0] == "JEQ" and ((line[1] in labels) or line[1].isdigit()): #JEQ Dir
        pass
    elif len(line) == 2 and line[0] == "JNE" and ((line[1] in labels) or line[1].isdigit()): #JNE Dir
        pass
    elif len(line) == 2 and line[0] == "JGT" and ((line[1] in labels) or line[1].isdigit()): #JGT Dir
        pass
    elif len(line) == 2 and line[0] == "JLT" and ((line[1] in labels) or line[1].isdigit()): #JLT Dir
        pass
    elif len(line) == 2 and line[0] == "JGE" and ((line[1] in labels) or line[1].isdigit()): #JGE Dir
        pass
    elif len(line) == 2 and line[0] == "JLE" and ((line[1] in labels) or line[1].isdigit()): #JLE Dir
        pass
    elif len(line) == 2 and line[0] == "JCR" and ((line[1] in labels) or line[1].isdigit()): #JCR Dir
        pass
    elif len(line) == 2 and line[0] == "JOV" and ((line[1] in labels) or line[1].isdigit()): #JOV Dir
        pass
    else:
        print(f"La función '{lineaux[count]}' no existe")
    count += 1

file.close()
