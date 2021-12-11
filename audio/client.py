import socket,os
import threading, wave, pyaudio, time, queue

host_name = socket.gethostname()
host_ip = '117.194.116.107'#  socket.gethostbyname(host_name)
print(host_ip)
port = 12000
# For details visit: www.pyshine.com
q = queue.Queue(maxsize=-1)

def audio_stream_UDP():
    BUFF_SIZE = 65536
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    p = pyaudio.PyAudio()
    CHUNK = 1024*5
    stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)

    # create socket
    message = b'Hello'
    client_socket.sendto(message,(host_ip,port))
    socket_address = (host_ip,port)
    
    def getAudioData():
        while True:
            frame,_= client_socket.recvfrom(BUFF_SIZE)
            q.put(frame)
            print('Queue size...',q.qsize())
    t1 = threading.Thread(target=getAudioData, args=())
    t1.start()
    time.sleep(1)
    print('Now Playing...')
    wf=wave.open('Audio_check.wav','wb')
    while not q.empty():
        frame = q.get()
        stream.write(frame)
    
    client_socket.close()
    print('Audio closed')
    os._exit(1)



t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()
