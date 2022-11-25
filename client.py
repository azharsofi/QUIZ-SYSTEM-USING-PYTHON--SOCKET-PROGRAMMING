import socket
# import os
# import subprocess

s = socket.socket()
host = "10.5.142.141" #Server's IP
port = 9999

s.connect((host,port))

while(True):
    Server_data = str(s.recv(20480),"utf-8")
    if(Server_data[:16]=='Your Score is : '):
        print('Your score is : ',Server_data[16:])
        print('Quiz Ended')
        s.close()
        break
    print("Question:\n"+Server_data)
    ans = input('Type the Option here : ')
    s.send(str.encode(ans))
    