from os.path import exists
import time
import pyautogui
import locate
from selenium import webdriver
import keyboard

url = "https://act.hoyolab.com/ys/app/interactive-map/?lang=en-us#/map/2?center=0.00,0.00"
driver = webdriver.Chrome()
driver.get(url)

SLEEP_TIME = 0
player_location = 0, 0

def locate_minimap():
    while True:
        pyautogui.screenshot("assets/minimap.png", (143, 73, 184, 184))
        time.sleep(0.1)
        player_location = locate.locate()
        x, y = player_location[0], player_location[1]
        if x != -9999:
            true_x, true_y = float(x - 8426), float(y - 3826)
            print("png co", x, y)
            print("map co", true_x,true_y)
            new_url = f"https://act.hoyolab.com/ys/app/interactive-map/?lang=en-us#/map/2?center=" + str(true_y) + "," + str(true_x)
            driver.execute_script(f"window.location.href = '{new_url}';")
            script = """
            var redDot = document.createElement("div");
            redDot.style.width = "10px";
            redDot.style.height = "10px";
            redDot.style.backgroundColor = "red";
            redDot.style.position = "fixed";
            redDot.style.top = "50%";
            redDot.style.left = "50%";
            redDot.style.transform = "translate(-50%, -50%)";
            document.body.appendChild(redDot);
            """
            driver.execute_script(script)
        time.sleep(SLEEP_TIME)


def main():  
    time.sleep(SLEEP_TIME)
    locate_minimap()
    
    
if __name__ == "__main__":
    main()