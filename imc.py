def line():  # cria a função line que repete '-' 30 vezes
    print('-' * 30)


while True: #cria um loop que irá rodar até a condição ser falsa
    line()
    print(f'CALCULADORA DE IMC'.center(30, '-')) #titulo do programa centralizado e com '-' ao redor
    line()
    print()
    print()
    peso = float(input('INFORME SEU PESO (KG): ')) #imprime a mesagem na tela tolicitando o peso e lê a resposta
    alt = float(input('INFORME SUA ALTURA (M): ')) #imprime a mesagem na tela tolicitando o a altura e lê a resposta
    imc = peso / alt ** 2 #define a variável imc que receve o valor da divisão do peso pela altura ao quadrado
    if imc < 18.5: # o bloco if das linhas 14 a 27 são condicionais que imprimirão algumas mensagens específicas
        # de acordo com o valor do resultado do imc
        line()
        print(f'SEU IMC É {imc:.2f}\n VOCÊ ESTÁ COM BAIXO PESO! ')
        line()
    elif 18.5 <= imc <= 24.9:
        line()
        print(f'SEU IMC FOI DE {imc:.2f} \n SEU PESO ESTÁ DENTRO DA NORMALIDADE! ')
        line()
    elif 25 <= imc <= 29.9:
        print(f'SEU IMC É DE {imc:.2f} \n VOCê ESTÁ ACIMA DO PESO! ')
    else:
        line()
        print(f'SEU IMC É {imc:.2f} \n VOCÊ ESTÁ OBESO!')
        line()
    continuar = input('VOCê DESEJA CALCULAR OUTRO IMC? [S] ou [N] ') #define a variável continuar e solicita ao usuário
    # uma str s ou n
    if continuar.lower() != 's': #converte a str S ou N em minusculo, independe se for S, s N ou n, ele converte o
        # maiusculo em minusculo e o minusculo permanece minusculo, gerando assim uma condição verdadeira em ambos os
        #os casos, no caso o programa consinua por conta do continue a baixo.
        continue
    elif continuar.lower() != 'n': #condição idêntica a anterior so que dessa vez se a entrada for n o codigo para
        #por conta do programa break.
        line()
        print('SAINDO DO PROGRAMA...')
        line()
        break
    else:
        print('CARACTERE INVÁLIDO, POR FAVOR DIGITE S OU N! ') #se o usuario digitar qualquer coisa inválida aparece
        #essa mensagem.

    # DIRCEU MACIEL TORRES
    # RA: 3687615201
