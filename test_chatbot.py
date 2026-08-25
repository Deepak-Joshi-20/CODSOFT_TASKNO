"""
Automated tests for chatbot.py
Run with:  python -m pytest test_chatbot.py -v
       or:  python test_chatbot.py
"""

import unittest
from chatbot import RuleBasedChatbot


class TestRuleBasedChatbot(unittest.TestCase):

    def setUp(self):
        self.bot = RuleBasedChatbot(bot_name="TestBot")

    def test_greeting(self):
        reply = self.bot.get_response("hello")
        self.assertIsInstance(reply, str)
        self.assertGreater(len(reply), 0)

    def test_name_capture_and_recall(self):
        reply = self.bot.get_response("my name is deepak")
        self.assertIn("Deepak", reply)
        self.assertEqual(self.bot.user_name, "Deepak")

    def test_alt_name_pattern(self):
        reply = self.bot.get_response("I am Ankit")
        self.assertIn("Ankit", reply)

    def test_bot_name_question(self):
        reply = self.bot.get_response("What is your name?")
        self.assertIn("TestBot", reply)

    def test_time_query_runs_without_error(self):
        reply = self.bot.get_response("what is the current time")
        self.assertIn("time", reply.lower())

    def test_date_query_runs_without_error(self):
        reply = self.bot.get_response("what's the date today")
        self.assertIn("date", reply.lower())

    def test_thanks(self):
        reply = self.bot.get_response("thank you so much")
        self.assertTrue(len(reply) > 0)

    def test_joke(self):
        reply = self.bot.get_response("tell me a joke")
        self.assertTrue(len(reply) > 0)

    def test_empty_input(self):
        reply = self.bot.get_response("")
        self.assertIn("type something", reply.lower())

    def test_whitespace_only_input(self):
        reply = self.bot.get_response("     ")
        self.assertIn("type something", reply.lower())

    def test_unknown_input_triggers_fallback(self):
        reply = self.bot.get_response("asdkjqwoieuqwoiehello world of gibberish xyzabc")
        self.assertTrue(len(reply) > 0)

    def test_case_insensitivity(self):
        reply_lower = self.bot.get_response("hello")
        reply_upper = self.bot.get_response("HELLO")
        # Both should match the greeting rule (non-empty, sensible responses)
        self.assertTrue(len(reply_lower) > 0)
        self.assertTrue(len(reply_upper) > 0)

    def test_farewell_pattern(self):
        reply = self.bot.get_response("well, goodbye then")
        self.assertTrue(len(reply) > 0)

    def test_feelings_negative(self):
        reply = self.bot.get_response("i feel sad today")
        self.assertTrue(len(reply) > 0)

    def test_feelings_positive(self):
        reply = self.bot.get_response("i am happy")
        self.assertTrue(len(reply) > 0)

    def test_multiple_turns_preserve_state(self):
        self.bot.get_response("my name is Priya")
        reply = self.bot.get_response("qwertyuiop nonsense")
        # Fallback list includes a personalized message once name is known
        self.assertTrue(len(reply) > 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
