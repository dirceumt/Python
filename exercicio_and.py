line = '=' * 40
message = 'TERMINAL DE LIBERAÇÃO DE ENTRADA'
print(line)
print(f'===={message}====')
print(line)
user = input('DIGITE SEU LOGUIN: ')
senha = input('digite sua senha :')
user_salvo = 'dirceu'
senha_salva = '123'
if senha == senha_salva and user_salvo==user:
    print('ACESSO LIBERADO!')
else:
    print('ACESSO NEGADO!!!')