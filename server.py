#Tugas Besar II Jarkom 
import socketserver
import webSocketHandler
import os

HOST = '0.0.0.0'
PORT = int(os.getenv('PORT', 9000))

if __name__ == "__main__":
    with socketserver.TCPServer((HOST, PORT), webSocketHandler.webSocketHandler) as server:
        server.serve_forever()