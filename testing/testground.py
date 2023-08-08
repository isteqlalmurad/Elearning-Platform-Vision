from gtts import gTTS
import os

def text_to_speech(text, lang, filename):
    tts = gTTS(text=text, lang=lang, slow=True)
    tts.save(filename)

def play_audio_file(filename):
    os.system("mpg321 " + filename)

text = "Hello, my name is khan and I am not a terrorist did you git that?"
lang = 'en'
filename = "output.mp3"

text_to_speech(text, lang, filename)
play_audio_file(filename)
