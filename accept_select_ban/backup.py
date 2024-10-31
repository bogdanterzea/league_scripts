import time
import ctypes
import pygetwindow as gw
from python_imagesearch.imagesearch import imagesearch, imagesearch_loop

# Constants for Windows API
MOUSEEVENTF_MOVE = 0x0001
MOUSEEVENTF_ABSOLUTE = 0x8000
MOUSEEVENTF_LEFTDOWN = 0x0002
MOUSEEVENTF_LEFTUP = 0x0004

screen_width = ctypes.windll.user32.GetSystemMetrics(0)
screen_height = ctypes.windll.user32.GetSystemMetrics(1)

# Prompt user for input to select champions and bans
def get_champion_and_ban_choices():
    print("Enter champions for picking (primary and 2 backups):")
    champions = [input("Primary champion: "), input("First backup: "), input("Second backup: ")]
    
    print("Enter champions for banning (primary and 2 backups):")
    bans = [input("Primary ban: "), input("First backup ban: "), input("Second backup ban: ")]
    
    return champions, bans

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

def search_and_select(champion_name, click_pos, gray_check_img):
    # Click on the search bar and enter the champion's name
    move_and_click(click_pos[0], click_pos[1])  # Click search bar
    time.sleep(0.1)
    # Code to clear the search bar (send Backspace key multiple times) can be added here
    
    print(f"Attempting to select {champion_name}...")
    # Enter the champion name (You would replace this part with keyboard input commands to type champion_name)
    
    # Check if the ban/pick button is gray (unavailable)
    gray_check = imagesearch(gray_check_img, 0.8)
    if gray_check[0] == -1:
        print(f"{champion_name} is available! Locking in.")
        # Code to click the 'ban/pick' button goes here
        return True
    else:
        print(f"{champion_name} is unavailable.")
        return False

def ban_champion(ban_choices, search_pos, gray_check_img):
    print("Ban Phase...")
    for ban in ban_choices:
        if search_and_select(ban, search_pos, gray_check_img):
            return True
    print("No ban choices available.")
    return False

def pick_champion(champion_choices, search_pos, gray_check_img):
    print("Pick Phase...")
    for champion in champion_choices:
        if search_and_select(champion, search_pos, gray_check_img):
            return True
    print("No champion choices available.")
    return False

def check_ban_phase(ban_phase_img):
    pos = imagesearch(ban_phase_img, 0.8)
    return pos[0] != -1

def check_pick_phase(pick_phase_img):
    pos = imagesearch(pick_phase_img, 0.8)
    return pos[0] != -1

# def main():
#     # Get champions and bans from user input
#     champions, bans = get_champion_and_ban_choices()
    
#     # Position for clicking the search bar (to be customized as per screen)
#     search_pos = (500, 300)  # Placeholder coordinates, update as needed
#     gray_check_img = './gray-check.png'  # Placeholder for gray check image
    
#     # Images for phase detection
#     ban_phase_img = './ban-phase.png'
#     pick_phase_img = './pick-phase.png'
    
#     print("Running...")
    
#     # Wait for the ban phase
#     while not check_ban_phase(ban_phase_img):
#         print("Waiting for ban phase...")
#         time.sleep(1)
    
#     # Execute the ban phase
#     if not ban_champion(bans, search_pos, gray_check_img):
#         print("Failed to ban any champions.")
    
#     # Wait for the pick phase
#     while not check_pick_phase(pick_phase_img):
#         print("Waiting for pick phase...")
#         time.sleep(1)
    
#     # Execute the pick phase
#     if not pick_champion(champions, search_pos, gray_check_img):
#         print("Failed to pick any champions.")
    
#     print("Champion selected. Closing script.")

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
