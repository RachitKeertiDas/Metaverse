import socket,os
import threading, wave, pyaudio, time, queue

host_name = socket.gethostname()
host_ip = '117.194.116.107'#  socket.gethostbyname(host_name)
print(host_ip)
port = 12000
# For details visit: www.pyshine.com
q_receive = queue.Queue(maxsize=-1)
q_send = queue.Queue(maxsize=-1)
        
def audio_stream_UDP():
    BUFF_SIZE = 65536
    client_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
    client_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
    p = pyaudio.PyAudio()
    CHUNK = 1024*5
    down_stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    output=True,
                    frames_per_buffer=CHUNK)
    up_stream = p.open(format=pyaudio.paInt16,
                    channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

    # create socket
    def record(stream, CHUNK):
        while True:
            q_send.put(stream.read(CHUNK))
       
    def send_audio():
        recorder_thread=threading.Thread(target=record,args=(up_stream,CHUNK,))
        recorder_thread.start()
        time.sleep(1)
        while True:
            data=q_send.get(CHUNK)
            client_socket.sendto(data,(host_ip,port))        
    sender_thread=threading.Thread(target=send_audio,args=())
    sender_thread.start()
    
    def getAudioData():
        while True:
            frame,_= client_socket.recvfrom(BUFF_SIZE)
            q_receive.put(frame)
            print('Queue size...',q_receive.qsize())
    receiver_thread = threading.Thread(target=getAudioData, args=())
    receiver_thread.start()
    time.sleep(1)
    print('Now Playing...')
    while True:
        frame = q_receive.get()
        down_stream.write(frame)
    
    client_socket.close()
    print('Audio closed')
    os._exit(1)



#t1 = threading.Thread(target=audio_stream_UDP, args=())
#t1.start()
audio_stream_UDP()