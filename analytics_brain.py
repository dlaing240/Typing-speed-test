import datetime

import matplotlib.pyplot as plt
import seaborn as sns

from results_io import ResultsInOut


class AnalyticsBrain:
    """
    Class responsible for producing analytics from test data.

    This class collects basic statistics from the data which may be useful or interesting to the user. Additionally,
    it produces plots to show the results history and results distribution.

    Attributes
    ----------
    results_io: ResultsInOut
        Instance of the ResultsInOut class which loads test data.
    df: pandas.Dataframe
        The dataframe containing the test data.
    mean_wpm: int
        The mean WPM (words per minute) value.
    top_wpm: int
        The highest WPM (words per minute) value in the data.
    avg_acc: int
        The mean typing accuracy.
    chars_typed: int
        The number of characters typed in all tests in the data.
    words_est: int
        An estimate for the total number of words typed, assuming 5 character words
    time_spent_typing: datetime.timedelta
        A datetime duration giving the total time spent typing.
    empty_results : bool
        Describes whether the results dataframe is empty.

    Methods
    -------
    update_stats()
        Updates the dataframe and statistics.
    open_plots(colour_scheme)
        Creates the figure containing the two subplots.

    """
    def __init__(self, results_io: ResultsInOut):
        """
        Parameters
        ----------
        results_io : ResultsInOut
            instance of the ResultsInOut class
        """
        self.results_io = results_io

        self.df = None
        self.mean_wpm, self.top_wpm, self.avg_acc, self.chars_typed, self.words_est, self.time_spent_typing = None, None, None, None, None, None
        self.empty_results = results_io.empty_results
        self.update_stats()

    def update_df(self):
        """
        Updates the dataframe to contain the latest data.
        """
        self.df = self.results_io.load_data()
        self.empty_results = self.results_io.empty_results

    def update_stats(self):
        """
        Updates the statistics.
        """
        self.update_df()
        if not self.results_io.empty_results:
            self.mean_wpm = round(self.df["wpm"].mean())
            self.top_wpm = round(self.df["wpm"].max())
            self.avg_acc = round(self.df["accuracy"].mean())

            self.chars_typed = round((self.df.wpm * 5 * self.df.duration/60).sum())
            self.words_est = round(self.chars_typed/5)
            seconds_spent_typing = float(self.df.duration.sum())
            self.time_spent_typing = datetime.timedelta(seconds=seconds_spent_typing)

    def configure_plots(self, colour_scheme):
        """
        Configures the styling for the plots.

        Parameters
        ----------
        colour_scheme : dict
            Colour scheme to apply to the styling.
        """
        sns.set(rc={"axes.edgecolor": colour_scheme["main_text"],
                    "grid.color": colour_scheme["main_text"],
                    "text.color": colour_scheme["main_text"]})
        sns.set_style("whitegrid",
                      {"figure.facecolor": colour_scheme["background"], "axes.facecolor": colour_scheme["background"],
                       "axes.edgecolor": colour_scheme["main_text"],
                       "grid.color": colour_scheme["main_text"]})

    def wpm_time_figure(self, colour_scheme, ax):
        """
        Plots WPM results against their index.

        Parameters
        ----------
        colour_scheme : dict
            Colour scheme for the plot.
        ax : matplotlib.axes.Axes
            The axes to plot on.
        """
        data = self.df

        palette = [colour_scheme["highlight"], colour_scheme["markers2"], colour_scheme["markers3"]]

        sns.scatterplot(x=data.index,
                        y=data.wpm,
                        hue=data.duration,
                        palette=palette,
                        s=50,
                        linewidth=0,
                        ax=ax)

        ax.grid(alpha=0.25)
        ax.xaxis.label.set_color(colour_scheme["main_text"])
        ax.yaxis.label.set_color(colour_scheme["main_text"])
        ax.tick_params(axis='x', colors=colour_scheme["main_text"])
        ax.tick_params(axis='y', colors=colour_scheme["main_text"])
        ax.set_title("Results History", fontsize=15)
        ax.title.set_color(colour_scheme["main_text"])
        ax.set_xlabel("Test Number")
        ax.set_ylabel("WPM")
        ax.set_xlim(0)
        ax.set_ylim(0)
        ax.legend(labelcolor=colour_scheme["main_text"])

    def wpm_hist(self, colour_scheme, ax):
        """
        Plots a histogram to show the distribution of test results.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to apply to the plot.
        ax : matplotlib.axes.Axes
            The axes to plot the histogram on.
        """
        df = self.df

        sns.histplot(data=df,
                     x="wpm",
                     stat="count",
                     binrange=(0, self.top_wpm + (5 - self.top_wpm % 5)),
                     binwidth=5,
                     color=colour_scheme["highlight"],
                     edgecolor=colour_scheme["main_text"],
                     ax=ax)

        ax.grid(alpha=0.25)

        ax.set_xlabel("WPM")
        ax.set_ylabel("Count")
        ax.xaxis.label.set_color(colour_scheme["main_text"])
        ax.yaxis.label.set_color(colour_scheme["main_text"])
        ax.tick_params(axis='x', colors=colour_scheme["main_text"])
        ax.tick_params(axis='y', colors=colour_scheme["main_text"])
        ax.set_title("Results Distribution", fontsize=15)
        ax.title.set_color(colour_scheme["main_text"])
        ax.set_xlim(0)
        ax.set_ylim(0)

    def open_plots(self, colour_scheme):
        """
        Creates the figure and subplots.

        Parameters
        ----------
        colour_scheme : dict
            Colour scheme to apply to the figure and subplots.
        """

        if self.empty_results:
            return

        self.configure_plots(colour_scheme)
        self.update_df()

        fig, (ax1, ax2) = plt.subplots(2, 1, figsize=(8, 6))
        self.wpm_time_figure(colour_scheme, ax1)
        self.wpm_hist(colour_scheme, ax2)
        fig.subplots_adjust(hspace=0.6)
        return fig
