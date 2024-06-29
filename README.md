# Typing Speed Test

A typing test app with a GUI, made using Python.
Features include:
- Three test durations (15s, 30s and 60s)
- Typing analytics
- Colour scheme options

![test_demo_gif](https://github.com/dlaing240/Typing-speed-test/assets/159714200/2f440edc-2676-4335-a05a-8d48c178276b)


## Installation

- Clone the repository
- Install dependencies by using ```pip install -r requirements.txt``` while in the project's directory
- Run using ```python main.py```

## Usage Guide
### Loading a Test
The app opens with a 15 second test loaded up and ready to go. Alternatively, there are three buttons at the bottom of the screen for loading tests of each duration.
### During the Test
Typing will begin the test and start the timer. Type the words that are shown on the screen until the timer reaches zero. Correctly typed characters will appear green, while incorrect characters will appear red. Once completed, the colour of the word changes. The current character will also be underlined, making it easy to keep track of your position.
### Results
Once the test is finished, you will be given a score in words per minute (WPM). It is calculated by dividing the number of characters typed by 5 ('words per minute' in this app assumes 5-letter words), and then divided by the duration in minutes. Only correctly typed words are included.
Along with the WPM, you will be provided with a percentage accuracy: the percent of the typed words which are correct.

### Additional features
- The top ten scores for each test category can be viewed by clicking the 'View Scores' button.
- The following additional analytics can be viewed by clicking the 'View Typing Analytics' button on the scoreboard page:
  - Scatter plot showing results history (WPM vs test number)
  - Histogram showing results distribution
  - Highest WPM
  - Average WPM
  - Average accuracy
  - Number of characters typed
  - Estimate for the number of words typed
  - Time spent typing.
![Analytics_screen](https://github.com/dlaing240/Typing-speed-test/assets/159714200/eadf2b39-7918-416f-b0ef-230e4e62048b)

- The Options page includes the option to change the colour scheme. There are six colour schemes to choose from. You can also change the default colour scheme.
- You can also toggle full screen (alternatively, use F11) and exit the application, from the options page.

![colour_scheme_demo_gif](https://github.com/dlaing240/Typing-speed-test/assets/159714200/11531dfe-bf4d-4c0e-981a-6c8a2c3accb3)
