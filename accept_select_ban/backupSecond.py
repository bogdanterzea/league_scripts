import time
import ctypes
import pygetwindow as gw
from python_imagesearch.imagesearch import imagesearch_loop, imagesearch

# Constants for Windows API
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# User-Defined Champion and Ban Choices
primary_champion_img = './champion1.png'
backup_champion_img = './champion2.png'
primary_ban_img = './ban1.png'
backup_ban_img = './ban2.png'

def focusWindow(title="League of Legends"):
    windows = gw.getWindowsWithTitle(title)
    if windows:
        league_window = windows[0]
        hwnd = league_window._hWnd
        ctypes.windll.user32.SetForegroundWindow(hwnd)
        time.sleep(0.1)
        return True
    else:
        print("League of Legends window not found.")
    return False

def move_and_click(x, y):
    abs_x = int(x * 65536 / screen_width)
    abs_y = int(y * 65536 / screen_height)

    focusWindow()
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_MOVE | MOUSEEVENTF_ABSOLUTE, abs_x, abs_y, 0, 0)
    time.sleep(0.1)

    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTDOWN, 0, 0, 0, 0)
    time.sleep(0.05)
    ctypes.windll.user32.mouse_event(MOUSEEVENTF_LEFTUP, 0, 0, 0, 0)
    print(f"Clicked at position: ({x}, {y})")

def selectChampion(primary_img, backup_img):
    pos = imagesearch(primary_img, 0.8)
    if pos[0] != -1:
        print("Primary champion found!")
        move_and_click(pos[0] + 30, pos[1] + 30)
    else:
        pos = imagesearch(backup_img, 0.8)
        if pos[0] != -1:
            print("Primary champion banned, selecting backup champion.")
            move_and_click(pos[0] + 30, pos[1] + 30)
        else:
            print("No champions available for selection.")

def banChampion(primary_ban, backup_ban):
    pos = imagesearch(primary_ban, 0.8)
    if pos[0] != -1:
        print("Primary ban target found!")
        move_and_click(pos[0] + 30, pos[1] + 30)
    else:
        pos = imagesearch(backup_ban, 0.8)
        if pos[0] != -1:
            print("Primary ban target already banned, selecting backup ban.")
            move_and_click(pos[0] + 30, pos[1] + 30)
        else:
            print("No ban options available.")

def checkChampionSelection():
    flashIMG = imagesearch(championSelectionImg_flash)
    searchIMG = imagesearch(championSelectionImg_search)

    if not searchIMG[0] == -1 or not flashIMG[0] == -1:
        return True
    else:
        return False

def championSelectionPhase():
    if checkChampionSelection():
        print("Champion Selection Phase...")
        selectChampion(primary_champion_img, backup_champion_img)

def banPhase():
    print("Ban Phase...")
    banChampion(primary_ban_img, backup_ban_img)

def main():
    print("Running...")
    run = True

    while run is True:
        checkGameAvailable()
        time.sleep(1)

        while True:
            cancelled = checkGameCancelled()
            if cancelled is True:
                print("Game cancelled, waiting...")
                break
            
            if checkChampionSelection():
                print("Starting champion selection...")
                championSelectionPhase()
                time.sleep(1)  # Delay to allow selection to process

            if checkBanPhase():
                print("Starting ban selection...")
                banPhase()
                time.sleep(1)  # Delay to allow ban to process
            
            time.sleep(1)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
