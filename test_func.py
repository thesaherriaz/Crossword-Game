
import unittest
from game import Game

class TestGame(unittest.TestCase):
    def test_add_word(self):
        valid_words = ["HIS", "TOP", "USE", "KEY"]
        game = Game(7, 7, valid_words)
        
        self.assertTrue(game.add_word("HIS", 0, 0, "horizontal"))
        self.assertFalse(game.add_word("INVALID", 0, 0, "horizontal"))

    def test_provide_hint(self):
        valid_words = ["HIS", "TOP", "USE"]
        game = Game(7, 7, valid_words)
        hint = game.provide_hint()
        self.assertIn(hint, valid_words)
        self.assertLess(game.players[game.current_player].score, 0)

    def test_switch_player(self):
        valid_words = ["HIS", "TOP"]
        game = Game(7, 7, valid_words)
        self.assertEqual(game.current_player, 0)
        game.switch_player()
        self.assertEqual(game.current_player, 1)


if __name__ == "__main__":
    unittest.main()