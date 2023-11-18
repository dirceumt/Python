def line():
    print('-'*30) #repetir o caractere - 30 vezes
def escreva(texto): #define outra função chamada escreva(texto), que recebe um argumento texto.
    line() #repetir o caractere - 30 vezes
    print(f'{texto:-^30}') #imprime o texto centralizado em uma largura total de 30 caracteres completando com -
    line() #repetir o caractere - 30 vezes
escreva('HELLO WORLD!') #chama a função escreva() com o argumento 'HELLO WORLD!'


