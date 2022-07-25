import unittest

from src.services.VoiceRecognitionService import speech_to_text
from src.util.IO import get_file_bytes


class VoiceAITest(unittest.TestCase):
    def test_audio_negro(self):
        bytes = get_file_bytes("tests/data/negro_sound.wav")
        text = speech_to_text(bytes)
        self.assertTrue("negro" in text)

    def test_audio_tuco(self):
        bytes = get_file_bytes("tests/data/tuco_sound.wav")
        text = speech_to_text(bytes)
        self.assertTrue("trabalha" in text)


if __name__ == '__main__':
    unittest.main()
