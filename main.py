import tkinter as tk

from typing_test import TypingTestLogic
from scoreboardlogic import ScoreBoardLogic
from home_ui import HomeUI
from options_ui import OptionsUI
from scoreboard_ui import ScoreboardUI
from currentdisplay import CurrentDisplay
from optionslogic import OptionsLogic
from results_io import ResultsInOut
from analytics_brain import AnalyticsBrain
from analytics_ui import AnalyticsUI


class TypingSpeedApp:
    """
    Typing speed test application.

    Attributes
    ----------
    root : tkinter.Tk
        The root window widget.
    """
    def __init__(self, root: tk.Tk):
        # Set up the main window
        self.root = root
        self.root.config(padx=50, pady=50)
        self.root.minsize(height=700, width=900)

        # Initialise the UI
        home_ui = HomeUI(root)
        scoreboard_ui = ScoreboardUI(root)
        options_ui = OptionsUI(root)

        results_io = ResultsInOut()
        analytics_brain = AnalyticsBrain(results_io)
        analytics_ui = AnalyticsUI(root, analytics_brain)

        current_display = CurrentDisplay(root, home_ui, scoreboard_ui, options_ui, analytics_ui)

        typing_test = TypingTestLogic(root, home_ui, results_io)
        scoreboard = ScoreBoardLogic(current_display, home_ui, scoreboard_ui, results_io, analytics_ui)
        options = OptionsLogic(current_display, home_ui, options_ui)

    def run(self):
        """
        Run the mainloop.
        """
        self.root.mainloop()


if __name__ == "__main__":
    root = tk.Tk()
    app = TypingSpeedApp(root)
    app.run()
