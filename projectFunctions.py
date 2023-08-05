# Imports
import sqlite3 as db  # Database to store presets
import PySimpleGUI as sg  # Used to make the GUI
import time  # Timer functionality
from playsound import playsound  # Timer done alert


# General functions
def h_min_sec_to_sec(h, min, sec):
    return (h * 3600) + (min * 60) + sec


# GUI functions
# Window functions (same window no matter what)
def window_main_menu():
    # Welcome and other windows
    layout = [[sg.Text("Welcome to linkedTmr", font=("Helvetica", 11, "bold"))],
              [sg.Button('Your Presets')],
              [sg.Button('Create A Preset')]]
    
    return sg.Window("Main Menu", layout, element_justification="center")


def window_presets(cur):
    # Read presets from db
    presets = []
    for row in cur.execute("""SELECT *
                              FROM presets
                              ORDER BY id ASC"""):
        presets.append(row)
    
    # Display presets in listbox
    layout = [[sg.Listbox(presets, size=(30, 6), key="selected_preset")],
              [sg.Button("Start linkedTmr"), sg.Button("Main Menu")]]
    
    return sg.Window("Presets", layout, element_justification="center")


def window_create_preset_0():
    # Ask name of preset and number of timers to be linked
    layout = [[sg.Text("What is the name of your preset?", font=("Helvetica", 11, "bold"))],
              [sg.Input(size=(30, 1), key="name")],
              [sg.Text("How many timers do you want to link?", font=("Helvetica", 11, "bold"))],
              [sg.Input(size=(3, 1), key="size")],
              [sg.Button('Next'), sg.Button('Main Menu')]]
    
    return sg.Window("Create A Preset", layout, element_justification="center")


# Button functions (window contents change)
def button_start(values, cur):
    # Get preset data from db
    preset_id = str(values["selected_preset"][0][0])
    preset_name_list = []
    for row in cur.execute("""SELECT name
                              FROM presets
                              WHERE id = ?""", preset_id):
        preset_name_list.append(row)
    preset_name = preset_name_list[0][0]
    
    # Get timer data from db
    timers = []
    for row in cur.execute("""SELECT rank, hour, minute, second
                              FROM timers
                              WHERE preset_id = ?
                              ORDER BY rank ASC""", preset_id):
        timers.append(row)
    
    # Prepare layout for loop
    layout = [[sg.Text("linkedTmr is running!", font=("Helvetica", 11, "bold"))],
              [sg.Text(f"Preset name: {preset_name}")]]
    
    # Add timers to layout with a loop
    for i in range(1, len(timers) + 1):
        timer = [sg.Text("Timer " + str(i), font=("Helvetica", 11, "bold")), 
                 sg.Text("Hour:"), sg.Text("", key=f"-HOUR{i}-"), 
                 sg.Text("Minute:"), sg.Text("", key=f"-MINUTE{i}-"), 
                 sg.Text("Second:"), sg.Text("", key=f"-SECOND{i}-")]
        layout.append(timer)
    
    # Add "Main Menu" button
    layout.append([sg.Button('Main Menu')])
    
    return sg.Window("linkedTmr is running!", layout, element_justification="center", finalize=True), timers


def run_timer(timers, window):
    # Determine length of each timer
    
    timer_lengths = []
    for timer in timers:
        timer_lengths.append(h_min_sec_to_sec(timer[1], timer[2], timer[3]))
    
    # Set initial values for timers
    for i in range(len(timers)):
        window.Element(f"-HOUR{i + 1}-").Update(timers[i][1])
        window.Element(f"-MINUTE{i + 1}-").Update(timers[i][2])
        window.Element(f"-SECOND{i + 1}-").Update(timers[i][3])
    # Refresh GUI
    event, values = window.read(timeout=0)
    
    # Update screen every second and play chimes when timers are over
    for i in range(len(timers)):
        # Cast h, min, sec from str to int
        hour = int(timers[i][1])
        minute = int(timers[i][2])
        second = int(timers[i][3])
        start_time = time.monotonic()
        while True:
            # Every 1 sec
            time.sleep(1 - ((time.monotonic() - start_time) % 1))
            # Update GUI
            window.Element(f"-HOUR{i + 1}-").Update(str(hour))
            window.Element(f"-MINUTE{i + 1}-").Update(str(minute))
            window.Element(f"-SECOND{i + 1}-").Update(str(second))
            # Refresh GUI
            event, values = window.read(timeout=0)
            # Calculate next hour, minute second values
            if second > 0:
                second -= 1
            else:
                if minute > 0:
                    minute -= 1
                    second = 59
                else:
                    if hour > 0:    
                        hour -= 1
                        minute = 59
                        second = 59
                    else:  # Timer over
                        playsound("chime.mp3")
                        break
                

def button_next_create_preset(values):
    # Prepate layout for loop
    layout = [[sg.Text("What is the length of each timer?", font=("Helvetica", 11, "bold"))]]
    
    # Add timers to layout with a loop
    for i in range(1, int(values["size"]) + 1):
        timer = [sg.Text("Timer " + str(i), font=("Helvetica", 11, "bold")), 
                 sg.Text("Hour:"), sg.Input(size=(3, 1), key="h" + str(i)), 
                 sg.Text("Minute:"), sg.Input(size=(3, 1), key="m" + str(i)), 
                 sg.Text("Second:"), sg.Input(size=(3, 1), key="s" + str(i))]
        layout.append(timer)
    
    # Add "Save Preset" button
    layout.append([sg.Button('Save Preset'), sg.Button('Main Menu')])
    
    return sg.Window("Create A Preset", layout, element_justification="center"), values["name"]


def button_save_preset(values, con, cur, name):
    # Insert preset name into db
    cur.execute("""INSERT INTO presets (name)
                   VALUES (?)""", (name, ))
    
    # Get id of last inserted preset
    preset_id_list = []
    for row in cur.execute("""SELECT id
                              FROM presets
                              ORDER BY id DESC
                              LIMIT 1"""):
        preset_id_list.append(row)
    preset_id = preset_id_list[0][0]
    
    # Insert timers
    for i in range(1, int((len(values) / 3 + 1))):
        cur.execute("""INSERT INTO timers (preset_id, rank, hour, minute, second)
                       VALUES (?, ?, ?, ?, ?)""", 
                       (preset_id, i, values["h" + str(i)], values["m" + str(i)], values["s" + str(i)]))
    
    # Commit changes to db
    con.commit()
    
    return window_main_menu()
