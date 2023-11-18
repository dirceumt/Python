#TESTE 1
def line():
    print('-'*30)

line()
print('TESTE DE DEFINICAO DE FUNCAO')
line()

#TESTE 2

def mensagem(msg):
    line()
    print(msg)
    line()
mensagem('TESTE DE DECLARACAO DE PARAMETROS')

#TESTE 3

def msn (txt):
    line()
    print(txt)
    line()
msn ('TESTE DEFINICAO DE PARAMETRO')
msn ('testando 1,2,3... ')
msn ('boa noite! ZzZ... ')

#TESTE 4

def dobro(lst): # definimos uma função chamada dobro que recebe uma lista lst como parâmetro.
    pos=0 #Inicializamos a variável pos com 0. Esta variável será usada para percorrer a lista.
    while pos < len(lst): #Iniciamos um loop com o while que irá executar enquanto a variável pos for 
        #menor do que o comprimento da lista lst o comando len faz essa checagem de quantidade de numeros 
        # da lista ou seja, enquanto não tivermos percorrido toda a lista.
        lst[pos]*=2 #multiplicamos o valor na posição pos da lista por 2
        pos+=1 #Incrementamos a variável pos em 1 para passar para o próximo elemento da lista na próxima iteração do loop.
val=[100, 200, 300, 400, 500]
dobro(val)
print(val)
