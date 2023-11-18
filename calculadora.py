while True:
    print('------------------------')
    print('----->CALCULADORA <-----')
    print('------------------------')
    
    n1 = float(input('DIGITE UM NUMERO: '))
    n2 = float(input('DIGITE OUTRO NUMERO: '))
    op = input('QUAL A OPERACAO (+, -, *, /): ')
    
    if op == '+':
        resultado = n1 + n2
    elif op == '-':
        resultado = n1 - n2
    elif op == '*':
        resultado = n1 * n2
    elif op == '/':
        if n2 != 0:  
            resultado = n1 / n2
        else:
            print('ERRO: Divisão por zero!')
            continue 
    else:
        print('OPERADOR INVALIDO!')
        continue 
    
    print(f'RESULTADO: {resultado:.2f}')
    
    sair = input('DESEJA SAIR? [s] sim ou [n] NAO: ').lower()
    if sair == 's':
        break
    else:
        continue






