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
