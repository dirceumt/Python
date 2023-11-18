while True:

    velocidade = int(input('QUAL A VELOCIDADE DO CARRO AO PASSAR DO RADAR 1? '))

    RADAR_1 = 100 #velocidade maxima no radar 1
    RADAR_RANGE = 1 #distancia que o radar pega

    if velocidade >= (RADAR_1 + RADAR_RANGE):
        print(f'>>>>> {velocidade} <<<<< \n VOCE EXCEDEU O LIMITE PERMITIDO! \n >>>>> CARRO MULTADO!!! <<<<< ')

    else:
        print(f'>>>>> {velocidade} <<<<< \n VELOCIDADE DENTRO DO LIMITE PERMITIDO! ')
        