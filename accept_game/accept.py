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
            pyautogui.moveTo(pos[0]+18, pos[1]+3)
            time.sleep(0.5)
            pyautogui.click()
            print("Game accepted!")
            break
        time.sleep(TIMELAPSE)
    

def checkChampionSelection():
    flash = imagesearch(championSelectionImg_flash)
    emote = imagesearch(championSelectionImg_search)

    if not emote[0] == -1 or not flash[0] == -1:
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
        print("Running...")
        main()
    except Exception as e:
        print(f"Error occurred: {e}")