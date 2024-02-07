from os.path import exists
import time
import pyautogui
import check
from selenium import webdriver
import keyboard
from cv2 import cvtColor, COLOR_RGB2GRAY, SIFT_create
from numpy import array
import pickle

# URL of Genshin's interactive map
URL = "https://act.hoyolab.com/ys/app/interactive-map/?lang=en-us#/map/2?center=0.00,0.00"

# Optionnal sleep time betwin checks
SLEEP_TIME = 0
player_location = 0, 0

# Fonction to continusly locate player
def locate_minimap():
    # Get selenium webdriver
    interactive_map = open_interactive_map()
    while True:
        if check.check_for_game_gui():
            # Screenshot minimap
            minimap = pyautogui.screenshot(region=(143, 73, 184, 184))
            # Converts pyautogui screeshot to opencv image
            minimap = cvtColor(array(minimap), COLOR_RGB2GRAY)
            # Get player position back
            player_location = check.locate(minimap)
            x, y = player_location[0], player_location[1]
            # Check if program could find location
            if x != -9999:
                # Update interactive map with new coordinates
                update_map_coordinates(interactive_map, x, y)
        else:
            print("no minimap")
            time.sleep(2)
        time.sleep(SLEEP_TIME)

# Function to update interactive map coordinates
def update_map_coordinates(driver, x : float, y : float):
    # Using floats as genshin's interactive map uses coordinates of format xxxx.xx
    # Ofsetting cordinates from original map and interactive map because Genshin's dev thought it would be a practical idea to center the interactive map to Mondstadt's Anemo Archon Statue
    x, y = float(x - 8426), float(y - 3826)
    # Changing interactive map url with new coordinates
    current_loc_url = f"https://act.hoyolab.com/ys/app/interactive-map/?lang=en-us#/map/2?center={y},{x}"
    # Actually updating the map
    driver.execute_script(f"window.location.href = '{current_loc_url}';")

# Function to open chrome and the interactive map
def open_interactive_map():
    # Starting chrome
    driver = webdriver.Chrome()
    # Oppening the map's url
    driver.get(URL)
    # Adding a red square in the middle of the map to visualize player's position
    script = """
            var redDot = document.createElement("div");
            redDot.style.width = "10px";
            redDot.style.height = "10px";
            redDot.style.backgroundColor = "red";
            redDot.style.position = "fixed";
            redDot.style.top = "50%";
            redDot.style.left = "50%";
            redDot.style.borderRadius = "50%";
            redDot.style.transform = "translate(-50%, -50%)";
            document.body.appendChild(redDot);
            """
    driver.execute_script(script)
    return driver

# Main function
def main():  
    time.sleep(SLEEP_TIME)
    locate_minimap()
    
    
if __name__ == "__main__":
    main()