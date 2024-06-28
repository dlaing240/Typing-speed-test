import random
from tkinter import END
import json
import datetime

from home_ui import HomeUI
from word_data import word_list, weights
from results_io import ResultsInOut


class TypingTestLogic:
    """
    Class that handles the functionality of the typing tests.

    Attributes
    ----------
    root : tkinter.Tk
        The parent of the home UI.
    home_ui : HomeUI
        Instance of the HomeUI class.
    text : tkinter.Text
        Tkinter text widget which is used to display the words during the test.
    timer_txt : tkinter.Label
        Tkinter label widget which displays the timer.
    start_buttons : list
        List of Tkinter buttons which set up the tests.
    results_io : ResultsInOut
        Instance of the ResultsInOut class.
    current_word : int
        Tracks which word of the test the user is currently typing.
    current_char : int
        Tracks which character of the current word the user is typing.
    page_num : int
        Tracks which page of words the user is currently on.
    test_words : list
        List to store the words selected for a test.
    test_duration : int
        Duration of the current test.
    left : int
        A marker for the left index of the test words to be displayed on the current page.
    right : int
        A marker for the right index of the test words to be displayed on the current page.
    space_counts : int
        A tracker for the number of times the spacebar has been pressed.
    test_started : bool
        The state of the current test.
    user_input : list
        A list to store the characters typed by the user during the test.
    """
    def __init__(self, root, home_ui: HomeUI, results_io: ResultsInOut):
        """
        Initialises the attributes needed for the tests and configures the functionality of the start buttons.

        Parameters
        ----------
        root : tkinter.Tk
            The parent of the home UI.
        home_ui : HomeUI
            Instance of the HomeUI class.
        results_io : ResultsInOut
            Instance of the ResultsInOut class.
        """
        self.root = root
        self.home_ui = home_ui
        self.text = home_ui.text
        self.timer_txt = home_ui.timer_txt
        self.start_buttons = home_ui.start_buttons

        self.results_io = results_io

        # Configure buttons to set up tests
        self.start_buttons[0].configure(command=self.test_15s)
        self.start_buttons[1].configure(command=self.test_30s)
        self.start_buttons[2].configure(command=self.test_60s)

        # Binds user-input detection to the timer widget; key presses are only registered when the timer is in focus.
        self.timer_txt.bind('<space>', self.check_word)
        self.timer_txt.bind('<Key>', self.check_char)

        # cursor position
        self.current_word = 0
        self.current_char = 0
        self.page_num = 0

        # Attributes for typing and text
        self.test_words = []
        self.test_duration = 15
        self.left = None
        self.right = None
        self.space_counts = 0
        self.test_started = False
        self.user_input = []
        self.excess_chars = 0

        # Prevent the focus from changing to the text widget when it is clicked on.
        self.text.bind('<Button-1>', self.mouse_click)

        self.setup_test()

    def mouse_click(self, event):
        """
        Interrupts the usual behaviour when a widget is clicked on.
        """
        return "break"

    def test_15s(self):
        """
        Bound to the button to start a 15-second test.
        Sets the test duration to 15 seconds and calls the setup_test() method.
        """
        self.test_duration = 15
        self.setup_test()

    def test_30s(self):
        """
        Bound to the button to start a 30-second test.
        Sets the test duration to 30 seconds and calls the setup_test() method.
        """
        self.test_duration = 30
        self.setup_test()

    def test_60s(self):
        """
        Bound to the button to start a 60-second test.
        Sets the test duration to 60 seconds and calls the setup_test() method.
        """
        self.test_duration = 60
        self.setup_test()

    def setup_test(self):
        """
        Carries out the procedure to set up a test.
        """
        self.text['state'] = 'normal'  # Makes text widget editable
        self.generate_words()
        self.test_started = False  # The timer doesn't start counting down until the user starts typing
        self.home_ui.test_focus = True
        self.prepare_user_input()

    def generate_words(self):
        """
        Randomly selects a list of words for the test.
        """
        self.test_words = (random.choices(word_list, weights=weights, k=200))  # The weighting makes 5-letter words the most likely
        self.left, self.right = 0, 31
        self.text.delete(1.0, END)
        self.text.insert(1.0, " ".join(self.test_words[self.left:self.right]))
        self.tag_last_word()

    def tag_last_word(self):
        """
    `   Highlights the last word to indicate that it is part of the next page.
        """
        self.text.tag_remove("last_word", 1.0, END)
        last_word_len = len(self.test_words[self.right - 1])
        self.text.tag_add("last_word", f"end-{last_word_len + 1}c", END)

    def prepare_user_input(self):
        """
        Resets the cursor position and listens for user input.
        """
        # Reset cursor
        self.current_word = 0
        self.current_char = 0
        self.page_num = 0
        self.space_counts = 0
        self.user_input = []
        self.excess_chars = 0

        # Prepare timer for test
        self.timer_txt.grid()
        self.timer_txt.focus_set()  # Starts listening to user input
        self.timer_txt.configure(text=f"Timer begins when you start typing ({self.test_duration}s)")

    def start_test(self):
        """
        Hides the button bar and starts the countdown.
        """
        self.test_started = True
        # hide the button bar
        self.home_ui.start_buttons_frame.grid_remove()
        self.home_ui.utility_buttons_frame.grid_remove()

        self.countdown(self.test_duration)

    def countdown(self, seconds):
        """
        Updates the timer every second until it reaches zero.

        Parameters
        ----------
        seconds : int
            The number of seconds left in the countdown.
        """
        # End condition
        if seconds < 0:
            self.timer_txt.focus_set()
            self.stop_test()
        else:
            # After 1000ms, update the timer
            self.timer_txt.config(text=seconds)
            self.root.after(1000, self.countdown, seconds - 1)

    def get_char_index(self):
        """
        Uses the cursor position to obtain the index for the current character in the list of test words.
        """
        index = self.current_char + self.excess_chars
        for i in range(0 + self.page_num * 30, self.current_word + self.page_num * 30):
            index += len(self.test_words[i]) + 1
        return index

    def back_space(self, word):
        """
        Handles the response when backspace is pressed.

        Parameters
        ----------
        word : str
            The word currently being typed by the user.
        """
        if not self.current_char:  # Space has just been pressed so they can no longer edit the previous word
            return

        self.user_input.pop()  # Remove the last character input

        if self.current_char > len(word):  # Delete excess characters
            self.current_char -= 1
            index = self.get_char_index()
            self.text.delete(f"1.{index}", f"1.{index+1}")
            return

        self.current_char -= 1  # Move the cursor back a step

        # remove the deleted character's tag
        index = self.get_char_index()
        self.text.tag_remove("correct", f"1.{index}", f"1.{index + 1}")
        self.text.tag_remove("incorrect", f"1.{index}", f"1.{index + 1}")
        self.text.tag_remove("current_char", f"1.{index+1}", f"1.{index + 2}")
        self.text.tag_add("current_char", f"1.{index}", f"1.{index+1}")
        return

    def check_char(self, event):
        """
        Handles the response when a key is pressed.

        Parameters
        ----------
        event : tkinter.Event
            The key press event that has been registered.
        """
        if event.keysym == 'Shift_L' or event.keysym == 'Shift_R' or event.keysym == "Escape" or event.keysym == "F11":
            return

        if not self.test_started:  # The timer starts the first time a key is pressed
            self.start_test()

        test_word = self.test_words[self.current_word + self.page_num * 30]  # Find the word which the user is supposed to be typing
        if event.keysym == 'BackSpace':
            self.back_space(test_word)
            return

        # Track user's input, after establishing that the input was a character
        self.user_input.append(event.char)

        if self.current_char >= len(test_word):  # Check for extra letters
            index = self.get_char_index()
            self.text.insert(f"1.{index}", event.char, "incorrect")
            self.current_char += 1
            return

        self.give_typing_feedback(event.char, test_word)  # Use tags to give the user feedback
        self.current_char += 1  # Update cursor position

    def give_typing_feedback(self, character, word):
        """
        Indicates to the user whether the character typed was correct or incorrect.

        Parameters
        ----------
        character : tkinter.Event.char
            The character the user typed
        word : str
            The word in the test list that the user is currently typing.
        """
        index = self.get_char_index()
        if character == word[self.current_char]:
            self.text.tag_add("correct", f"1.{index}", f"1.{index + 1}")
        else:
            self.text.tag_add("incorrect", f"1.{index}", f"1.{index + 1}")

        self.text.tag_remove("current_char", f"1.{index}", f"1.{index + 1}")
        self.text.tag_add("current_char", f"1.{index + 1 }", f"1.{index + 2}")

    def show_next_words(self):
        """
        Shows the next page of the test words.
        """
        self.left += 30  # 30 words are shown on a page.
        self.right += 30
        self.text.delete(1.0, END)
        self.text.insert(1.0, " ".join(self.test_words[self.left:self.right]))
        self.tag_last_word()
        # Reset cursor
        self.excess_chars = 0
        self.current_char = 0
        self.current_word = 0
        self.page_num += 1

    def check_word(self, event):
        """
        Handles the response to a spacebar press.

        Parameters
        ----------
        event : tkinter.Event
            The event that triggered the response.
        """
        # Prevent repeated presses of the spacebar to skip through the words
        if self.current_char == 0:
            return

        test_word = self.test_words[self.current_word + self.page_num * 30]
        if self.current_char > len(test_word):
            self.excess_chars += (self.current_char - len(test_word))

        # Record the spacebar press and update cursor
        self.user_input.append(event.char)
        self.current_char = 0
        self.current_word += 1

        # User feedback: tag previous words as 'finished'
        index = self.get_char_index()
        self.text.tag_add("finished", 1.0, f"1.{index}")

        self.text.tag_remove("current_char", f"1.0", f"1.{index}")
        self.text.tag_add("current_char", f"1.{index}", f"1.{index + 1}")

        # Displays the next 30 words after the first 30 have been typed
        self.space_counts += 1
        if self.space_counts % 30 == 0:
            self.show_next_words()

    def obtain_test_statistics(self):
        """
        Calculates the average typing speed and accuracy during the test.

        Returns
        -------
        wpm : float
            The average time taken to type 5 characters. (words per minute)
        accuracy : float
            The percentage of the words typed that were correct.
        """
        words_correct = 0
        correct_chars = 0
        words_incorrect = 0
        test_input = "".join(self.user_input).split()  # Words typed by the user during the test

        for i in range(len(test_input) - 1):
            if test_input[i] == self.test_words[i]:
                words_correct += 1
                correct_chars += len(test_input[i])
            elif i <= len(test_input) - 2:
                words_incorrect += 1
        # Define wpm as the average number of 5-letter words that would be typed in a minute
        wpm = (correct_chars + len(test_input) - 1) / ((self.test_duration / 60) * 5)

        if len(test_input) > 1:
            accuracy = round(words_correct / (len(test_input) - 1) * 100, 0)
        else:
            accuracy = 0

        timestamp = datetime.datetime.now()

        return wpm, accuracy, timestamp

    def stop_test(self):
        """
        Ends the test procedure and displays the user's test statistics. Makes the button bar visible again.
        """
        wpm, accuracy, timestamp = self.obtain_test_statistics()

        self.results_io.save_data(wpm, accuracy, timestamp, duration=self.test_duration)

        self.text.delete(1.0, END)
        self.text.insert(1.0, f"Your typing speed was: {wpm} words per minute.\nYour accuracy was {accuracy}%.")
        self.text['state'] = 'disabled'

        self.home_ui.home_frame.focus_set()  # Stops listening for user input by taking focus away from the timer.
        self.home_ui.test_focus = False
        self.home_ui.start_buttons_frame.grid()
        self.home_ui.utility_buttons_frame.grid()
