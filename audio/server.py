import socket
import threading, wave, pyaudio, time
import math
host_name = socket.gethostname()
host_ip = socket.gethostbyname(host_name)
print(host_ip)
port = 12000
# For details visit: www.pyshine.com
from queue import Queue

wf = Queue(maxsize=-1)

# def console(q):
#     while 1:
#         cmd = input('> ')
#         q.put(cmd)
#         if cmd == 'q':
#             break


def record(stream,CHUNK):
	while True:
		wf.put(stream.read(CHUNK))
	
FORMAT = pyaudio.paInt16
CHANNELS = 2
RATE  = 44100

CHUNK = 1024*5

p = pyaudio.PyAudio()

stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,  input = True, frames_per_buffer = CHUNK )




def audio_stream_UDP():

	BUFF_SIZE = 65536
	server_socket = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
	server_socket.setsockopt(socket.SOL_SOCKET,socket.SO_RCVBUF,BUFF_SIZE)

	server_socket.bind((host_ip, (port)))


	print('server listening at',(host_ip, (port)),wf.qsize())
	
	# stream = p.open(format=p.get_format_from_width(wf.getsampwidth()),
	# 				channels=wf.getnchannels(),
	# 				rate=wf.getframerate(),
	# 				input=True,
	# 				frames_per_buffer=CHUNK)

	data = None
	sample_rate = RATE
	while True:
		msg,client_addr = server_socket.recvfrom(BUFF_SIZE)
		print('[GOT connection from]... ',client_addr,msg)
		DATA_SIZE = math.ceil(wf.qsize()/CHUNK)
		DATA_SIZE = str(DATA_SIZE).encode()
		print('[Sending data size]...',wf.qsize()/sample_rate)
		server_socket.sendto(DATA_SIZE,client_addr)
		while True:
			
			data = wf.get(CHUNK)
			# if(data == 'q'):
			# 	break
			server_socket.sendto(data,client_addr)
			time.sleep(0.001) # Here you can adjust it according to how fast you want to send data keep it > 0
		break
	print('SENT...')            

t1 = threading.Thread(target=audio_stream_UDP, args=())
t2 = threading.Thread(target = record, args = (stream, CHUNK,))
# t3 = threading.Thread(target=console,args=(wf))

t2.start()
t1.start()
# t3.start()

t2.join()
# t3.join()
t1.join()