import socket
import threading
from tkinter import *
import time


IP = '127.0.0.1'
PORT = 8080
ADDR = (IP, PORT)
HEADER = 1024
FORMAT = "utf-8"


# se ocupa cu SIGN up : genereaza partea grafica, preia datele introduse si le trimite catre server 
def return_sign_up():
    

    root = Tk()
    root.title('My Mess')
    root.geometry('500x500+710+290')
    root.resizable(0, 0)

    welcome = Label(root, text='Sign Up', font=('Courier', 30, 'bold'))
    welcome.pack(pady=30)

    username = Entry(root, font=('Helvetica', 14), width=25, fg='#5E5E5E', bd=1)
    username.pack(pady=10)
    username.insert(0, "Username")

    password = Entry(root, font=('Helvetica', 14), width=25, fg='#5E5E5E', bd=1)
    password.pack(pady=10)
    password.insert(0, "Password")

    name = Entry(root, font=('Helvetica', 14), width=25, fg='#5E5E5E', bd=1)
    name.pack(pady=10)
    name.insert(0, "Name")


    def clear_username(e):
        username.delete(0, END)


    def clear_password(e):
        password.delete(0, END)
        password.config(show='*')

    def clear_name(e):
        name.delete(0, END)
    

    username.bind('<Button-1>', clear_username)
    password.bind('<Button-1>', clear_password)
    name.bind('<Button-1>', clear_name)
   
    # Conectarea la server si introducerea datelor
    def update_database():
        
        nume_user = username.get()        
        parola = password.get()
        nume = name.get()
        date = [nume_user, parola, nume]
        head = "__SIGN_UP__"
        print (f"{head} : {date}")

        c1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
        c1.connect(ADDR)
        c1.send(head.encode(FORMAT))
        time.sleep(0.1)
        
        for item in date:
            c1.send(item.encode(FORMAT))
            time.sleep(0.1)
        
        c1.close()

        root.destroy()


    create = Button(root, text='Sign Up', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd = 0, width=16, command=update_database)
    create.pack(pady=10)
    
    root.mainloop()
 
    
def return_log_in():
    username = 0
    password = 0
    root = Tk()
    root.title('My Mess')
    root.geometry('500x500+710+290')
    root.resizable(0, 0)

    welcome = Label(root, text='Log In', font=('Courier', 30, 'bold'))
    welcome.pack(pady=30)

    un = Entry(root, font=('Helvetica', 14), width=25, fg='#5E5E5E', bd=1)
    un.pack(pady=10)
    un.insert(0, "Username")

    pw = Entry(root, font=('Helvetica', 14), width=25, fg='#5E5E5E', bd=1)
    pw.pack(pady=10)
    pw.insert(0, "Password")

    def clear_un(e):
        un.delete(0, END)


    def clear_pw(e):
        pw.delete(0, END)
        pw.config(show='*')


    un.bind('<Button-1>', clear_un)
    pw.bind('<Button-1>', clear_pw)

    def log_in():
        nonlocal username
        username = un.get()
        nonlocal password
        password = pw.get()

        root.destroy()
        return


    lg_button = Button(root, text='Log In', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=log_in)
    lg_button.pack(pady=10)

    not_re = Label(root, text='Don\'t have an account? ', font=('Helvetica', 16))
    not_re.pack(pady=(60,10))

    c_a_button = Button(root, text='Create Acount', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=return_sign_up)
    c_a_button.pack(pady=10)

    root.mainloop()
    return username, password



user_pass = return_log_in()
username = user_pass[0]
password = user_pass[1]
print(f"{username} ; {password}")


c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(ADDR)

head = "__LOG_IN__"



connected = True
while connected:
    mesage = input("say something !!!")
    handle_connection(mesage)