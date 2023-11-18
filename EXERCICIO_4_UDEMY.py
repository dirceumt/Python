while True:

    nome = input('DIGITE SEU NOME: ')
    tamanho = len(nome)
    if 1<= tamanho <= 4:
        print('SEU NOME E CURTO! ')
    elif 1 <= tamanho >= 5:
            print('SEU NOME E NORMAL!')
    elif tamanho > 6:
        print('SEU NOME E GRANDE! ')
    else:
        print('DIGITE PELOMENOS UMA LETRA! ')
