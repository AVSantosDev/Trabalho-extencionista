from tkinter import *

from tkinter import messagebox
import json
import os


co0 = "#f0f3f5"  # Preta / black
co1 = "#feffff"  # branca / white
co2 = "#3fb5a3"  # verde / green
co3 = "#38576b"  # valor / value
co4 = "#403d3d"   # letra / letters


# Criando janela de login
janela = Tk()
janela.title('')
janela.geometry('310x400')
janela.configure(background=co1)
janela.resizable(width=FALSE, height=FALSE)


# dividindo janela

frame_cima = Frame(janela, width=310, height=50, bg=co1, relief='flat')
frame_cima.grid(row=0, column=0, pady=1, padx=0, sticky=NSEW)

frame_baixo = Frame(janela, width=310, height=300, bg=co1, relief='flat')
frame_baixo.grid(row=1, column=0, pady=1, padx=0, sticky=NSEW)

# Configurando frame cimna

l_nome = Label(frame_cima, text='LOGIN', anchor=NE,
               font=('Ivy 25'), bg=co1, fg=co4)
l_nome.place(x=5, y=5)

l_linha = Label(frame_cima, text='', width=275,
                anchor=NW, font=('Ivy 1'), bg=co2, fg=co4)
l_linha.place(x=10, y=45)


# credenciais de acesso ao app
# credenciais = ['joao', '123456789']

# Função para carregar credenciais de um arquivo JSON
def carregar_credenciais():
    if not os.path.exists('usuarios.json'):
        with open('usuarios.json', 'w') as file:
            json.dump({}, file)
    with open('usuarios.json', 'r') as file:
        return json.load(file)
    
# Função para salvar credenciais em um arquivo JSON
def salvar_credenciais(credenciais):
    with open('usuarios.json', 'w') as file:
        json.dump(credenciais, file)


credenciais = carregar_credenciais()


# Funcão para verificar senha
def verificar_senha():
    nome = e_nome.get()
    senha = e_pass.get()

    # Verifique se o nome do usuário existe nas credenciais
    if nome in credenciais:
        # Verifique se a senha fornecida corresponde à senha armazenada
        if credenciais[nome]['senha'] == senha:
            messagebox.showinfo('Login', f'Seja bem-vindo {nome}!!')
            # Limpar o conteúdo dos frames
            for widget in frame_baixo.winfo_children():
                widget.destroy()
            for widget in frame_cima.winfo_children():
                widget.destroy()
            nova_janela(nome)
        else:
            messagebox.showwarning('Erro', 'Senha incorreta')
    else:
        messagebox.showwarning('Erro', 'Nome de usuário não encontrado')

#criando janela de login com os input de dados
def nova_janela():
    l_nome = Label(frame_cima, text='Usuario: '+credenciais[0], anchor=NE,
                   font=('Ivy 20'), bg=co1, fg=co4)
    l_nome.place(x=5, y=5)

    l_linha = Label(frame_cima, text='', width=275,
                    anchor=NW, font=('Ivy 1'), bg=co2, fg=co4)
    l_linha.place(x=10, y=45)
# Frame baixo
    l_nome = Label(frame_baixo, text='Seja bem vindo '+credenciais[0], anchor=NE,
                   font=('Ivy 20'), bg=co1, fg=co4)
    l_nome.place(x=5, y=105)


#criando janela de cadastro de usuario com os input
def abrir_cadastro():
    janela_cadastro = Toplevel(janela)
    janela_cadastro.title('Cadastro de Usuario')
    janela_cadastro.geometry('310x390')
    janela_cadastro.configure(background=co1)
    janela_cadastro.resizable(width=FALSE, height=FALSE)

    l_nome_cad = Label(janela_cadastro, text='Nome *',
                       anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_nome_cad.place(x=10, y=10)
    e_nome_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_nome_cad.place(x=14, y=30)

    l_idade_cad = Label(janela_cadastro, text='Idade *',
                        anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_idade_cad.place(x=10, y=60)
    e_idade_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_idade_cad.place(x=14, y=80)

    l_peso_cad = Label(janela_cadastro, text='Peso *',
                       anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_peso_cad.place(x=10, y=110)
    e_peso_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_peso_cad.place(x=14, y=130)

    l_altura_cad = Label(janela_cadastro, text='Altura *',
                         anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_altura_cad.place(x=10, y=160)
    e_altura_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_altura_cad.place(x=14, y=180)

    l_senha_cad = Label(janela_cadastro, text='Senha *',
                        anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_senha_cad.place(x=10, y=210)
    e_senha_cad = Entry(janela_cadastro, width=25, justify='left',
                        show='*', font=("", 15), highlightthickness=1, relief='solid')
    e_senha_cad.place(x=14, y=230)


    #função para cadastrar o usuario no arquivo json, pega os dados do input da tela de cadastro e salva no arquivo json
    def cadastrar_usuario():
        nome = e_nome_cad.get()
        idade = e_idade_cad.get()
        peso = e_peso_cad.get()
        altura = e_altura_cad.get()
        senha = e_senha_cad.get()

        if nome in credenciais:
            messagebox.showwarning('Erro', 'Usuario já existe')
        else:
            credenciais[nome] = {'idade': idade,
                                 'peso': peso, 'altura': altura, 'senha': senha}
            salvar_credenciais(credenciais)
            messagebox.showinfo('Sucesso', 'Usuario cadastrado com sucesso')
            janela_cadastro.destroy

    b_confirmar_cad = Button(janela_cadastro, command=cadastrar_usuario, text='Cadastrar', width=39, height=2, font=(
        'Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
    b_confirmar_cad.place(x=15, y=270)
    #botão de voltar ao menu de acesso
    b_voltar = Button(janela_cadastro, command=janela_cadastro.destroy, text='Voltar', width=39,
                      height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=RAISED, overrelief=RIDGE)
    b_voltar.place(x=15, y=320)


# Configurando frame baixo tela inicial
l_nome = Label(frame_baixo, text='Nome *', anchor=NW,
               font=('Ivy 10'), bg=co1, fg=co4)
l_nome.place(x=10, y=20)
e_nome = Entry(frame_baixo, width=25, justify='left', font=(
    "", 15), highlightthickness=1, relief='solid')
e_nome.place(x=14, y=50)

l_pass = Label(frame_baixo, text='Senha *', anchor=NW,
               font=('Ivy 10'), bg=co1, fg=co4)
l_pass.place(x=10, y=95)
e_pass = Entry(frame_baixo, width=25, justify='left', show='*', font=(
    "", 15), highlightthickness=1, relief='solid')
e_pass.place(x=14, y=130)

b_confirmar = Button(frame_baixo, command=verificar_senha, text='Entrar', width=39, height=2,
                     font=('Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
b_confirmar.place(x=15, y=180)


b_cadastrar = Button(frame_baixo, command=abrir_cadastro, text='Cadastrar', width=39,
                     height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=RAISED, overrelief=RIDGE)
b_cadastrar.place(x=15, y=230)


janela.mainloop()
