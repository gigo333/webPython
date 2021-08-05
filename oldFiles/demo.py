import socket

arr="""HTTP/1.1 200 OK
Content-Type:text/html
Content-Length: 16

<h1>testing</h1>"""

sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.bind(("127.0.0.1",80))
while(1):
    sc.listen(1)
    so, addr = sc.accept()
    so.send(arr.encode())
    print(so.recv(1000))
    so.close()
