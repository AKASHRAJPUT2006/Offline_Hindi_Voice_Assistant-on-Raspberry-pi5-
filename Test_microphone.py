# Testing of microphone for sample rate, mic index etc.

# Find PyAudio index for that mic


import pyaudio

p = pyaudio.PyAudio()
for i in range(p.get_device_count()):
    info = p.get_device_info_by_index(i)
    print(i, info["name"], "inputs:", info["maxInputChannels"])

python list_mics.py
