import tkinter as tk


class HomeUI:
    """
    Class responsible for setting up the Home screen UI components.

    This class creates the widgets and frames for the Home screen UI, including main test frame
    and the button bar. It also configures the colour scheme and controls the visibility of the UI.

    Attributes
    ----------
    root : tkinter.Tk
        The parent widget
    home_frame : tkinter.Frame
        A Tkinter frame containing the main test widgets
    text : tkinter.Text
        A Tkinter text widget for displaying the test words
    timer_txt : tkinter.Label
        A Tkinter Label widget which displays the timer
    start_buttons_frame : tkinter.Button
        A Tkinter frame containing the start (test setup buttons) buttons
    utility_buttons_frame : tkinter.Frame
        A Tkinter frame containing the utility buttons: view scores, options
    options_button : tkinter.Button
        A Tkinter button to open the options page
    start_buttons : list
        List containing Tkinter buttons responsible for setting up tests
    utility_buttons : list
        List containing Tkinter buttons with non-test functionality

    Methods
    -------
    config_home_ui(colour_scheme)
        Configures the home screen widgets according to the given colour scheme.
    hide()
        Hides the home UI
    show()
        Shows the home UI
    """
    def __init__(self, root):
        """
        Initialises the HomeUI

        Parameters
        ----------
        root : tkinter.Tk
            The parent widget
        """
        self.root = root

        home_main = self.setup_home_main()
        self.home_frame = home_main[0]
        self.text = home_main[1]
        self.timer_txt = home_main[2]

        home_buttons = self.setup_home_buttons()
        self.start_buttons_frame = home_buttons[0]
        self.utility_buttons_frame = home_buttons[1]
        self.options_button = home_buttons[2]

        # It's useful to have lists of the buttons for some of the other classes.
        self.start_buttons = self.start_buttons_frame.winfo_children()
        self.utility_buttons = self.utility_buttons_frame.winfo_children()

        self.test_focus = True  # Maintains that the home screen is in a test-ready state

    def setup_home_main(self):
        """
        Sets up the frame and widgets for the tests

        Returns
        -------
        home_frame : tkinter.Frame
            A Tkinter frame containing the main test widgets
        text : tkinter.Text
            A Tkinter text widget for displaying the test words
        timer_txt : tkinter.Label
            A Tkinter Label widget which displays the timer
        """
        home_frame = tk.Frame(self.root)
        home_frame.grid(row=0, column=0, columnspan=5)
        # Set up the text widget
        text = tk.Text(home_frame, width=50, height=4, highlightthickness=0, bd=0, font=("Arial", "32"),
                       wrap="word", spacing2=0.5, spacing3=0.5)
        text.grid(row=1, column=0, columnspan=5, rowspan=2, pady=80)

        # Set up the timer widget
        timer_txt = tk.Label(home_frame, text="Timer", font=("Helvetica", "24"))
        timer_txt.grid(row=0, column=2, columnspan=5, pady=80)
        timer_txt.grid_remove()

        return home_frame, text, timer_txt

    def setup_home_buttons(self):
        """
        Sets up the button frames and widgets for the home screen

        Returns
        -------
        start_buttons_frame : tkinter.Frame
            A Tkinter frame containing the start (test setup buttons) buttons
        utility_buttons_frame : tkinter.Frame
            A Tkinter frame containing the utility buttons: view scores, options
        options_button : tkinter.Button
            A Tkinter button to open the options page
        """
        start_button_frame = tk.Frame(self.root)
        start_button_frame.grid(row=4, column=0, columnspan=3, sticky="ew")
        utility_button_frame = tk.Frame(self.root)
        utility_button_frame.grid(row=4, column=3, columnspan=2, sticky="ew")
        # Allow frames to resize
        for i in range(3):
            start_button_frame.columnconfigure(i, weight=1)
        for i in range(3, 5):
            utility_button_frame.columnconfigure(i, weight=1)

        # Set up buttons
        start_btn_15 = tk.Button(start_button_frame, text="15s", font=("Arial", "16"), bd=2)
        start_btn_15.grid(row=4, column=0, sticky='new')
        start_btn_30 = tk.Button(start_button_frame, text="30s", font=("Arial", "16"), bd=2)
        start_btn_30.grid(row=4, column=1, sticky='new')
        start_btn_60 = tk.Button(start_button_frame, text="60s", font=("Arial", "16"), bd=2)
        start_btn_60.grid(row=4, column=2, sticky='new')
        score_button = tk.Button(utility_button_frame, text="View Scores", font=("Arial", "16"))
        score_button.grid(row=4, column=3, sticky='new')
        options_button = tk.Button(utility_button_frame, text="Options", font=("Arial", "16"))
        options_button.grid(row=4, column=4, sticky='new')

        return start_button_frame, utility_button_frame, options_button

    def config_home_ui(self, colour_scheme):
        """
        Updates the colour properties of the home widgets according to the given colour scheme.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to apply to the home UI.
        """
        # Frames
        self.home_frame.configure(bg=colour_scheme["background"])
        self.start_buttons_frame.configure(bg=colour_scheme["background"])
        self.utility_buttons_frame.configure(bg=colour_scheme["background"])

        # Text and timer
        self.text.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        # Tags for the text to give typing feedback to the user
        self.text.tag_config("correct", foreground='green')
        self.text.tag_config("incorrect", foreground='red')
        self.text.tag_config("finished", foreground=colour_scheme["highlight"])
        self.text.tag_config("last_word", foreground='grey')
        self.text.tag_config("current_char", underline=True)
        self.timer_txt.configure(bg=colour_scheme["background"], fg=colour_scheme["highlight"])

        # buttons
        for button in self.start_buttons:
            button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])
        for button in self.utility_buttons:
            button.configure(bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])

    def show(self):
        """
        Shows the home UI
        """
        self.home_frame.grid()
        self.start_buttons_frame.grid()
        self.utility_buttons_frame.grid()
        if self.test_focus:
            self.timer_txt.focus_set()

    def hide(self):
        """
        Hides the home UI
        """
        self.home_frame.focus_set()
        self.home_frame.grid_remove()
        self.start_buttons_frame.grid_remove()
        self.utility_buttons_frame.grid_remove()
