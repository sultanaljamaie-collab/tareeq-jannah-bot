from gtts import gTTS

def speak(text):

    formatted_text = f"""
أهلاً بك في مسابقة طريق الجنة.

{text}

اختر الإجابة الصحيحة.
"""

    filename = "voice.mp3"

    tts = gTTS(
        text=formatted_text,
        lang="ar",
        slow=False
    )

    tts.save(filename)

    return filename
