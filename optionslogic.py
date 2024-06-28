from currentdisplay import CurrentDisplay
from home_ui import HomeUI
from options_ui import OptionsUI


class OptionsLogic:
    """
    Class that provides the functionality for the options screen.

    Attributes
    ----------
    current_display : CurrentDisplay
        Instance of the CurrentDisplay class.
    preview_cs_index : int
        Index for the colour scheme displayed in the preview box.
    options_ui : OptionsUI
        Instance of the OptionsUI class.
    """
    def __init__(self, current_display: CurrentDisplay, home_ui: HomeUI, options_ui: OptionsUI):
        """
        Configures the options buttons to have functionality.

        Parameters
        ----------
        current_display : CurrentDisplay
            Instance of the CurrentDisplay class.
        home_ui : HomeUI
            Instance of the HomeUI class.
        options_ui : OptionsUI
            Instance of the OptionsUI class.
        """
        self.current_display = current_display
        self.preview_cs_index = self.current_display.default_cs_index  # Preview starts by showing the default colour screen

        self.options_ui = options_ui

        # configure option buttons
        options_ui.next_cs_button.config(command=self.preview_next_colour_scheme)
        options_ui.apply_button.config(command=self.apply_colour_scheme)
        home_ui.options_button.config(command=lambda: self.current_display.open_ui(options_ui))
        options_ui.close_options_button.config(command=lambda: self.current_display.open_ui(home_ui))
        options_ui.set_default_button.config(command=self.set_default_cs)
        options_ui.fullscreen_button.config(command=self.fullscreen_button_pressed)
        options_ui.exit_button.config(command=self.current_display.exit_app)

        options_ui.config_fullscreen_btn(self.current_display.is_fullscreen)

    def preview_next_colour_scheme(self):
        """
        Updates the index of the colour scheme shown by the preview.
        """
        if self.preview_cs_index < self.current_display.max_cs_index:
            self.preview_cs_index += 1
        else:
            self.preview_cs_index = 0

        self.current_display.options_ui.configure_preview(self.preview_cs_index)

    def apply_colour_scheme(self):
        """
        Bound to the apply button. Tells the current_display instance to update the colour scheme.
        """
        self.current_display.set_colour_scheme(self.current_display.colour_schemes[self.preview_cs_index])

    def set_default_cs(self):
        """
        Saves the default colour scheme to the file and updates the relevant variables.
        """
        with open("default_cs.txt", "w") as f:
            f.write(f"{self.preview_cs_index}")
        self.options_ui.default_cs_index = self.preview_cs_index
        self.options_ui.configure_preview(self.preview_cs_index)

    def fullscreen_button_pressed(self):
        """
        Toggles full screen and updates the text on the full screen button.
        """
        self.current_display.toggle_fullscreen()
        self.options_ui.config_fullscreen_btn(is_fullscreen=self.current_display.is_fullscreen)

