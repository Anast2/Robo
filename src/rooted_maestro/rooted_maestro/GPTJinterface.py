# echo-client.py
import socket

def history_add(hist, new_item):
   if len(hist)>1:
       hist.pop(0)
   hist.append(new_item)


def GPTJ(msg, ip="165.93.125.232", port=5050):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        client_socket.connect(server_address)
        myHist = []
        message = msg#input('Enter a message: ')
        if message == "exit":
            client_socket.close()
            
        #client_socket.sendall(("This is history, do not answer it:\n"+"\n".join(myHist[:-1])+"This is my current question: "+myHist[-1]).encode())
    #        hist = "These are previous conversations, use it only for context, do not reply: "
    ##        hist+=";".join(myHist)
    #       hist+="\nThis is the actual message, reply to this:\n"+ message
    #       history_add(myHist,message)
    #      print(myHist)
    #        client_socket.sendall(hist.encode())
    #        client_socket.sendall(hist.encode())
        client_socket.sendall(message.encode())
        
        message = client_socket.recv(2048)
        if not message:pass
        else:
            message = message.decode("utf-8")
            history_add(myHist, message)
            return(message)
    except:
        return("Server not reachable")