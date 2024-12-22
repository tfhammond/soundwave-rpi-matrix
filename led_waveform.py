# This script is to be run on the Raspberry Pi
# Receives audio data via UDP and displays it as a waveform on the LED matrix


import socket
import numpy as np
from rgbmatrix import RGBMatrix, RGBMatrixOptions
import time

# LED Matrix configuration
options = RGBMatrixOptions()
options.rows = 32
options.cols = 64
options.chain_length = 1
options.parallel = 1
options.hardware_mapping = 'adafruit-hat'  # Adjust if needed
options.gpio_slowdown = 4 # Not needed if sodered
options.brightness = 45 # Adjust if needed
matrix = RGBMatrix(options=options)


max_amplitude = 1


PORT = 5000
sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
sock.bind(('0.0.0.0', PORT))

def display_waveform(audio_data):
    global max_amplitude
    matrix.Clear()

    # LED matrix dimensions
    height, width = 32, 64
    center = height // 2

    # Downsample with averaging for smoother transitions
    step = max(1, len(audio_data) // width)
    downsampled = np.array([np.mean(audio_data[i:i + step]) for i in range(0, len(audio_data), step)])[:width]

    # Smooth scaling with a rolling maximum
    max_amplitude = max(max_amplitude * 0.9, max(abs(downsampled)))
    normalized = (downsampled / max_amplitude) * (height // 2)

    # Draw the wave
    prev_y = None
    for x in range(len(normalized)):
        y = int(center + normalized[x])
        if 0 <= y < height:
            matrix.SetPixel(x, y, 255, 255, 255)  # White pixel
            if prev_y is not None:
                draw_line(matrix, x - 1, prev_y, x, y, 255, 255, 255)
            prev_y = y

def draw_line(matrix, x0, y0, x1, y1, r, g, b):
    """Drawing a line on the LED matrix using Bresenham's algorithm"""
    dx = abs(x1 - x0)
    dy = abs(y1 - y0)
    sx = 1 if x0 < x1 else -1
    sy = 1 if y0 < y1 else -1
    err = dx - dy

    while True:
        if 0 <= x0 < 64 and 0 <= y0 < 32:
            matrix.SetPixel(x0, y0, r, g, b)
        if x0 == x1 and y0 == y1:
            break
        e2 = 2 * err
        if e2 > -dy:
            err -= dy
            x0 += sx
        if e2 < dx:
            err += dx
            y0 += sy

print("Listening for audio...")
try:
    while True:
        data, _ = sock.recvfrom(2048)
        audio_data = np.frombuffer(data, dtype=np.int16)
        display_waveform(audio_data)
        time.sleep(0.01)
except KeyboardInterrupt:
    print("Stopping...")
finally:
    sock.close()
