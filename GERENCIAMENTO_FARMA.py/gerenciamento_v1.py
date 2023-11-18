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

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import sqlite3
import re
from datetime import datetime

class Cliente:
    def __init__(self, nome, logradouro, bairro, cidade, cep, telefone, cpf):
        self.nome = nome
        self.logradouro = logradouro
        self.bairro = bairro
        self.cidade = cidade
        self.cep = cep
        self.telefone = telefone
        self.cpf = cpf
        self.historico_compras = []

    def adicionar_compra(self, medicamento, quantidade, valor):
        data_compra = datetime.now().strftime('%d/%m/%Y')
        self.historico_compras.append({
            'medicamento': medicamento,
            'quantidade': quantidade,
            'valor': valor,
            'data_compra': data_compra
        })

class SistemaCadastroClientes:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS clientes (
                nome TEXT PRIMARY KEY,
                logradouro TEXT,
                bairro TEXT,
                cidade TEXT,
                cep TEXT,
                telefone TEXT,
                cpf TEXT
            )
        ''')
        self.conn.commit()

    def cadastrar_cliente(self, nome, logradouro, bairro, cidade, cep, telefone, cpf):
        try:
            self.cursor.execute('INSERT INTO clientes (nome, logradouro, bairro, cidade, cep, telefone, cpf) VALUES (?, ?, ?, ?, ?, ?, ?)', (nome, logradouro, bairro, cidade, cep, telefone, cpf))
            self.conn.commit()
            return True
        except sqlite3.IntegrityError:
            messagebox.showerror("Erro", "Cliente já cadastrado.")
            return False

    def listar_clientes(self):
        self.cursor.execute('SELECT * FROM clientes ORDER BY nome')
        clientes = self.cursor.fetchall()
        return clientes

    def excluir_cliente(self, nome):
        try:
            self.cursor.execute('DELETE FROM clientes WHERE nome = ?', (nome,))
            self.conn.commit()
        except sqlite3.Error:
            pass

    def validar_cliente(self, nome):
        self.cursor.execute('SELECT * FROM clientes WHERE nome = ?', (nome,))
        cliente = self.cursor.fetchone()
        return cliente

    def atualizar_cliente(self, nome, logradouro, bairro, cidade, cep, telefone, cpf):
        try:
            self.cursor.execute('''
                UPDATE clientes
                SET logradouro = ?, bairro = ?, cidade = ?, cep = ?, telefone = ?, cpf = ?
                WHERE nome = ?
            ''', (logradouro, bairro, cidade, cep, telefone, cpf, nome))
            self.conn.commit()
            return True
        except sqlite3.Error:
            pass
        return False

    def fechar_conexao(self):
        self.conn.close()

    @staticmethod
    def formatar_cep(event, limite=8):
        entrada = event.widget.get()
        cep_limpo = ''.join(filter(str.isdigit, entrada))[:limite]

        cep_formatado = ''
        for i, char in enumerate(cep_limpo):
            if i == 4:
                cep_formatado += '-'
            cep_formatado += char

        event.widget.delete(0, tk.END)
        event.widget.insert(0, cep_formatado)

    @staticmethod
    def formatar_telefone(event, limite=11):
        entrada = event.widget.get()
        telefone_limpo = ''.join(filter(str.isdigit, entrada))[:limite]

        telefone_formatado = '('
        for i, char in enumerate(telefone_limpo):
            if i == 2:
                telefone_formatado += ') '
            elif i == 7:
                telefone_formatado += '-'
            telefone_formatado += char

        event.widget.delete(0, tk.END)
        event.widget.insert(0, telefone_formatado)

    @staticmethod
    def formatar_cpf(event, limite=11):
        entrada = event.widget.get()
        cpf_limpo = ''.join(filter(str.isdigit, entrada))[:limite]

        cpf_formatado = ''
        for i, char in enumerate(cpf_limpo):
            if i == 3 or i == 6:
                cpf_formatado += '.'
            elif i == 9:
                cpf_formatado += '-'
            cpf_formatado += char

        event.widget.delete(0, tk.END)
        event.widget.insert(0, cpf_formatado)

class InterfaceGraficaClientes:
    def __init__(self, janela, sistema):
        self.janela = janela
        self.janela.title("Sistema de Cadastro de Clientes")
        self.sistema = sistema

        # Crie um notebook para alternar entre as telas de cadastro e listagem
        self.notebook = ttk.Notebook(self.janela)

        # Tela de cadastro de clientes
        self.tela_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.tela_cadastro, text="Cadastrar Cliente")
        self.criar_interface_cadastro(self.tela_cadastro)

        # Tela de listagem de clientes
        self.tela_listagem = ttk.Frame(self.notebook)
        self.notebook.add(self.tela_listagem, text="Listar Clientes")
        self.criar_interface_listagem(self.tela_listagem)

        self.notebook.pack(expand=1, fill="both")

    def criar_interface_cadastro(self, tela):
        # Elementos da interface para cadastrar clientes
        lbl_nome = ttk.Label(tela, text="Nome:")
        lbl_logradouro = ttk.Label(tela, text="Logradouro:")
        lbl_bairro = ttk.Label(tela, text="Bairro:")
        lbl_cidade = ttk.Label(tela, text="Cidade:")
        lbl_cep = ttk.Label(tela, text="CEP:")
        lbl_telefone = ttk.Label(tela, text="Telefone:")
        lbl_cpf = ttk.Label(tela, text="CPF:")

        self.entry_nome = ttk.Entry(tela)
        self.entry_logradouro = ttk.Entry(tela)
        self.entry_bairro = ttk.Entry(tela)
        self.entry_cidade = ttk.Entry(tela)
        self.entry_cep = ttk.Entry(tela)
        self.entry_telefone = ttk.Entry(tela)
        self.entry_cpf = ttk.Entry(tela)

        btn_cadastrar = ttk.Button(tela, text="Cadastrar", command=self.cadastrar_cliente)

        lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_logradouro.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        lbl_bairro.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        lbl_cidade.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        lbl_cep.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        lbl_telefone.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        lbl_cpf.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        self.entry_logradouro.grid(row=1, column=1, padx=5, pady=5)
        self.entry_bairro.grid(row=2, column=1, padx=5, pady=5)
        self.entry_cidade.grid(row=3, column=1, padx=5, pady=5)
        self.entry_cep.grid(row=4, column=1, padx=5, pady=5)
        self.entry_telefone.grid(row=5, column=1, padx=5, pady=5)
        self.entry_cpf.grid(row=6, column=1, padx=5, pady=5)

        btn_cadastrar.grid(row=7, columnspan=2, pady=10)

        self.entry_cep.bind("<KeyRelease>", lambda event: self.sistema.formatar_cep(event, 8))
        self.entry_telefone.bind("<KeyRelease>", lambda event: self.sistema.formatar_telefone(event, 11))
        self.entry_cpf.bind("<KeyRelease>", lambda event: self.sistema.formatar_cpf(event, 11))

    def criar_interface_listagem(self, tela):
        # Elementos da interface para listar clientes
        lbl_listagem = ttk.Label(tela, text="Clientes Cadastrados:")
        lbl_listagem.grid(row=0, column=0, padx=5, pady=5, columnspan=3)

        self.tree = ttk.Treeview(tela, columns=("Nome", "Logradouro", "Bairro", "Cidade", "CEP", "Telefone", "CPF"))
        self.tree.heading("#1", text="Nome")
        self.tree.heading("#2", text="Logradouro")
        self.tree.heading("#3", text="Bairro")
        self.tree.heading("#4", text="Cidade")
        self.tree.heading("#5", text="CEP")
        self.tree.heading("#6", text="Telefone")
        self.tree.heading("#7", text="CPF")

        self.tree.grid(row=1, column=0, padx=5, pady=5, columnspan=3)

        btn_atualizar = ttk.Button(tela, text="Atualizar", command=self.atualizar_listagem)
        btn_atualizar.grid(row=2, column=0, padx=5, pady=5)

        btn_alterar = ttk.Button(tela, text="Alterar Cliente", command=self.abrir_janela_alterar)
        btn_alterar.grid(row=2, column=1, padx=5, pady=5)

        btn_excluir = ttk.Button(tela, text="Excluir Cliente", command=self.excluir_cliente_selecionado)
        btn_excluir.grid(row=2, column=2, padx=5, pady=5)

    def cadastrar_cliente(self):
        nome = self.entry_nome.get()
        logradouro = self.entry_logradouro.get()
        bairro = self.entry_bairro.get()
        cidade = self.entry_cidade.get()
        cep = self.entry_cep.get()
        telefone = self.entry_telefone.get()
        cpf = self.entry_cpf.get()

        # Verifique se pelo menos o nome foi preenchido
        if not nome:
            messagebox.showerror("Erro", "O campo 'Nome' deve ser preenchido.")
            return

        if self.sistema.cadastrar_cliente(nome, logradouro, bairro, cidade, cep, telefone, cpf):
            messagebox.showinfo("Cadastro de Cliente", "Cliente cadastrado com sucesso!")
            self.limpar_campos_cadastro()
            self.atualizar_listagem()
        else:
            messagebox.showerror("Erro", "Erro ao cadastrar cliente.")

    def limpar_campos_cadastro(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_logradouro.delete(0, tk.END)
        self.entry_bairro.delete(0, tk.END)
        self.entry_cidade.delete(0, tk.END)
        self.entry_cep.delete(0, tk.END)
        self.entry_telefone.delete(0, tk.END)
        self.entry_cpf.delete(0, tk.END)

    def atualizar_listagem(self):
        clientes = self.sistema.listar_clientes()
        self.tree.delete(*self.tree.get_children())
        for cliente in clientes:
            self.tree.insert("", "end", values=cliente)

    def excluir_cliente_selecionado(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            nome_cliente = self.tree.item(item_selecionado, "values")[0]
            resultado = messagebox.askquestion("Exclusão de Cliente", "Deseja excluir o cliente selecionado?")
            if resultado == "yes":
                self.sistema.excluir_cliente(nome_cliente)
                self.atualizar_listagem()
        else:
            messagebox.showerror("Erro", "Selecione um cliente para excluir.")

    def abrir_janela_alterar(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            nome_cliente = self.tree.item(item_selecionado, "values")[0]
            cliente = self.sistema.validar_cliente(nome_cliente)
            if cliente:
                janela_alterar = tk.Toplevel(self.janela)
                janela_alterar.title("Alterar Dados do Cliente")
                self.criar_interface_alterar(janela_alterar, cliente)
            else:
                messagebox.showerror("Erro", "Cliente não encontrado.")
        else:
            messagebox.showerror("Erro", "Selecione um cliente para alterar.")

    def criar_interface_alterar(self, janela, cliente):
        # Elementos da interface para alterar cliente
        lbl_nome = ttk.Label(janela, text="Nome:")
        lbl_logradouro = ttk.Label(janela, text="Logradouro:")
        lbl_bairro = ttk.Label(janela, text="Bairro:")
        lbl_cidade = ttk.Label(janela, text="Cidade:")
        lbl_cep = ttk.Label(janela, text="CEP:")
        lbl_telefone = ttk.Label(janela, text="Telefone:")
        lbl_cpf = ttk.Label(janela, text="CPF:")

        entry_nome = ttk.Entry(janela)
        entry_nome.insert(0, cliente[0])  # Preencha o nome atual

        entry_logradouro = ttk.Entry(janela)
        entry_logradouro.insert(0, cliente[1])  # Preencha o logradouro atual

        entry_bairro = ttk.Entry(janela)
        entry_bairro.insert(0, cliente[2])  # Preencha o bairro atual

        entry_cidade = ttk.Entry(janela)
        entry_cidade.insert(0, cliente[3])  # Preencha a cidade atual

        entry_cep = ttk.Entry(janela)
        entry_cep.insert(0, cliente[4])  # Preencha o CEP atual

        entry_telefone = ttk.Entry(janela)
        entry_telefone.insert(0, cliente[5])  # Preencha o telefone atual

        entry_cpf = ttk.Entry(janela)
        entry_cpf.insert(0, cliente[6])  # Preencha o CPF atual

        btn_salvar = ttk.Button(janela, text="Salvar", command=lambda: self.salvar_alteracoes(cliente[0], entry_nome.get(), entry_logradouro.get(), entry_bairro.get(), entry_cidade.get(), entry_cep.get(), entry_telefone.get(), entry_cpf.get(), janela))

        lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_logradouro.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        lbl_bairro.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        lbl_cidade.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        lbl_cep.grid(row=4, column=0, padx=5, pady=5, sticky="e")
        lbl_telefone.grid(row=5, column=0, padx=5, pady=5, sticky="e")
        lbl_cpf.grid(row=6, column=0, padx=5, pady=5, sticky="e")

        entry_nome.grid(row=0, column=1, padx=5, pady=5)
        entry_logradouro.grid(row=1, column=1, padx=5, pady=5)
        entry_bairro.grid(row=2, column=1, padx=5, pady=5)
        entry_cidade.grid(row=3, column=1, padx=5, pady=5)
        entry_cep.grid(row=4, column=1, padx=5, pady=5)
        entry_telefone.grid(row=5, column=1, padx=5, pady=5)
        entry_cpf.grid(row=6, column=1, padx=5, pady=5)

        btn_salvar.grid(row=7, columnspan=2, pady=10)

        entry_cep.bind("<KeyRelease>", lambda event: self.sistema.formatar_cep(event, 8))
        entry_telefone.bind("<KeyRelease>", lambda event: self.sistema.formatar_telefone(event, 11))
        entry_cpf.bind("<KeyRelease>", lambda event: self.sistema.formatar_cpf(event, 11))

    def salvar_alteracoes(self, nome_antigo, nome, logradouro, bairro, cidade, cep, telefone, cpf, janela):
        if nome:
            if self.sistema.atualizar_cliente(nome_antigo, nome, logradouro, bairro, cidade, cep, telefone, cpf):
                messagebox.showinfo("Alteração de Cliente", "Dados do cliente alterados com sucesso!")
                self.atualizar_listagem()
                janela.destroy()
            else:
                messagebox.showerror("Erro", "Erro ao alterar dados do cliente.")
        else:
            messagebox.showerror("Erro", "O campo 'Nome' deve ser preenchido.")

def main():
    database_name = "clientes.db"
    sistema = SistemaCadastroClientes(database_name)

    janela = tk.Tk()
    app = InterfaceGraficaClientes(janela, sistema)
    janela.mainloop()

if __name__ == "__main__":
    main()

import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from datetime import datetime
import sqlite3

class Produto:
    def __init__(self, codigo, nome, descricao, preco, quantidade_estoque, data_validade):
        self.codigo = codigo
        self.nome = nome
        self.descricao = descricao
        self.preco = preco
        self.quantidade_estoque = quantidade_estoque
        self.data_validade = data_validade

class SistemaCadastroProdutos:
    def __init__(self, database_name):
        self.conn = sqlite3.connect(database_name)
        self.cursor = self.conn.cursor()
        self.cursor.execute('''
            CREATE TABLE IF NOT EXISTS produtos (
                codigo INTEGER PRIMARY KEY,
                nome TEXT,
                descricao TEXT,
                preco REAL,
                quantidade_estoque INTEGER,
                data_validade TEXT
            )
        ''')
        self.conn.commit()

    def cadastrar_produto(self, nome, descricao, preco, quantidade_estoque, data_validade):
        if self.validar_data(data_validade):
            try:
                preco = float(preco)
                quantidade_estoque = int(quantidade_estoque)
                self.cursor.execute('''
                    INSERT INTO produtos (nome, descricao, preco, quantidade_estoque, data_validade)
                    VALUES (?, ?, ?, ?, ?)
                ''', (nome, descricao, preco, quantidade_estoque, data_validade))
                self.conn.commit()
                return True
            except ValueError:
                pass
        return False

    def listar_produtos(self):
        self.cursor.execute('SELECT * FROM produtos ORDER BY nome')
        produtos = self.cursor.fetchall()
        return produtos

    def buscar_produto(self, nome_produto):
        self.cursor.execute('SELECT * FROM produtos WHERE nome LIKE ?', ('%' + nome_produto + '%',))
        produtos = self.cursor.fetchall()
        return produtos

    def buscar_produto_por_codigo(self, codigo):
        self.cursor.execute('SELECT * FROM produtos WHERE codigo = ?', (codigo,))
        produto = self.cursor.fetchone()
        return produto

    def excluir_produto(self, codigo):
        try:
            self.cursor.execute('DELETE FROM produtos WHERE codigo = ?', (codigo,))
            self.conn.commit()
        except sqlite3.Error:
            pass

    def atualizar_produto(self, codigo, nome, descricao, preco, quantidade_estoque, data_validade):
        try:
            preco = float(preco)
            quantidade_estoque = int(quantidade_estoque)
            if self.validar_data(data_validade):
                self.cursor.execute('''
                    UPDATE produtos
                    SET nome = ?, descricao = ?, preco = ?, quantidade_estoque = ?, data_validade = ?
                    WHERE codigo = ?
                ''', (nome, descricao, preco, quantidade_estoque, data_validade, codigo))
                self.conn.commit()
                return True
        except (ValueError, sqlite3.Error):
            pass
        return False

    def validar_data(self, data):
        try:
            datetime.strptime(data, '%d/%m/%Y')
            return True
        except ValueError:
            return False

    def fechar_conexao(self):
        self.conn.close()

class InterfaceGrafica:
    def __init__(self, janela, sistema):
        self.janela = janela
        self.janela.title("Sistema de Cadastro de Produtos")
        self.sistema = sistema

        # Crie um notebook para alternar entre as telas de cadastro, listagem e busca
        self.notebook = ttk.Notebook(self.janela)

        # Tela de cadastro
        self.tela_cadastro = ttk.Frame(self.notebook)
        self.notebook.add(self.tela_cadastro, text="Cadastrar Produto")
        self.criar_interface_cadastro(self.tela_cadastro)

        # Tela de listagem
        self.tela_listagem = ttk.Frame(self.notebook)
        self.notebook.add(self.tela_listagem, text="Listar Produtos")
        self.criar_interface_listagem(self.tela_listagem)

        self.notebook.pack(expand=1, fill="both")

    def criar_interface_cadastro(self, tela):
        # Elementos da interface para cadastrar produtos
        lbl_nome = ttk.Label(tela, text="Nome:")
        lbl_descricao = ttk.Label(tela, text="Descrição:")
        lbl_preco = ttk.Label(tela, text="Preço:")
        lbl_estoque = ttk.Label(tela, text="Quantidade em Estoque:")
        lbl_validade = ttk.Label(tela, text="Data de Validade (DD/MM/AAAA):")

        self.entry_nome = ttk.Entry(tela)
        self.entry_descricao = ttk.Entry(tela)
        self.entry_preco = ttk.Entry(tela)
        self.entry_estoque = ttk.Entry(tela)
        self.entry_validade = ttk.Entry(tela)

        btn_cadastrar = ttk.Button(tela, text="Cadastrar", command=self.cadastrar_produto)

        lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
        lbl_descricao.grid(row=1, column=0, padx=5, pady=5, sticky="e")
        lbl_preco.grid(row=2, column=0, padx=5, pady=5, sticky="e")
        lbl_estoque.grid(row=3, column=0, padx=5, pady=5, sticky="e")
        lbl_validade.grid(row=4, column=0, padx=5, pady=5, sticky="e")

        self.entry_nome.grid(row=0, column=1, padx=5, pady=5)
        self.entry_descricao.grid(row=1, column=1, padx=5, pady=5)
        self.entry_preco.grid(row=2, column=1, padx=5, pady=5)
        self.entry_estoque.grid(row=3, column=1, padx=5, pady=5)
        self.entry_validade.grid(row=4, column=1, padx=5, pady=5)

        btn_cadastrar.grid(row=5, columnspan=2, pady=10)

    def criar_interface_listagem(self, tela):
        # Elementos da interface para listar produtos
        lbl_listagem = ttk.Label(tela, text="Produtos Cadastrados:")
        lbl_listagem.grid(row=0, column=0, padx=5, pady=5, columnspan=2)

        self.tree = ttk.Treeview(tela, columns=("Código", "Nome", "Descrição", "Preço", "Estoque", "Validade"))
        self.tree.heading("#1", text="Código")
        self.tree.heading("#2", text="Nome")
        self.tree.heading("#3", text="Descrição")
        self.tree.heading("#4", text="Preço")
        self.tree.heading("#5", text="Estoque")
        self.tree.heading("#6", text="Validade")

        self.tree.grid(row=1, column=0, padx=5, pady=5, columnspan=2)

        btn_atualizar = ttk.Button(tela, text="Atualizar", command=self.atualizar_listagem)
        btn_atualizar.grid(row=2, column=0, padx=5, pady=5, columnspan=2)

        btn_excluir = ttk.Button(tela, text="Excluir Produto", command=self.excluir_produto_selecionado)
        btn_excluir.grid(row=3, column=0, padx=5, pady=5)

        btn_alterar = ttk.Button(tela, text="Alterar Produto", command=self.alterar_produto_selecionado)
        btn_alterar.grid(row=3, column=1, padx=5, pady=5)

    def cadastrar_produto(self):
        nome = self.entry_nome.get()
        descricao = self.entry_descricao.get()
        preco = self.entry_preco.get()
        estoque = self.entry_estoque.get()
        validade = self.entry_validade.get()

        # Verifique se os campos não estão vazios
        if not nome or not descricao or not preco or not estoque or not validade:
            messagebox.showerror("Erro", "Todos os campos devem ser preenchidos.")
            return

        try:
            preco = float(preco)
            estoque = int(estoque)
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos.")
            return

        if '/' not in validade:
            messagebox.showerror("Erro", "A data de validade deve estar no formato DD/MM/AAAA.")
            return

        if self.sistema.cadastrar_produto(nome, descricao, preco, estoque, validade):
            messagebox.showinfo("Cadastro de Produto", "Produto cadastrado com sucesso!")
            self.limpar_campos_cadastro()
        else:
            messagebox.showerror("Erro", "Data de validade inválida. Use o formato DD/MM/AAAA.")

    def limpar_campos_cadastro(self):
        self.entry_nome.delete(0, tk.END)
        self.entry_descricao.delete(0, tk.END)
        self.entry_preco.delete(0, tk.END)
        self.entry_estoque.delete(0, tk.END)
        self.entry_validade.delete(0, tk.END)

    def atualizar_listagem(self):
        produtos = self.sistema.listar_produtos()
        self.tree.delete(*self.tree.get_children())
        for produto in produtos:
            self.tree.insert("", "end", values=produto)

    def excluir_produto_selecionado(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            codigo_produto = self.tree.item(item_selecionado, "values")[0]
            resultado = messagebox.askquestion("Exclusão de Produto", "Deseja excluir o item selecionado?")
            if resultado == "yes":
                self.sistema.excluir_produto(codigo_produto)
                self.atualizar_listagem()  # Atualize a lista após a exclusão
        else:
            messagebox.showerror("Erro", "Selecione um produto para excluir.")

    def alterar_produto_selecionado(self):
        item_selecionado = self.tree.selection()
        if item_selecionado:
            codigo_produto = self.tree.item(item_selecionado, "values")[0]
            resultado = messagebox.askquestion("Alteração de Produto", "Deseja alterar o item selecionado?")
            if resultado == "yes":
                self.janela_alteracao = tk.Toplevel(self.janela)
                self.janela_alteracao.title("Alterar Produto")
                self.criar_interface_alteracao(codigo_produto)
        else:
            messagebox.showerror("Erro", "Selecione um produto para alterar.")

    def criar_interface_alteracao(self, codigo_produto):
        produto = self.sistema.buscar_produto_por_codigo(codigo_produto)
        if produto:
            lbl_nome = ttk.Label(self.janela_alteracao, text="Nome:")
            lbl_descricao = ttk.Label(self.janela_alteracao, text="Descrição:")
            lbl_preco = ttk.Label(self.janela_alteracao, text="Preço:")
            lbl_estoque = ttk.Label(self.janela_alteracao, text="Quantidade em Estoque:")
            lbl_validade = ttk.Label(self.janela_alteracao, text="Data de Validade (DD/MM/AAAA):")

            entry_nome = ttk.Entry(self.janela_alteracao)
            entry_descricao = ttk.Entry(self.janela_alteracao)
            entry_preco = ttk.Entry(self.janela_alteracao)
            entry_estoque = ttk.Entry(self.janela_alteracao)
            entry_validade = ttk.Entry(self.janela_alteracao)

            btn_salvar = ttk.Button(self.janela_alteracao, text="Salvar Alterações", command=lambda: self.salvar_alteracoes(codigo_produto, entry_nome.get(), entry_descricao.get(), entry_preco.get(), entry_estoque.get(), entry_validade.get()))

            lbl_nome.grid(row=0, column=0, padx=5, pady=5, sticky="e")
            lbl_descricao.grid(row=1, column=0, padx=5, pady=5, sticky="e")
            lbl_preco.grid(row=2, column=0, padx=5, pady=5, sticky="e")
            lbl_estoque.grid(row=3, column=0, padx=5, pady=5, sticky="e")
            lbl_validade.grid(row=4, column=0, padx=5, pady=5, sticky="e")

            entry_nome.grid(row=0, column=1, padx=5, pady=5)
            entry_descricao.grid(row=1, column=1, padx=5, pady=5)
            entry_preco.grid(row=2, column=1, padx=5, pady=5)
            entry_estoque.grid(row=3, column=1, padx=5, pady=5)
            entry_validade.grid(row=4, column=1, padx=5, pady=5)

            btn_salvar.grid(row=5, columnspan=2, pady=10)

            # Preencha os campos com os valores atuais
            entry_nome.insert(0, produto[1])
            entry_descricao.insert(0, produto[2])
            entry_preco.insert(0, produto[3])
            entry_estoque.insert(0, produto[4])
            entry_validade.insert(0, produto[5])
        else:
            messagebox.showerror("Erro", "Produto não encontrado.")

    def salvar_alteracoes(self, codigo, nome, descricao, preco, estoque, validade):
        try:
            preco = float(preco)
            estoque = int(estoque)
            if '/' not in validade:
                validade = f"{validade[:2]}/{validade[2:4]}/{validade[4:]}"
            if self.sistema.validar_data(validade):
                if self.sistema.atualizar_produto(codigo, nome, descricao, preco, estoque, validade):
                    messagebox.showinfo("Alteração de Produto", "Produto alterado com sucesso!")
                    self.janela_alteracao.destroy()
                    self.atualizar_listagem()
                else:
                    messagebox.showerror("Erro", "Erro ao salvar alterações.")
            else:
                messagebox.showerror("Erro", "Data de validade inválida. Use o formato DD/MM/AAAA.")
        except ValueError:
            messagebox.showerror("Erro", "Preço e estoque devem ser números válidos.")

    def abrir_busca_produto(self):
        self.entry_busca.focus()

def main():
    database_name = "estoque.db"
    sistema = SistemaCadastroProdutos(database_name)

    janela = tk.Tk()
    app = InterfaceGrafica(janela, sistema)
    janela.mainloop()

if __name__ == "__main__":
    main()
