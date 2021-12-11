import socket
import os
import threading
import wave
import pyaudio
import time
import queue

host_name = socket.gethostname()
host_ip = '117.194.116.107'  # socket.gethostbyname(host_name)
print(host_ip)
port = 12000
q = queue.Queue(maxsize=-1)


def record(stream, CHUNK):
    while True:
        q.put(stream.read(CHUNK))


def audio_stream_UDP():
	t = 1
	BUFF_SIZE = 65536
	client_socket = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
	client_socket.setsockopt(socket.SOL_SOCKET, socket.SO_RCVBUF, BUFF_SIZE)
	p = pyaudio.PyAudio()
	CHUNK = 1024*5
	stream = p.open(format=pyaudio.paInt16,
	                channels=2,
                    rate=44100,
                    input=True,
                    frames_per_buffer=CHUNK)

    # create socket
	t_record = threading.Thread(target=record,args=())
	t_record.start()
	message = b'Hello'
	client_socket.sendto(message, (host_ip, port))
	socket_address = (host_ip, port)

	def getAudioData():
		while True:
			data = q.get(CHUNK)
			client_socket.sendto(data, socket_address)
			time.sleep(0.001)

	t1 = threading.Thread(target=getAudioData, args=())
	
	t1.start()
	time.sleep(1)
	print('Now Playing...')
	wf = wave.open('Audio_check.wav', 'wb')

	client_socket.close()
	print('Audio closed')
	os._exit(1)


t1 = threading.Thread(target=audio_stream_UDP, args=())
t1.start()