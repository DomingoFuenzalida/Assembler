a = "-2"
if int(a) < 0:
    a = str(256 + int(a))
b = bin(int(a))[2:].zfill(8)

print(b)