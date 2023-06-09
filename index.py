import speech_recognition as sr
import wave
from deep_translator import GoogleTranslator
import json
import pyaudio

FORMAT = pyaudio.paInt16
CHANNELS = 1
RATE = 44100
CHUNK = 1024
RECORD_SECONDS = 5
WAVE_OUTPUT_FILENAME = "signals.wav"

# initialize things
r = sr.Recognizer()
# record audio from microphone
with sr.Microphone() as source:
    print('Speak now...')
    audio = r.listen(source, timeout=15)
# save file
with wave.open("recorded_audio.wav", "wb") as wav_file:
    wav_file.setnchannels(1)
    wav_file.setsampwidth(audio.sample_width)
    wav_file.setframerate(audio.sample_rate)
    wav_file.writeframes(audio.get_wav_data())
# save audio
with open("recorded_audio.wav", "wb") as f:
    f.write(audio.get_wav_data())
# recognize speech
try:
    with open('signals.json', 'r') as f:
        mapping = json.load(f)

    text = r.recognize_google(audio, language='pt-Br')
    print('Recognized text: ', text)

    for key in mapping.keys():
        text = text.replace(key, mapping[key])
    print('Texto transformado', text)

except sr.UnknownValueError:
    print('Speech recognition could not understand the audio')
except sr.RequestError as e:
    print('Error: ', e)
