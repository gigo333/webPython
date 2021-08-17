import socket
from threading import Thread

from httpServer import handleHTTP
from webSocketServer import handleWS

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
    st=s.split("\r")
    code=''
    for head in st:
        if "Sec-WebSocket-Key:" in head:
            code=head.split(" ")[1]
            break

    if(code==''):
        th = Thread(target= handleHTTP, args=(so,s))
        th.setDaemon(True)
        th.start()
    else:
        th = Thread(target=handleWS, args=(so, s, code))
        th.setDaemon(True)
        th.start()