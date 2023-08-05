# Imports
import sqlite3 as db  # Database to store presets
import PySimpleGUI as sg  # Used to make the GUI
from projectFunctions import *  # Functions written for linkedTmr


# Database setup
con = db.connect("linkedTmr.db")
cur = con.cursor()


# Set GUI theme
sg.theme("DarkGray6")

# Create the window
window = window_main_menu()


# Event Loop to process events and get the values of the inputs
while True:
    # Read the event and values from the current window
    event, values = window.read()
    
    # According to the event, either:
    # - Call a button function
    # - Call a window function
    # - Close the window
    if event == sg.WINDOW_CLOSED or event == "Exit":
        break
    elif event == "Main Menu":
        window.close()
        window = window_main_menu()
    elif event == "Your Presets":
        window.close()
        window = window_presets(cur)
    elif event == "Create A Preset":
        window.close()
        window = window_create_preset_0()
    elif event == "Next":
        window.close()
        window, name = button_next_create_preset(values)
    elif event == "Save Preset":
        window.close()
        window = button_save_preset(values, con, cur, name)
    elif event == "Start linkedTmr":
        window.close()
        window, timers = button_start(values, cur)
        run_timer(timers, window)
    else:
        window.close()


# Program is finished, disconnect from db, close the GUI
con.close()
window.close()