from tkinter import END

from currentdisplay import CurrentDisplay
from home_ui import HomeUI
from scoreboard_ui import ScoreboardUI
from results_io import ResultsInOut
from analytics_ui import AnalyticsUI


class ScoreBoardLogic:
    """
    Class that provides the functionality for the scoreboard screen.

    Attributes
    ----------
    current_display : CurrentDisplay
        Instance of the CurrentDisplay class.
    scoreboard_ui : ScoreboardUI
        Instance of the ScoreboardUI class.
    titles : list
        List of the scoreboard title widgets.
    boards : list
        List of the scoreboard widgets.
    close_button : tkinter Button
        Tkinter button to close the scoreboard screen.
    analytics_button : tkinter.Button
        Button to open the analytics page.
    close_analytics : tkinter.Button
        Button to close the anlaytics page.
    results_io : ResultsInOut
        Instance of the ResultsInOut class.
    """
    def __init__(self, current_display: CurrentDisplay, home_ui: HomeUI, scoreboard_ui: ScoreboardUI, results_io: ResultsInOut, analytics_ui: AnalyticsUI):
        """
        Configures the functionality of the open and close scoreboard buttons.

        Parameters
        ----------
        current_display : CurrentDisplay
            Instance of the CurrentDisplay class.
        home_ui : HomeUI
            Instance of the HomeUI class.
        scoreboard_ui : ScoreboardUI
            Instance of the ScoreboardUI class.
        results_io : ResultsInOut
            Instance of the ResultsInOut class.
        analytics_ui : AnalyticsUI
            Instance of the AnalyticsUI class.
        """
        self.current_display = current_display
        self.scoreboard_ui = scoreboard_ui
        self.titles = scoreboard_ui.score_titles
        self.boards = scoreboard_ui.scoreboards
        self.close_button = scoreboard_ui.close_scores_button
        self.analytics_button = scoreboard_ui.analytics_button
        self.close_analytics = analytics_ui.close_button
        self.results_io = results_io

        home_ui.utility_buttons[0].configure(command=self.show_scoreboard)
        self.close_button.configure(command=lambda: current_display.open_ui(home_ui))
        self.analytics_button.configure(command=lambda: current_display.open_ui(analytics_ui))
        self.close_analytics.configure(command=lambda: current_display.open_ui(scoreboard_ui))


        # Need to prevent focus being set to the scoreboards when they're clicked on because that would interfere with
        # test logic.
        for board in self.boards:
            board.bind("<Button-1>", self.mouse_click)

    def mouse_click(self, event):
        """
        Interrupts the usual behaviour when a widget is clicked on.
        """
        return "break"

    def obtain_scores(self):
        """
        Loads data from the file to display the top 10 scores on the scoreboards.

        Returns
        -------
        top_scores : dict
            Dictionary of the top 10 scores for each test type.
        """
        scores_data = self.results_io.load_data()
        grouped_scores = scores_data.groupby("duration")

        top_scores = {}

        for duration, group in grouped_scores:
            group_top_scores = group['wpm'].sort_values(ascending=False)[0:10].values
            top_scores[duration] = group_top_scores

        if all(len(score_list) == 0 for score_list in top_scores.values()):
            return "no scores"

        return top_scores


    def show_scoreboard(self):
        """
        Shows the scoreboard UI and inserts the scoreboard data into the scoreboards.
        """
        self.current_display.open_ui(self.scoreboard_ui)

        top_scores = self.obtain_scores()
        if top_scores == "no scores":
            self.scoreboard_ui.no_scores()
            return

        self.scoreboard_ui.normal_title_text()

        for i, scores in enumerate(top_scores.values(), 0):
            self.boards[i]['state'] = 'normal'  # Allows the text widgets to be edited.
            self.boards[i].delete(1.0, END)  # Clear the boards
            j = 0
            for score in scores:
                self.boards[i].insert(j+1.0, f"{j+1}. {score}\n")
                j += 1
            self.boards[i].grid()
            self.boards[i]['state'] = 'disabled'  # Prevents the user from being able to edit the text widgets themselves.
        self.close_button.grid()
