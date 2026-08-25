"""
CODSOFT_TASKSNO - Task 1: Chatbot with Rule-Based Responses
Author: Deepak Joshi (0251CYS023)

A simple rule-based chatbot that uses pattern matching (regular expressions)
to understand user intent and respond appropriately. No external libraries
or internet connection required - runs anywhere Python 3 runs.

Concepts demonstrated:
    - Pattern matching with regex
    - Intent recognition via keyword/pattern rules
    - Simple conversational state (remembering the user's name)
    - Graceful fallback when no rule matches
"""

import random
import re
from datetime import datetime


class RuleBasedChatbot:
    """A chatbot that maps user input to a response using an ordered
    list of (pattern, response-generator) rules. The FIRST matching
    pattern wins, so rules are ordered from most specific to most
    general, ending with a catch-all fallback.
    """

    def __init__(self, bot_name: str = "CodBot"):
        self.bot_name = bot_name
        self.user_name = None
        # Each rule is (compiled_regex, list_of_possible_responses_or_callable)
        self.rules = self._build_rules()

    # ------------------------------------------------------------------
    # Rule definitions
    # ------------------------------------------------------------------
    def _build_rules(self):
        rules = [
            # Greetings
            (r"\b(hi|hello|hey|hola|yo)\b",
             ["Hello! How can I help you today?",
              "Hi there! What can I do for you?",
              "Hey! Good to see you."]),

            # Asking the bot's name
            (r"\bwhat.*(your|ur) name\b",
             [f"I'm {self.bot_name}, your friendly rule-based chatbot."]),

            # User introduces themselves -> remember it
            (r"\bmy name is (\w+)", self._handle_name),
            (r"\bi am (\w+)$", self._handle_name),
            (r"\bi'm (\w+)$", self._handle_name),

            # Ask for the time / date
            (r"\b(what.*time|current time)\b", self._handle_time),
            (r"\b(what.*date|today.*date|what day)\b", self._handle_date),

            # How are you
            (r"\bhow are you\b",
             ["I'm just a program, but I'm running smoothly! How about you?",
              "Doing great, thanks for asking!"]),

            # Feelings from the user
            (r"\bi (feel|am) (sad|down|upset|depressed)\b",
             ["I'm sorry to hear that. I'm just a simple bot, but I hope things get better soon.",
              "That sounds tough. Take care of yourself, and consider talking to someone you trust."]),
            (r"\bi (feel|am) (happy|great|good|excited)\b",
             ["That's wonderful to hear! Keep that energy up.",
              "Awesome! Glad you're doing well."]),

            # Thanks
            (r"\b(thanks|thank you|thx)\b",
             ["You're welcome!", "No problem at all!", "Happy to help!"]),

            # Bot capabilities
            (r"\bwhat can you do\b",
             ["I can chat with you, tell you the time/date, and answer a few "
              "predefined questions. I use pattern matching, not real AI, "
              "so my knowledge is limited to my rule set."]),

            # Small talk: weather (bot honestly admits it has no live data)
            (r"\bweather\b",
             ["I don't have access to live weather data, but I hope it's nice outside!"]),

            # Jokes
            (r"\b(joke|make me laugh)\b",
             ["Why do programmers prefer dark mode? Because light attracts bugs!",
              "I told my computer I needed a break, and it said 'No problem, "
              "I'll go to sleep.'",
              "Why do Python programmers wear glasses? Because they can't C."]),

            # Help
            (r"\b(help|assist)\b",
             ["Sure - try asking me my name, the time, the date, or just say hi. "
              "Type 'bye' or 'exit' whenever you want to leave."]),

            # Farewell (checked explicitly in the main loop too, kept here
            # so free-form goodbyes are also caught)
            (r"\b(bye|goodbye|see you|farewell)\b",
             ["Goodbye! Have a great day!", "See you later!", "Bye! Take care."]),
        ]
        # Pre-compile all regex patterns (case-insensitive)
        return [(re.compile(pattern, re.IGNORECASE), response)
                for pattern, response in rules]

    # ------------------------------------------------------------------
    # Special handlers (used when a rule needs logic, not just text)
    # ------------------------------------------------------------------
    def _handle_name(self, match: re.Match) -> str:
        self.user_name = match.group(1).capitalize()
        return f"Nice to meet you, {self.user_name}!"

    def _handle_time(self, match: re.Match) -> str:
        return f"The current time is {datetime.now().strftime('%I:%M %p')}."

    def _handle_date(self, match: re.Match) -> str:
        return f"Today's date is {datetime.now().strftime('%A, %B %d, %Y')}."

    # ------------------------------------------------------------------
    # Core response logic
    # ------------------------------------------------------------------
    def get_response(self, user_input: str) -> str:
        """Match user_input against the rule set and return a response.
        Falls back to a default message if nothing matches.
        """
        text = user_input.strip()
        if not text:
            return "Please type something so I can help you."

        for pattern, response in self.rules:
            match = pattern.search(text)
            if match:
                if callable(response):
                    return response(match)
                return random.choice(response)

        # Fallback -> personalize with name if we know it
        fallback = [
            "I'm not sure I understand. Could you rephrase that?",
            "Hmm, I don't have a rule for that yet. Try asking about the time, date, or say hi!",
            "Sorry, I didn't quite catch that.",
        ]
        if self.user_name:
            fallback.append(f"I'm not sure what you mean, {self.user_name}. "
                             f"Could you try rephrasing?")
        return random.choice(fallback)


def run_cli():
    """Interactive command-line loop."""
    bot = RuleBasedChatbot()
    print(f"{bot.bot_name}: Hello! I'm {bot.bot_name}, a rule-based chatbot. "
          f"Type 'bye' or 'exit' to quit.\n")

    exit_words = {"bye", "exit", "quit", "goodbye"}

    while True:
        try:
            user_input = input("You: ")
        except (EOFError, KeyboardInterrupt):
            print(f"\n{bot.bot_name}: Goodbye!")
            break

        if user_input.strip().lower() in exit_words:
            print(f"{bot.bot_name}: Goodbye! Have a great day!")
            break

        reply = bot.get_response(user_input)
        print(f"{bot.bot_name}: {reply}")


if __name__ == "__main__":
    run_cli()
