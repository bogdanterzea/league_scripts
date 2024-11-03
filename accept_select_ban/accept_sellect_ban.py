import time
import ctypes
import pyautogui

from python_imagesearch.imagesearch import imagesearch_loop, imagesearch

# Constants for Windows API
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

TIMELAPSE = 1

acceptButtonImgFirst = './accept-backup.png'
acceptedButtonImg = './sample-accepted.png'
championSelectionImg_flash = './flash-icon.png'
championSelectionImg_search = './search-bar.png'
playButtonImg = './play-button.png'

banPhaseTitle = "./ban-phase-title.png"
banPhaseButton = "./ban-phase-button.png"
banPhaseUnavailableButton = "./ban-phase-unavailable-button.png"

lockInphaseTitle = "./lock-in-phase-title.png"
lockInphaseButton = "./lock-in-phase-button.png"
lockInphaseUnavailableButton = "./lock-in-phase-unavailable-button.png"

gameReadyText = "./prepare-for-battle.png"

def focusWindow(title="League of Legends"):
    windows = gw.getWindowsWithTitle(title)
    if windows:
        league_window = windows[0]
        league_window.minimize()
        time.sleep(0.1)
        league_window.restore()
        time.sleep(0.1)
        return True
    else:
        print("League of Legends window not found.")
    return False

def move_and_click(x, y):\
    # Calculate absolute x and y for Windows
    abs_x = int(x * 65536 / screen_width)
    abs_y = int(y * 65536 / screen_height)

    focusWindow()
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, abs_x, abs_y, 0, 0)
    time.sleep(0.1)

    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    # Performing double click just to be sure.

    print(f"Double clicked at position: ({x}, {y})")

def get_champion_and_ban_choices():
    print("Enter champions for picking (primary and 2 backups):")
    champions = [input("Primary champion: "), input("First backup: "), input("Second backup: ")]
    
    print("Enter champions for banning (primary and 2 backups):")
    bans = [input("Primary ban: "), input("First backup ban: "), input("Second backup ban: ")]
    
    return champions, bans

def checkGameAvailable():
    print("Check if game is available...")

    while True:
        pos = imagesearch(acceptButtonImgFirst, 0.8)

        if not pos[0] == -1:
            time.sleep(0.5)
            move_and_click(pos[0] + 30, pos[1] + 30)
            print("Game accepted!")
            return True
        time.sleep(TIMELAPSE)

def checkChampionSelection():
    flashIMG = imagesearch(championSelectionImg_flash)
    searchIMG = imagesearch(championSelectionImg_search)

    if not searchIMG[0] == -1 or not flashIMG[0] == -1:
        return True
    else:
        return False
    
def checkChampionBanning():
    banIMG = imagesearch(banPhaseTitle)

    if not banIMG[0] == -1:
        return True
    else:
        return False

def checkGameCancelled():
    accepted = imagesearch(acceptedButtonImg)
    play = imagesearch(playButtonImg)

    if accepted[0] == -1 and not play[0] == -1:
        return True
    else:
        return False

def checkChampionPick():
    lockInTitleImage = imagesearch(lockInphaseTitle)

    if not lockInTitleImage[0] == -1:
        return True
    else:
        return False
    
def selectMainChampion(champions):
    search_pos = imagesearch(championSelectionImg_search)
    if search_pos[0] == -1:
        print("Search bar not found.")
        return False

    move_and_click(search_pos[0] + 30, search_pos[1] + 30)
    time.sleep(0.1)

    pyautogui.hotkey('ctrl', 'a')
    time.sleep(0.1)
    pyautogui.press('backspace')
    time.sleep(0.1)

    primary_champion = champions[0]
    pyautogui.write(primary_champion, interval=0.1)
    time.sleep(0.1)

    move_and_click(search_pos[0] , search_pos[1] + 90)
    print(f"Selected champion: {primary_champion}")

    return True

def detectGameStart():
    print("Checking if game has started...")
    game_start_pos = imagesearch(gameReadyText)
    return game_start_pos is not None

def banChampion(bans):
    for champion in bans:
        # Locate and click the search bar to focus
        search_pos = imagesearch(championSelectionImg_search)
        if search_pos[0] == -1:
            print("Search bar not found.")
            return False

        move_and_click(search_pos[0] + 30, search_pos[1] + 30)
        time.sleep(0.1)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('backspace')
        time.sleep(0.1)

        pyautogui.write(champion, interval=0.1)
        print(f"Attempting to ban champion: {champion}")
        time.sleep(0.5)

        ban_button_pos = imagesearch('ban-button.png') # TO GET ASSETS
        if ban_button_pos[0] != -1:
            move_and_click(ban_button_pos[0] + 30, ban_button_pos[1] + 30)
            print(f"Banned champion: {champion}")
            return True
        else:
            print(f"{champion} not available for banning, trying next...")

    print("No champions available to ban from the list.")
    return False

def pickChampion(champions):
    for champion in champions:
        search_pos = imagesearch(championSelectionImg_search)
        if search_pos[0] == -1:
            print("Search bar not found.")
            return False

        move_and_click(search_pos[0] + 30, search_pos[1] + 30)
        time.sleep(0.1)

        pyautogui.hotkey('ctrl', 'a')
        time.sleep(0.1)
        pyautogui.press('backspace')
        time.sleep(0.1)

        pyautogui.write(champion, interval=0.1)
        print(f"Attempting to pick champion: {champion}")
        time.sleep(0.5)  # Delay to allow image recognition

        pick_button_pos = imagesearch('pick-button.png')
        if pick_button_pos[0] != -1:
            move_and_click(pick_button_pos[0] + 30, pick_button_pos[1] + 30)
            print(f"Picked champion: {champion}")
            return True
        else:
            print(f"{champion} not available for picking, trying next...")

    print("No champions available to pick from the list, using default position.")
    move_and_click(search_pos[0] + 400, search_pos[1] - 200)
    return False

def main():
    print("Running...")

    champions, bans = get_champion_and_ban_choices()
    run = True

    print(champions)
    print(bans)

    while run is True:

# to improve this loop and maybe find new assets for the cancel and start phase
        checkGameAvailable()
        time.sleep(TIMELAPSE)

        while True:
            # if detectGameStart():
            #     print("Game has started. Exiting script.")
            #     return

            if checkGameCancelled():
                print("Game cancelled, waiting...")
                break

            if checkChampionSelection():
                print("Selecting Champion...")
                selectMainChampion(champions)
                time.sleep(TIMELAPSE)

            elif checkChampionBanning():
                print("Ban champion phase...")
                banChampion(bans)
                time.sleep(TIMELAPSE)

            elif checkChampionPick():
                print("Picking champion...")
                pickChampion(champions)
                time.sleep(TIMELAPSE)
                break

            time.sleep(TIMELAPSE)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
