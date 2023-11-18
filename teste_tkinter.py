import tkinter as tk

def formatar_cpf(event):
    entrada = cpf_entry.get()
    cpf_limpo = ''.join(filter(str.isdigit, entrada))

    cpf_formatado = ''
    for i, char in enumerate(cpf_limpo):
        if i == 3 or i == 6:
            cpf_formatado += '.'
        elif i == 9:
            cpf_formatado += '-'
        cpf_formatado += char
    
    cpf_entry.delete(0, tk.END)
    cpf_entry.insert(0, cpf_formatado)

app = tk.Tk()
app.title("Cadastro de CPF")

cpf_label = tk.Label(app, text="CPF:")
cpf_label.pack(padx=10, pady=5)

cpf_entry = tk.Entry(app, font=("Arial", 12))
cpf_entry.pack(padx=10, pady=5)

cpf_entry.bind("<KeyRelease>", formatar_cpf)

app.mainloop()
