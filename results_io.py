import pandas as pd


FILENAME = "results.csv"


class ResultsInOut:
    """
    Class that handles loading data and saving results to the file.

    Attributes
    ----------
    filename : str
        Name of the results file.
    empty_results : bool
        Describes whether the dataframe is empty.
    """
    def __init__(self):
        self.filename = FILENAME
        self.empty_results = False

    def load_data(self) -> pd.DataFrame:
        """
        Loads the data from the csv file as a pandas dataframe

        Returns
        -------
        df : pandas.Dataframe
            Dataframe containing test results.
        """
        try:
            df = pd.read_csv(self.filename, parse_dates=["timestamp"])
            if df.empty:
                self.empty_results = True
            else:
                self.empty_results = False
        except FileNotFoundError:
            df = pd.DataFrame(columns=["wpm", "accuracy", "timestamp", "duration"])
            self.empty_results = True
        return df

    def save_data(self, wpm, accuracy, timestamp, duration):
        """
        Saves the given data to the csv file.

        Parameters
        ----------
        wpm : float
            Words per minute (WPM).
        accuracy : float
            Accuracy result.
        timestamp : datetime object
            The time and date at which the test was completed.
        duration : int
            The duration of the test taken.
        """
        df = self.load_data()
        new_data = pd.DataFrame([[wpm, accuracy, timestamp, duration]], columns=["wpm", "accuracy", "timestamp", "duration"])
        df = pd.concat([df, new_data], ignore_index=True)
        df.to_csv(self.filename, index=False)

