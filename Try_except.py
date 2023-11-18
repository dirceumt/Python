while True: #CRIA UM LOOP INFINITO QUE SO PARA QUANDO UMA CONDICAO E ATENDIDA

    try:
        n1 = int(input('INFORME UM NUMERO INTEIRO: \n DIGITE 0 SE DESEJA SAIR DO PROGRAMA'))
        if n1 == 0: #CONDICAO PARA A PARADA DO LOOP
            print(f'VOCE DIGITOU {n1}, SAINDO DO PROGRAMA...')
            break #SE A CONDICAO FOR ATENDIDA O PROGRAMA PARA AQUI
        resultado = 10 / n1
        print(f'Resultado: {resultado}')
    except ZeroDivisionError: #IMPRIME A MENSAGEM SE TENTAR DIVIDIR POR 0
        print('Erro: Divisão por zero não permitida.')
    except ValueError: #IMPRIME QUANDO A STR INFORMADA NAO PODE SER CONVERTIDA NA VAR DECLARADA
        print('Erro: Você deve inserir um número válido.')
    except Exception as e:
        print(f'Erro inesperado: {e}')