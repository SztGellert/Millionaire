How to compile python script to binary executable?
-------------

credits: https://towardsdatascience.com/how-to-easily-convert-a-python-script-to-an-executable-file-exe-4966e253c7e9

*Steps to reproduce auto-run for python with auto-py-to-exe cli:*

pip3 install pillow # to convert the icon for the executable file to .ico

pip3 install auto-py-to-exe - gui for generating .exe from .py
https://pypi.org/project/auto-py-to-exe/

pyinstaller
https://pyinstaller.org/en/v3.6/usage.html

generated command: pyinstaller ~ can be found in
https://github.com/SztGellert/Millionaire/blob/0efac47504ff58fef08f50c45660e45734aa9c47/install.bat#L2

Attention: for importing modules use --paths PATH

How to Automatically Install Required Packages From a Python Script?
-------------

credits: https://www.geeksforgeeks.org/how-to-automatically-install-required-packages-from-a-python-script/


How to run python scripts in batch and wait for return from their executions?
-------------
credits: https://stackoverflow.com/questions/24935107/run-python-scripts-in-batch-and-wait-for-return-from-their-executions

Linux Topics
-------------
Virtualenv Environment - venv Python Interpreter
sudo apt update && sudo apt upgrade -y
sudo apt install software-properties-common -y
sudo add-apt-repository ppa:deadsnakes/ppa
sudo apt install python3.10
sudo apt install python3-pip
sudo apt install pythonpy

**pygame.init() tries to initialize all the pygame module and sometimes get: "ALSA lib pcm.c:8526:(snd_pcm_recover) underrun occurred" when I run a pygame program**
sudo apt-get install libasound2
credits:https://stackoverflow.com/questions/31847497/pygame-tries-to-use-alsa

Increase buffer size in pygame.mixer.init(buffer=)

**PyCharm Notes:**
###
1. Under PyCharm Clear Screen command does not work 
    Select 'Edit Configurations' from the 'Run' menu.
    Under the 'Execution' section, select 'Emulate terminal in output console'

   Or run from separate windows command line.

   Current supported os platform is windows.


