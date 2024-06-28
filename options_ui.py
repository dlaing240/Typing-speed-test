import tkinter as tk

from colour_schemes import COLOUR_SCHEMES


class OptionsUI:
    """
    Class responsible for setting up the Options screen UI components.

    This class creates the widgets and frames for the options screen UI.
    It also configures the colour scheme and controls the visibility of the UI.

    Attributes
    ----------
    root : tkinter.Tk
        The parent widget
    options_frame : tkinter.Frame
        Tkinter frame containing the options widgets.
    options_title : tkinter.Label
        Tkinter label that displays the options title.
    colour_schemes : list
        List of colour schemes.
    default_cs_index : int
        Index of the default colour scheme.
    set_col_label : tkinter.Label
        Tkinter label for the option to change colour scheme.
    next_cs_button : tkinter.Button
        Tkinter button to cycle through the colour scheme options.
    apply_button : tkinter.Button
        Tkinter button to update the colour scheme for the whole GUI.
    close_options_button : tkinter.Button
        Tkinter button to close the options and return to the home screen.
    set_default_button : tkinter.Button
        Button to set a particular colour scheme to be the default colour scheme for the app.
    fullscreen_button : tkinter.Button
        Button to toggle full screen mode.
    ext_button : tkinter.Button
        Button to exit the application.
    preview_frame : tkinter.Frame
        Tkinter frame containing the colour scheme preview.

    Methods
    -------
    config_options_ui(colour_scheme)
                Configures the options screen widgets according to the given colour scheme.
    hide()
        Hides the options UI.
    show()
        Shows the options UI.
    """
    def __init__(self, root):
        """
        Initialises the options UI.

        Parameters
        ----------
        root : tkinter.Tk
            The parent widget.
        """
        self.root = root
        self.options_frame = self.setup_options_frame()
        self.options_title, self.close_options_button = self.setup_options()

        self.colour_schemes = COLOUR_SCHEMES
        self.default_cs_index = 0

        colour_scheme_option_widgets = self.setup_colour_scheme_options()
        self.set_col_label = colour_scheme_option_widgets[0]
        self.next_cs_button = colour_scheme_option_widgets[1]
        self.apply_button = colour_scheme_option_widgets[2]
        self.set_default_button = colour_scheme_option_widgets[3]

        self.fullscreen_button = self.setup_fullscreen_options()

        self.exit_button = self.setup_exit_button()

        self.preview_frame = self.setup_colours_preview()

    def setup_options_frame(self):
        """
        Sets up the options frame.

        Returns
        -------
        options_frame : tkinter.Frame
            Tkinter frame widget to contain all the options widgets.
        """
        options_frame = tk.Frame(self.root)
        options_frame.grid(row=0, column=0, columnspan=5, rowspan=5, sticky="news")
        # Allow the options frame to resize
        for i in range(5):
            options_frame.columnconfigure(i, weight=1)
            options_frame.rowconfigure(i, weight=1)
        return options_frame

    def setup_options(self):
        """
        Sets up the options page title and close button.

        Returns
        -------
        options_title : tkinter.Label
            Tkinter label widget for the title.
        close_options_button : tkinter.Button
            Button to close the options page.
        """
        options_title = tk.Label(self.options_frame, text="Options", font=("Arial", "30"))
        options_title.grid(row=0, column=0, pady=50, sticky="n")

        close_options_button = tk.Button(self.options_frame, text="Close", font=("Arial", "16"))
        close_options_button.grid(row=7, column=0, sticky="news", pady=100)

        return options_title, close_options_button

    def setup_colour_scheme_options(self):
        """
        Sets up the widgets for the colour scheme options.

        Returns
        -------
        set_col_label : tkinter.Label
            Tkinter label for the option to change colour scheme.
        next_col_scheme : tkinter.Button
            Tkinter button to cycle through the colour scheme options.
        apply_button : tkinter.Button
            Tkinter button to update the colour scheme for the whole GUI.
        close_options_button : tkinter.Button
            Tkinter button to close the options and return to the home screen.
        """
        set_col_label = tk.Label(self.options_frame, text="Select Colour Scheme:", font=("Arial", "16"), height=1)
        set_col_label.grid(row=1, column=0, columnspan=1, sticky="news")
        next_col_scheme = tk.Button(self.options_frame, text="Next", font=("Arial", "16"))
        next_col_scheme.grid(row=2, column=0, sticky="ews")
        apply_button = tk.Button(self.options_frame, text="Apply", font=("Arial", "16"))
        apply_button.grid(row=3, column=0, sticky="news")
        set_default_button = tk.Button(self.options_frame, text="Set Default", font=("Arial", "16"))
        set_default_button.grid(row=4, column=0, sticky="new")

        return set_col_label, next_col_scheme, apply_button, set_default_button

    def setup_fullscreen_options(self):
        """
        Sets up the button to toggle full screen.
        """
        fullscreen_button = tk.Button(self.options_frame, font=("Arial", "16"))
        fullscreen_button.grid(row=5, column=0, pady=50, sticky="ew")
        return fullscreen_button

    def config_fullscreen_btn(self, is_fullscreen):
        """
        Adjusts the text on the full screen button to reflect the current display mode.

        Parameters
        ----------
        is_fullscreen : bool
            States whether the current display mode is full screen
        """
        if is_fullscreen:
            text = "Exit full screen"
        else:
            text = "Enter full screen"

        self.fullscreen_button.configure(text=text)

    def setup_exit_button(self):
        """
        Sets up the exit application button.
        """
        exit_button = tk.Button(self.options_frame, text="Exit Application", font=("Arial", "16"))
        exit_button.grid(row=6, column=0, sticky="ew")
        return exit_button

    def setup_colours_preview(self):
        """
        Sets up the preview box for the colour scheme option.

        Returns
        -------
        preview_frame : tkinter.Frame
            Tkinter frame containing the colour scheme preview.
        """
        preview_frame = tk.Frame(self.options_frame, highlightthickness=2)
        preview_frame.grid(row=2, column=1, columnspan=1, rowspan=3, padx=50, pady=0, sticky="news")
        preview_frame.columnconfigure(1, weight=1)

        preview_label = tk.Label(preview_frame, text="Preview", font=("Arial", "16"))
        preview_label.grid(row=0, column=1, sticky="news", pady=10)
        preview_button = tk.Button(preview_frame, font=("Arial", "16"))
        preview_button.grid(row=2, column=1, sticky="new", padx=50, pady=10)

        return preview_frame

    def configure_preview(self, colour_scheme_index):
        """
        Configures the preview box to display the colour scheme given by its index.

        Parameters
        ----------
        colour_scheme_index : int
            The index of the colour scheme to be displayed in the preview box.
        """
        colour_scheme = self.colour_schemes[colour_scheme_index]
        preview_label, preview_button = self.preview_frame.winfo_children()

        if colour_scheme_index == self.default_cs_index:
            preview_text = " (Default)"
        else:
            preview_text = ""

        self.preview_frame.configure(bg=colour_scheme["background"], highlightbackground=colour_scheme["highlight"])
        preview_label.configure(text=f"Preview", bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        preview_button.configure(text=colour_scheme["name"]+preview_text, bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])

    def config_options_ui(self, colour_scheme):
        """
        Configures the colour properties of the options page widgets according to the given colour scheme.

        Parameters
        ----------
        colour_scheme : dict
            The colour scheme to apply to the options UI.
        """
        self.options_frame.configure(bg=colour_scheme["background"])
        self.options_title.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.set_col_label.configure(bg=colour_scheme["background"], fg=colour_scheme["main_text"])
        self.next_cs_button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])
        self.apply_button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])
        self.set_default_button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])
        self.close_options_button.configure(bg=colour_scheme["highlight"], fg=colour_scheme["main_text"])
        self.fullscreen_button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])
        self.exit_button.configure(bg=colour_scheme["main_text"], fg=colour_scheme["highlight"])

    def show(self):
        """
        Shows the options UI.
        """
        self.options_frame.grid()
        self.preview_frame.grid()

    def hide(self):
        """
        Hides the options UI.
        """
        self.options_frame.grid_remove()
        self.preview_frame.grid_remove()
