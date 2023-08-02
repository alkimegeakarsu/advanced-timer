# Imports
import sqlite3 as sql
import PySimpleGUI as sg  # Used to make the GUI
from projectFunctions import *  # Functions written for linkedTmr


# Database setup
con = sql.connect("linkedTmr.db")
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
    elif event == "Your Presets":
        window.close()
        window = window_presets()
    else:
        return


# Program is finished, close the GUI
window.close()