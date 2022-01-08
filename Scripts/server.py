import socket
import threading
import sqlite3
from sqlite3 import Error

IP = '127.0.0.1'
PORT = 8080
ADDR = (IP, PORT)
HEADER = 1024
FORMAT = "utf-8"


clients={}
addresses={}

s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
s.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
s.bind(ADDR)


# introduce datele de SIGN UP in baza de date
def update_database(date):
    db_file = r"mess.db"    
    try:
        my_db = sqlite3.connect(db_file)
        c = my_db.cursor()
        query = "INSERT INTO users (username,password,name) VALUES (?, ?, ?);"
        values = (date[0],date[1],date[2])
        c.execute(query, values)
        my_db.commit()
    except Error as e:
        print("Error while connecting to MySQL \"sign up\" :", e)
    finally:
        c.close()
        my_db.close()


# primeste datele pentru SIGN UP ale noilor clienti
def handel_sign_up(conn):
    date = []
    for msg in range(3):
        msg = conn.recv(HEADER).decode(FORMAT)
        date.append(msg)    
    print(date, "\n")
    update_database(date)
    conn.close()


# se ocupa de manipularea datelor venite de la client 
def handle_client(conn,addr):

    print("__HANDEL CLIENT__")
    head = conn.recv(HEADER).decode(FORMAT)
    print(head)

    if head == "__SIGN_UP__":
        handel_sign_up(conn)


# porneste serverul(serverul incepe sa asculte si sa accepte noile conexiuni)
def start():
    s.listen(1)
    print("___SERVER ON___")
    while True:
        client_conn, client_addr = s.accept()
        t = threading.Thread(target=handle_client, args=(client_conn,client_addr))
        t.start()

        
print("___SERVER IS STARTING___")
start()

#rowid