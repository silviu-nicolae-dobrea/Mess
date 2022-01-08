import socket
import threading
from tkinter import *
import time
import re


IP = '127.0.0.1'
PORT = 8080
ADDR = (IP, PORT)
HEADER = 1024
FORMAT = "utf-8"

my_username = ""


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

        def error_p(i):

            root2 = Tk()
            root2.title('My Mess')
            root2.geometry('400x250+760+415')
            root2.resizable(0, 0)

            def exit_error():
                root2.destroy()  
            
            if i == "exist":
                error = Label(root2, text='username already exist', font=('Courier', 15, 'bold')) 
                error.pack(pady=10)
            else :
                if i =="parola":
                    error = Label(root2, text='password error', font=('Courier', 15, 'bold')) 
                    error.pack(pady=10)
                elif i == "nume_user":
                    error = Label(root2, text='username error', font=('Courier', 15, 'bold')) 
                    error.pack(pady=10)
                elif i == "nume":
                    error = Label(root2, text='name error', font=('Courier', 15, 'bold')) 
                    error.pack(pady=10)

                error = Label(root2, text='Only letters and numbers', font=('Courier', 15)) 
                error.pack(pady=10)
                error = Label(root2, text='At least 8 characters ', font=('Courier', 15)) 
                error.pack(pady=10)

            exit_button =  Button(root2, text='OK', font=('Helvetica', 15, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=exit_error)
            exit_button.pack(pady=20)
            root2.mainloop()
            
        pattern = re.compile(r"[A_Za-z0-9]{8,}")
        pattern2 = re.compile(r"[A_Za-z0-9 ]{8,}")

        check = pattern.fullmatch(nume_user)
        check2 = pattern.fullmatch(parola)
        check3 = pattern2.fullmatch(nume)

        if check == None:
            error_p("nume_user")
        elif check2 == None:
            error_p("parola")
        elif check3 == None:
            error_p("nume")

        else:
            head = "__SIGN_UP__"
            print (f"{head} : {date}")

            c1 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            c1.connect(ADDR)
            c1.send(head.encode(FORMAT))
            time.sleep(0.1)
        
            for item in date:
                c1.send(item.encode(FORMAT))
                time.sleep(0.1)
            check = c1.recv(HEADER).decode(FORMAT)
            if check == "NO":
                c1.close()
                error_p("exist")
            else :
                c1.close()
                root.destroy()



    create = Button(root, text='Sign Up', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd = 0, width=16, command=update_database)
    create.pack(pady=10)
    
    root.mainloop()
 
def return_log_in(conn):
    check = "NO"
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
        nonlocal check
        global my_username
        
        def log_in_error(check):
            root2 = Tk()
            root2.title('My Mess')
            root2.geometry('400x250+760+415')
            root2.resizable(0, 0)   

            def exit_error():
                root2.destroy() 
            if check == "WRONG":
                error = Label(root2, text='Username or password\n to short', font=('Courier', 15)) 
                error.pack(pady=30)
            else:
                if check =="CONNECTED":
                    error = Label(root2, text='Already connected.', font=('Courier', 15)) 
                    error.pack(pady=30)  
                elif check == "NO":
                    error = Label(root2, text='User dosen\'t exist.\nor\nWrong password.', font=('Courier', 15)) 
                    error.pack(pady=30)  
             
            exit_button =  Button(root2, text='OK', font=('Helvetica', 15, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=exit_error)
            exit_button.pack(pady=20)

        username = un.get()
        password = pw.get()
        date =[username, password]
        my_username = username

        pattern = re.compile(r"[A_Za-z0-9]{8,}")
        check_us = pattern.fullmatch(username)
        check_pw = pattern.fullmatch(password)

        if ((check_us == None) or (check_pw == None)):
            log_in_error("WRONG")
        else:
            head = "__LOG_IN__"
            conn.send(head.encode(FORMAT))
            time.sleep(0.1)

            for item in date:
                conn.send(item.encode(FORMAT))
                time.sleep(0.1)

            check = conn.recv(HEADER).decode(FORMAT)
            if check == "YES":
                root.destroy()
            else :
                log_in_error(check)
    
    def exit():
        head = "QUIT"
        conn.send(head.encode(FORMAT))
        time.sleep(0.1)
        conn.close()
        root.destroy()
        nonlocal check
        check = "QUIT"
           
    lg_button = Button(root, text='Log In', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=log_in)
    lg_button.pack(pady=10)

    not_re = Label(root, text='Don\'t have an account? ', font=('Helvetica', 16))
    not_re.pack(pady=(60,10))

    c_a_button = Button(root, text='Create Acount', font=('Helvetica', 20, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=return_sign_up)
    c_a_button.pack(pady=10)
    root.protocol("WM_DELETE_WINDOW",exit)
    root.mainloop()
    return check

def send_select_add_friend(conn):

    def friend_dont_exist(check):
        root2 = Tk()
        root2.title('My Mess')
        root2.geometry('400x250+760+415')
        root2.resizable(0, 0)

        def exit_error():
            root2.destroy()  

        if check == "NOT":
            error = Label(root2, text='Username Dosen\'t Exist', font=('Courier', 20, 'bold')) 
            error.pack(pady=40)
        elif check == "WRONG_CD":
            error = Label(root2, text='Insert a valide username', font=('Courier', 20, 'bold')) 
            error.pack(pady=40)


        exit_button =  Button(root2, text='OK', font=('Helvetica', 15, 'bold'), bg='#3DED97', fg='white',bd=0, width=16, command=exit_error)
        exit_button.pack(pady=20)
        root2.mainloop()


    friend = ""
    friends =[]
    root = Tk()
    root.title('My Mess')
    root.geometry('500x500+710+290')
    root.resizable(0, 0)

    add_us_entry = Entry(root, font=('Helvetica', 14), width=40, fg='#5E5E5E', bd=1, borderwidth=5)
    add_us_entry.pack(pady=10)
    add_us_entry.insert(0,'Insert friend username')
    def clear_add_friend_us(e):
        add_us_entry.delete(0,END)
    add_us_entry.bind('<Button-1>',clear_add_friend_us)

    friends = conn.recv(HEADER).decode(FORMAT)
    friends = eval(friends)
    
    


    def add_us_friend():

        head = "__ADD_FRIEND__"
        conn.send(head.encode(FORMAT))
        time.sleep(0.1)

        friend_username = add_us_entry.get()
        pattern = re.compile(r"[A_Za-z0-9]{8,}")
        check_fr = pattern.fullmatch(friend_username)
        if check_fr == None:
            friend_dont_exist("WRONG_CD")


        conn.send(friend_username.encode(FORMAT))
        time.sleep(0.1)
        check2 = conn.recv(HEADER).decode(FORMAT) 
        nonlocal friends
        if check2 == "YES":
            if friend_username not in friends:
                friend_list_box.insert(END,friend_username)
                friends.append(friend_username)
        elif check2 == "NOT":
            friend_dont_exist(check2)
        
    def exit():
        exit = "__EXIT__"
        conn.send(exit.encode(FORMAT))
        time.sleep(0.1)
        nonlocal friend
        friend = friend_list_box.get(ANCHOR)
        conn.send(friend.encode(FORMAT))
        root.destroy()
        


    friends_us_but = Button(root, text = ' Add Friend',font=('Helvetica', 14, 'bold'),bg='#3DED97', fg='white',bd = 0, width=14,command =add_us_friend)
    friends_us_but.pack(pady=10)
    friend_list_box = Listbox(root,width=30,height=11,font=('Helvetica', 15, 'bold'))
    friend_list_box.pack(pady=10)
    
    for item in friends:
        friend_list_box.insert(END, item)
    
    exit_button = Button(root, text = 'Select',font=('Helvetica', 14, 'bold'),bg='#3DED97', fg='white',bd = 0, width=14,command =exit)
    exit_button.pack(pady=10)

    root.mainloop()
    return friend

def speack_to(conn,friend):
    root = Tk()
    root.title('My Mess')
    root.geometry('500x500+710+290')
    root.resizable(0, 0)

    welcome = Label(root, text=f"You are sending messages to {friend}", font=('Courier', 13, 'bold'))
    welcome.pack(pady=5)

    msg_from_database = conn.recv(100000).decode(FORMAT)
    msg_from_database = eval(msg_from_database)
    
    def send():
        msg = my_msg.get()
        my_msg.set("")    
        conn.send(msg.encode(FORMAT))

        msg1 = f"<<  {msg}"
        msg_list.insert(END,msg1)



    def primeste(conn,friend):
        connected = "YES"
        while connected == "YES":
            msg = conn.recv(HEADER).decode(FORMAT)
            if msg == "#quit":
                connected = "NO"
                conn.close()  
            else:
                msg1 = f">>  {msg}"
                msg_list.insert(END,msg1)
                
                

    def on_closing():
        my_msg.set("#quit")        
        send()
        root.destroy()
     
    t1 = threading.Thread(target=primeste,args=(conn,friend))
    t1.start()
    
    my_msg = StringVar()
    my_msg.set("")
    msg_frame = Frame(root)
    scrool_bar = Scrollbar(msg_frame,orient=VERTICAL)
    msg_list = Listbox(msg_frame,height=15,width=30,font=('Helvetica', 16, 'bold'),yscrollcommand=scrool_bar.set)
    scrool_bar.pack(side=RIGHT,fill=Y)
    msg_list.pack()
    msg_frame.pack()

    for item in msg_from_database:
        msg_l = item.split(" : ")
        if msg_l[0] == my_username:
            i = f"<<  {msg_l[1]}"
            msg_list.insert(END,i)
        else :
            i = f">>  {msg_l[1]}"
            msg_list.insert(END,i)

    msg_frame2 = Frame(root)
    quit_button = Button(msg_frame2,text = "Quit",font=('Helvetica', 14, 'bold'),command = on_closing)
    quit_button.grid(row = 0, column = 0, pady = 2)
    entry_msg=Entry(msg_frame2,textvariable = my_msg, font=('Helvetica', 14),width = 25, fg='#5E5E5E', bd=1, borderwidth=5)
    entry_msg.grid(row = 0, column = 1, pady = 2)
    send_button = Button(msg_frame2, text = "Send",font=('Helvetica', 14, 'bold'),command=send)
    send_button.grid(row = 0, column = 2, pady = 2)
    msg_frame2.pack()
    root.protocol("WM_DELETE_WINDOW",on_closing)
    

    root.mainloop()

    if t1.is_alive():
        print('Still running')
    else:
        print('Completed')

c = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
c.connect(ADDR)

check = "NO"
while ((check == "NO") or (check =="CONNECTED")):
    check = return_log_in(c)

print("You are logged in\n")

if check == "YES":
    friend = send_select_add_friend(c)
    if len(friend) != 0:
        speack_to(c,friend)

print("__FINISH__")




    




