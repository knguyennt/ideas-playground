import pyautogui
import time

battle_button="battle.png"

battle_button_loc = pyautogui.locateOnScreen(battle_button, confidence=0.7)

pyautogui.click(battle_button_loc)
pyautogui.click(battle_button_loc)
time.sleep(3)
hunt_stage = "hunt.png"
hunt_stage_loc = pyautogui.locateOnScreen(hunt_stage, confidence=0.7)
pyautogui.click(hunt_stage_loc)
time.sleep(3)
wyren_hunt = "wyren.png"
wyren_loc = pyautogui.locateOnScreen(wyren_hunt, confidence=0.7)
pyautogui.click(wyren_loc)
time.sleep(3)
select_team = "select_team.png"
select_team_loc = pyautogui.locateOnScreen(select_team, confidence=0.7)
pyautogui.click(select_team_loc)
time.sleep(3)
auto_pet = "empty_pet_auto.png"
auto_pet_loc = pyautogui.locateOnScreen(auto_pet, confidence=0.7)
pyautogui.click(auto_pet_loc)
time.sleep(3)
start_hunt = "start_hunt.png"
start_hunt_loc = pyautogui.locateOnScreen(start_hunt, confidence=0.7)
pyautogui.click(start_hunt_loc)

while True:
    try:
        end_battling = "end_battling.png"
        end_battling_loc = pyautogui.locateOnScreen(end_battling, confidence=0.7)

        if end_battling_loc:
            hunt_confirm = "hunt_confirm.png"
            hunt_confirm_loc = pyautogui.locateOnScreen(hunt_confirm, confidence=0.7)
            pyautogui.click(hunt_confirm_loc)
            break

    except:
        print("battling not end waiting.....")
        time.sleep(5)

time.sleep(3)
lobby_button = "lobby_button.png"
lobby_button_loc = pyautogui.locateOnScreen(lobby_button, confidence=0.7)
pyautogui.click(lobby_button_loc)
