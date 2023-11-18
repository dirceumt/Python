num = [float(input('DIGITE O PRIMEIRO NUMERO: ')), float(input('DIGITE O SEGUNDO NUMERO: ')), float(input('DIGITE O TERCEIRO NUMERO: '))]
cre = sorted(num) # a funçao sorted poe os numeros em ordem crescente
decre = sorted(num, reverse=True) #o reverse=true poe em ordem decrescente
print(f'SEUS NUMEROS EM ORDEM CRESCENTE SAO: {cre}')
print(f'SEUS NUMEROS EM ORDEM DECRESCENTE SAO: {decre}')