import socket

from httpServer import handleHTTP

ADDRESS="192.168.0.120"
PORT=80

sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind((ADDRESS,PORT))
while(1):
    sc.listen(1)
    so, addr = sc.accept()
    print("##############")
    print(addr[0])
    r=so.recv(1000)
    s=r.decode()
    toSend=handleHTTP(s)
    if toSend!=None:
        so.send(toSend)
    
    so.close()