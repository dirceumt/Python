a = 1
b = 2
eq = "a * x + b"  # Substitua esta string pela equação desejada

for x in range(5):
    y = eval(eq)  # Avalie a equação com base nos valores de a, b e x
    print(f"O resultado da equação para x={x} é {y}")

