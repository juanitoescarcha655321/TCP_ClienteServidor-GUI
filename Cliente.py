import socket
import tkinter
import tkinter.scrolledtext

dirServ = ("127.0.0.1",20001)
tamBuff = 4

def enviar():
    flag = True
    texto = cajaTexto.get()
    cajaTexto.delete(0,tkinter.END)
    message = str.encode(texto)

    try:
        clienteTCP = socket.socket(family = socket.AF_INET,type = socket.SOCK_STREAM)
        clienteTCP.connect(dirServ)
    except:
        flag = False

    todoTexto.config(state = "normal")

    if(flag==True):
        todoTexto.tag_config("CR",foreground = 'red')
        todoTexto.insert(tkinter.INSERT,"SEND: ","CR")
        todoTexto.insert(tkinter.INSERT,texto + "\n")

        clienteTCP.sendall(message)

        cant_recibida = 0
        cant_esperada = len(message)

        while(cant_recibida<cant_esperada):
            datos = clienteTCP.recv(tamBuff)
            cant_recibida = cant_recibida + len(datos)
            todoTexto.tag_config("CB",foreground = 'blue')
            todoTexto.insert(tkinter.INSERT,"\nRECV: ","CB")
            todoTexto.insert(tkinter.INSERT,datos.decode())

        clienteTCP.close()
        todoTexto.insert(tkinter.INSERT,"\n\nSOCKET CLOSED.")
    else:
        todoTexto.insert(tkinter.INSERT,"CONNECTION FAILED.")
    
    todoTexto.insert(tkinter.INSERT,"\n\n--------------------\n\n")
    todoTexto.config(state = "disabled")

def limpio():
    todoTexto.config(state = "normal")
    todoTexto.delete("1.0",tkinter.END)
    todoTexto.config(state = "disabled")

mainW = tkinter.Tk()
mainW.configure(background = "green")
mainW.title("Interfaz-Cliente")
mainW.geometry("400x287")

todoTexto = tkinter.scrolledtext.ScrolledText(mainW,height = 15,state = "disabled",width = 46)
todoTexto.place(x = 5,y = 5)

cajaTexto = tkinter.Entry(mainW,width = 39)
cajaTexto.place(x = 5,y = 260)

boton = tkinter.Button(mainW,command = enviar,text = "SEND",width = 8)
boton.place(x = 327,y = 256)

boton2 = tkinter.Button(mainW,command = limpio,text = "CLEAR",width = 8)
boton2.place(x = 255,y = 256)

mainW.mainloop()