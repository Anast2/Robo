#!/usr/bin/env python3
import socket
import ollama
import requests

def GPTJ(msg, ip="165.93.125.232", port=5050):
    try:
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        server_address = (ip, port)
        client_socket.connect(server_address)
        myHist = []
        message = msg#input('Enter a message: ')
        if message == "exit":
            client_socket.close()
            
        client_socket.sendall(message.encode())
        
        message = client_socket.recv(2048)
        if not message:pass
        else:
            message = message.decode("utf-8")
            history_add(myHist, message)
            return(message)
    except:
        return("Server not reachable")
    
def ollama_local(msg, model="llama3"):
    response = ollama.chat(
        model=model, 
        messages=[
            {
                "role": "user",
                "content": msg,
            },
        ],
    )
    return response["message"]["content"]

def ollama_server(msg, model ="llama3", IP="localhost", port=11434):
    json_data = {
        'model': model,
        'messages':[{'role' : "user",
        'content':msg, 
        }],
        'stream':False
    }
    response = requests.post(f'http://{IP}:{port}/api/chat', json=json_data)
    return response.text
