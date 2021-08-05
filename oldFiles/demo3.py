import socket

arr="""HTTP/1.1 200 OK
Content-Type:application/pdf

"""

sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.bind(("127.0.0.1",1234))
while(1):
    sc.listen(1)
    so, addr = sc.accept()
    with open("cs9.pdf", "rb") as f:
        toSend=arr.encode()+f.read()
        so.send(toSend)
        
    print(so.recv(1000))
    so.close()
