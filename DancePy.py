# -*- coding: utf-8 -*-
"""
Created on Sun Nov 26 21:37:23 2023

@author: ikbel
"""

#Importing necessary modules and functions
import music, time
from pgzero.builtins import Actor, clock
import pgzrun
from random import randint

#Setting up the game window dimensions
WIDTH = 800
HEIGHT = 600

# Center of the Screen
CENTER_X = WIDTH / 2
CENTER_Y = HEIGHT / 2

#Initializing lists
move_list = []          
display_list = []      

# Starting Global Variables
# Individual Player Scores
score1 = 0              
score2 = 0              
current_move = 0        
count = 4               #Countdown timer value
dance_length = 4        

# Flags
say_dance = False       # Flag to display "Dance!" message
show_countdown = True   # Flag to display countdown
moves_complete = False  # Flag to indicate if all moves have been displayed
game_over = False       # Flag to indicate if the game is over
auto_play = False       # Flag to indicate if it's Auto-Play mode

#Creating actor objects for the dancer and dance move arrows
dancer = Actor("dancer-start")
dancer.pos = CENTER_X + 5, CENTER_Y - 40
up = Actor("up")
up.pos = CENTER_X, CENTER_Y + 110
right = Actor("right")
right.pos = CENTER_X + 60, CENTER_Y + 170
down = Actor("down")
down.pos = CENTER_X, CENTER_Y + 230
left = Actor("left")
left.pos = CENTER_X - 60, CENTER_Y + 170

# Function to draw the game elements on the screen
def draw():  
    global game_over, score1, score2, say_dance, count, show_countdown, secondplayer
    if not game_over:
        #If the game is not over, draw the dancer, arrows, and scores
        screen.clear()
        screen.blit("stage", (0, 0))
        dancer.draw()
        up.draw()
        down.draw()
        right.draw()
        left.draw()
        
        # Tracking Player 1 and 2 Scores
        screen.draw.text("Player 1 Score: " + str(score1), color="black", topleft=(10, 10))
        screen.draw.text("Player 2 Score: " + str(score2), color="black", topleft=(WIDTH - 135, 10))
        # The countdown to the start of the next sequence of dances
        if secondplayer == 1:
           screen.draw.text("Player 1's Turn", color="black", topleft=(CENTER_X - 80, 10))
        else:
           screen.draw.text("Player 2's Turn", color="black", topleft=(CENTER_X - 80, 10))
        if say_dance:
            screen.draw.text("Dance!", color="black", topleft=(CENTER_X - 65, 150), fontsize=60)
        if show_countdown:
            screen.draw.text(str(count), color="black", topleft=(CENTER_X - 8, 150), fontsize=60)
    else:
        # If the game is over, only draw the scores and "GAME OVER!" message and song being used.
        screen.clear()
        screen.blit("stage", (0, 0))
        screen.draw.text("Player 1 Score: " + str(score1), color="black", topleft=(10, 10))
        screen.draw.text("Player 2 Score: " + str(score2), color="black", topleft=(WIDTH - 135, 10))
        screen.draw.text("GAME OVER!", color="black", topleft=(CENTER_X - 130, 220), fontsize=60)
       



# This function is to reset the dancer and arrow images after User presses button.
def reset_dancer():
    global game_over
    if not game_over:
        dancer.image = "dancer-start"
        up.image = "up"
        right.image = "right"
        down.image = "down"
        left.image = "left"

# Update the dancer and arrow images based on the moves presented
def update_dancer(move):
    global game_over
    if not game_over:
        if move == 0:
            up.image = "up-lit"
            dancer.image = "dancer-up"
            clock.schedule(reset_dancer, 0.5)
        elif move == 1:
            right.image = "right-lit"
            dancer.image = "dancer-right"
            clock.schedule(reset_dancer, 0.5)
        elif move == 2:
            down.image = "down-lit"
            dancer.image = "dancer-down"
            clock.schedule(reset_dancer, 0.5)
        else:
            left.image = "left-lit"
            dancer.image = "dancer-left"
            clock.schedule(reset_dancer, 0.5)


# This function will display the set of dance moves on the screen through the actor and highlighting the
# arrows.
def display_moves():
    global move_list, display_list, dance_length, say_dance, show_countdown, current_move
    # If there are moves left to display, get the next move from the list
    if display_list: 
        this_move = display_list[0]
        display_list = display_list[1:]
        if this_move == 0:
            update_dancer(0)
            clock.schedule(display_moves, 1)
        elif this_move == 1:
            update_dancer(1)
            clock.schedule(display_moves, 1)
        elif this_move == 2:
            update_dancer(2)
            clock.schedule(display_moves, 1)
        else:
            update_dancer(3)
            clock.schedule(display_moves, 1)
    else:
        say_dance = True
        show_countdown = False

# This function is to generate random dance moves for the user to mimic
def generate_moves():
    global move_list, dance_length, count, show_countdown, say_dance
    count = 4
    move_list = []
    say_dance = False
    for move in range(0, dance_length):
        #Generate a random move (0: up, 1: right, 2: down, 3: left) and add it to the move list
        rand_move = randint(0, 3)
        move_list.append(rand_move)
        display_list.append(rand_move)
    show_countdown = True
    countdown()

# This function to implement the countdown before displaying a sequence of dance moves
def countdown():
    
    global count, game_over, show_countdown
    if count > 1:
        count = count - 1
        clock.schedule(countdown, 1)
    else:
        show_countdown = False
        display_moves()

# Function to move to the next dance move in the sequence
def next_move():
    global dance_length, current_move, moves_complete
    if current_move < dance_length - 1:
        current_move = current_move + 1
    else:
        moves_complete = True

# Function to handle key release events
def on_key_up(key):
    global score1, score2, game_over, move_list, current_move, secondplayer, auto_play
    # If it's Player 1's turn, check the released key and update the dancer and scores accordingly
    if secondplayer == 1:
        if key == keys.UP:
            update_dancer(0)
            if move_list[current_move] == 0:
                score1 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.RIGHT:
            update_dancer(1)
            if move_list[current_move] == 1:
                score1 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.DOWN:
            update_dancer(2)
            if move_list[current_move] == 2:
                score1 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.LEFT:
            update_dancer(3)
            if move_list[current_move] == 3:
                score1 += 1
                next_move()
            else:
                game_over = True

        # If Player 1 loses, switch to Player 2 automatically
        if game_over:
            auto_switch_player()

    # If it's Player 2's turn, check the released key and update the dancer and scores accordingly
    elif secondplayer == 2:
        if key == keys.W:
            update_dancer(0)
            if move_list[current_move] == 0:
                score2 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.D:
            update_dancer(1)
            if move_list[current_move] == 1:
                score2 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.S:
            update_dancer(2)
            if move_list[current_move] == 2:
                score2 += 1
                next_move()
            else:
                game_over = True
        elif key == keys.A:
            update_dancer(3)
            if move_list[current_move] == 3:
                score2 += 1
                next_move()
            else:
                game_over = True

        # If Player 2 loses, switch to Player 1 automatically
        if game_over:
            auto_switch_player()

# Function to switch to the second player automatically
def auto_switch_player():
    global secondplayer, game_over
    secondplayer = 2  # Set to the second player
    game_over = False  # Reset game_over flag
    generate_moves()

# update the game state
# Update the game state
# Update the game state
def update():
    global game_over, current_move, moves_complete, secondplayer, auto_play
    if not game_over:
        if auto_play:
            auto_play_moves()
        elif moves_complete:
            generate_moves()
            moves_complete = False
            current_move = 0
            secondplayer = secondplayer * -1


#Setting the initial player to 1 and generating the first dance moves
secondplayer = 1
generate_moves()
music.play("bee.ogg")

pgzrun.go()
update()