import socket
# import sys
import threading
import time
# from queue import Queue

all_connections = []
all_address = []
Report = {} # dict of tuples. #(address:marks)

QUESTIONS = [" What is the Italian word for PIE? \n a.Mozarella b.Pasty c.Patty d.Pizza",
     " Water boils at 212 Units at which scale? \n a.Fahrenheit b.Celsius c.Rankine d.Kelvin",
     " Which sea creature has three hearts? \n a.Dolphin b.Octopus c.Walrus d.Seal",
     " Who was the character famous in our childhood rhymes associated with a lamb? \n a.Mary b.Jack c.Johnny d.Mukesh",
     " How many bones does an adult human have? \n a.206 b.208 c.201 d.196",
     " How many wonders are there in the world? \n a.7 b.8 c.10 d.4",
     " What element does not exist? \n a.Xf b.Re c.Si d.Pa",
     " How many states are there in India? \n a.24 b.29 c.30 d.31",
     " Who invented the telephone? \n a.A.G Bell b.John Wick c.Thomas Edison d.G Marconi",
     " Who is Loki? \n a.God of Thunder b.God of Dwarves c.God of Mischief d.God of Gods",
     " Who was the first Indian female astronaut ? \n a.Sunita Williams b.Kalpana Chawla c.None of them d.Both of them ",
     " What is the smallest continent? \n a.Asia b.Antarctic c.Africa d.Australia",
     " The beaver is the national embelem of which country? \n a.Zimbabwe b.Iceland c.Argentina d.Canada",
     " How many players are on the field in baseball? \n a.6 b.7 c.9 d.8",
     " Hg stands for? \n a.Mercury b.Hulgerium c.Argenine d.Halfnium",
     " Who gifted the Statue of Libery to the US? \n a.Brazil b.France c.Wales d.Germany",
     " Which planet is closest to the sun? \n a.Mercury b.Pluto c.Earth d.Venus"]

ANSWERS = ['d', 'a', 'b', 'a', 'a', 'a', 'a', 'b', 'a', 'c', 'b', 'd', 'd', 'c', 'a', 'b', 'a']

NUM = len(ANSWERS)

def create_socket():
    try:
        global host
        global port
        global s
        host = ""
        port = 9999
        s = socket.socket()

    except socket.error as msg:
        print("socket creation error "+str(msg))

# Binding the socket and listening for connections
def bind_socket():
    try:
        global host
        global port
        global s

        print("Binding the Port: "+str(port))
        s.bind((host,port))
        s.listen(5)

    except socket.error as msg:
        print("Socket Binding error "+str(msg)+"\n"+"Retrying...")
        bind_socket()

# Handling connection from multiple clients and saving to a list
# Closing previous connections when server.py file is restarted

def accepting_connection():
    for c in all_connections:
        c.close()
    
    del all_connections[:]
    # count = 0
    while(True):
        try:
            conn,address = s.accept()
            s.setblocking(1) #prevents time out
            all_connections.append(conn)
            all_address.append(address)

            print("Connection has been established :"+address[0])
            t = threading.Thread(target=Communication_client,args=(conn,address))
            t.daemon = True
            t.start()
        except:
            print("Error accepting connections")

def Communication_client(conn,address):
    Report[address] = 0
    for i in range(NUM):
        conn.send(str.encode(QUESTIONS[i]))
        client_response = str(conn.recv(1024),"utf-8") # Assuming that as an option(a,b,c,d)
        if(ANSWERS[i] == client_response):
            Report[address] = Report.get(address,0)+1
    conn.send(str.encode("Your Score is : "+str(Report[address])))
    time.sleep(2)
    conn.close()
    all_connections.remove(conn)

create_socket()
bind_socket()
accepting_connection()