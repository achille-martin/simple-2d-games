# Description
Simple 2D pygame.
This is the start of a python game project.

# Requirements
* Make sure that python3 is installed (packages should work with python2 as well)
> python3 --version
* Make sure that you have installed all necessary packages:
> pip3 install -r <path>/requirements.txt
* Make sure that you have added your project path to the PYTHONPATH:
> export PYTHONPATH="${PYTHONPATH}:<project_path>/"

# List of Games

## Multiplayer Chase

### Introduction
This game consists in chasing another player in a multiplayer online game.

### Setup
To run the game you will need to run an instane of *server.py* on one machine. Then you can run instances of *run.py* on other machines to connect.

You need to change the **server** address in both *server.py* and *network.py* to be the IPV4 address of your machine or the server ips you are using.

### Development ideas
Latest update: 15/06/2020

| Task  | State  |
|:-----:|:------:|
| Improve python socket connection (security, reliability, speed) | Not started |
| Improve data communication between clients and server (security, reliability, speed). Study the use of pickle and equivalent object serialisation tools | Not started |
| Improve the robustness of the simple 2D square movement game for 2 players | Not started |
| Implement the simple 2D square movement game for N players (add names to the squares for instance to differentiate them) | Not started |
| Implement the shooting mechanism for the squares, for N players | Not started |

### Credits
The python networking concept is inspired from TechWithTim thanks to his [online multiplayer games tutorial](https://www.techwithtim.net/tutorials/python-online-game-tutorial).

# Fish Adventure

### Introduction
This game consists in embodying a fish and swim in a virtual space.

### Setup

To run the game, start main.py.
You will then be prompted with a mode in the terminal.

# Further game ideas

* Cat and mouse N players
* Connect4 2D
* Connect4 3D
* Little tanks N players
* Space invaders N players
* The dinosaur jump game N players
* Mario-like game (platforms) N players
* Chess game
* Card game (poker, black jack,...)
* Werewolf game
* MTG game (replicate one set for instance)
