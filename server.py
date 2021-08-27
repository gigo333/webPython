import socket
from threading import Thread

from httpServer import handleHTTP
from webSocketServer import handleWS

from thermalImg import ThremalImg

ADDRESS="192.168.0.120"
PORT=80

thermalImg=ThremalImg()

sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind((ADDRESS,PORT))
thread = Thread(target=thermalImg.run)
thread.setDaemon(True)
thread.start()

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
        th = Thread(target=handleHTTP, args=(so, s))
        th.setDaemon(True)
        th.start()
    else:
        th = Thread(target=handleWS, args=(so, s, code, thermalImg))
        th.setDaemon(True)
        th.start()