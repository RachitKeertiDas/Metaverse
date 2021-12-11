import pyaudio
import socket
from threading import Thread
import sys

frames = []
hosts = ['117.214.44.62']
port = 12000
def udpStreamIn():
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    while True:
        soundData, addr = udp.recvfrom(CHUNK * 2 * CHANNELS)
        frames.append(soundData)
    
    udp.close()


def record(stream, CHUNK):
    while True:
        frames.append(stream.read(CHUNK))

def udpStreamOut(CHUNK):
    udp = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
    udp.bind(("192.168.0.188", 12000))
    while True:
        if len(frames) > 0:
            data = frames.pop(0)
            for host in hosts:
                udp.sendto(data, (host, port))
    

    udp.close()

def play(stream, CHUNK):
    BUFFER = 10
    while True:
            if len(frames) == BUFFER:
                while True:
                    if len(frames) > 0:
                        stream.write(frames.pop(0), CHUNK)

if __name__ == '__main__':
    CHUNK = 1024
    FORMAT = pyaudio.paInt16
    CHANNELS = 2
    RATE = 44100

    p = pyaudio.PyAudio()

    if len(sys.argv) < 2:
        print('Please specify either server or client')
        sys.exit(0)
    if sys.argv[1] == 'INPUT':    
        stream = p.open(format = FORMAT, channels = CHANNELS, rate = RATE,  output = True, frames_per_buffer = CHUNK )
        Tr = Thread(target = play, args = (stream, CHUNK,))
        Ts = Thread(target = udpStreamIn)
    else:
        stream = p.open(format=FORMAT, channels = CHANNELS, rate = RATE, input = True, frames_per_buffer = CHUNK)    
        Ts = Thread(target = udpStreamOut, args=(CHUNK,))
        Tr = Thread(target = record, args=(stream, CHUNK,))
    Tr.setDaemon(True)
    Ts.setDaemon(True)
    Tr.start()
    Ts.start()
    Tr.join()
    Ts.join()