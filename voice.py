from gtts import gTTS

def speak(text):

    filename = "voice.mp3"

    tts = gTTS(text=text, lang="ar")

    tts.save(filename)

    return filename
