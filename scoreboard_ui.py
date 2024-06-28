import tkinter as tk


class ScoreboardUI:
    """
        Class responsible for setting up the scoreboard screen UI components.

        This class creates the widgets and frames for the scoreboard screen UI.
        It also configures the colour scheme and controls the visibility of the UI.

        Attributes
        ----------
        root : tkinter.Tk
            The parent widget
        scoreboard_frame : tkinter.Frame
            Tkinter frame containing the scoreboard widgets.
        score_titles : list
            List of tkinter labels for the titles of the scoreboards.
        scoreboards : list
            List of tkinter text widgets displaying the top 10 scores for each test duration.
        close_scores_button : tkinter.Button
            Tkinter button to close the scoreboard UI and return to the home UI.
        analytics_button : tkinter.Button
            Button to open the analytics page.

        Methods
        -------
        config_scores_ui(colour_scheme)
                    Configures the scoreboard screen widgets according to the given colour scheme.
        hide()
            Hides the scoreboard UI.
        show()
            Shows the scoreboard UI.
        """
    def __init__(self, root):
        """
        Initialises the scoreboard UI.

        Parameters
        ----------
        root : tkinter.Tk
            The parent widget.
        """
        self.root = root
        self.scoreboard_frame = self.setup_scoreboard_frame()
        scoreboard_widgets = self.setup_scoreboards(self.scoreboard_frame)
        self.score_titles = scoreboard_widgets[0]
        self.scoreboards = scoreboard_widgets[1]
        self.close_scores_button, self.analytics_button = self.setup_scores_buttons(self.scoreboard_frame)

    def setup_scoreboard_frame(self):
        """
        Sets up the scoreboard frame widget.

        Returns
        -------
        scoreboard_frame : tkinter.Frame
            Tkinter frame containing the scoreboard widgets.
        """
        scoreboard_frame = tk.Frame(self.root)
        scoreboard_frame.grid(row=0, column=0, columnspan=5, rowspan=5, sticky="news")
        # Allow the scoreboard frame to resize
        for i in range(3):
            scoreboard_frame.columnconfigure(i, weight=1)
        for i in range(5):
            scoreboard_frame.rowconfigure(i, weight=1)
        return scoreboard_frame

    def setup_scoreboards(self, scoreboard_frame):
        """
        Sets up the scoreboard widgets.

        Parameters
        ----------
        scoreboard_frame : tkinter.Frame
            The frame to attach the scoreboard widgets to.

        Returns
        -------
        score_titles : list
            Tkinter labels for the titles of the scoreboards.
        scoreboards : list
            Tkinter text widgets displaying the top 10 scores for each test duration.
        """
        score_titles = []
        scoreboards = []
        # Create scoreboards for each of the possible test durations: 15s, 30s and 60s.
        for (duration, column) in [(15, 0), (30, 1), (60, 2)]:
            # Create the Label widget for the scoreboard title
            score_title = tk.Label(scoreboard_frame, text=f"{duration} seconds (wpm)", font=("Arial", "24"))
            score_title.grid(row=0, column=column, padx=20, sticky="news")
            score_titles.append(score_title)
            # Create the text widget for the scoreboard
            scoreboard = tk.Text(scoreboard_frame, width=9, height=10, font=("Arial", "24"), spacing2=0.5, spacing3=1, bd=0, highlightthickness=0, wrap='word')
            scoreboard.grid(row=1, column=column, padx=20, pady=20, sticky="ns")
            scoreboards.append(scoreboard)
        return score_titles, scoreboards

    def setup_scores_buttons(self, scoreboard_frame):
        """
        Creates the close button widget for the scoreboard UI.

        Parameters
        ----------
        scoreboard_frame : tkinter.Frame
            The frame to attach the scoreboard widgets to.

        Returns
        -------
        close_scores_button : tkinter.Button
            Tkinter button to close the scoreboard UI and return to the home UI.
        analytics_button : tkinter.Button
            Button to open the analytics page.
        """
        close_button = tk.Button(scoreboard_frame, text="Close", font=("Arial", "16"))
        close_button.grid(row=3, column=1, sticky="news")

        analytics_button = tk.Button(scoreboard_frame, text="View Typing Analytics", font=("Arial", "16"))
        analytics_button.grid(row=2, column=1, sticky="news")
        return close_button, analytics_button

    def config_scores_ui(self, colour_scheme):
        """
        Configures the colour properties of the scoreboard UI widgets.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to apply to the scoreboard UI.
        """
        self.scoreboard_frame.configure(bg=colour_scheme["background"])

        for title in self.score_titles:
            title.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        for scoreboard in self.scoreboards:
            scoreboard.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])

        self.close_scores_button.configure(bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])
        self.analytics_button.configure(bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])

    def no_scores(self):
        """
        Changes the scoreboard screen if the user hasn't taken any tests.
        """
        for i, title in enumerate(self.score_titles, 0):
            if i == 1:
                title.configure(text="No results yet.\nTake a test to record your typing speed!")
            else:
                title.configure(text="")

    def normal_title_text(self):
        """
        Restores the default scoreboard titles.
        """
        for index, duration in enumerate([15, 30, 60], 0):
            self.score_titles[index].configure(text=f"{duration} seconds (wpm)")

    def show(self):
        """
        Shows the scoreboard UI.
        """
        self.scoreboard_frame.grid()

    def hide(self):
        """
        Hides the scoreboard UI and returns to the home screen.
        """
        self.scoreboard_frame.grid_remove()
