import unittest

from src.services.VoiceRecognitionService import speech_to_text
from src.util.IO import get_file_bytes


class VoiceAITest(unittest.TestCase):
    def test_audio_negro(self):
        bytes = get_file_bytes("tests/data/sound_test.wav")
        self.assertTrue("negro" in speech_to_text(bytes))


if __name__ == '__main__':
    unittest.main()
