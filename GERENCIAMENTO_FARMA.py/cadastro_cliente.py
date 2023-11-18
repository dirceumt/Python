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
