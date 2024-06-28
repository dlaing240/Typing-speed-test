from home_ui import HomeUI
from scoreboard_ui import ScoreboardUI
from options_ui import OptionsUI
from colour_schemes import COLOUR_SCHEMES
from analytics_ui import AnalyticsUI


class CurrentDisplay:
    """
    Class to control which UI is currently displayed, and configures all UI colour schemes.

    Attributes
    ----------
    root : tkinter.Tk
        The parent widget of the home, options and scoreboard UI.
    colour_schemes : list
        List of colour schemes.
    default_cs_index : int
        Index of the default colour scheme.
    max_cs_index : int
        Maximum colour scheme index.
    home_ui : HomeUI
        Instance of the HomeUI class.
    scoreboard_ui : ScoreboardUI
        Instance of the ScoreboardUI class.
    options_ui : OptionsUI
        Instance of the OptionsUI class.
    analytics_ui : AnalyticsUI
        Instance of the AnalyticsUI class.
    ui_list : list
        List of the UI instances.

    Methods
    -------
    set_colour_scheme(colour_scheme)
        Applies the given colour scheme to each UI component
    open_ui(ui_to_open)
        Opens the given UI.
    """
    def __init__(self, root, home_ui: HomeUI, scoreboard_ui: ScoreboardUI, options_ui: OptionsUI, analytics_ui: AnalyticsUI):
        """
        Initialises the current display.

        This class initialises the display, opening the home UI on startup and applying the default colour scheme.

        Parameters
        ----------
        root : tkinter.Tk
            The parent widget of the home, options and scoreboard UI.
        home_ui : HomeUI
            TInstance of the HomeUI class.
        scoreboard_ui : ScoreboardUI
            Instance of the ScoreboardUI class.
        options_ui : OptionsUI
            Instance of the OptionsUI class.
        analytics_ui : AnalyticsUI
            Instance of the AnalyticsUI class.
        """
        self.root = root
        self.root.rowconfigure(tuple(range(5)), weight=1)
        self.root.columnconfigure(tuple(range(5)), weight=1)

        self.is_fullscreen = False
        self.root.bind("<F11>", self.toggle_fullscreen)
        self.root.bind("<Escape>", self.exit_fullscreen)

        # Initially apply the default colour scheme
        self.colour_schemes = COLOUR_SCHEMES
        self.default_cs_index = self.get_default_cs()
        options_ui.default_cs_index = self.default_cs_index
        options_ui.configure_preview(self.default_cs_index)
        self.max_cs_index = len(self.colour_schemes) - 1

        self.home_ui = home_ui
        self.scoreboard_ui = scoreboard_ui
        self.options_ui = options_ui
        self.analytics_ui = analytics_ui

        self.ui_list = [self.home_ui, self.scoreboard_ui, self.options_ui, self.analytics_ui]

        self.set_colour_scheme(self.colour_schemes[self.default_cs_index])

        # Open the home screen on startup
        self.open_ui(home_ui)

    def get_default_cs(self):
        """
        Get the index of the default colour scheme.

        Returns
        -------
        default_cs_index : int
            Index of the default colour scheme.
        """
        try:
            with open("default_cs.txt", "r") as f:
                default_cs_index = int(f.read())
            return default_cs_index
        except FileNotFoundError:
            with open("default_cs.txt", "w") as f:
                f.write("0")
            return 0

    def set_colour_scheme(self, colour_scheme):
        """
        Set the colour scheme of the whole application to the given colour scheme.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to be applied.
        """
        self.root.config(bg=colour_scheme["background"])
        self.home_ui.config_home_ui(colour_scheme)
        self.scoreboard_ui.config_scores_ui(colour_scheme)
        self.options_ui.config_options_ui(colour_scheme)
        self.analytics_ui.configure_cs(colour_scheme)

    def open_ui(self, ui_to_open):
        """
        Opens the given UI component.

        Parameters
        ----------
        ui_to_open : HomeUI, AnalyticsUI, ScoreboardUI, OptionsUI
            The UI page which is to be displayed.
        """
        for ui in self.ui_list:
            ui.hide()
        ui_to_open.show()

    def toggle_fullscreen(self, event=None):
        """
        Toggles fullscreen mode.
        """
        self.is_fullscreen = not self.is_fullscreen
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.options_ui.config_fullscreen_btn(self.is_fullscreen)
        return "break"

    def exit_fullscreen(self, event=None):
        """
        Exits fullscreen mode.
        """
        self.is_fullscreen = False
        self.root.attributes("-fullscreen", self.is_fullscreen)
        self.options_ui.config_fullscreen_btn(self.is_fullscreen)

    def exit_app(self):
        """
        Closes the application.
        """
        self.root.destroy()
