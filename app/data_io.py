"""
    Data IO module
"""

import speech_recognition as sr


audio_file = sr.AudioFile('test.wav')

recognizer = sr.Recognizer()
recognizer.recognize_google()
