import socket
import threading
import sqlite3
from sqlite3 import Error
import time




IP = '127.0.0.1'
PORT = 8080
ADDR = (IP, PORT)
HEADER = 1024
FORMAT = "utf-8"


clients={}


s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)


# introduce datele de SIGN UP in baza de date
def update_database(date):
    print("\n__update_database__")
    check = "NO"
    db_file = r"mess.db"    
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()
        query = "INSERT INTO users (username,password,name) VALUES (?, ?, ?);"
        values = (date[0],date[1],date[2])
        c.execute(query, values)
        my_db.commit()
        check = "YES"
    except Error as e:
        pass
    finally:
        c.close()
        my_db.close()
    return check
    
# primeste datele pentru SIGN UP ale noilor clienti
def handel_sign_up(conn):
    print("\n__handel_sign_up__")
    date = []
    for msg in range(3):
        msg = conn.recv(HEADER).decode(FORMAT)
        date.append(msg)    
    print(date, "\n")
    check = update_database(date)
    conn.send(check.encode(FORMAT))
    conn.close()

#verifica in baza de date daca clientul exista
def check_database(date):
    print("\n__check_database__")
    check = "NO"
    db_file = r"mess.db"
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()        
        query = "SELECT * FROM users"
        c.execute(query)
        rezultat = c.fetchall()
        for row in rezultat:                      
            for item in row :
                if  date[0] == row[0] and date[1] == row[1]:
                    check = "YES" 
                    break          
        my_db.commit()
    except Error as e:
        print("Error while connecting to MySQL \"check\" :", e)
    finally:
        c.close()
        my_db.close()
    return check

# primeste datele pentru LOG IN ale clienti si apeleaza functia de verificare
def handel_log_in(conn):
    print("\n__handel_log_in__")
    date = []
    for msg in range(2):
        msg = conn.recv(HEADER).decode(FORMAT)
        date.append(msg)    
    check = check_database(date)

    if check == "YES":
        if date[0] not in clients.keys():
            clients[date[0]]=conn
        else:
            check = "CONNECTED"
    try:
        conn.send(check.encode(FORMAT))
        time.sleep(0.1)
    except Error as e:
        print("Error while sending message : ", e)
    return check

# functie de se ocupa cu datele privind prietenii si returneaza prietenul cu care doreste sa comunice clientul
def send_select_friend(conn):
    print("\n__send_select_friend__")
    for key,value in clients.items():
        if conn == value:
            i = key       
    
    #verifica daca clientul exista
    def check_if_friend_exist(friend):
        check = "NOT"
        db_file = r"mess.db"
        try:
            my_db = sqlite3.connect(db_file)
            c = my_db.cursor()        
            query = "SELECT * FROM users"
            c.execute(query)
            rezultat = c.fetchall()
            for row in rezultat:                      
                for item in row :
                    if  ((friend == row[0]) and (friend != i)):
                        check = "YES" 
                        break          
            my_db.commit()
        except Error as e:
            print("Error while connecting to MySQL \"check\" :", e)
        finally:
            c.close()
            my_db.close()
        return check
    
    #verifica daca sunteti deja prieteni
    def check_if_you_are_friends(user1, user2):
        check = "NOT"
        db_file = r"mess.db"
        try:
            my_db = sqlite3.connect(db_file)
            c = my_db.cursor()        
            query = f"SELECT * FROM friends"
            c.execute(query)
            rezultat = c.fetchall()
            for row in rezultat:                      
                for item in row :
                    if ((user1 == row[0] and user2 == row[1]) or (user2 == row[0] and user1 == row[1])):                        
                        check = "YES"          
            my_db.commit()
        except Error as e:
            print("Error while returning friends list", e)
        finally:
            c.close()
            my_db.close()
        return check
    
    # adauga clientul ca prieten in baza de date
    def add_friends_to_database(user1, user2):
        db_file = r"mess.db"    
        try:
            my_db = sqlite3.connect(db_file)
            c = my_db.cursor()
            query = "INSERT INTO friends (user1,user2) VALUES (?, ?);"
            values = (user1,user2)
            c.execute(query, values)
            my_db.commit()
        except Error as e:
            print("Error while connecting to MySQL \"add friend\" :", e)
        finally:
            c.close()
            my_db.close()

    # primeste numele clientului cu care vrei sa fii prieten
    def add_friends(conn,i):
        check = True
        while check:
            try :
                head = conn.recv(HEADER).decode(FORMAT)
                if head == "__ADD_FRIEND__":
                    friend = conn.recv(HEADER).decode(FORMAT)
                    check2 = check_if_friend_exist(friend)
                    conn.send(check2.encode(FORMAT))
                    time.sleep(0.1)
                    if check2 == "YES":
                        check3 = check_if_you_are_friends(i,friend)
                        if check3 == "NOT":
                            add_friends_to_database(i, friend)
                else :
                    check = False
            except Error as e :
                print("Error add friend :", e)
                
    # creaza o lista cu clientii care iti sunt prieteni
    friends = []
    db_file = r"mess.db"
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()        
        query = f"SELECT * FROM friends WHERE user1 = \'{i}\' "
        c.execute(query)
        rezultat = c.fetchall()
        for row in rezultat:                      
            for item in row :
                if item == i:
                    friends.append(row[1])          
        my_db.commit()

        query = f"SELECT * FROM friends WHERE user2 = \'{i}\'"
        c.execute(query)
        rezultat = c.fetchall()
        for row in rezultat:                      
            for item in row :
                if item == i:
                    friends.append(row[0])          
        my_db.commit()
    except Error as e:
        print("Error while returning friends list", e)
    finally:
        c.close()
        my_db.close()

    friends.sort() 
    

    #trimite lista cu prieteni
    friends = str(friends)
    conn.send(friends.encode(FORMAT))
    time.sleep(0.1)

    add_friends(conn,i)

    # primeste username-ul prietenului cu care doresti sa vorbesti
    friend = conn.recv(HEADER).decode(FORMAT)

    return friend

# inscrie in baza de date mesajele
def update_mesage(i,friend,msg):
    print("\n__update_mesage__")
    db_file = r"mess.db"    
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()
        query = "INSERT INTO mesages (send,recv,mesage) VALUES (?, ?, ?);"
        values = (i,friend,msg)
        c.execute(query, values)
        my_db.commit()
    except Error as e:
        print("Error while connecting to MySQL \"update mesage\" :", e)
    finally:
        c.close()
        my_db.close()

# preia mesajele din baza de date
def msg_from_databsae(i,friend):
    print("\n__msg_from_databsae__")
    msg_list=[]
    db_file = r"mess.db"
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()        
        query = "SELECT * FROM mesages"
        c.execute(query)
        rezultat = c.fetchall()
        for row in rezultat:                      
            if  ((i == row[0]) and (friend == row[1])) or ((i == row[1]) and (friend == row[0])) :
                item = f"{row[0]} : {row[2]}"
                msg_list.append(item)                       
        my_db.commit()
    except Error as e:
        print("Error while tacking messages from database:", e)
    finally:
        c.close()
        my_db.close()
    
    return msg_list

#trimite mesajele catre prieten
def message_from_to(i,friend):
    print("\n__message_from_to__")
    for key,value in clients.items():
        if i == key:
            i_conn = value
    
    msg_list = msg_from_databsae(i,friend)
    msg_list = str(msg_list)
    i_conn.send(msg_list.encode(FORMAT))
    time.sleep(0.1)

    connected = True
    while connected == True:
        msg = i_conn.recv(HEADER).decode(FORMAT)

        friend_online = "NO"
        try:    
            for key,value in clients.items():
                if friend == key:
                    friend_conn = value
                    friend_online = "YES"
        except Error as e:
            pass

        if msg != "#quit":
            if friend_online == "YES":
                friend_conn.send(msg.encode(FORMAT))
            update_mesage(i,friend,msg)
        else:
            i_conn.send(msg.encode(FORMAT))
            connected = False
            i_conn.close()
            del clients[i]

# se ocupa de manipularea datelor venite de la client 
def handle_client(conn,addr):
    
    print("\n__HANDEL CLIENT__")
    head = conn.recv(HEADER).decode(FORMAT)
    print(head)

    if head == "__SIGN_UP__":
        handel_sign_up(conn)
        
    
    if head == "__LOG_IN__":
        check = handel_log_in(conn)
        if check == "YES":
            friend = send_select_friend(conn)
            if len(friend) != 0:
                for key,value in clients.items():
                    if conn == value:
                        i = key
                message_from_to(i,friend)     
        else :
            handle_client(conn, addr)
    if head =="QUIT":
        conn.close()
      
# porneste serverul(serverul incepe sa asculte si sa accepte noile conexiuni)
def start():
    s.listen()
    print("___SERVER ON___")
    while True:
        client_conn, client_addr = s.accept()
        t = threading.Thread(target=handle_client, args=(client_conn,client_addr))
        t.start()
      

print("___SERVER IS STARTING___")
start()


