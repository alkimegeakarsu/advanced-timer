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