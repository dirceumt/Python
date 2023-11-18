while True:

    try:
        hora = int(input('QUE HORAS SAO? '))
        if hora >= 0 and hora <= 11:
            print('BOM DIA! ')
        elif hora >= 12 and hora <= 17:
           print('BOA TARDE! ')
        elif hora >= 18 and hora <= 23:
            print('BOA NOITE! ZzZ...')
        else:
            print('DIGITE UM VALOR ENTRE 0 E 23H')
    except ValueError:
        print('ENTRADA INVALIDA, POR FAVOR DIGITE UM NUMERO VALIDO! ')
