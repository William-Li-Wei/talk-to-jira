"""
    Testing Data IO
"""

import os

from speech_recognition import AudioData

from app import data_io


resource_path = os.path.abspath(os.path.join(os.path.dirname(os.path.abspath(__file__)), '../resources/'))


def test_record_audio_from_file():
    """test record_audio_from_file"""

    sample_audio_path = os.path.join(resource_path, 'sample_speech.wav')
    audio = data_io.record_audio_from_file(sample_audio_path)

    assert isinstance(audio, AudioData)


def test_record_audio_from_microphone():
    """test record_audio_from_microphone"""

    audio = data_io.record_audio_from_microphone()

    assert isinstance(audio, AudioData)


def test_recognize_speech_from_audio():
    """test recognize_speech_from_audio"""

    sample_audio_path = os.path.join(resource_path, 'sample_speech.wav')
    audio = data_io.record_audio_from_file(sample_audio_path)
    text = data_io.recognize_speech_from_audio(audio)
    text = text.lower()

    expected = "every word and phrase he speaks is true"

    assert text.startswith(expected)
