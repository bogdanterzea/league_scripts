import pyautogui
from python_imagesearch.imagesearch import imagesearch_loop, imagesearch
import time

pyautogui.FAILSAFE = False
TIMELAPSE = 1

acceptButtonImg = './accept-backup.png'
acceptedButtonImg = './sample-accepted.png'
championSelectionImg_flash = './flash-icon.png'
championSelectionImg_search = './search-bar.png'
playButtonImg = './play-button.png'

def checkGameAvailable():
    while True:
        pos = imagesearch(acceptButtonImg, 0.8)
        if not pos[0] == -1:
            pyautogui.moveTo(pos[0]+30, pos[1]+30)

            # #Solution 0 ------------------------------------------------------------------------------------------
            # time.sleep(0.5)
            # pyautogui.click()
            # pyautogui.click()

            # # Solution 1 - enter before clicking ------------------------------------------------------------------------------------------
            # pyautogui.press('enter')  # Simulate pressing Enter key
            # pyautogui.click()

            # # Solution 3 ---------------------------------------------------------------------------------------------------------------------------------------
            # time.sleep(1)
            # pyautogui.click()
            # time.sleep(1)

            # # Solution 4 - other library ------------------------------------------------------------------------------------------
            # # pip install pydirectinput
            # # import pydirectinput
            # pydirectinput.click()

            # # Solution 5 ---------------------------------------------------------------------------------------------------------------------------------------
            # # pip install pywin32
            # # import win32api, win32con
            # # import time
            # def click_at(x, y):
            # # Move the mouse to the specified position
            # win32api.SetCursorPos((x, y))
            
            # # Simulate a left mouse button down and up (click)
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTDOWN, x, y, 0, 0)
            # time.sleep(0.5)
            # win32api.mouse_event(win32con.MOUSEEVENTF_LEFTUP, x, y, 0, 0)

            # # Solution 6 ---------------------------------------------------------------------------------------------------------------------------------------
            # # pip install PyDirectInput
            # # import pydirectinput
            # # import time

            # def click_at(x, y):
            #     pydirectinput.moveTo(x, y)
            #     pydirectinput.click()

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
