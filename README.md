# linkedTmr

#### Video Demo:
https://www.youtube.com/watch?v=9Nxpie62MsA

#### Description:
If the default timer in your device is not flexible enough, this program is for you! Create presets and chain timers one after another. 
Timers you have linked will start sequentially automatically so you can focus on the task at hand. Two example uses of the app can be 
given as cooking (how long to cook each side of a steak) and studying (periodic study and rest timers).

The project contains two .py files, one database file, and an .mp3 file. "main.py" file contains the main logic of the code, while the 
"projectFunctions.py" file contains window, button and other functions used in "main.py". The database file contains the presets created 
by the user. Finally, the .mp3 file is the chime sound used to notify the user of the end of a timer (playsound module is used).

In "main.py" the following are handled:
- Database setup (sqlite3 is used)
- GUI setup (PySimpleGUI is used)
- Event loop

In "projectFunctions.py" the following functions are present:
- h_min_sec_to_sec(h, min, sec)
- window_main_menu()
- window_presets(cur)
- window_create_preset_0()
- button_start(values, cur)
- run_timer(timers, window)
- button_next_create_preset(values)
- button_save_preset(values, con, cur, name)

#### Installation
1. Clone this repository to your local machine.
2. Make sure you have Python 3.x installed.
3. Install the required packages using pip: pip install PySimpleGUI playsound

#### Usage
To use linkedTmr, follow these steps:
1. Run the `main.py` file: python main.py
2. The main menu window will open, showing two options:
   - **Your Presets**: View and run previously saved presets.
   - **Create A Preset**: Create a new preset with linked timers.
3. **Create A Preset**: Clicking this option will open a new window where you can enter the name of your preset and the number of timers to be linked.
4. **Next**: After entering the preset details, click the "Next" button to set the length of each timer in the preset.
5. **Save Preset**: Once you've set the timer lengths, click the "Save Preset" button to save the preset into the database.
6. **Your Presets**: Clicking this option will open a window displaying your saved presets. Select a preset from the list and click "Start linkedTmr" to run the timers.
7. **linkedTmr is running!**: The timers will start running, and the remaining time for each timer will be displayed on the screen.
8. **Timer Completion**: When a timer completes, a chime sound will be played to notify you.

#### Dependencies
- PySimpleGUI
- playsound
- sqlite3
- time