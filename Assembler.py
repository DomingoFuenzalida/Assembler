import re
memory = []
A = 0
B = 0
alu = 0
error = 0

for i in range(256):
    memory.append(0)

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

labels = {}
lineaux = []
lines = []
pos = 0
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
            labels[line[0].strip(":")] = pos
        else:
            print(f"Label {line.strip(':')} definido anteriormente")
    pos += 1

count = 0
for line in lines:
    try:
        if int(line[2]) < 0:
            line[2] = str(256 + int(line[2]))
    except:
        pass
    try:
        if int(line[1]) < 0:
            line[1] = str(256 + int(line[1]))
    except:
        pass
    try:
        dir1 = re.search(mem, line[1])
        if dir1:
            first = hexadecimal_a_decimal(dir.group(1))
            dir = re.search(mem, line[i])
            line[i] = str(f"({binario_a_decimal(dir.group(1))})")
        line[i] = str(hexadecimal_a_decimal(line[i]))
        line[i] = str(binario_a_decimal(line[i]))
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
            A = B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #MOV A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int (line[2]))
            A = int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #MOV A, (Dir)
            A = memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #MOV A, (B)
            A = memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #MOV B, A
            B = A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #MOV B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B = int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #MOV B, (Dir)
            B = memory[int(dir2.group(1))]
            alu = B
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #MOV A, (B)
            A = memory[B]
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1) == "B": #MOV B, (B)
            B = memory[B]
            alu = B
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #MOV (Dir), A
            memory[int(dir1.group(1))] = A
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #MOV (Dir), B
            memory[int(dir1.group(1))] = B
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1) == "B" and line[2] == "A": #MOV (B), A
            memory[B] = A
            alu = memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "ADD":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #ADD A, B
            A += B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #ADD A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            A += int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #ADD A, (Dir)
            A += memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #ADD A, (B)
            A += memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #ADD B, A
            B += A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #ADD B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B += int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #ADD B, (Dir)
            B += memory[int(dir2.group(1))]
            alu = B
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and len(line) == 2: #ADD (Dir)
            memory[int(dir1.group(1))] = A + B
            alu = memory[int(dir1.group(1))]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "SUB":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #SUB A, B
            A -= B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #SUB A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            A -= int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #SUB A, (Dir)
            A -= memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #SUB A, (B)
            A -= memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SUB B, A
            B = A - B
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #SUB B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B -= int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #SUB B, (Dir)
            B -= memory[int(dir2.group(1))]
            alu = B
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #SUB (Dir)
            memory[int(dir1.group(1))] = A - B
            alu = memory[int(dir1.group(1))]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "AND":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #AND A, B
            A = A & B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #AND A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            A = A & int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #AND A, (Dir)
            A = A & memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #AND A, (B)
            A = A & memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #AND B, A
            B = B & A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #AND B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B = B & int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #AND B, (Dir)
            B = B & memory[int(dir2.group(1))]
            alu = B
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #AND (Dir)
            memory[int(dir1.group(1))] = A & B
            alu = memory[int(dir1.group(1))]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "OR":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #OR A, B
            A = A | B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #OR A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            A = A | int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #OR A, (Dir)
            A = A | memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #OR A, (B)
            A = A | memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #OR B, A
            B = B | A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #OR B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B = B | int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #OR B, (Dir)
            B = B | memory[int(dir2.group(1))]
            alu = B
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #OR (Dir)
            memory[int(dir1.group(1))] = A | B
            alu = memory[int(dir1.group(1))]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "NOT":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #NOT A, A
            A = ~A
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #NOT A, B
            A = ~B
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #NOT B, A
            B = ~A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #NOT B, B
            B = ~B
            alu = B
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #NOT (Dir), A
            memory[int(dir1.group(1))] = ~A
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #NOT (Dir), B
            memory[int(dir1.group(1))] = ~B
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1) == "B" and len(line) == 2: #NOT (B)
            memory[B] = ~A
            alu = memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "XOR":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #XOR A, B
            A = A ^ B
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #XOR A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            A = A ^ int(line[2])
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #XOR A, (Dir)
            A = A ^ memory[int(dir2.group(1))]
            alu = A
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #XOR A, (B)
            A = A ^ memory[B]
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #XOR B, A
            B = B ^ A
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #XOR B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            B = B ^ int(line[2])
            alu = B
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #XOR B, (Dir)
            B = B ^ memory[int(dir2.group(1))]
            alu = B
        elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #XOR (Dir)
            memory[int(dir1.group(1))] = A ^ B
            alu = memory[int(dir1.group(1))]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "SHL":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHL A, A
            A = A << 1
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHL A, B
            A = B << 1
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHL B, A
            B = A << 1
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHL B, B
            B = B << 1
            alu = B
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHL (Dir), A
            memory[int(dir1.group(1))] = A << 1
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHL (Dir), B
            memory[int(dir1.group(1))] = ~B << 1
            alu = memory[int(dir1.group(1))]
        elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHL (B)
            memory[B] = A << 1
            alu = memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "SHR":
        if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHR A, A
            A = A >> 1
            alu = A
        elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHR A, B
            A = B >> 1
            alu = A
        elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHR B, A
            B = A >> 1
            alu = B
        elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHR B, B
            B = B >> 1
            alu = B
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHR (Dir), A
            memory[int(dir1.group(1))] = A >> 1
            alu = memory[int(dir1.group(1))]
        elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHR (Dir), B
            memory[int(dir1.group(1))] = ~B >> 1
            alu = memory[int(dir1.group(1))]
        elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHR (B)
            memory[B] = A >> 1
            alu = memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "INC":
        if len(line) == 2 and line[1] == "B": #INC B
            B += 1
            alu = B
        elif len(line) == 2 and dir1 and dir1.group(1).isdigit(): #INC (Dir)
            memory[int(dir1.group(1))] += 1
            alu = memory[int(dir1.group(1))]
        elif len(line) == 2 and dir1 and dir1.group(1) == "B": #INC (B)
            memory[B] += 1
            alu = memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
    elif line[0] == "RST":
        if len(line) == 2 and dir1 and dir1.group(1).isdigit(): #RST (Dir)
            memory[int(dir1.group(1))] = 0
        elif len(line) == 2 and dir1 and dir1.group(1) == "B": #RST (B)
            memory[B] = 0
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
        alu = 0
    elif line[0] == "CMP":
        if len(line) == 3 and line[1] == "A" and line[2] == "B": #CMP A, B
            alu = A - B
        elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #CMP A, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            alu = A - int(line[2])
        elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #CMP B, Lit
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
            alu = B - int(line[2])
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #CMP A, Dir
            alu = A - memory[int(dir2.group(1))]
        elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #CMP B, Dir
            alu = B - memory[int(dir2.group(1))]
        elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #CMP A, (B)
            alu = A - memory[B]
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
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
        error = 1
    count += 1

file.close()


if error == 0:
    A = 0
    B = 0
    filename = file_name.strip()
    filename = filename.split(".")
    archivo_out = open(f"{filename[0]}.out", "w")
    j = 0
    while j < len(lines):
        line = lines[j]
        try:
            if int(line[2]) < 0:
                line[2] = str(256 + int(line[2]))
        except:
            pass
        try:
            if int(line[1]) < 0:
                line[1] = str(256 + int(line[1]))
        except:
            pass
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
                A = B
                alu = A
                archivo_out.write("0000000 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #MOV A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A = int(line[2])
                alu = A
                archivo_out.write(f"0000010 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #MOV A, (Dir)
                A = memory[int(dir2.group(1))]
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0100101 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #MOV A, (B)
                A = memory[B]
                alu = A
                archivo_out.write(f"0101011 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #MOV B, A
                B = A
                alu = B
                archivo_out.write(f"0000001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #MOV B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B = int(line[2])
                alu = B
                archivo_out.write(f"0000011 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #MOV B, (Dir)
                B = memory[int(dir2.group(1))]
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0100110 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #MOV B, (B)
                B = memory[B]
                alu = B
                archivo_out.write(f"0101001 00000000")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1) == "B": #MOV B, (B)
                B = memory[B]
                alu = B
                archivo_out.write(f"0101010 00000000")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #MOV (Dir), A
                memory[int(dir1.group(1))] = A
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0100111 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #MOV (Dir), B
                memory[int(dir1.group(1))] = B
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0101000 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1) == "B" and line[2] == "A": #MOV (B), A
                memory[B] = A
                alu = memory[B]
                archivo_out.write(f"0101011 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "ADD":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #ADD A, B
                A += B
                alu = A
                archivo_out.write(f"0000100 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #ADD A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A += int(line[2])
                alu = A
                archivo_out.write(f"0000110 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #ADD A, (Dir)
                A += memory[int(dir2.group(1))]
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0101100 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #ADD A, (B)
                A += memory[B]
                alu = A
                archivo_out.write(f"0101110 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "B": #ADD B, A
                B += A
                alu = B
                archivo_out.write(f"0000101 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #ADD B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B += int(line[2])
                alu = B
                archivo_out.write(f"0000111 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #ADD B, (Dir)
                B += memory[int(dir2.group(1))]
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0101101 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 2 and dir1 and dir1.group(1).isdigit() and len(line) == 2: #ADD (Dir)
                memory[int(dir1.group(1))] = A + B
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0101111 {bin(int(aux))[2:].zfill(8)}")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "SUB":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #SUB A, B
                A -= B
                if A < 0:
                    A = 256 - A
                alu = A
                archivo_out.write(f"0001000 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #SUB A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A -= int(line[2])
                if A < 0:
                    A = 256 + A
                alu = A
                archivo_out.write(f"0001010 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #SUB A, (Dir)
                A -= memory[int(dir2.group(1))]
                if A < 0:
                    A = 256 + A
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0110000 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #SUB A, (B)
                A -= memory[B]
                if A < 0:
                    A = 256 + A
                alu = A
                archivo_out.write(f"0110010 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SUB B, A
                B = A - B
                if B < 0:
                    B = 256 + B
                alu = B
                archivo_out.write(f"0001001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #SUB B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B -= int(line[2])
                if B < 0:
                    B = 256 + B
                alu = B
                archivo_out.write(f"0001011 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #SUB B, (Dir)
                B -= memory[int(dir2.group(1))]
                if B < 0:
                    B = 256 + B
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0110001 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #SUB (Dir)
                memory[int(dir1.group(1))] = A - B
                if memory[int(dir1.group(1))] < 0:
                    memory[int(dir1.group(1))] = 256 - memory[int(dir1.group(1))]
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0110011 {bin(int(aux))[2:].zfill(8)}")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "AND":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #AND A, B
                A = A & B
                alu = A
                archivo_out.write(f"0001100 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #AND A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A = A & int(line[2])
                alu = A
                archivo_out.write(f"00001110 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #AND A, (Dir)
                A = A & memory[int(dir2.group(1))]
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0110100 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #AND A, (B)
                A = A & memory[B]
                alu = A
                archivo_out.write(f"0110110 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #AND B, A
                B = B & A
                alu = B
                archivo_out.write(f"0001101 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #AND B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B = B & int(line[2])
                alu = B
                archivo_out.write(f"0001111 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #AND B, (Dir)
                B = B & memory[int(dir2.group(1))]
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0110101 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #AND (Dir)
                memory[int(dir1.group(1))] = A & B
                alu = memory[int(dir1.group(1))]
                archivo_out.write(f"0110111 {bin(int(line[1]))[2:].zfill(8)}")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "OR":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #OR A, B
                A = A | B
                alu = A
                archivo_out.write(f"0010000 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #OR A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A = A | int(line[2])
                alu = A
                archivo_out.write(f"0010010 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #OR A, (Dir)
                A = A | memory[int(dir2.group(1))]
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0111000 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #OR A, (B)
                A = A | memory[B]
                alu = A
                archivo_out.write(f"0111010 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #OR B, A
                B = B | A
                alu = B
                archivo_out.write(f"0010001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #OR B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B = B | int(line[2])
                alu = B
                archivo_out.write(f"0010011 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #OR B, (Dir)
                B = B | memory[int(dir2.group(1))]
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0111001 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #OR (Dir)
                memory[int(dir1.group(1))] = A | B
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0111011 {bin(int(aux))[2:].zfill(8)}")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "NOT":
            if len(line) == 3 and line[1] == "A" and line[2] == "A": #NOT A, A
                A = ~A
                alu = A
                archivo_out.write(f"0010100 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2] == "B": #NOT A, B
                A = ~B
                alu = A
                archivo_out.write(f"0010101 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #NOT B, A
                B = ~A
                alu = B
                archivo_out.write(f"0010110 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "B": #NOT B, B
                B = ~B
                alu = B
                archivo_out.write(f"0010111 00000000")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #NOT (Dir), A
                memory[int(dir1.group(1))] = ~A
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0111100 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #NOT (Dir), B
                memory[int(dir1.group(1))] = ~B
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"0111101 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1) == "B" and len(line) == 2: #NOT (B)
                memory[B] = ~A
                alu = memory[B]
                archivo_out.write(f"0111110 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "XOR":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #XOR A, B
                A = A ^ B
                alu = A
                archivo_out.write(f"0011000 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #XOR A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                A = A ^ int(line[2])
                alu = A
                archivo_out.write(f"0011010 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #XOR A, (Dir)
                A = A ^ memory[int(dir2.group(1))]
                alu = A
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"011111111 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #XOR A, (B)
                A = A ^ memory[B]
                alu = A
                archivo_out.write(f"1000001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #XOR B, A
                B = B ^ A
                alu = B
                archivo_out.write(f"0011001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #XOR B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                B = B ^ int(line[2])
                alu = B
                archivo_out.write(f"0011011 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #XOR B, (Dir)
                B = B ^ memory[int(dir2.group(1))]
                alu = B
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000000 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1).isdigit() and len(line) == 2: #XOR (Dir)
                memory[int(dir1.group(1))] = A ^ B
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000010 {bin(int(aux))[2:].zfill(8)}")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "SHL":
            if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHL A, A
                A = A << 1
                alu = A
                archivo_out.write(f"0011100 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHL A, B
                A = B << 1
                alu = A
                archivo_out.write(f"0011101 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHL B, A
                B = A << 1
                alu = B
                archivo_out.write(f"0011110 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHL B, B
                B = B << 1
                alu = B
                archivo_out.write(f"0011111 00000000")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHL (Dir), A
                memory[int(dir1.group(1))] = A << 1
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000011 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHL (Dir), B
                memory[int(dir1.group(1))] = ~B << 1
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000100 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHL (B)
                memory[B] = A << 1
                alu = memory[B]
                archivo_out.write(f"1000101 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "SHR":
            if len(line) == 3 and line[1] == "A" and line[2] == "A": #SHR A, A
                A = A >> 1
                alu = A
                archivo_out.write(f"0100000 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2] == "B": #SHR A, B
                A = B >> 1
                alu = A
                archivo_out.write(f"0100001 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "A": #SHR B, A
                B = A >> 1
                alu = B
                archivo_out.write(f"0100010 00000000")
            elif len(line) == 3 and line[1] == "B" and line[2] == "B": #SHR B, B
                B = B >> 1
                alu = B
                archivo_out.write(f"0100011 00000000")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "A": #SHR (Dir), A
                memory[int(dir1.group(1))] = A >> 1
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000110 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and dir1 and dir1.group(1).isdigit() and line[2] == "B": #SHR (Dir), B
                memory[int(dir1.group(1))] = ~B >> 1
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1000111 {bin(int(aux))[2:].zfill(8)}")
            elif dir1 and dir1.group(1) == "B" and len(line) == 2: #SHR (B)
                memory[B] = A >> 1
                alu = memory[B]
                archivo_out.write(f"1001000 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "INC":
            if len(line) == 2 and line[1] == "B": #INC B
                B += 1
                alu = B
                archivo_out.write(f"0100100 00000000")
            elif len(line) == 2 and dir1 and dir1.group(1).isdigit(): #INC (Dir)
                memory[int(dir1.group(1))] += 1
                alu = memory[int(dir1.group(1))]
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1001001 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 2 and dir1 and dir1.group(1) == "B": #INC (B)
                memory[B] += 1
                alu = memory[B]
                archivo_out.write(f"1001010 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif line[0] == "RST":
            if len(line) == 2 and dir1 and dir1.group(1).isdigit(): #RST (Dir)
                memory[int(dir1.group(1))] = 0
                aux = int(dir1.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1001011 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 2 and dir1 and dir1.group(1) == "B": #RST (B)
                memory[B] = 0
                archivo_out.write(f"1001100 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
            alu = 0
        elif line[0] == "CMP":
            if len(line) == 3 and line[1] == "A" and line[2] == "B": #CMP A, B
                alu = A - B
                archivo_out.write(f"1001101 00000000")
            elif len(line) == 3 and line[1] == "A" and line[2].isdigit(): #CMP A, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                alu = A - int(line[2])
                archivo_out.write(f"1001110 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and line[2].isdigit(): #CMP B, Lit
                if int(line[2]) < 0:
                    line[2] = str(256 + int(line[2]))
                alu = B - int(line[2])
                archivo_out.write(f"1001111 {bin(int(line[2]))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1).isdigit(): #CMP A, (Dir)
                alu = A - memory[int(dir2.group(1))]
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1010000 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "B" and dir2 and dir2.group(1).isdigit(): #CMP B, (Dir)
                alu = B - memory[int(dir2.group(1))]
                aux = int(dir2.group(1))
                if aux < 0:
                    aux = 256 + aux
                archivo_out.write(f"1010001 {bin(int(aux))[2:].zfill(8)}")
            elif len(line) == 3 and line[1] == "A" and dir2 and dir2.group(1) == "B": #CMP A, (B)
                alu = A - memory[B]
                archivo_out.write(f"1010010 00000000")
            else:
                print(f"La función '{lineaux[count]}' no existe")
                error = 1
        elif len(line) == 2 and line[0] == "JMP" and ((line[1] in labels) or line[1].isdigit()): #JMP Dir
            if line[1] in labels:
                j = labels[line[1]]
                archivo_out.write(f"1010011 00000000")
            else:
                j = int(line[1]) - 2
                if int(line[1]) < 0:
                    line[1] = str(256 + int(line[1]))
                archivo_out.write(f"1010011 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JEQ" and ((line[1] in labels) or line[1].isdigit()): #JEQ Dir
            if alu == 0:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1010100 00000000")
            else:
                if int(line[1]) < 0:
                        line[1] = str(256 + int(line[1]))
                archivo_out.write(f"1010100 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JNE" and ((line[1] in labels) or line[1].isdigit()): #JNE Dir
            if alu != 0:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1010101 00000000")
            else:
                archivo_out.write(f"1010101 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JGT" and ((line[1] in labels) or line[1].isdigit()): #JGT Dir-------------------------------------
            if alu <= 127 and alu != 0:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1010110 00000000")
            else:
                archivo_out.write(f"1010110 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JLT" and ((line[1] in labels) or line[1].isdigit()): #JLT Dir
            if alu > 127:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1010111 00000000")
            else:
                archivo_out.write(f"1010111 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JGE" and ((line[1] in labels) or line[1].isdigit()): #JGE Dir
            if alu <= 127:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1011000 00000000")
            else:
                archivo_out.write(f"1011000 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JLE" and ((line[1] in labels) or line[1].isdigit()): #JLE Dir
            if alu > 127 or alu == 0:
                if line[1] in labels:
                    j = labels[line[1]]
                else:
                    j = int(line[1]) - 2
            if line[1] in labels:
                archivo_out.write(f"1011001 00000000")
            else:
                archivo_out.write(f"1011001 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JCR" and ((line[1] in labels) or line[1].isdigit()): #JCR Dir
            if line[1] in labels:
                j = labels[line[1]]
            else:
                j = int(line[1]) - 2
            archivo_out.write(f"1011010 {bin(int(line[1]))[2:].zfill(8)}")
        elif len(line) == 2 and line[0] == "JOV" and ((line[1] in labels) or line[1].isdigit()): #JOV Dir
            if line[1] in labels:
                j = labels[line[1]]
            else:
                j = int(line[1]) - 2
            archivo_out.write(f"1011011 {bin(int(line[1]))[2:].zfill(8)}")
        else:
            print(f"La función '{lineaux[count]}' no existe")
            error = 1
        archivo_out.write(f"\n")
        j += 1



    archivo_out.close()