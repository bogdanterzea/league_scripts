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

TIMELAPSE = 1

acceptButtonImgFirst = './accept-backup.png'
acceptedButtonImg = './sample-accepted.png'
championSelectionImg_flash = './flash-icon.png'
championSelectionImg_search = './search-bar.png'
playButtonImg = './play-button.png'

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

def checkGameAvailable():
    while True:
        pos = imagesearch(acceptButtonImgFirst, 0.8)

        if not pos[0] == -1:
            time.sleep(0.5)
            move_and_click(pos[0] + 30, pos[1] + 30)
            print("Game accepted!")
            break
        time.sleep(TIMELAPSE)
    

def checkChampionSelection():
    flashIMG = imagesearch(championSelectionImg_flash)
    searchIMG = imagesearch(championSelectionImg_search)

    if not searchIMG[0] == -1 or not flashIMG[0] == -1:
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

def main():
    print("Running...")
    run = True

    while run is True:
        checkGameAvailable()
        time.sleep(TIMELAPSE)

        while True:
            cancelled = checkGameCancelled()
            if cancelled is True:
                print("Game cancelled, waiting...")
                break
            
            csResult = checkChampionSelection()
            if csResult is True:
                print("Good Luck! Have Fun!")
                time.sleep(TIMELAPSE)
                run = False
                break

            time.sleep(TIMELAPSE)

if __name__ == "__main__":
    try:
        main()
    except Exception as e:
        print(f"Error occurred: {e}")
