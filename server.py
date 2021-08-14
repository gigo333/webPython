import socket
import json
from os.path import exists
from os import listdir

ADDRESS="192.168.0.120"
PORT=80

htmlHeader="""HTTP/1.1 200 OK
Content-Type:text/html

"""

jsonHeader="""HTTP/1.1 200 OK
Content-Type:application/json

"""

imageHeader="""HTTP/1.1 200 OK
Content-Type:image

"""

PDFHeader="""HTTP/1.1 200 OK
Content-Type:application/pdf

"""

documentHeader="""HTTP/1.1 200 OK
Content-Type:document/extension

"""

def handleHTML(filename):
    page=""
    with open(filename) as f:
        page=f.read()

    toSend=htmlHeader+page
    return toSend.encode()

def handleImage(fileName):
    with open(fileName, "rb") as f:
        img=f.read()

    return imageHeader.encode()+img

def handlePDF(fileName):
    with open(fileName, "rb") as f:
        document=f.read()

    return PDFHeader.encode()+document

def handleDocument(fileName):
    extension=requestFile.split(".")[1]
    header=documentHeader.replace("extesion", extension)
    with open(fileName, "rb") as f:
        document=f.read()

    return header.encode()+document

def handleFolder(folderName):
    fileRef="""<p><a href="link">fileName</a></p>\n"""
    files=""
    for fileName in listdir(folderName):
        link=folderName.split("/")[-1]+"/"+fileName
        s=fileRef.replace("link",link)
        s=s.replace("fileName", fileName)
        files+=s

    with open("folderExplorer.html") as f:
        s=f.read()

    s=s.replace("folderName", folderName)
    s=s.replace("files", files)
    toSend = htmlHeader+s
    return s.encode()

def handleFavicon():
    with open("oldFiles/img.jpg", "rb") as f:
        img=f.read()

    return imageHeader.encode()+img

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
    if s[0:4]=="POST":
        st=s.split('\r')[-1]
        obj=json.loads(st)
        print(obj)
        obj["Success"]=True
        toSend=jsonHeader+json.dumps(obj)
        so.send(toSend.encode())
    else:
        request=s.split(" ")[1][1:].split("?")
        requestFile=request[0]
        print(requestFile)
        if(len(request)>1):
            getRequest=request[1].split("&")
            reqestDict={}
            for req in getRequest:
                req=req.split("=")
                reqestDict[req[0]]=req[1]
        
            print(reqestDict)

        if requestFile=="":
            toSend=handleHTML("index.html")
        elif requestFile=="favicon.ico":
            toSend=handleFavicon()
        elif requestFile.find(".")==-1:
            if(not exists(requestFile)):
                toSend=handleHTML("notFound.html")
            else:
                toSend=handleFolder(requestFile)
        else:
            if(not exists(requestFile)):
                toSend=handleHTML("notFound.html")
            else:
                format=requestFile.split(".")[1].lower()
                if(format=="html"):
                    toSend=handleHTML(requestFile)
                elif(format=="pdf"):
                    toSend=handlePDF(requestFile)
                elif(format in ["jpeg", "jpg", "png"]):
                    toSend=handleImage(requestFile)
                else:
                    toSend=handleDocument(requestFile)

        so.send(toSend)
        
    so.close()