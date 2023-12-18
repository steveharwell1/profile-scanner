# Installation

## MacOS Installation
- Install Visual Studio Code and git
- Create a folder and open it in Visual Studio Code
- Use the command `git clone https://github.com/steveharwell1/profile-scanner.git .` don't forget the dot at the end. It will prevent an extra folder from being created.
- Create a new environment on the command line.
	- Open the command line in VS Code ``ctrl + ` `` that character is a lowercase tilde
	- Enter the command `python3 -m venv venv` and hit `return` to execute the command
	- Start the environment with `source venv/bin/activate` and hit `return`
		- You should see the text `(venv)` appear at the beginning of the command line.
	- Install the dependencies with `pip install -r requirements.txt` and hit `return`
- Outside the command line on the left of the editor. Copy the file `secrets.py.example` and paste it in the same `scanner` folder. Rename it to `secrets.py` and enter your LinkedIn password in place of the quoted **password** and you LinkedIn email inside of the quoted **youremail**
	- You'll know the file is in the right place if it appears right next to the original file.
	- The quotes should remain like `password = "updated password"`
- You should be ready to use the scanner.

## Windows Installation
- Install Visual Studio Code, git and Python
- Create a folder and open it in Visual Studio Code
- Use the command `git clone https://github.com/steveharwell1/profile-scanner.git .` don't forget the dot at the end. It will prevent an extra folder from being created.
- Create a new environment on the command line.
	- Open the command line in VS Code ``ctrl + ` `` that character is a lowercase tilde
	- Enter the command `python -m venv venv` and hit `return` to execute the command
	- Start the environment with `source venv/bin/activate` and hit `return`
		- You should see the text `(venv)` appear at the beginning of the command line.
	- Install the dependencies with `pip install -r requirements.txt` and hit `return`
- Outside the command line on the left of the editor. Copy the file `secrets.py.example` and paste it in the same `scanner` folder. Rename it to `secrets.py` and enter your LinkedIn password in place of the quoted **password** and you LinkedIn email inside of the quoted **youremail**
	- You'll know the file is in the right place if it appears right next to the original file.
	- The quotes should remain like `password = "updated password"`
- You should be ready to use the scanner.