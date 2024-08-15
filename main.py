from tkinter import *
import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
import json
import os

co0 = "#f0f3f5"  # Preta / black
co1 = "#feffff"  # branca / white
co2 = "#3fb5a3"  # verde / green
co3 = "#38576b"  # valor / value
co4 = "#403d3d"  # letra / letters


class Usuario:
    def __init__(self, nome, idade, peso, altura, genero, senha):
        self.nome = nome
        self.idade = idade
        self.peso = peso
        self.altura = altura
        self.genero = genero
        self.senha = senha

    def calcularIMC(self):
        if self.altura > 0:
            return self.peso / (self.altura ** 2)
        else:
            return 0

    def classificar_imc(self, imc):
        if imc < 18.5:
            return 'Abaixo do peso', 'Recomenda-se uma avaliação nutricional para ganhar peso de forma saudável.'
        elif 18.5 <= imc < 24.9:
            return 'Peso normal', 'Continue mantendo uma dieta equilibrada e exercício regular.'
        elif 25 <= imc < 29.9:
            return 'Sobrepeso', 'Considere ajustar sua dieta e aumentar a atividade física para alcançar um peso saudável.'
        else:
            return 'Obesidade', 'É importante procurar orientação médica para um plano de perda de peso e saúde.'

    def registrar(self):
        return {
            'nome': self.nome,
            'idade': self.idade,
            'peso': self.peso,
            'altura': self.altura,
            'genero': self.genero,
            'senha': self.senha
        }


class inicioDoPrograma:
    def __init__(self):
        self.credenciais = self.carregar_credenciais()
        self.janela_login = None

    def entrar(self):
        nome = e_nome.get()
        senha = e_pass.get()

        if nome in self.credenciais:
            usuario = self.credenciais[nome]
            if usuario.senha == senha:
                if self.janela_login:
                    self.janela_login.destroy()
                self.nova_janela(nome)
            else:
                messagebox.showwarning('Erro', 'Senha incorreta')
        else:
            messagebox.showwarning('Erro', 'Nome de usuário inválido')

    def cadastrar(self):
        nome = e_nome_cad.get()
        idade_str = e_idade_cad.get()
        peso_str = e_peso_cad.get()
        altura_str = e_altura_cad.get().replace(',', '.')
        senha = e_senha_cad.get()

        genero = var_genero.get()

        if genero == 'Não especificado':
            messagebox.showwarning('Erro', 'Você deve selecionar um gênero.')
            return

        try:
            idade = int(idade_str)
            peso = int(peso_str)
            altura = float(altura_str)
        except ValueError:
            messagebox.showwarning(
                'Erro', 'Por favor, insira valores válidos.')
            return

        if nome in self.credenciais:
            messagebox.showwarning('Erro', 'Usuário já existe')
        else:
            usuario = Usuario(nome, idade, peso, altura, genero, senha)
            self.credenciais[nome] = usuario
            self.salvar_credenciais()
            messagebox.showinfo('Sucesso', 'Usuário cadastrado com sucesso')
            janela_cadastro.destroy()

    def carregar_credenciais(self):
        if not os.path.exists('usuarios.json'):
            with open('usuarios.json', 'w') as file:
                json.dump({}, file)

        credenciais = {}

        try:
            with open('usuarios.json', 'r') as file:
                data = json.load(file)
                if not isinstance(data, dict):
                    raise ValueError(
                        "O arquivo JSON não contém um objeto JSON válido.")

                for nome, info in data.items():
                    idade = info.get('idade', 0)
                    peso = info.get('peso', 0)
                    altura = info.get('altura', 0.0)
                    genero = info.get('genero', 'desconhecido')
                    senha = info.get('senha', '')

                    credenciais[nome] = Usuario(
                        nome,
                        idade,
                        peso,
                        altura,
                        genero,
                        senha
                    )
        except (json.JSONDecodeError, ValueError) as e:
            print(f"Erro ao carregar credenciais: {e}")

        return credenciais

    def salvar_credenciais(self):
        data = {nome: usuario.registrar()
                for nome, usuario in self.credenciais.items()}
        with open('usuarios.json', 'w') as file:
            json.dump(data, file)

    def carregar_exercicios(self):
        try:
            with open('exercicios.json', 'r') as file:
                data = json.load(file)
                return data.get('exercicios', [])
        except FileNotFoundError:
            return []

    def nova_janela(self, nome):
        janela = tk.Tk()
        janela.title("Tela Principal")
        janela.geometry("500x400")

        label_nova = ttk.Label(janela, text=f"Bem-vindo, {nome}!")
        label_nova.pack(pady=20)

        b_dados_usuario = Button(janela, text='Dados do Usuário', command=lambda: self.dados_usuario(
            nome), width=39, height=2, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
        b_dados_usuario.pack(pady=10)

        b_exercicios = tk.Button(janela, text='Exercícios', command=lambda: self.exercicios(
            nome), width=39, height=2, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
        b_exercicios.pack(pady=10)

        b_Fechar = tk.Button(janela, text='Fechar', command=janela.destroy, width=39, height=2, font=(
            'Ivy 8 bold'), bg=co3, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
        b_Fechar.pack(pady=10)

        janela.mainloop()

    def dados_usuario(self, nome):
        janela_dados = tk.Toplevel()
        janela_dados.title("Dados do Usuário")
        janela_dados.geometry("600x300")

        usuario = self.credenciais.get(nome)
        if usuario:
            imc = usuario.calcularIMC()
            classificacao, recomendacao = usuario.classificar_imc(imc)

            label_imc = ttk.Label(janela_dados, text=f"Seu IMC é: {imc:.2f}")
            label_imc.pack(pady=10)

            label_classificacao = ttk.Label(
                janela_dados, text=f"Classificação: {classificacao}")
            label_classificacao.pack(pady=10)

            label_recomendacao = ttk.Label(
                janela_dados, text=f"Recomendação: {recomendacao}")
            label_recomendacao.pack(pady=10)

            b_voltar = Button(janela_dados, text='Voltar para a Tela Principal', command=janela_dados.destroy,
                              width=39, height=2, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
            b_voltar.pack(pady=10)

        janela_dados.mainloop()

    def exercicios(self, nome):
        janela_exercicio = tk.Toplevel()
        janela_exercicio.title("Exercícios")
        janela_exercicio.geometry("600x500")

        # Dados dos exercícios (substitua ou adicione conforme necessário)
        exercicios = [
            {"nome": "Flexão", "repeticoes": 15, "duracao": "30s"},
            {"nome": "Abdominal", "repeticoes": 20, "duracao": "40s"},
            {"nome": "Agachamento", "repeticoes": 25, "duracao": "50s"},
            {"nome": "Corrida", "repeticoes": None, "duracao": None},
        ]

        frame = ttk.Frame(janela_exercicio)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        # Variável para armazenar os exercícios selecionados
        selecionados = []

        def adicionar_exercicio(nome):
            if nome in selecionados:
                selecionados.remove(nome)
            else:
                selecionados.append(nome)

        def selecionar_corredor():
            tempo_ou_distancia = var_tempo_ou_distancia.get()
            if tempo_ou_distancia == 'Tempo':
                corrida_detalhes = f"Corrida - Tempo: {e_tempo.get()} min"
            else:
                corrida_detalhes = f"Corrida - Distância: {e_distancia.get()} km"

            if corrida_detalhes not in selecionados:
                selecionados.append(corrida_detalhes)

        # Adiciona um Checkbutton para cada exercício
        for exercicio in exercicios:
            if exercicio['nome'] == "Corrida":
                var_tempo_ou_distancia = tk.StringVar(value='Tempo')

                label_opcao = tk.Label(
                    frame, text="Escolha a opção para Corrida:")
                label_opcao.pack(anchor=tk.W, pady=5)

                rb_tempo = tk.Radiobutton(
                    frame, text="Tempo", variable=var_tempo_ou_distancia, value="Tempo", font=('Ivy 10'))
                rb_tempo.pack(anchor=tk.W, pady=5)
                rb_distancia = tk.Radiobutton(
                    frame, text="Distância (km)", variable=var_tempo_ou_distancia, value="Distância", font=('Ivy 10'))
                rb_distancia.pack(anchor=tk.W, pady=5)

                label_tempo = tk.Label(frame, text="Tempo (min):")
                label_tempo.pack(anchor=tk.W, pady=5)
                e_tempo = tk.Entry(frame, width=10, font=('Ivy 10'))
                e_tempo.pack(anchor=tk.W, pady=5)

                label_distancia = tk.Label(frame, text="Distância (km):")
                label_distancia.pack(anchor=tk.W, pady=5)
                e_distancia = tk.Entry(frame, width=10, font=('Ivy 10'))
                e_distancia.pack(anchor=tk.W, pady=5)

                # Adiciona um Checkbutton para corrida
                cb_corrida = tk.Checkbutton(
                    frame, text="Corrida", command=selecionar_corredor, font=('Ivy 10'))
                cb_corrida.pack(anchor=tk.W, pady=5)

            else:
                texto = f"{exercicio['nome']} - {exercicio['repeticoes']} repetições - {exercicio['duracao']}"
                cb = tk.Checkbutton(
                    frame, text=texto, command=lambda n=exercicio['nome']: adicionar_exercicio(n), font=('Ivy 10'))
                cb.pack(anchor=tk.W, pady=5)

        # Botão "Iniciar"
        b_iniciar = tk.Button(frame, text='Iniciar', command=lambda: self.iniciar_exercicio(
            selecionados, janela_exercicio), width=39, height=2, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
        b_iniciar.pack(pady=10)

        # Botão "Voltar"
        b_voltar = tk.Button(frame, text='Voltar para a Tela Principal', command=janela_exercicio.destroy,
                             width=39, height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
        b_voltar.pack(pady=10)

    def iniciar_exercicio(self, selecionados, janela_exercicio):
        janela_exercicio.destroy()  # Fecha a janela de exercícios

        janela_execucao = tk.Toplevel()
        janela_execucao.title("Execução de Exercícios")
        janela_execucao.geometry("600x400")

        frame = ttk.Frame(janela_execucao)
        frame.pack(fill=tk.BOTH, expand=True, padx=10, pady=10)

        label_titulo = tk.Label(
            frame, text="Exercícios Selecionados", font=('Ivy 12 bold'))
        label_titulo.pack(pady=10)

        index_atual = 0
        labels_exercicios = []

        def concluir_exercicio(exercicio, index):
            # Atualiza o texto da label do exercício para incluir "Concluído"
            if index < len(labels_exercicios):
                labels_exercicios[index].config(
                    text=f"{exercicio} - Concluído")

            # Atualiza o índice atual para o próximo exercício
            nonlocal index_atual
            index_atual += 1
            if index_atual < len(labels_exercicios):
                labels_exercicios[index_atual].config(state=tk.NORMAL)
            else:
                tk.messagebox.showinfo(
                    "Concluído", "Todos os exercícios foram concluídos.")

        for index, exercicio in enumerate(selecionados):
            texto = f"{exercicio}"
            label_exercicio = tk.Label(frame, text=texto, font=('Ivy 10'))
            label_exercicio.pack(anchor=tk.W, pady=5)
            labels_exercicios.append(label_exercicio)

            b_concluir = tk.Button(frame, text='Concluir', command=lambda e=exercicio, i=index: concluir_exercicio(
                e, i), width=15, height=1, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
            b_concluir.pack(anchor=tk.W, pady=5)

            # Desabilita o botão de conclusão para o próximo exercício, se houver
            if index < len(selecionados) - 1:
                b_concluir.config(state=tk.NORMAL)
            else:
                b_concluir.config(state=tk.DISABLED)

        b_voltar = tk.Button(frame, text='Voltar para a Tela Principal', command=janela_execucao.destroy,
                             width=39, height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=tk.RAISED, overrelief=tk.RIDGE)
        b_voltar.pack(pady=10)


def abrir_cadastro():
    global e_nome_cad, e_idade_cad, e_peso_cad, e_altura_cad, e_senha_cad
    global var_genero, janela_cadastro

    janela_cadastro = Toplevel(app.janela_login)
    janela_cadastro.title('Cadastro de Usuário')
    janela_cadastro.geometry('310x600')
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
    l_idade_cad.place(x=10, y=70)
    e_idade_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_idade_cad.place(x=14, y=90)

    l_peso_cad = Label(janela_cadastro, text='Peso (kg) *',
                       anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_peso_cad.place(x=10, y=130)
    e_peso_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_peso_cad.place(x=14, y=150)

    l_altura_cad = Label(janela_cadastro, text='Altura (m) *',
                         anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_altura_cad.place(x=10, y=190)
    e_altura_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), highlightthickness=1, relief='solid')
    e_altura_cad.place(x=14, y=210)

    l_senha_cad = Label(janela_cadastro, text='Senha *',
                        anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_senha_cad.place(x=10, y=250)
    e_senha_cad = Entry(janela_cadastro, width=25, justify='left', font=(
        "", 15), show='*', highlightthickness=1, relief='solid')
    e_senha_cad.place(x=14, y=270)

    l_genero_cad = Label(janela_cadastro, text='Gênero *',
                         anchor=NW, font=('Ivy 10'), bg=co1, fg=co4)
    l_genero_cad.place(x=10, y=310)

    var_genero = StringVar(value='Não especificado')
    r1 = Radiobutton(janela_cadastro, text='Masculino', variable=var_genero,
                     value='Masculino', bg=co1, fg=co4, font=('Ivy 10'))
    r1.place(x=10, y=340)
    r2 = Radiobutton(janela_cadastro, text='Feminino', variable=var_genero,
                     value='Feminino', bg=co1, fg=co4, font=('Ivy 10'))
    r2.place(x=10, y=370)
    r3 = Radiobutton(janela_cadastro, text='Não-binário', variable=var_genero,
                     value='Não-binário', bg=co1, fg=co4, font=('Ivy 10'))
    r3.place(x=10, y=400)
    r4 = Radiobutton(janela_cadastro, text='Outro', variable=var_genero,
                     value='Outro', bg=co1, fg=co4, font=('Ivy 10'))
    r4.place(x=10, y=430)

    b_cadastrar = Button(janela_cadastro, text='Cadastrar', command=app.cadastrar, width=39, height=2, font=(
        'Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
    b_cadastrar.place(x=14, y=490)
    b_voltar = Button(janela_cadastro, command=janela_cadastro.destroy, text='Voltar', width=39,
                      height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=RAISED, overrelief=RIDGE)
    b_voltar.place(x=15, y=530)


app = inicioDoPrograma()

# Tela de login
app.janela_login = Tk()
app.janela_login.title('Tela de Login')
app.janela_login.geometry('310x300')
app.janela_login.configure(background=co1)
app.janela_login.resizable(width=FALSE, height=FALSE)

l_nome = Label(app.janela_login, text='Nome', anchor=NW,
               font=('Ivy 10'), bg=co1, fg=co4)
l_nome.place(x=10, y=10)
e_nome = Entry(app.janela_login, width=25, justify='left',
               font=("", 15), highlightthickness=1, relief='solid')
e_nome.place(x=14, y=30)

l_senha = Label(app.janela_login, text='Senha', anchor=NW,
                font=('Ivy 10'), bg=co1, fg=co4)
l_senha.place(x=10, y=70)
e_pass = Entry(app.janela_login, width=25, justify='left', font=(
    "", 15), show='*', highlightthickness=1, relief='solid')
e_pass.place(x=14, y=90)

b_entrar = Button(app.janela_login, text='Entrar', command=app.entrar, width=39,
                  height=2, font=('Ivy 8 bold'), bg=co2, fg=co1, relief=RAISED, overrelief=RIDGE)
b_entrar.place(x=14, y=150)

b_cadastro = Button(app.janela_login, text='Cadastrar', command=abrir_cadastro, width=39,
                    height=2, font=('Ivy 8 bold'), bg=co3, fg=co1, relief=RAISED, overrelief=RIDGE)
b_cadastro.place(x=14, y=200)

app.janela_login.mainloop()
