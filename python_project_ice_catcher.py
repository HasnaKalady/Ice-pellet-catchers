from itertools import cycle
from random import randrange
from tkinter import Tk, Canvas, Button, messagebox
from tkinter import PhotoImage 
import pygame

canvas_width = 626
canvas_height = 417
win = Tk()

# Initialize Pygame mixer
pygame.mixer.init()

# Load the sound file for the pellet dropped event
pellet_drop_sound = pygame.mixer.Sound("bgsound.mp3")  # Replace with your sound file
pellet_drop_sound.play(loops=-1)

# Assuming you have an image file named "icebg.png"
background_image = PhotoImage(file="icebg.png")
original_width = background_image.width()
original_height = background_image.height()

# Calculate the scaling factors for the image
scale_width = canvas_width / original_width
scale_height = canvas_height / original_height

# Choose the smallest scaling factor to fit the entire image within the canvas
scale_factor = min(scale_width, scale_height)

# Resize the image using the chosen scale factor
background_image = background_image.subsample(int(1.5 / scale_factor))

c = Canvas(win, width=canvas_width, height=canvas_height)
background = c.create_image(0, 0, anchor='nw', image=background_image)

c.pack()

color_cycle = cycle(['white'])
ice_pellet_width = 30
ice_pellet_height = 30
ice_pellet_score = 10
ice_pellet_speed = 100
ice_pellet_interval = 4000
difficulty_factor = 0.95

catcher_color = 'blue'
catcher_width = 100
catcher_height = 100
catcher_start_x = canvas_width / 2 - catcher_width / 2
catcher_start_y = canvas_height - catcher_height - 20
catcher_start_x2 = catcher_start_x + catcher_width
catcher_start_y2 = catcher_start_y + catcher_height

catcher = c.create_arc(catcher_start_x, catcher_start_y, catcher_start_x2, catcher_start_y2, start=200, extent=140,
                       style='arc', outline=catcher_color, width=3)

score = 0
score_text = c.create_text(10, 10, anchor='nw', font=('Arial', 18, 'bold'), fill='black', text='Score : ' + str(score))

lives_remaining = 5
lives_text = c.create_text(canvas_width - 10, 10, anchor='ne', font=('Arial', 18, 'bold'), fill='black',
                            text='Lives : ' + str(lives_remaining))

ice_pellets = []
game_started = False  # Flag to check if the game has started
game_over = False     # Flag to check if the game is over

# Function to start the game
def start_game():
    global game_started
    if not game_started:
        game_started = True
        start_button.destroy()  # Remove the button
        create_ice_pellets()
        move_ice_pellets()
        catch_check()

# Button to start the game
start_button = Button(win, text="Start Game", font=('Arial', 18, 'bold'), command=start_game)
start_button.pack(pady=50)

def create_ice_pellets():
    if game_started:
        x = randrange(10, 740)
        y = 40
        ice_pellet_radius = 8  # Define radius for rounded corners
        new_pellet = c.create_oval(x, y, x + ice_pellet_width, y + ice_pellet_height,
                                        fill=next(color_cycle), width=0, outline='',
                                        tags='ice_pellet')

        ice_pellets.append(new_pellet)
        win.after(ice_pellet_interval, create_ice_pellets)

def move_ice_pellets():
    global game_over
    if game_started and not game_over and lives_remaining > 0:
        for pellet in ice_pellets:
            (pellet_x, pellet_y, pellet_x2, pellet_y2) = c.coords(pellet)
            c.move(pellet, 0, 10)
            if pellet_y2 > canvas_height:
                ice_pellet_dropped(pellet)
        win.after(ice_pellet_speed, move_ice_pellets)

           

# Initialize Pygame mixer
pygame.mixer.init()

# Load the sound file for the pellet dropped event
pellet_drop_sound = pygame.mixer.Sound("drop.mp3")
pellet_drop_sound.set_volume(0.5) # Replace with your sound file

def ice_pellet_dropped(pellet):
    
    ice_pellets.remove(pellet)
    c.delete(pellet)
    lose_a_life()
    if lives_remaining == 0:
        f1 = open("hii.txt", 'r')
        y = (f1.read())
        x = int(y)
        if score >= x:
            x = str(score)
            f1 = open("hii.txt", 'w')
            f1.write(x)
            messagebox.showinfo("GAME OVER!", "New Highscore : " + " " + str(x))
        else:
            messagebox.showinfo("GAME OVER!",
                                "Your Score : " + " " + str(score) + "\n" + "Highest Score : " + " " + str(x))
        win.destroy()

def lose_a_life():
    global lives_remaining
    lives_remaining -= 1
    c.itemconfigure(lives_text, text='Lives : ' + str(lives_remaining))

def catch_check():
    
    (catcher_x, catcher_y, catcher_x2, catcher_y2) = c.coords(catcher)
    for pellet in ice_pellets:
        (pellet_x, pellet_y, pellet_x2, pellet_y2) = c.coords(pellet)
        if catcher_x < pellet_x and pellet_x2 < catcher_x2 and catcher_y2 - pellet_y2 < 40:
            ice_pellets.remove(pellet)
            c.delete(pellet)
            increase_score(ice_pellet_score)
            pellet_drop_sound.play()
    win.after(100, catch_check)

def increase_score(points):
    global score, ice_pellet_speed, ice_pellet_interval
    score += points
    ice_pellet_speed = int(ice_pellet_speed * difficulty_factor)
    ice_pellet_interval = int(ice_pellet_interval * difficulty_factor)
    c.itemconfigure(score_text, text='Score : ' + str(score))

def move_left(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x1 > 0:
        c.move(catcher, -20, 0)

def move_right(event):
    (x1, y1, x2, y2) = c.coords(catcher)
    if x2 < canvas_width:
        c.move(catcher, 20, 0)

c.bind('<Left>', move_left)
c.bind('<Right>', move_right)
c.focus_set()

win.after(1000, create_ice_pellets)
win.after(1000, move_ice_pellets)
win.after(1000, catch_check)

win.mainloop()