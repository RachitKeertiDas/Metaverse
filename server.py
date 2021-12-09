from socket import *
import threading

serverPort = 12000 
serverSocket = socket(AF_INET, SOCK_STREAM)
serverSocket.bind(('', serverPort))

serverSocket.listen(20)

print("The Server is Ready to receive")

conns = [False for i in range(20)]

def fn(conn, addr, i):
    while True:
        message = conn.recv(1024)
        msg = message.decode()
        if msg == 'exit':
            conn.send('exit'.encode())
            conn.close()
            conns[i] = False
            return

        broadcast(msg.encode())


def broadcast(message):
    for i in range(20):
        if not conns[i]:
            continue
        print(f"Sending Message {message} to ")
        conns[i].send(message)

while True:
    connSocket, addr = serverSocket.accept()
    print(f"New Connection created by {addr}")
    
    for i in range(20):
        if not conns[i]:
            conns[i] = connSocket
            break

    process = threading.Thread(target=fn, args=[connSocket, addr, i])
    process.start()
