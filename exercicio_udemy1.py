nome = input('DIGITE SEU NOME: ')
idade = int(input('DIGITE SUA IDADE: '))
if nome and idade:
    print(f'seu nome e: {nome}')
    print(f'seu nome invertido e: {nome[::-1]}') #fatiamento, nome invertido
else:
    print(f'VOCE NAO DIGITOU NENHUM VALOR!')
if '' in nome:
    print(f'seu nome tem espaço!')
else:
    print(f'seu nome nao tem espaço')
print(f'seu nome tem {len(nome)} letras! ')
print(f'a primeira letra do seu nome e: {nome[0]} \n a ultima do seu nome e: {nome[-1]}')
