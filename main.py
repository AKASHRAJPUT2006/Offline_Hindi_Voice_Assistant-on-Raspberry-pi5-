from vosk import Model, KaldiRecognizer
import pyaudio
import json
import os

#  IMPORT INTENT MODULE
from intent import recognize_intent, handle_intent

MODEL_PATH = "/home/akash/vosk_models/vosk-model-small-hi-0.22"
SAMPLE_RATE = 44100
FRAMES = 4096

def speak(text):
    os.system(
        
        f'espeak-ng -v hi -s 160 -p 50 -a 180 --stdout "{text}" | pw-play -'
    )


# Load Vosk model
model = Model(MODEL_PATH)
recognizer = KaldiRecognizer(model, SAMPLE_RATE)

p = pyaudio.PyAudio()

# Auto-detect microphone
MIC_INDEX = None
for i in range(p.get_device_count()):
    if p.get_device_info_by_index(i).get("maxInputChannels", 0) > 0:
        MIC_INDEX = i
        print(f"Using mic {i}: {p.get_device_info_by_index(i)['name']}")
        break

if MIC_INDEX is None:
    raise RuntimeError("No microphone detected")

stream = p.open(
    format=pyaudio.paInt16,
    channels=1,
    rate=SAMPLE_RATE,
    input=True,
    input_device_index=MIC_INDEX,
    frames_per_buffer=FRAMES
)


startup_message = "आपका स्वागत है, मैं आपकी कैसे मदद कर सकता हूँ?"
print(startup_message)
speak(startup_message)

stream.start_stream()

try:
    while True:
        data = stream.read(FRAMES, exception_on_overflow=False)

        if recognizer.AcceptWaveform(data):
            result = json.loads(recognizer.Result())
            text = result.get("text", "")

            if text:
                print(" सुना गया:", text)

                intent = recognize_intent(text)
                print("Intent:", intent)

                response = handle_intent(intent)
                speak(response)

                if intent == "EXIT":
                    break

except KeyboardInterrupt:
    pass

finally:
    stream.stop_stream()
    stream.close()
    p.terminate()