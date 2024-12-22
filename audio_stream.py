# This script is to be run on the computer.
# Captures system audio and streams it to the Raspberry Pi via UDP


import socket
import pyaudio
import sounddevice as sd

RASPBERRY_PI_IP = "xxx.xxx.x.xxx"  # Replace with your Raspberry Pi's IP
PORT = 5000
CHUNK = 1024
RATE = 44100
FORMAT = pyaudio.paInt16
CHANNELS = 1

sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
server_address = (RASPBERRY_PI_IP, PORT)

# Set up audio input (default microphone)
p = pyaudio.PyAudio()
stream = p.open(format=FORMAT, channels=CHANNELS, rate=RATE, input=True, frames_per_buffer=CHUNK)

print(f"Streaming audio to {RASPBERRY_PI_IP}:{PORT}...")
try:
    while True:
        data = stream.read(CHUNK, exception_on_overflow=False)
        sock.sendto(data, server_address)
except KeyboardInterrupt:
    print("Stopping stream...")
finally:
    stream.stop_stream()
    stream.close()
    p.terminate()
    sock.close()
