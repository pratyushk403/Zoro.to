import requests
import shutil
import os
import zipfile
import pyautogui
import time

mpv_url = 'https://excellmedia.dl.sourceforge.net/project/mpv-player-windows/bootstrapper.zip'
output_file = 'mpv.zip'
output_folder = 'mpv'

# Check if the 'mpv.zip' file exists in the current directory
if os.path.isfile(output_file):
    print('File Already Exists')
else:
    print('Downloading MPV file ...')
    try:
        response = requests.get(mpv_url, stream=True)
        if response.status_code == 200:
            with open(output_file, 'wb') as f:
                shutil.copyfileobj(response.raw, f)
            print(f"Downloaded MPV to {output_file}")
        else:
            print("Failed to download MPV.")
    except Exception as e:
        print(f"An error occurred: {e}")

# Extract the 'mpv.zip' file if it exists
if os.path.isfile(output_file):
    with zipfile.ZipFile(output_file, 'r') as zip_ref:
        zip_ref.extractall(output_folder)
    if os.path.isdir(output_folder):
        print(f"Unzipped MPV to {output_folder}")
    else:
        print("Failed to find 'mpv.zip'.")


batch_script = '.\\updater.bat'

try:
    # Open Command Prompt
    pyautogui.hotkey('win', 'r')  # Open Run dialog
    time.sleep(1)  # Wait for Run dialog to appear
    pyautogui.write('cmd')  # Type 'cmd' to open Command Prompt
    pyautogui.press('enter')  # Press Enter to run Command Prompt

    # Wait for Command Prompt to open
    time.sleep(2)
    current_directory = os.getcwd()

    print("Current Directory:", current_directory)
    dir = current_directory+".\\mpv\\"
    # Run the batch script
    pyautogui.write('cd '+dir)
    pyautogui.press('enter')
    time.sleep(1)
    pyautogui.write(f'{batch_script}')  # Run the batch script
    pyautogui.press('enter')

    print("Batch script executed.")
except Exception as e:
    print(f"An error occurred: {e}")