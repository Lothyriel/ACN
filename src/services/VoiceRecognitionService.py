import string
import speech_recognition as sr


def speech_to_text(bytes) -> string:
    r = sr.Recognizer()
    test_audio = sr.AudioFile(bytes)
    with test_audio as source:
        audio_data = r.record(source)
        return r.recognize_google(audio_data, language="pt-BR")
