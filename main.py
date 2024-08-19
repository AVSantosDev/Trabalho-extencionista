import customtkinter as ctk
from tkinter import messagebox, Tk, Listbox, Canvas, ttk
from tkinter import *
import json
import tkinter as tk
import os
import math
import time
from datetime import datetime

# Cores
co0 = "#000000"  # Preta / black
co1 = "#feffff"  # branca / white
co2 = "#403d4e"  # verde / green
co3 = "#38576b"  # valor / value
co4 = "#403d3d"  # letra / letters



class Relogio(Canvas):
    def __init__(self, master, **kwargs):
        super().__init__(master, width=150, height=150, bg=co4, **kwargs)
        self.create_oval(10, 10, 140, 140, outline=co1, fill=co4)
        self.pointer = self.create_line(75, 75, 75, 10, fill=co1, width=2)
        self.update_clock()

    def update_clock(self):
        now = time.localtime()
        segundos = now.tm_sec

        # Calcula o ângulo para o ponteiro dos segundos
        angulo = (segundos / 60) * 360
        radianos = math.radians(angulo)
        x = 75 + 60 * math.sin(radianos)
        y = 75 - 60 * math.cos(radianos)

        self.coords(self.pointer, 75, 75, x, y)

        # Atualiza a cada 1000 ms (1 segundo)
        self.after(1000, self.update_clock)


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


class InicioDoPrograma:
    def __init__(self):
        self.credenciais = self.carregar_credenciais()
        self.janela_login = None
        self.janela_principal = None
        
        
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

    def salvar_tarefas_concluidas(self, nome_exercicio, repeticoes,):
        data_atual = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        tarefa = {
            "data": data_atual,
            "exercicio": nome_exercicio,
            "repeticoes": repeticoes
        }

        if os.path.exists('tarefas_concluidas.json'):
            with open('tarefas_concluidas.json', 'r') as file:
                tarefas = json.load(file)
        else:
            tarefas = []

        tarefas.append(tarefa)

        with open('tarefas_concluidas.json', 'w') as file:
            json.dump(tarefas, file, indent=4)

    def limpar_exercicios(self):
        try:
            with open('exercicios.txt', 'w') as file:
                # Abrir o arquivo no modo de escrita limpa o conteúdo existente
                pass
        except IOError as e:
            print(f"Erro ao limpar o arquivo de exercícios: {e}")

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
            #janela_cadastro.destroy()

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
        if self.janela_principal:
            self.janela_principal.destroy()  # Fecha a janela principal

        janela = ctk.CTk()
        janela.title("Tela Principal")
        janela.geometry("500x400")

        label_nova = ctk.CTkLabel(janela, text=f"Bem-vindo, {nome}!")
        label_nova.pack(pady=20)

        b_dados_usuario = ctk.CTkButton(janela, text='Dados do Usuário', command=lambda: self.dados_usuario(nome),
                                        width=200, height=40, font=('Ivy', 12), fg_color=co2, bg_color=co2)
        b_dados_usuario.pack(pady=10)

        b_exercicios = ctk.CTkButton(janela, text='Exercícios', command=lambda: self.exercicios(nome),
                                     width=200, height=40, font=('Ivy', 12), fg_color=co2, bg_color=co2)
        b_exercicios.pack(pady=10)

        b_ultimos_exercicios = ctk.CTkButton(janela, text='Últimos Exercícios', command=self.mostrar_ultimos_exercicios,
                                         width=200, height=40, font=('Ivy', 12), fg_color=co2, bg_color=co2)
        b_ultimos_exercicios.pack(pady=10)

        b_Fechar = ctk.CTkButton(janela, text='Fechar', command=janela.destroy,
                                 width=200, height=40, font=('Ivy', 12), fg_color=co3, bg_color=co4)
        b_Fechar.pack(pady=10)

        self.janela_principal = janela  # Atualiza a referência da janela principal
        janela.mainloop()

    def mostrar_ultimos_exercicios(self):
        janela_exercicios = ctk.CTkToplevel()
        janela_exercicios.title("Últimos Exercícios")
        janela_exercicios.geometry("600x400")

        # Ler os dados dos exercícios concluídos
        try:
            with open('tarefas_concluidas.json', 'r') as file:
                tarefas = json.load(file)
        except FileNotFoundError:
            tarefas = []

        # Formatar o texto dos exercícios
        texto_exercicios = ""
        if tarefas:
            for tarefa in tarefas:
                texto_exercicios += f"Data: {tarefa['data']}, Exercício: {tarefa['exercicio']}, Repetições: {tarefa['repeticoes']}\n"
        else:
            texto_exercicios = "Nenhum exercício concluído encontrado."

        # Label para exibir os exercícios concluídos
        label_exercicios = ctk.CTkLabel(janela_exercicios, text=texto_exercicios, anchor="w", justify="left", padx=10, pady=10)
        label_exercicios.pack(expand=True, fill=ctk.BOTH)

        b_voltar = ctk.CTkButton(janela_exercicios, text="Voltar para a Tela Principal", command=janela_exercicios.destroy,
                                 width=200, height=40, font=('Ivy', 12), fg_color=co2, bg_color=co2)
        b_voltar.pack(pady=10)

        janela_exercicios.mainloop()

    def dados_usuario(self, nome):
        janela_dados = ctk.CTkToplevel()
        janela_dados.title("Dados do Usuário")
        janela_dados.geometry("600x300")

        usuario = self.credenciais.get(nome)
        if usuario:
            imc = usuario.calcularIMC()
            classificacao, recomendacao = usuario.classificar_imc(imc)

            label_imc = ctk.CTkLabel(
                janela_dados, text=f"Seu IMC é: {imc:.2f}")
            label_imc.pack(pady=10)

            label_classificacao = ctk.CTkLabel(
                janela_dados, text=f"Classificação: {classificacao}")
            label_classificacao.pack(pady=10)

            label_recomendacao = ctk.CTkLabel(
                janela_dados, text=f"Recomendação: {recomendacao}")
            label_recomendacao.pack(pady=10)

            b_voltar = ctk.CTkButton(janela_dados, text='Voltar para a Tela Principal', command=janela_dados.destroy,
                                     width=200, height=40, font=('Ivy', 12), fg_color=co2, bg_color=co2)
            b_voltar.pack(pady=10)

        janela_dados.mainloop()

      #Criação da tela  

    def exercicios(self, nome):
        janela_exercicio = ctk.CTkToplevel()
        janela_exercicio.title("Exercícios")
        janela_exercicio.geometry("900x500")

        # Dados dos exercícios
        exercicios = [
            {"nome": "Flexão", "repeticoes": None, "duracao": None},
            {"nome": "Abdominal", "repeticoes": None, "duracao": None},
            {"nome": "Agachamento", "repeticoes": None, "duracao": None},
            {"nome": "Corrida", "repeticoes": None, "duracao": None},
        ]

        # Frame principal
        frame = ctk.CTkFrame(janela_exercicio)
        frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)

        # Frame de entrada (para os exercícios)
        frame_input = ctk.CTkFrame(frame)
        frame_input.pack(side=ctk.LEFT, fill=ctk.BOTH,
                        expand=True, padx=10, pady=10)

        # Frame para os botões
        frame_buttons = ctk.CTkFrame(frame)
        frame_buttons.pack(side=ctk.RIGHT, fill=ctk.BOTH,
                        expand=False, padx=10, pady=10)

        # Label de status
        self.label_status = ctk.CTkLabel(
            frame_input, text="", fg_color=co4, width=250, height=200, anchor="w", justify="left")
        self.label_status.pack(pady=10, fill=ctk.BOTH)

        selecionados = []

        def adicionar_exercicio(nome, entry_reps, entry_duracao):
            reps = entry_reps.get()
            duracao = entry_duracao.get()

            if nome in selecionados:
                selecionados.remove(nome)
            else:
                selecionados.append(nome)

            lista_exercicios_texto = []
            for ex in selecionados:
                if ex == "Corrida":
                    texto = f"{ex} - KM: {entry_reps.get()}, Duração: {entry_duracao.get()}"
                else:
                    texto = f"{ex} - Reps: {entry_reps.get()}, Duração: {entry_duracao.get()}"
                lista_exercicios_texto.append(texto)

            self.label_status.configure(
                text=f"Selecionados:\n" + "\n".join(lista_exercicios_texto))

            # Adicionar exercício ao arquivo
            with open('exercicios.txt', 'a') as file:
                file.write(f"{nome} - Reps: {reps}, Duração: {duracao}\n")

        for ex in exercicios:
            nome = ex["nome"]
            frame_ex = ctk.CTkFrame(frame_input)
            frame_ex.pack(pady=5, fill=ctk.X)

            ctk.CTkLabel(frame_ex, text=nome, width=120).pack(
                side=ctk.LEFT, padx=5, fill=ctk.X)

            entry_reps = ctk.CTkEntry(
                frame_ex, placeholder_text="Repetições", width=120)
            entry_reps.pack(side=ctk.LEFT, padx=5)
            entry_duracao = ctk.CTkEntry(
                frame_ex, placeholder_text="Duração em Segundos", width=120)
            entry_duracao.pack(side=ctk.LEFT, padx=5)

            if nome == "Corrida":
                entry_reps.configure(placeholder_text="KM")

            b_add = ctk.CTkButton(frame_ex, text="Adicionar", command=lambda n=nome,
                                e_r=entry_reps, e_d=entry_duracao: adicionar_exercicio(n, e_r, e_d), fg_color=co2)
            b_add.pack(side=ctk.LEFT, padx=5)

        def salvar_exercicios():
            # Aqui você pode adicionar lógica adicional se necessário, mas a função adicionar_exercicio já faz a gravação em arquivo.
            self.label_status.configure(text="Exercícios salvos")

        # Botões de ação
        b_salvar = ctk.CTkButton(
            frame_buttons, text="Salvar Exercícios", width=200, command=salvar_exercicios, fg_color=co2)
        b_salvar.pack(pady=10)

        b_executar = ctk.CTkButton(
            frame_buttons, text="Executar Exercícios", width=200, command=self.abrir_execucao_exercicios, fg_color=co2)
        b_executar.pack(pady=10)

        b_voltar = ctk.CTkButton(
            frame_buttons, text="Voltar para a Tela Principal", width=200, command=janela_exercicio.destroy, fg_color=co2)
        b_voltar.pack(pady=10)

        # Tela de execução de exercicio

    
    def abrir_execucao_exercicios(self):
        janela_execucao = ctk.CTkToplevel()
        janela_execucao.title("Execução dos Exercícios")
        janela_execucao.geometry("800x500")

        frame = ctk.CTkFrame(janela_execucao)
        frame.pack(fill=ctk.BOTH, expand=True, padx=15, pady=15)

        frame_exercicios = ctk.CTkFrame(frame)
        frame_exercicios.pack(side=ctk.LEFT, fill=ctk.BOTH, expand=True, padx=10, pady=10)

        frame_botoes = ctk.CTkFrame(frame)
        frame_botoes.pack(side=ctk.RIGHT, fill=ctk.Y, padx=10, pady=10)

        exercicios = self.carregar_exercicios()

        relogio_canvas = None

        def iniciar_exercicio(nome):
            nonlocal relogio_canvas

            if relogio_canvas:
                relogio_canvas.destroy()

            relogio_canvas = Relogio(frame_botoes)
            relogio_canvas.pack(pady=10)

            if hasattr(self, 'label_status') and self.label_status.winfo_exists():
                self.label_status.configure(text=f"Iniciando exercício: {nome}", fg_color=co4)
            else:
                print("A label_status não está mais disponível.")

        def concluir_exercicio(nome):
            nonlocal relogio_canvas

            if relogio_canvas:
                relogio_canvas.destroy()
                relogio_canvas = None

            if hasattr(self, 'label_status') and self.label_status.winfo_exists():
                self.label_status.configure(text=f"Exercício {nome} concluído", fg_color="green")
            else:
                print("A label_status não está mais disponível.")

            for ex in exercicios:
                if ex["nome"] == nome:
                    self.salvar_tarefas_concluidas(nome, ex["repeticoes"])
                    break

        for ex in exercicios:
            frame_ex = ctk.CTkFrame(frame_exercicios)
            frame_ex.pack(pady=5, fill=ctk.X)

            texto_exercicio = f"{ex['nome']}: "
            if ex['nome'] == "Corrida":
                texto_exercicio += f"KM: {ex['repeticoes']}, Duração: {ex['duracao']}"
            else:
                texto_exercicio += f"Reps: {ex['repeticoes']}, Duração: {ex['duracao']}"

            ctk.CTkLabel(frame_ex, text=texto_exercicio, width=350).pack(side=ctk.LEFT, padx=5, anchor='w')

            frame_botoes_ex = ctk.CTkFrame(frame_ex)
            frame_botoes_ex.pack(side=ctk.RIGHT, fill=ctk.Y, padx=5)

            b_iniciar = ctk.CTkButton(frame_botoes_ex, text="Iniciar",
                                      width=80, command=lambda n=ex['nome']: iniciar_exercicio(n), fg_color=co2)
            b_iniciar.pack(pady=5)

            b_concluir = ctk.CTkButton(frame_botoes_ex, text="Concluir",
                                       width=80, command=lambda n=ex['nome']: concluir_exercicio(n), fg_color=co2)
            b_concluir.pack(pady=5)

        self.label_status = ctk.CTkLabel(frame_botoes, text="Pronto para iniciar",
                                         fg_color=co4, width=200, height=150, anchor="w", justify="center")
        self.label_status.pack(pady=10, fill=ctk.BOTH)

        b_voltar_principal = ctk.CTkButton(
            frame_botoes, text="Voltar para a Tela Principal", width=200, command=janela_execucao.destroy, fg_color=co3)
        b_voltar_principal.pack(side=ctk.BOTTOM, pady=10)

        b_voltar_exercicios = ctk.CTkButton(
            frame_botoes, text="Voltar para a Tela de Exercícios", width=200, command=janela_execucao.destroy, fg_color=co3)
        b_voltar_exercicios.pack(side=ctk.BOTTOM, pady=10)

        janela_execucao.mainloop()

    def carregar_exercicios(self):
        # Esta função deve carregar os dados dos exercícios salvos de um arquivo
       
        try:
            with open('exercicios.txt', 'r') as file:
                linhas = file.readlines()
            exercicios = []
            for linha in linhas:
                partes = linha.strip().split(" - Reps: ")
                nome = partes[0]
                reps_duracao = partes[1].split(", Duração: ")
                reps = reps_duracao[0]
                duracao = reps_duracao[1] if len(reps_duracao) > 1 else ''
                exercicios.append(
                    {"nome": nome, "repeticoes": reps, "duracao": duracao})
            return exercicios
        except FileNotFoundError:
            return []


# tela de login do programa

    def abrir_tela_login(self):
        self.janela_login = ctk.CTk()
        self.janela_login.title("Login")
        self.janela_login.geometry("400x300")

        # Configurar grid
        self.janela_login.grid_columnconfigure(1, weight=1)

        # Nome de Usuário
        ctk.CTkLabel(self.janela_login, text="Nome de Usuário").grid(
            row=0, column=0, padx=10, pady=10, sticky="e")
        global e_nome
        e_nome = ctk.CTkEntry(
            self.janela_login, placeholder_text="Digite seu nome")
        e_nome.grid(row=0, column=1, padx=10, pady=10, sticky="ew")

        # Senha
        ctk.CTkLabel(self.janela_login, text="Senha").grid(
            row=1, column=0, padx=10, pady=10, sticky="e")
        global e_pass
        e_pass = ctk.CTkEntry(
            self.janela_login, placeholder_text="Digite sua senha", show="*")
        e_pass.grid(row=1, column=1, padx=10, pady=10, sticky="ew")

        # Botões
        b_entrar = ctk.CTkButton(
            self.janela_login, text="Entrar", command=self.entrar,fg_color=co3)
        b_entrar.grid(row=2, column=0, columnspan=2, pady=20)

        ctk.CTkButton(self.janela_login, text="Cadastrar", command=self.abrir_tela_cadastro,fg_color=co3).grid(
            row=3, column=0, columnspan=2, pady=10)


        
        self.janela_login.mainloop()

    def abrir_tela_cadastro(self):
        print("Abrindo tela de cadastro")  # Verificar se esta mensagem aparece no console
        global e_nome_cad, e_idade_cad, e_peso_cad, e_altura_cad, e_senha_cad
        global var_genero, janela_cadastro

        def cadastrarefechar():
            app.cadastrar()
            janela_cadastro.destroy()

        janela_cadastro = ctk.CTkToplevel(app.janela_login)
        janela_cadastro.title('Cadastro de Usuário')
        janela_cadastro.geometry('400x600')
        janela_cadastro.configure(bg=co4)  # CustomTkinter usa bg para o fundo
        janela_cadastro.resizable(width=False, height=False)

        l_nome_cad = ctk.CTkLabel(janela_cadastro, text='Nome *',
                                anchor='nw', font=('Ivy', 10), text_color=co1)
        l_nome_cad.place(x=10, y=10)
        e_nome_cad = ctk.CTkEntry(janela_cadastro, width=370, font=("", 15), border_width=1,
                                bg_color=co4, fg_color=co4)
        e_nome_cad.place(x=14, y=30)

        l_idade_cad = ctk.CTkLabel(janela_cadastro, text='Idade *',
                                anchor='nw', font=('Ivy', 10), text_color=co1)
        l_idade_cad.place(x=10, y=70)
        e_idade_cad = ctk.CTkEntry(janela_cadastro, width=370, font=("", 15), border_width=1,
                                bg_color=co4, fg_color=co4)
        e_idade_cad.place(x=14, y=90)

        l_peso_cad = ctk.CTkLabel(janela_cadastro, text='Peso (kg) *',
                                anchor='nw', font=('Ivy', 10), text_color=co1)
        l_peso_cad.place(x=10, y=130)
        e_peso_cad = ctk.CTkEntry(janela_cadastro, width=370, font=("", 15), border_width=1,
                                bg_color=co4, fg_color=co4)
        e_peso_cad.place(x=14, y=150)

        l_altura_cad = ctk.CTkLabel(janela_cadastro, text='Altura (m) *',
                                anchor='nw', font=('Ivy', 10), text_color=co1)
        l_altura_cad.place(x=10, y=190)
        e_altura_cad = ctk.CTkEntry(janela_cadastro, width=370, font=("", 15), border_width=1,
                                    bg_color=co4, fg_color=co4)
        e_altura_cad.place(x=14, y=210)

        l_senha_cad = ctk.CTkLabel(janela_cadastro, text='Senha *',
                                anchor='nw', font=('Ivy', 10), text_color=co1)
        l_senha_cad.place(x=10, y=250)
        e_senha_cad = ctk.CTkEntry(janela_cadastro, width=370, font=("", 15), border_width=1,
                                show='*', bg_color=co4, fg_color=co4)
        e_senha_cad.place(x=14, y=270)

        l_genero_cad = ctk.CTkLabel(janela_cadastro, text='Gênero *',
                                    anchor='nw', font=('Ivy', 10), text_color=co1)
        l_genero_cad.place(x=10, y=310)

        var_genero = tk.StringVar(value='Não especificado')
        r1 = ctk.CTkRadioButton(janela_cadastro, text='Masculino', variable=var_genero,
                                value='Masculino', font=('Ivy', 10))
        r1.place(x=10, y=340)
        r2 = ctk.CTkRadioButton(janela_cadastro, text='Feminino', variable=var_genero,
                                value='Feminino', font=('Ivy', 10))
        r2.place(x=10, y=370)
        r3 = ctk.CTkRadioButton(janela_cadastro, text='Não-binário', variable=var_genero,
                                value='Não-binário', font=('Ivy', 10))
        r3.place(x=10, y=400)
        r4 = ctk.CTkRadioButton(janela_cadastro, text='Outro', variable=var_genero,
                                value='Outro', font=('Ivy', 10))
        r4.place(x=10, y=430)

        b_cadastrar = ctk.CTkButton(janela_cadastro, text='Cadastrar', command=cadastrarefechar, width=370, height=40,
                                    font=('Ivy', 12, 'bold'),fg_color=co3)
        b_cadastrar.place(x=14, y=490)
        b_voltar = ctk.CTkButton(janela_cadastro, text='Voltar', command=janela_cadastro.destroy, width=370, height=40,
                                font=('Ivy', 12, 'bold'),fg_color=co3)
        b_voltar.place(x=15, y=540)

        janela_cadastro.mainloop()

    def iniciar_app(self):
        self.limpar_exercicios()
        self.abrir_tela_login()
        self.janela_login.mainloop()


# Iniciar o programa
if __name__ == "__main__":
    app = InicioDoPrograma()
    app.iniciar_app()
