import os
import subprocess
import time
import keyboard

# ------->>>> EM PRODUÇAO <--------

# Adiciona o usuário aos grupos "input" e "tty"
def adicionar_aos_grupos():
    try:
        subprocess.run(["sudo", "usermod", "-a", "-G", "input", "$(whoami)"], check=True)
        subprocess.run(["sudo", "usermod", "-a", "-G", "tty", "$(whoami)"], check=True)
        print("Usuário adicionado aos grupos 'input' e 'tty'. Por favor, faça logout e login novamente para que as alterações tenham efeito.")
    except subprocess.CalledProcessError:
        print("Erro ao adicionar o usuário aos grupos. Certifique-se de executar o script com permissões de superusuário (sudo).")

# Caminho para a pasta do seu projeto no VSCode
caminho_projeto = "/home/dirceu/Desktop/EXERCICIOS PYTHON/estudo"

# Função para realizar o versionamento
def fazer_versionamento(nome_arquivo):
    os.chdir(caminho_projeto)
    subprocess.run(["git", "pull", "origin", "main"])
    subprocess.run(["git", "add", nome_arquivo + ".py"])
    subprocess.run(["git", "commit", "-m", f'"{nome_arquivo}"'])
    subprocess.run(["git", "push", "origin", "main"])

# Função para verificar a inatividade
def verificar_inatividade():
    inatividade = True
    while inatividade:
        if keyboard.is_pressed("esc"):  # Verifica se a tecla "esc" foi pressionada
            inatividade = False
        time.sleep(30)  # Espera 30 segundos antes de verificar novamente

# Nome do arquivo que você deseja versionar (sem a extensão .py)
nome_do_arquivo = "nome_do_arquivo"

# Verifica a inatividade, adiciona aos grupos e realiza o versionamento
verificar_inatividade()
adicionar_aos_grupos()
fazer_versionamento(nome_do_arquivo)