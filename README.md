# Connect4Project

### Final Project for CS 4260: Artificial Intelligence

By Parker Smith, Sam Sliman, Tim Schachner, & Josh Scherer

## Description
Connect 4 is a 2 player strategy game where players take turns dropping 
pieces into a 6x7 grid. The objective is to be the first to form a horizontal, 
vertical, or diagonal line of one's own pieces. Players must 
anticipate the opponent's moves to block, while simultaneously 
working towards their own winning line.

## Installation

In order to run the program, please perform the following steps:

1. Clone this repository locally using GitHub Desktop or using `git clone https://github.com/smsliman/Connect4Project.git`
2. If numpy is not already installed, use `pip install numpy` if using pip or `conda install numpy` if using Anaconda.
3. If tkinter is not already installed, use `pip install tkinter` if using pip or `conda install tkinter` if using Anaconda.
4. Run `Framework.py` either through an IDE or by going to the command line, navigating to the directory where the repo was cloned, and running `python Framework.py` or `python3 Framework.py`
5. The program should now be running, please view instructions for play below.

## Instructions

Once the program is running, two visual depictions of the board should pop up. One, which uses the tkinter module, will be 
in a pop-up window. This is merely to help you visually understand the state of the board for when you are playing the Agent. 
The board will also be printed to the console, which is where you will provide your move. The board uses zero-indexing, so 
0 is the first column and 6 is the last column. When prompted, please enter the number of the column in which you would like to 
make your move. 

*Note: We have not yet added additional logic for having the user re-enter a move if they provide one which is invalid. Please only 
make valid moves, or the game will crash*

You will then alternate moves with the agent. A win for the player, a win for the agent, or a draw will be indicated through 
another pop-up window displaying the result.

## Modifications

**1) Depth Parameter**

In its current configuration, the game allows you to play the agent a depth of 2. That is, the agent will determine its moves by 
looking at potential outcomes for 2 additional turns. This is a configurable metric, and you may choose to add to or remove this depth. 
In order to change the depth factor, you may modify the first line of the `reward` function in `Agent.py`. We recommend keeping this value 
at 2 for the best play, but a value of 1 or 3 is also acceptable. 

*Note: Increased depth **WILL** result in increased computation time (expect ~20 seconds for depth 3). The agent behaves the same way 
for each depth, but quality of play increases as this depth parameter increases*

**2) Agent or Human Play**

We have added the capability for the agent to play either a human or itself. Right now, the agent is configured to play a human. That is, 
you will enter your moves, and the agent will respond. However, if you'd like to see how the agent would perform against itself, you may 
change `self.mode` in the `Connect4Game` class in `Framework.py` to hold a value of 'computer' instead of 'human'. This modification is 
by no means necessary, but you may do so if desired.

