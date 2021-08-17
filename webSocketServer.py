import hashlib
import base64
import json

def formatWSText(text):
    decoded=text.encode()
    length=len(text)
    buffer=None
    if(length<126):
        buffer=bytearray(2)
        opcode=1
        buffer[0]=128+opcode
        buffer[1]=length
    else: 
        buffer=bytearray(4)
        opcode=1
        buffer[0]=128+opcode
        buffer[1]=126
        buffer[2]=length//256
        buffer[3]=length%256

    return bytes(buffer)+decoded

def decodeWSText(buffer):
    opcode=buffer[0] & 15
    if(opcode!=1):
        return None

    length=buffer[1]%128
    k=2
    if length==126:
        k=4
        length=buffer[2]*256+buffer[3]

    mask=buffer[k:k+4]
    encoded=buffer[k+4:]
    decoded=bytearray(length)
    for i in range(length):
        decoded[i]=encoded[i]^mask[i%4]

    return decoded.decode()

wsAcceptHeader="""HTTP/1.1 101 Switching Protocols\r
Upgrade: websocket\r
Connection: Upgrade\r
Sec-WebSocket-Accept: AcceptCode\r
\r\n"""
def handleWS(so, s, code):
    request=s.split(" ")[1][1:].split("?")
    requestPath=request[0]
    print(requestPath)
    print(code)
    code=code+"258EAFA5-E914-47DA-95CA-C5AB0DC85B11"
    AcceptCode=base64.b64encode(hashlib.sha1(code.encode()).digest()).decode()
    toSend=wsAcceptHeader.replace("AcceptCode", AcceptCode).encode()
    so.send(toSend)    
    while(1):
        try:
            buffer=so.recv(1000)
            print("##############")
            print("WS: "+bin(buffer[0])+"\t"+bin(buffer[1]))
            message=decodeWSText(buffer)
            if(message!=None):
                print("WS: "+message)
                toSend={"Temperature":31.5, "Humidity":50}
                buffer=formatWSText(json.dumps(toSend))
                so.send(buffer)
        except:
            print("WS: Disconnected!")
            so.close()
            break