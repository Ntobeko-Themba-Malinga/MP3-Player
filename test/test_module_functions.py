import unittest
from music_player import main


class ModuleFunctionsTest(unittest.TestCase):

    @classmethod
    def setUpClass(cls):
        main.songs = [
            'test/songs/a.mp3',
            'test/songs/b.mp3',
            'test/c.mp3',
            'test/d.mp3',
            'test/e.mp3',
        ]

    def test_1_load_song_function(self):
        main.load_song()
        self.assertTrue(main.mixer.get_busy())

    def test_2_pause_function(self):
        main.load_song()
        main.pause()
        self.assertFalse(main.mixer.get_busy())

    def test_3_play_function(self):
        main.load_song()
        main.pause()
        main.play()
        self.assertTrue(main.mixer.get_busy())
