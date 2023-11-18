import tkinter as tk
from tkinter import ttk, messagebox, simpledialog
import sqlite3
from cryptography.fernet import Fernet

# Gere uma chave de criptografia para proteger as senhas
chave = Fernet.generate_key()
fernet = Fernet(chave)

# Função para criptografar senhas
def criptografar_senha(senha):
    return fernet.encrypt(senha.encode()).decode()

# Função para descriptografar senhas
def descriptografar_senha(senha_cifrada):
    return fernet.decrypt(senha_cifrada.encode()).decode()

class InterfaceLogin:
    def __init__(self, janela):
        self.janela = janela
        self.janela.title("Login")
        self.usuario_atual = None  # Armazena o nome de usuário logado

        # Configuração do banco de dados criptografado
        self.conexao = sqlite3.connect("usuarios.db")
        self.cursor = self.conexao.cursor()
        self.criar_tabela_usuarios()

        # Interface de login
        self.criar_interface_login()

    def criar_tabela_usuarios(self):
        # Crie a tabela de usuários (se não existir)
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS usuarios (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                nome TEXT,
                login TEXT UNIQUE,
                senha TEXT,
                tipo_usuario TEXT
            )
        ''')
        self.conexao.commit()

    def criar_interface_login(self):
        # Elementos da interface de login
        lbl_login = ttk.Label(self.janela, text="Login:")
        lbl_senha = ttk.Label(self.janela, text="Senha:")

        self.entry_login = ttk.Entry(self.janela)
        self.entry_senha = ttk.Entry(self.janela, show="*")

        btn_entrar = ttk.Button(self.janela, text="Entrar", command=self.efetuar_login)
        btn_cadastrar = ttk.Button(self.janela, text="Cadastrar Usuário", command=self.abrir_janela_cadastro)

        lbl_login.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_senha.grid(row=1, column=0, padx=5, pady=5, sticky="e")

        self.entry_login.grid(row=0, column=1, padx=5, pady=5)
        self.entry_senha.grid(row=1, column=1, padx=5, pady=5)

        btn_entrar.grid(row=2, column=0, padx=5, pady=5)
        btn_cadastrar.grid(row=2, column=1, padx=5, pady=5)

    def abrir_janela_cadastro(self):
        # Solicitar senha da master account para cadastrar administrador
        master_password = simpledialog.askstring("Master Account", "Digite a senha da Master Account para continuar:")

        if master_password == "senha123":
            janela_cadastro = tk.Toplevel(self.janela)
            janela_cadastro.title("Cadastro de Usuário")

            lbl_nome = ttk.Label(janela_cadastro, text="Nome:")
            lbl_novo_login = ttk.Label(janela_cadastro, text="Novo Login:")
            lbl_nova_senha = ttk.Label(janela_cadastro, text="Nova Senha:")
            lbl_repetir_senha = ttk.Label(janela_cadastro, text="Repetir Senha:")
            lbl_tipo_usuario = ttk.Label(janela_cadastro, text="Tipo de Usuário:")

            self.entry_nome = ttk.Entry(janela_cadastro)
            self.entry_novo_login = ttk.Entry(janela_cadastro)
            self.entry_nova_senha = ttk.Entry(janela_cadastro, show="*")
            self.entry_repetir_senha = ttk.Entry(janela_cadastro, show="*")

            # Variável para armazenar o tipo de usuário selecionado
            self.tipo_usuario = tk.StringVar()
            self.tipo_usuario.set("convidado")  # Valor padrão

            # Opções de tipo de usuário
            rbtn_admin = ttk.Radiobutton(janela_cadastro, text="Admin", variable=self.tipo_usuario, value="admin")
            rbtn_convidado = ttk.Radiobutton(janela_cadastro, text="Convidado", variable=self.tipo_usuario, value="convidado")

            btn_salvar = ttk.Button(janela_cadastro, text="Salvar", command=lambda: self.salvar_cadastro(master_password))

            lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
            lbl_novo_login.grid(row=1, column=0, padx=5, pady=5, sticky="e")
            lbl_nova_senha.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            lbl_repetir_senha.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            lbl_tipo_usuario.grid(row=4, column=0, padx=5, pady=5, sticky="e")

            self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
            self.entry_novo_login.grid(row=1, column=1, padx=5, pady=5)
            self.entry_nova_senha.grid(row=2, column=1, padx=5, pady=5)
            self.entry_repetir_senha.grid(row=3, column=1, padx=5, pady=5)

            rbtn_admin.grid(row=4, column=1, padx=5, pady=5)
            rbtn_convidado.grid(row=4, column=2, padx=5, pady=5)

            btn_salvar.grid(row=5, columnspan=2, pady=10)
        else:
            messagebox.showerror("Erro", "Senha da Master Account incorreta.")

    def salvar_cadastro(self, master_password):
        nome = self.entry_nome.get()
        novo_login = self.entry_novo_login.get()
        nova_senha = self.entry_nova_senha.get()
        repetir_senha = self.entry_repetir_senha.get()
        tipo_usuario = self.tipo_usuario.get()

        # Verifica se as senhas são iguais
        if nova_senha == repetir_senha:
            # Criptografa a senha antes de salvar
            senha_cifrada = criptografar_senha(nova_senha)

            # Salva o novo usuário no banco de dados
            self.cursor.execute('''
                INSERT INTO usuarios (nome, login, senha, tipo_usuario)
                VALUES (?, ?, ?, ?)
            ''', (nome, novo_login, senha_cifrada, tipo_usuario))
            self.conexao.commit()

            messagebox.showinfo("Sucesso", "Cadastro realizado com sucesso!", parent=self.janela)
        else:
            messagebox.showerror("Erro", "As senhas digitadas não são iguais.")

    def efetuar_login(self):
        # Implemente a lógica de login aqui
        # Simulando um login bem-sucedido para exibir a mensagem
        messagebox.showinfo("Sucesso", "Login realizado com sucesso!", parent=self.janela)

def main():
    janela = tk.Tk()
    app = InterfaceLogin(janela)                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                                            
    janela.mainloop()

if __name__ == "__main__":
    main()
