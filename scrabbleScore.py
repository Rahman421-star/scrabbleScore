import unittest
import random
import time
import requests

LETTER_SCORES = {
    'A': 1, 'E': 1, 'I': 1, 'O': 1, 'U': 1,
    'L': 1, 'N': 1, 'R': 1, 'S': 1, 'T': 1,
    'D': 2, 'G': 2,
    'B': 3, 'C': 3, 'M': 3, 'P': 3,
    'F': 4, 'H': 4, 'V': 4, 'W': 4, 'Y': 4,
    'K': 5,
    'J': 8, 'X': 8,
    'Q': 10, 'Z': 10
}
"""Calculate the scrabble score for a given word."""
def get_scrabble_score(word):
    score = 0
    word = word.upper()  # Handle both upper and lower case letters
    for letter in word:
        if letter in LETTER_SCORES:
            score += LETTER_SCORES[letter]
    return score

"""Check if the word is valid using an online dictionary API."""
def is_valid_word(word):
    url = f"https://api.dictionaryapi.dev/api/v2/entries/en/{word}"
    response = requests.get(url)
    return response.status_code == 200

"""Function to play a Scrabble game with all the requirements."""
def play_scrabble_game():
    total_score = 0
    rounds = 10  # Maximum number of rounds
    for round_number in range(1, rounds + 1):
        print(f"\nRound {round_number}")

        # Generate a random word length
        word_length = random.randint(3, 7)
        print(f"Enter a word with {word_length} letters. You have 15 seconds.")

        # Start the timer
        start_time = time.time()

        while True:
            user_word = input("Enter your word: ").strip()

            # Check if the user wants to quit
            if user_word.lower() == 'quit':
                print("You chose to quit the game.")
                print(f"Your total score is: {total_score}")
                return

            # Check word length
            if len(user_word) != word_length:
                print(f"Invalid word length! You need to enter a word with {word_length} letters.")
                continue

            # Check if the word contains only alphabetic characters
            if not user_word.isalpha():
                print("Invalid input! Please enter a word with only alphabetic characters.")
                continue

            # Validate the word using the dictionary API
            if not is_valid_word(user_word):
                print("Invalid word. Please enter a valid word from the dictionary.")
                continue

            # If all validations pass, break the loop
            break

        # Calculate how long the user took to enter the word
        end_time = time.time()
        time_taken = end_time - start_time

        # Calculate the score for the word
        round_score = get_scrabble_score(user_word)

        # Add a bonus based on how quickly the user entered the word
        if time_taken < 15:
            round_score += (15 - int(time_taken))

        total_score += round_score
        print(f"Score for '{user_word}': {round_score}. Total score: {total_score}")

    print(f"Game over! Your total score is: {total_score}")


# Unit Tests for TDD
class TestScrabbleGame(unittest.TestCase):
    def test_scrabble_score(self):
        # Test if scrabble scores are calculated correctly
        self.assertEqual(get_scrabble_score("cabbage"), 14)
        self.assertEqual(get_scrabble_score("apple"), 9)
        self.assertEqual(get_scrabble_score("Assignment"), 13)
        self.assertEqual(get_scrabble_score("XylophOne"), 24)

    def test_valid_word(self):
        # Test if valid words are recognized
        self.assertTrue(is_valid_word("apple"))
        self.assertTrue(is_valid_word("assignment"))

    def test_invalid_word(self):
        # Test if invalid words are rejected
        self.assertFalse(is_valid_word("zzzzzzzz"))  # Assuming this isn't a real word
        self.assertFalse(is_valid_word("123"))       # Numbers are not valid

if __name__ == "__main__":
    # Run the game
    play_scrabble_game()

    # Run unit tests
    unittest.main(exit=False)
