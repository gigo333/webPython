import hashlib
import base64
import json
from threading import Thread
from struct import pack, unpack

def recvAll(so, l):
    b=b''
    while(len(b)<l):
        b+=so.recv(l-len(b))

    return b

def formatWS(toSend, dType="string"):
    dType=dType.lower()
    opcode={"string":1, "text":1, "bin":2, "binary":2, "bytes":2, "buffer":2 }
    length=len(toSend)
    buffer=None
    if(length<126):
        buffer=bytearray(2)
        buffer[0]=128+opcode[dType]
        buffer[1]=length
    elif(length<2**16): 
        buffer=bytearray(4)
        buffer[0]=128+opcode[dType]
        buffer[1]=126
        buffer[2]=length//256
        buffer[3]=length%256
    else:
        buffer=bytearray(2)
        buffer[0]=128+opcode[dType]
        buffer[1]=127
        buffer+=pack("!Q", length)

    return bytes(buffer)+toSend

def receiveWS(so):
    buffer=so.recv(1)
    length=buffer[0]%128
    if length==126:
        buffer=recvAll(so, 2)
        length=buffer[1]*256+buffer[0]
    elif(length==127):
        buffer=recvAll(so, 8)
        length=unpack("!Q", buffer)[0]

    buffer=recvAll(so, 4+length)
    mask=buffer[:4]
    encoded=buffer[4:]
    decoded=bytearray(length)
    for i in range(length):
        decoded[i]=encoded[i]^mask[i%4]

    return decoded

wsAcceptHeader="""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: AcceptCode\r
\r\n"""

def sendThread(so):
    while(1):
        try:
            t=input("\nTemperature?\n")
            t=t.replace(",",".")
            obj={"Temperature":float(t), "Humidity":50}
            toSend=json.dumps(obj).encode()
            buffer=formatWS(toSend)
            so.send(buffer)
        except:
            break

def handleWS(so, s, code):
    request=s.split(" ")[1][1:].split("?")
    requestPath=request[0]
    print(requestPath)
    code=code+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    AcceptCode=base64.b64encode(hashlib.sha1(code.encode()).digest()).decode()
    toSend=wsAcceptHeader.replace("AcceptCode", AcceptCode).encode()
    so.send(toSend)
    with open("oldFIles/images/img.jpg", "rb") as f:
        buffer=f.read()
        print(len(buffer))
        b=formatWS(buffer, "Binary")
        so.sendall(b)
        
    th = Thread(target=sendThread, args=(so,))
    th.setDaemon(True)
    th.start()    
    while(1):
        try:
            buffer=so.recv(1)
            opcode=buffer[0] & 15
            buffer=receiveWS(so)
            if(opcode==1):
                message=buffer.decode()
                print("##############")
                print("WS: "+message)
                
        except:
            print("##############")
            print("WS: Disconnected!")
            so.close()
            break