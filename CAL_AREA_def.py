#SEM DEF
def line():
    print('-'*30)
line()
print('- CALCULO DA AREA DE TERRENOS -')
line()
l = float(input('INFORME A LARGURA DO TERRENO: '))
c = float(input('INFORME O COMPRIMENTO DO TERRENO: '))
resu = l*c
print(f'A AREA DO SEU TERRENO E: {resu} m2')


#COM DEF
line()
print('CALCULO DA AREA DE TERRENOS_v2')
line()
def area(c,l):
    a = l * c
    print(f'INFORMAÇOES DO SEU TERRENO: \n -> COMPRIMENTO: {c} METROS\n -> LARGURA: {l} METROS\n -> AREA: {a} m2')
l = float(input('INFORME A LARGURA E (M): '))
c = float(input('INFORME O COMPRIMENTO EM (M): '))
area(l,c)
