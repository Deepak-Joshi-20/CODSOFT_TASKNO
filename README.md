# Task 1 — Chatbot with Rule-Based Responses

A simple chatbot that uses **pattern matching (regex)** to understand user
input and respond with predefined rules. No internet or external libraries
required — pure Python 3 standard library only.

## How it works
- User input is checked against an ordered list of regex patterns.
- The first pattern that matches determines the response.
- Some rules (name capture, time, date) run small handler functions instead
  of returning static text, so the bot can hold minimal state (e.g. it
  remembers your name for the rest of the conversation).
- If nothing matches, a friendly fallback message is shown.

## Run it
```bash
python3 chatbot.py
```
Type `bye`, `exit`, or `quit` anytime to end the conversation.

## Run the tests
```bash
python3 -m unittest test_chatbot.py -v
```
16/16 tests passing — covers greetings, name capture, time/date queries,
case-insensitivity, empty input, and fallback behavior.

## Example conversation
```
CodBot: Hello! I'm CodBot, a rule-based chatbot. Type 'bye' or 'exit' to quit.

You: hi
CodBot: Hi there! What can I do for you?
You: my name is Deepak
CodBot: Nice to meet you, Deepak!
You: what time is it
CodBot: The current time is 12:54 PM.
You: bye
CodBot: Goodbye! Have a great day!
```
