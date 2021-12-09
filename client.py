from socket import *
import threading

serverName = 'localhost'
serverPort = 12000


clientSocket = socket(AF_INET, SOCK_STREAM)
clientSocket.connect((serverName,serverPort))

def send(clientSocket):
    while True:
        sentence = input('Input Message to be sent: ')
        if sentence == 'exit':
            clientSocket.send(sentence.encode())
            return
        clientSocket.send(sentence.encode())


def listen(clientSocket):
    # Listen From Server. If Server sends the message exit, we terminate"
    while True:
        message = clientSocket.recv(1024)
        # Do Whatever with the message here, pass it to the GUI for rendering
        msg = message.decode()
        if msg == 'exit':
            clientSocket.close()
            return 
        print("Message Recieved From Server", msg)
"""
while True:
    sentence = input('Input Lowercase Sentence')
    clientSocket.send(sentence.encode())
    if sentence == 'exit':
        clientSocket.close()
        break
    modifiedSentence = clientSocket.recv(1024)
    print("From Server", modifiedSentence.decode())
# clientSocket.close()\
"""

send_proc = threading.Thread(target=send, args=[clientSocket])
listen_proc = threading.Thread(target=listen, args=[clientSocket])

send_proc.start()
listen_proc.start()


