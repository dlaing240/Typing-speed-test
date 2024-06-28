import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.pyplot as plt


from analytics_brain import AnalyticsBrain


class AnalyticsUI:
    """
    Class responsible for setting up the analytics screen UI.

    This class sets up the widgets for the analytics page, implementing the analytics given by the instance of the
    AnalyticsBrain class.

    Attributes
    ----------
    root : tkinter.Tk
        The parent widget
    analytics_brain : AnalyticsBrain
        Instance of the AnalyticsBrain class.
    colour_scheme : dict
        The current colour scheme for the app.
    top_wpm : tkinter.Label
        Tkinter Label displaying the highest WPM (words per minute) value in the data.
    avg_wpm : tkinter.Label
        Tkinter Label displaying the mean WPM (words per minute) value.
    avg_acc : tkinter.Label
        Tkinter Label displaying the mean typing accuracy.
    chars_typed : tkinter.Label
        Tkinter Label displaying the number of characters typed in all tests in the data.
    words_est : tkinter.Label
        Tkinter Label displaying an estimate for the total number of words typed, assuming 5 character words.
    typing_time : tkinter.Label
        Tkinter Label displaying the total time spent typing; The sum of the durations of all tests in the data.
    close_button : tkinter.Button
        Tkinter button widget that closes the analytics page.

    Methods
    -------
    config_cs(colour_scheme)
        Configures the analytics page UI according to the given colour scheme.
    hide()
        Hides the analytics page UI
    show()
        Shows the analytics page UI
    """
    def __init__(self, root, analytics_brain: AnalyticsBrain):
        """
        Initialises the analytics page UI.

        Parameters
        ----------
        root : tkinter.Tk
            The parent widget.
        analytics_brain : AnalyticsBrain
            Instance of the AnalyticsBrain class.
        """
        self.root = root
        self.analytics_brain = analytics_brain

        self.colour_scheme = None

        self.top_wpm, self.avg_wpm, self.avg_acc, self.chars_typed, self.words_est, self.typing_time, self.close_button = self.create_widgets(root)

        self.canvas = None

    def create_widgets(self, root):
        """
        Creates the widgets for the analytics page.

        Parameters
        ----------
        root : tkinter.Tk
            Parent widget.
        """
        top_wpm = tk.Label(root, font=("Arial", 16))
        top_wpm.grid(row=0, column=2, padx=10, pady=10, sticky="s")
        avg_wpm = tk.Label(root, font=("Arial", 16))
        avg_wpm.grid(row=1, column=2, padx=10, pady=10, sticky="ns")
        avg_acc = tk.Label(root, font=("Arial", 16))
        avg_acc.grid(row=2, column=2, padx=10, pady=10, sticky="n")

        chars_typed = tk.Label(root, font=("Arial", 16))
        chars_typed.grid(row=0, column=3, padx=10, pady=10, sticky="s")
        words_est = tk.Label(root, font=("Arial", 16))
        words_est.grid(row=1, column=3, padx=10, pady=10, sticky="ns")
        typing_time = tk.Label(root, font=("Arial", 16))
        typing_time.grid(row=2, column=3, padx=10, pady=10, sticky="n")

        close_button = tk.Button(root, text="close", font=("Arial", 16))
        close_button.grid(row=3, column=2, columnspan=2, sticky="")
        return top_wpm, avg_wpm, avg_acc, chars_typed, words_est, typing_time, close_button

    def configure_cs(self, colour_scheme):
        """
        Configures the colour scheme of the analytics page widgets according to the given colour scheme.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to apply.
        """
        self.top_wpm.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.avg_wpm.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.avg_acc.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.chars_typed.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.words_est.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.typing_time.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.close_button.configure(bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])

        self.colour_scheme = colour_scheme

    def update_stat_widgets(self):
        """
        Updates the values displayed in the statistic widgets.
        """
        self.top_wpm.configure(text=f"Highest WPM: {self.analytics_brain.top_wpm}")
        self.avg_wpm.configure(text=f"Average WPM: {self.analytics_brain.mean_wpm}")
        self.avg_acc.configure(text=f"Average Accuracy: {self.analytics_brain.avg_acc}")
        self.chars_typed.configure(text=f"Characters typed: {self.analytics_brain.chars_typed}")
        self.words_est.configure(text=f"Estimated words typed: {self.analytics_brain.words_est}")
        self.typing_time.configure(text=f"Time spent typing: {self.analytics_brain.time_spent_typing}")

    def open_analytics_page(self, colour_scheme):
        """
        Performs the procedure to open the analytics page.

        Updates the stats widgets and creates the figure canvas widgets.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to use when creating figures.
        """
        self.analytics_brain.update_stats()
        self.update_stat_widgets()

        if self.analytics_brain.empty_results:
            return

        fig = self.analytics_brain.open_plots(colour_scheme)
        self.canvas = FigureCanvasTkAgg(fig, self.root)
        self.canvas.get_tk_widget().grid(row=0, rowspan=4, column=0, columnspan=2, sticky="news")

    def show(self):
        """
        Procedure to make the analytics page the current display
        """
        self.top_wpm.grid()
        self.avg_wpm.grid()
        self.avg_acc.grid()
        self.chars_typed.grid()
        self.words_est.grid()
        self.typing_time.grid()
        self.close_button.grid()
        self.open_analytics_page(self.colour_scheme)

    def hide(self):
        """
        Procedure to stop analytics page being displayed.
        """
        self.top_wpm.grid_remove()
        self.avg_wpm.grid_remove()
        self.avg_acc.grid_remove()
        self.chars_typed.grid_remove()
        self.words_est.grid_remove()
        self.typing_time.grid_remove()
        self.close_button.grid_remove()

        plt.close("all")  # close the figure.

        if self.canvas:
            self.canvas.get_tk_widget().destroy()
