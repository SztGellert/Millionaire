Steps to reproduce auto-run for python with auto-py-to-exe cli:
pip3 install auto-py-to-exe
auto-py-to-exe


credits: https://towardsdatascience.com/how-to-easily-convert-a-python-script-to-an-executable-file-exe-4966e253c7e9

pip3 install pillow (convert the icon for the executable file)

generated command: pyinstaller ~ can be found in https://github.com/SztGellert/Millionaire/blob/0efac47504ff58fef08f50c45660e45734aa9c47/install.bat#L2

How to Automatically Install Required Packages From a Python Script?	

credits: https://www.geeksforgeeks.org/how-to-automatically-install-required-packages-from-a-python-script/

Quick notes:
1. Under PyCharm Clear Screen command does not work 
    Select 'Edit Configurations' from the 'Run' menu.
    Under the 'Execution' section, select 'Emulate terminal in output console'

   Or run from separate windows command line.

   Current supported os platform is windows.

run python scripts in batch and wait for return from their executions
https://stackoverflow.com/questions/24935107/run-python-scripts-in-batch-and-wait-for-return-from-their-executions
