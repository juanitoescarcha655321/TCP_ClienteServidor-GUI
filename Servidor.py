import socket
import threading
import tkinter
import tkinter.scrolledtext

localIP = "127.0.0.1"
locport = 20001
tamBuff = 4

serverTCP = socket.socket(family = socket.AF_INET,type = socket.SOCK_STREAM)
serverTCP.bind((localIP,locport))
serverTCP.listen()

def limpio():
    todoTexto.config(state = "normal")
    todoTexto.delete("1.0",tkinter.END)
    todoTexto.config(state = "disabled")

def recibir():
    while(True):
        todoTexto.config(state = "normal")
        todoTexto.insert(tkinter.INSERT,"WAITING...\n\n")
        todoTexto.config(state = "disabled")
        conexion,puerto = serverTCP.accept()
        cont = 0
        mensaje = ""
        todoTexto.config(state = "normal")
        todoTexto.tag_config("CR",foreground = 'red')
        todoTexto.insert(tkinter.INSERT,"ADDRESS: ".format(puerto),"CR")
        todoTexto.insert(tkinter.INSERT,"{}\n\n".format(puerto))

        while(True):
            parteRecibida = conexion.recv(tamBuff)
            cont = cont + 1

            if(parteRecibida):
                mensaje = mensaje + parteRecibida.decode()
                todoTexto.insert(tkinter.INSERT,"%02d: " % cont)
                todoTexto.insert(tkinter.INSERT,"%4s - " % parteRecibida.decode())
                todoTexto.insert(tkinter.INSERT,"SENDING ACK...\n")
                conexion.sendall(parteRecibida)
            else:
                todoTexto.tag_config("CB",foreground = 'blue')
                todoTexto.insert(tkinter.INSERT,"\nMESSAGE: ","CB")
                todoTexto.insert(tkinter.INSERT,mensaje)
                todoTexto.insert(tkinter.INSERT,"\n\nNO MORE DATA AVAILABLE.")
                break

        conexion.close()
        todoTexto.insert(tkinter.INSERT,"\n\n-----------------------\n\n")
        todoTexto.config(state = "disabled")

mainW = tkinter.Tk()
mainW.configure(background = "purple")
mainW.title("Interfaz-Servidor (TCP)")
mainW.geometry("400x287")

todoTexto = tkinter.scrolledtext.ScrolledText(mainW,height = 15,state = "disabled",width = 46)
todoTexto.place(x = 5,y = 5)

boton2 = tkinter.Button(mainW,command = limpio,text = "CLEAR",width = 8)
boton2.place(x = 168,y = 256)

t = threading.Thread(target = recibir)
t.start()
mainW.mainloop()