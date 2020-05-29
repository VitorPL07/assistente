import speech_recognition as sr
import pyttsx3
import config
from tkinter import ttk, Frame, PhotoImage, Entry, Button, Checkbutton, LEFT, RIGHT, Tk, Label, messagebox, IntVar
from random import choice
import DataBase
from platform import system
import getpass

if system() == "Linux":
	en = pyttsx3.init()
	voices = en.getProperty('voices')
	en.setProperty('rate', 175)
	for voice in voices:
		if voice.languages[0] == b'\x05pt-br':
			en.setProperty('voice', voice.id)
			break

else:
	en = pyttsx3.init('sapi5')

city = ""
User_Global = ""
contagem = 0

# Gambiarra
username = getpass.getuser()
caminho_img = f"/home/{username}/Área de Trabalho/Sexta-feira/image/logo_mini.png"

# Sistema de som
def sai_som(reposta):
    en.say(reposta)
    en.runAndWait()

# Cabeça da janela
jan = Tk()
jan.geometry("600x350+200+200")
jan.title("Friday System - Login")
jan.resizable(width=False, height=False)
jan.configure(bg="white")

# Icones
logo = PhotoImage(file=caminho_img)

#Definir funções
def Logar():
    User = En_User.get()
    Pass2 = En_Pass.get()
    global User_Global
    User_Global = User
    global city
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
        bt_Confirm.place(x=5000, y=5000)
        Lb_City.place(x=50, y=160)
        En_City.place(x=170, y=165)

    elif contagem % 2 == 1:
        Name = En_User.get()
        Pass = En_Pass.get()
        Cid = En_City.get()

        if Name == "" or Pass == "" or Cid == "":
            messagebox.showerror(title="Register Error", message="Preencha todos os camos")
            Lb_City.place(x=5000, y=5000)
            En_City.place(x=5000, y=5000)
            bt_Confirm.place(x=100, y=220)

        else:
            DataBase.cursor.execute("""
            INSERT INTO LoginUsers(User, Password, Cidade) VALUES(?, ?, ?)
            """, (Name, Pass, Cid))
            DataBase.conn.commit()
            messagebox.showinfo(title="Register Info", message="Registrado Com Sucesso")

            
            Lb_City.place(x=5000, y=5000)
            En_City.place(x=5000, y=5000)
            bt_Confirm.place(x=100, y=220)

    
    contagem += 1

# Frames
FrameEsquerdo = Frame(jan, width='198', height='350', bg='#4169E1', relief='raise')
FrameEsquerdo.pack(side=LEFT)
FrameDireito = Frame(jan, width='400', height='350', bg='#6A5ACD', relief='raise')
FrameDireito.pack(side=RIGHT)

# Widgets Left
Icon = Label(FrameEsquerdo, image=logo, bg="#4169E1")
Icon.place(x=60, y=100)
Name = Label(FrameEsquerdo, text='Friday', font=('FreeSerif', 25), bg='#4169E1')
Name.place(x=50, y=180)

# Widgets Right
#      Labels
Lb_Init = Label(FrameDireito, text='Login System', font=('Comic Sans, bold', 20), bg='#6A5ACD', fg='white')
Lb_Init.place(x=50, y=30)
Lb_User = Label(FrameDireito, text='Username:', font=('Comic Sans', 15), bg='#6A5ACD')
Lb_User.place(x=50, y=100)
Lb_Pass = Label(FrameDireito, text='Password:', font=('Comic Sans', 15), bg='#6A5ACD')
Lb_Pass.place(x=50, y=130)
Lb_City = Label(FrameDireito, text='City:', font=('Comic Sans', 15), bg='#6A5ACD')

#      Entrys
En_User = Entry(FrameDireito)
En_User.place(x=170, y=105)
En_Pass = Entry(FrameDireito, show='*')
En_Pass.place(x=170, y=135)
En_City = Entry(FrameDireito)

#      Buttons
bt_Confirm = Button(FrameDireito, text='Confirm', activebackground='#6495ED', width='20', command=Logar)
bt_Confirm.place(x=100, y=220)
bt_Register = Button(FrameDireito, text='Register', activebackground='#6495ED', width='20', command=RegisterData)
bt_Register.place(x=100, y=270)

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
        #rec = sr.Recognizer()

        #with sr.Microphone() as s:
            #rec.adjust_for_ambient_noise(s)
            #audio = rec.listen(s, timeout=1, phrase_time_limit=1)

        while True:
            fri = input("Me chame: ")
            fri = fri.lower()

            if "sexta" in fri and "feira" in fri:
                sai_som("Sim mestre")
                while True:
                    try:
                        #audio = rec.listen(s, timeout=1, phrase_time_limit=3)
                        entrada = input("O que deseja: ")
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
                        else:
                            resposta = config.conversas[entrada]

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
                    except sr.UnknownValueError:
                        sai_som(resposta_erro_aleatoria)
                    except KeyError:
                        pass


if __name__ == '__main__':
    config.intro()
    sai_som("Iniciando")
    assistente()