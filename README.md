

# soundwave-rpi-matrix

A simple real-time audio visualizer that streams microphone input from a computer to a Raspberry Pi and renders a live waveform on a 64×32 RGB LED matrix using the **rpi-rgb-led-matrix** library.
![IMG_4765](https://github.com/user-attachments/assets/c072740f-ed5b-4768-ad4a-793d0592d50b)
---

## Overview

This project is split into two components:

* **Audio Streamer (Computer)** – Captures microphone audio and sends raw PCM data over UDP.
* **Waveform Renderer (Raspberry Pi)** – Receives audio packets and displays a scrolling waveform on an RGB LED matrix.

The result is a low-latency, hardware-based soundwave visualization driven entirely by live audio input.

---

## Features

* Real-time waveform rendering on a 64×32 LED matrix
* UDP-based audio streaming for low latency
* Automatic amplitude normalization with smoothing
* Line interpolation for a continuous waveform display
* Minimal dependencies and simple architecture

---

## Hardware Requirements

* Raspberry Pi (Pi 3 / Pi 4 recommended)
* 64×32 RGB LED matrix panel
* RGB matrix HAT or compatible adapter (e.g., Adafruit RGB Matrix HAT)
* Computer with a microphone

---

## Software Requirements

### Raspberry Pi

* Python 3
* [`rpi-rgb-led-matrix`](https://github.com/hzeller/rpi-rgb-led-matrix)
* `numpy`

### Computer

* Python 3
* `pyaudio`

---

## Installation

### Raspberry Pi Setup

1. Install and configure **rpi-rgb-led-matrix** following its official documentation.
2. Install Python dependencies:

```bash
pip3 install numpy
```

3. Copy `led_waveform.py` to the Raspberry Pi.

---

### Computer Setup

1. Install `pyaudio`:

```bash
pip install pyaudio
```

> You may need PortAudio development packages depending on your OS.

2. Copy `audio_stream.py` to your computer.

---

## Configuration

### Set Raspberry Pi IP Address

In `audio_stream.py`, update the following line:

```python
RASPBERRY_PI_IP = "<your_pi_ip_here>"
```

### LED Matrix Settings

In `led_waveform.py`, adjust these values to match your hardware if needed:

```python
options.rows = 32
options.cols = 64
options.hardware_mapping = 'adafruit-hat'
options.gpio_slowdown = 4
options.brightness = 45
```

---

## Usage

### 1. Start the LED Visualizer (Raspberry Pi)

Run with root privileges (required by `rpi-rgb-led-matrix`):

```bash
sudo python3 led_waveform.py
```

You should see:

```text
Listening for audio...
```

---

### 2. Start Audio Streaming (Computer)

```bash
python audio_stream.py
```

You should see:

```text
Streaming audio to <pi-ip>:5000...
```

Audio picked up by the microphone will now be visualized on the LED matrix.

---

## Notes and Limitations

* Audio is streamed as raw 16-bit mono PCM over UDP (no compression or error correction).
* Packet loss may cause brief visual artifacts.
* Uses microphone input by default (not system audio loopback).
* UDP port **5000** must be open and reachable on the Raspberry Pi.

