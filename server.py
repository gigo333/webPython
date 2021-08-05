import socket
import json

arr="""HTTP/1.1 200 OK
Content-Type:text/html

"""

arr1="""HTTP/1.1 200 OK
Content-Type:application/json

"""
sc=socket.socket(socket.AF_INET, socket.SOCK_STREAM)
sc.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
sc.bind(("192.168.0.120",80))
while(1):
    sc.listen(1)
    so, addr = sc.accept()
    r=so.recv(1000)
    s=r.decode()
    print("##############")
    if s[0:4]=="POST":
        st=s.split('\r')[-1]
        obj=json.loads(st)
        print(obj)
        obj["Success"]=True
        toSend=arr1+json.dumps(obj)
        so.send(toSend.encode())
    else:
        print(s)
        with open("index.html") as f:
            page=f.read()
            js=page.find("<script src=")
            while(js!=-1):
                s=page[js+1:]
                i=s.find("\"")
                j=s.find("\'")
                c="\""
                if (i==-1 or (j!=-1 and j<i)):
                    c="\'"
                    i=j

                s=s[i+1:]
                i=s.find(c)
                scriptName=s[:i]
                print(scriptName)
                script=open(scriptName)
                page=page.replace(" src="+c+scriptName+c+">"," language=\"javascript\">"+script.read())
                script.close()
                js=page.find("<script src=")

            toSend=arr+page
            so.send(toSend.encode())
        
    so.close()
