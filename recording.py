# -*- coding: utf-8 -*-

u"""
生活音の録音を行う
"""
import pyaudio
import wave
from pylab import *
from numpy import *

FORMAT = pyaudio.paInt16
#FORMAT = pyaudio.paInt24
#FORMAT = pyaudio.paInt32
CHANNELS = 1
RATE = 44100
CHUNK = 2**10
RECORD_SECONDS = 10

#WAVE_OUTPUT_FILENAME = "senmendai1/1_mizuoto1/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/2_tearai/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/3_handwash/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/4_kao/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/5_voice/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/6_muon/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/7_ugai/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/8_hamigaki/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1/9_ugai_only/4.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1_server/1_mizuoto2/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1_server/2_tearai/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1_server/3_handwash/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1_server/4_kao/1.wav"
#WAVE_OUTPUT_FILENAME = "senmendai1_server/5_voice/1.wav"
#WAVE_OUTPUT_FILENAME = "daidokoro1_server/6_muon/4.wav"
#WAVE_OUTPUT_FILENAME = "daidokoro1_server/7_ugai/4.wav"
#WAVE_OUTPUT_FILENAME = "daidokoro1_server/8_hamigaki/1.wav"
#WAVE_OUTPUT_FILENAME = "daidokoro1_server/9_ugai_only/4.wav"
#WAVE_OUTPUT_FILENAME = "daidokoro1_server/9_ugai_only/4.wav"
#WAVE_OUTPUT_FILENAME = "./rec_white_noise.wav"
WAVE_OUTPUT_FILENAME = "./rec_white_noise1.wav"
#WAVE_OUTPUT_FILENAME = "./test1.wav"

audio = pyaudio.PyAudio()
stream = audio.open(format=FORMAT, channels=CHANNELS,
                rate=RATE, input=True,
                input_device_index=2, 
                frames_per_buffer=CHUNK)
print ("recording...")

frames = []
inp = []
for i in range(0, int(RATE / CHUNK * RECORD_SECONDS)):
    data = stream.read(CHUNK)
    frames.append(data)
print ("finished recording")

stream.stop_stream()
stream.close()
audio.terminate()

waveFile = wave.open(WAVE_OUTPUT_FILENAME, 'wb')
waveFile.setnchannels(CHANNELS)
waveFile.setsampwidth(audio.get_sample_size(FORMAT))
waveFile.setframerate(RATE)
waveFile.writeframes(b''.join(frames))
waveFile.close()

