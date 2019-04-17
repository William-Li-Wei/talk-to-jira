"""
    Data IO module
"""

from speech_recognition import Recognizer
from speech_recognition import Microphone, AudioFile
from speech_recognition import AudioData
from speech_recognition import RequestError, UnknownValueError


def record_audio_from_file(audio_path: str):
    """
    captures audio data from a file

    Args:
        audio_path(str): path to the audio file

    Returns:
        audio: instance of AudioData
    """

    recognizer = Recognizer()
    with AudioFile(audio_path) as source:
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.record(source)

    return audio


def record_audio_from_microphone():
    """
    captures audio data from microphone

    Args:

    Returns:
        audio: instance of AudioData
    """

    recognizer = Recognizer()

    with Microphone() as source:
        print('>>> processing noise ...')
        recognizer.adjust_for_ambient_noise(source)
        print('>>> say something.')
        audio = recognizer.listen(source)
        print('>>> audio captured.')

    return audio


def recognize_speech_from_audio(audio: AudioData, engine: str = "google"):
    """
    returns the recognized text

    Args:
        audio(AudioData): input audio source
        engine(str, optional): the engine used for recognizing speech, default to "google", should be one of:
            google, google_cloud, bing, houndify, ibm, sphinx and wit

    Returns:
        text: recognized text or None
    """

    text = None
    recognizer = Recognizer()

    try:
        if engine == "google":
            text = recognizer.recognize_google(audio)
        if engine == "google_cloud":
            text = recognizer.recognize_google(audio)
        if engine == "bing":
            text = recognizer.recognize_google(audio)
        if engine == "houndify":
            text = recognizer.recognize_google(audio)
        if engine == "ibm":
            text = recognizer.recognize_google(audio)
        if engine == "sphinx":
            text = recognizer.recognize_google(audio)
        if engine == "wit":
            text = recognizer.recognize_google(audio)
    except UnknownValueError:
        print("Recognition engine({engine}) could not understand audio.".format(engine=engine))
    except RequestError as e:
        print("Could not request results from Recognition engine({engine}); {err}.".format(engine=engine, err=e))

    return text


def read_from_microphone(message: str = None):
    print(message)
    audio = record_audio_from_microphone()
    text = recognize_speech_from_audio(audio)
    return text


def read_from_keyboard(message: str = None):
    return input(message)
