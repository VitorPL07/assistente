import speech_recognition as sr
import pyttsx3
import config
import tkinter
from tkinter import messagebox
from random import choice
import DataBase
from platform import system
import getpass
import conversar

# Gambiarra
username = getpass.getuser()

if system() == "Linux":
    caminho_img = f"/home/{username}/Documentos/Friday Image/image/LogoPrincipal.png"

    en = pyttsx3.init()
    voices = en.getProperty('voices')
    en.setProperty('rate', 175)
    for voice in voices:
        if voice.languages[0] == b'\x05pt-br':
            en.setProperty('voice', voice.id)
            break

else:
    caminho_img = f"C:/Users/{username}/Documents/Friday Image/image/LogoPrincipal.png"
    caminho_ico = f"C:/Users/{username}/Documents/Friday Image/image/logo_mini.ico"
    en = pyttsx3.init('sapi5')

city = ""
User_Global = ""
contagem = 0
pergunta = ""

# Sistema de som
def sai_som(reposta):
    en.say(reposta)
    en.runAndWait()

# Cabeça da janela
jan = tkinter.Tk()
jan.geometry("600x350+200+200")
jan.title("Friday System - Login")
jan.resizable(width=False, height=False)
jan.configure(bg="white")
if system() == "Windows":
    jan.iconbitmap(default=caminho_ico)
else:
    pass

# Icones
logo = tkinter.PhotoImage(file=caminho_img)

#Definir funções
def Logar():
    User = En_User.get()
    Pass2 = En_Pass.get()
    global User_Global
    User_Global = User
    global city
    global pergunta
    pergunta = var.get()
    DataBase.cursor.execute("""
    SELECT * FROM LoginUsers
    WHERE (User = ? and Password = ?)
    """, (User, Pass2))
    VerifyLogin = DataBase.cursor.fetchone()
    try:
        if User in VerifyLogin and Pass2 in VerifyLogin:
            messagebox.showinfo(title='Login Info', message='Acesso Confirmado. Bem Vindo')
            jan.destroy()
            city = VerifyLogin[3]

    except:
        messagebox.showerror(title='Login Info', message='Acesso Negado. Verifique se você esta cadastrado no sistema.')

def RegisterData():
    global contagem
    if contagem % 2 == 0:
        Lb_Init['text'] = "Register System"
        bt_Confirm.place(x=5000, y=5000)
        Lb_City.place(x=50, y=160)
        En_City.place(x=170, y=165)
        bt_Check.place(x=5000, y=5000)

    elif contagem % 2 == 1:
        Name = En_User.get()
        Pass = En_Pass.get()
        Cid = En_City.get()

        if Name == "" or Pass == "" or Cid == "":
            messagebox.showerror(title="Register Error", message="Preencha todos os camos")
            Lb_City.place(x=5000, y=5000)
            En_City.place(x=5000, y=5000)
            bt_Confirm.place(x=100, y=220)
            bt_Check.place(x=65, y=170)
            Lb_Init['text'] = "Login System"

        else:
            DataBase.cursor.execute("""
            INSERT INTO LoginUsers(User, Password, Cidade) VALUES(?, ?, ?)
            """, (Name, Pass, Cid))
            DataBase.conn.commit()
            messagebox.showinfo(title="Register Info", message="Registrado Com Sucesso")

            
            Lb_City.place(x=5000, y=5000)
            En_City.place(x=5000, y=5000)
            bt_Confirm.place(x=100, y=220)
            bt_Check.place(x=65, y=170)
            Lb_Init['text'] = "Login System"

    
    contagem += 1

# Frames
FrameEsquerdo = tkinter.Frame(jan, width='198', height='350', bg='#4169E1', relief='raise')
FrameEsquerdo.pack(side=tkinter.LEFT)
FrameDireito = tkinter.Frame(jan, width='400', height='350', bg='#6A5ACD', relief='raise')
FrameDireito.pack(side=tkinter.RIGHT)

# Widgets Left
Icon = tkinter.Label(FrameEsquerdo, image=logo)
Icon.place(x=-50, y=-110)

# Widgets Right
#      Labels
Lb_Init = tkinter.Label(FrameDireito, text='Login System', font=('Comic Sans, bold', 20), bg='#6A5ACD', fg='white')
Lb_Init.place(x=50, y=30)
Lb_User = tkinter.Label(FrameDireito, text='Username:', font=('Comic Sans', 15), bg='#6A5ACD')
Lb_User.place(x=50, y=100)
Lb_Pass = tkinter.Label(FrameDireito, text='Password:', font=('Comic Sans', 15), bg='#6A5ACD')
Lb_Pass.place(x=50, y=130)
Lb_City = tkinter.Label(FrameDireito, text='City:', font=('Comic Sans', 15), bg='#6A5ACD')

#      Entrys
En_User = tkinter.Entry(FrameDireito)
En_User.place(x=170, y=105)
En_Pass = tkinter.Entry(FrameDireito, show="*")
En_Pass.place(x=170, y=135)
En_City = tkinter.Entry(FrameDireito)

#      Buttons
bt_Confirm = tkinter.Button(FrameDireito, text='Confirm', activebackground='#6495ED', width='20', command=Logar)
bt_Confirm.place(x=100, y=220)
bt_Register = tkinter.Button(FrameDireito, text='Register', activebackground='#6495ED', width='20', command=RegisterData)
bt_Register.place(x=100, y=270)

#       CheckButtom
var = tkinter.IntVar()
bt_Check = tkinter.Checkbutton(FrameDireito, text="Start with voice command",font=("Comic Sans", 10), variable=var, bg='#6A5ACD', activebackground='#6A5ACD')
bt_Check.place(x=90, y=170)

#Deixar a janela em loop
def pythonExit():
    if messagebox.askokcancel("Sair", "Você realmente deseja sair?"):
        jan.destroy()
        exit()

jan.protocol("WM_DELETE_WINDOW", pythonExit)
jan.mainloop()


# Introduçao
Niver = config.Verificar_Niver()
user = f"Bem vindo {User_Global}"

# Sistema principal
def assistente():
    print("=" * len(user))
    print(user)
    print("=" * len(user))
    sai_som(user)
    print(Niver)
    sai_som(Niver)
    print("Ouvindo...")

    while True:
        resposta_erro_aleatoria = choice(config.lista_erros)

        def microfone_entrada():
            if pergunta == 0:
                ent = input("Pode digitar: ")
                return ent

            elif pergunta == 1:
                rec = sr.Recognizer()

                with sr.Microphone() as s:
                    rec.adjust_for_ambient_noise(s)
                    audio = rec.listen(s, phrase_time_limit=5)

                    while True:
                        try:
                            ent = rec.recognize_google(audio, language="pt-br")
                            return ent
                        except sr.UnknownValueError:
                            sai_som(resposta_erro_aleatoria)

        def microfone_fri():
            if pergunta == 0:
                ent = input("Me chame: ")
                return ent

            elif pergunta == 1:
                rec = sr.Recognizer()

                with sr.Microphone() as s:
                    rec.adjust_for_ambient_noise(s)
                    audio = rec.listen(s, phrase_time_limit=2)

                    while True:
                        try:
                            ent = rec.recognize_google(audio, language="pt-br")
                            return ent
                        except sr.UnknownValueError:
                            sai_som(resposta_erro_aleatoria)
        
        while True:
            fri = microfone_fri()
            fri = fri.lower()

            if "sexta" in fri and "feira" in fri:
                sai_som("Sim mestre")
                while True:
                    try:
                        entrada = microfone_entrada()
                        entrada = entrada.lower()
                        print("User: {}".format(entrada.capitalize()))

                        # Abri links no navegador
                        if "abrir" in entrada:
                            resposta = config.abrir(entrada)
                        
                        # Registrar Data de Niver
                        elif "adicionar" in entrada and "aniversario" in entrada:
                            resposta = config.adicionar_data()

                        # Sair
                        elif "sair" in entrada:
                            print("Saindo...")
                            sai_som("Saindo")
                            exit()
                        
                        # Reiniciar
                        elif "reiniciar" in entrada:
                            print("Reiniciando...")
                            sai_som("Reiniciando")
                            config.Reiniciar()

                        # Tocar música do youtube
                        elif entrada.startswith('tocar'):
                            sai_som("Carregando")
                            resposta = config.tocar(entrada)

                        # Fazer pesquisa no google
                        elif "pesquisar por" in entrada:
                            resposta = config.pesquisa(entrada)

                        # Operações matemáticas
                        elif "quanto é" in entrada:
                            entrada = entrada.replace("quanto é", "")
                            resposta = config.calcula(entrada)

                        # Pede tempo
                        elif "qual a temperatura" in entrada:

                            lista_tempo = config.clima_tempo(city)
                            temp = lista_tempo[2]
                            temp_max = lista_tempo[5]
                            temp_min = lista_tempo[6]

                            resposta = "A temperatura de hoje é {:.2f}°. Temos uma máxima de {:.2f}° e uma minima de {:.2f}°".format(
                                temp, temp_max, temp_min)

                        # Informações da cidade
                        elif "informações" in entrada and "cidade" in entrada:

                            resposta = "Mostrando informações da cidade"
                        elif "vamos" in entrada and "conversar" in entrada:
                            print("Tudo bem :)")
                            sai_som("Tudo bem")
                            while True:
                                entrada = microfone_entrada()
                                if entrada == "sair":
                                    resposta = "Okey, se precisar é só chamar"
                                    break

                                conv = conversar.conversas[entrada]
                                print(f"Assistente: {conv}")
                                sai_som(conv)

                        if resposta == "Mostrando informações da cidade":
                            # mostra informações da cidade

                            lista_infos = config.clima_tempo(city)
                            longitude = lista_infos[0]
                            latitude = lista_infos[1]
                            temp = lista_infos[2]
                            pressao = lista_infos[3]
                            humidade = lista_infos[4]
                            temp_max = lista_infos[5]
                            temp_min = lista_infos[6]
                            v_speed = lista_infos[7]
                            v_direc = lista_infos[8]
                            nebulosidade = lista_infos[9]
                            id_da_cidade = lista_infos[10]

                            print("Assistente:")
                            print("Mostrando informações de {}\n\n".format(city))
                            sai_som("Mostrando informações de {}".format(city))
                            print("Longitude: {}, Latitude: {}\nId: {}\n".format(longitude, latitude, id_da_cidade))
                            print("Temperatura: {:.2f}º".format(temp))
                            print("Temperatura máxima: {:.2f}º".format(temp_max))
                            print("Temperatura minima: {:.2f}º".format(temp_min))
                            print("Humidade: {}".format(humidade))
                            print("Nebulosidade: {}".format(nebulosidade))
                            print("Pressao atmosférica: {}".format(pressao))
                            print("Velocidade do vento: {}m/s\nDireção do vento: {}".format(v_speed, v_direc))
                            break

                        else:
                            print("Assistente: {}".format(resposta))
                            sai_som("{}".format(resposta))
                            break
                    except KeyError:
                        pass


if __name__ == '__main__':
    config.intro()
    sai_som("Carregando")
    assistente()