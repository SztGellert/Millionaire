		🅦̲🅗̲🅞̲ 🅦̲🅐̲🅝̲🅣̲🅢̲ 🅣̲🅞̲ 🅑̲🅔̲ 🅐̲ 🅜̲🅘̲🅛̲🅛̲🅘̲🅞̲🅝̲🅐̲🅘̲🅡̲🅔̲ ❔̲ 
		ⒷⓎ
		ⒼⒺⓁⓁⒺ́ⓇⓉ ⓈⓏⓉⒶⓃⓀⓄⓋⓈⓏⓀⓎ
 


		This is the README file of The Helpless Gooses' Millionare game.

		This game is developed by Gellért Sztankovszky based on a team work 
		week of the Helpless Gooses Team.
		The aim of this development is self-entertainment and learning 
		python/programming.

		What is it?

		It's a game based on the TV show "Who wants to be a Millionaire?".
		You will get 15 questions in a random order, and you have to choose the 
		correct answer out of 4.

		How it works / instrucitons:

		You have to type for every question: a / b / c / d

		You have 3 kinds of helps:
			Audience'help
			Telephone help
			Halving the questions by the computer
		 
		If you choose an incorrect answer you will instantly lose the game.

		The money that you bring home depends on your performance.
		  - You earn guaranteed money after the 5th correct question.
		  - You earn guaranteed money after the 10th correct question.
		  - You earn guaranteed money after the 15th correct question.
		 
		And you win the game of course, if you've guessed all the answers correct.

		MODULES USED:

		third party: pygame, sty
		built in: random, copy, sys, os, time
		(+ circle is an own module) 

		Future goals:

		A game script, that can be executed instantly from a file in a separate window.
		Hungarian and English language selection.


		 Please enjoy!
		 Best wishes from the Gooses!

PREQUISITES:
	WRITTEN IN PYTHON 3.10
	INSTALL PYTHON
	https://www.python.org/downloads/

	ALTERNATIVELY PYTHON 3.10 x64 can be installed via
		millionaire/install_python_x64.
			Right click/run with PowerShell

To install game & download dependencies: double-click on "install" file
this will auto-install required python dependencies

To run: use "millionaire".exe



Steps to reproduce auto-run for python programme:
	pip3 install auto-py-to-exe
	auto-py-to-exe


credits: https://towardsdatascience.com/how-to-easily-convert-a-python-script-to-an-executable-file-exe-4966e253c7e9

pip3 install pillow (convert the icon for the executable file)

generated command: pyinstaller --noconfirm --onefile --console --icon "C:/Users/Yourname/PycharmProjects/Millionaire/loim.ico"  "C:/Users/Yourname/PycharmProjects/Millionaire/millionaire.py"

How to Automatically Install Required Packages From a Python Script?	

credits: https://www.geeksforgeeks.org/how-to-automatically-install-required-packages-from-a-python-script/

Quick notes:
	1. Under PyCharm Clear Screen command does not work 
	    Select 'Edit Configurations' from the 'Run' menu.
	    Under the 'Execution' section, select 'Emulate terminal in output console'
	
	   Or run from separate windows command line.
	   
	   Current supported os platform is windows.