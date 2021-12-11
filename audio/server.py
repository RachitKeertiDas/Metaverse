import socket
import threading, wave, pyaudio, time
import math
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 12000
# For details visit: www.pyshine.com
from queue import Queue
broadcast_queue = Queue(maxsize=-1)
server_queue = Queue(maxsize=-1)


def console(q):
    while True:
        cmd = input('> ')
        q.put(cmd)
        if cmd == 'q':
            break
	
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE  = 44100

CHUNK = 1024

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,  output = True, frames_per_buffer = CHUNK )


def audio_stream_UDP():

	BUFF_SIZE = 65536
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)
	server_socket.bind((host_ip, (port)))


	print('server listening at',(host_ip, (port)),broadcast_queue.qsize())

	data = None
	sample_rate = RATE
	clients = set()

	def reciever():
		while True:
			frame,addr = server_socket.recvfrom(BUFF_SIZE)
			server_queue.put(frame)
			if(addr not in clients):
				print(f'{addr} JOINED')
				clients.add(addr)
			broadcast_queue.put((frame,addr))
		
	def broadcast():
		while True:
			frame,addr = broadcast_queue.get(CHUNK)
			print(len(clients))
			for c in clients:
				if c != addr:
					server_socket.sendto(frame,c)
		

	recorder_thread = threading.Thread(target=reciever,args=())
	recorder_thread.start()
	time.sleep(2)
	# broadcast()

	# while True:
	# 	msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
	# 	print('[GOT connection from]... ',client_addr,msg)
	# 	DATA_SIZE = math.ceil(wf.qsize()/CHUNK)
	# 	DATA_SIZE = str(DATA_SIZE).encode()
	# 	print('[Sending data size]...',wf.qsize()/sample_rate)
	# 	# server_socket.sendto(DATA_SIZE,client_addr)
	# 	while True:
	# 		frame, _ = server_socket.recvfrom(BUFF_SIZE)
	# 		wf.put(frame)
	# 		print('Queue size',wf.qsize())

	# 	break
	# print('SENT...')            


streaming_tread = threading.Thread(target=audio_stream_UDP, args=())
streaming_tread.start()
time.sleep(1)
while True:
		frame = server_queue.get()
		stream.write(frame)

# t3 = threading.Thread(target=console,args=(wf,))