import pygame
import random
import os
#TODO PORT CUSTOMIZATIONS FROM OLD TETRIS
pygame.font.init()
pygame.mixer.init()
music = pygame.mixer.music.load("tetris.mp3")
pygame.mixer.music.play(-1)
lsr = pygame.mixer.Sound("laser.wav")
s_width = 1280
s_height = 720
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height

S = [['.....',
      '......',
      '..00..',
      '.00...',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '...0.',
      '.....']]

Z = [['.....',
      '.....',
      '.00..',
      '..00.',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '.0...',
      '.....']]

I = [['..0..',
      '..0..',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '0000.',
      '.....',
      '.....',
      '.....']]

O = [['.....',
      '.....',
      '.00..',
      '.00..',
      '.....']]

J = [['.....',
      '.0...',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..00.',
      '..0..',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '...0.',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '.00..',
      '.....']]

L = [['.....',
      '...0.',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..0..',
      '..00.',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '.0...',
      '.....'],
     ['.....',
      '.00..',
      '..0..',
      '..0..',
      '.....']]

T = [['.....',
      '..0..',
      '.000.',
      '.....',
      '.....'],
     ['.....',
      '..0..',
      '..00.',
      '..0..',
      '.....'],
     ['.....',
      '.....',
      '.000.',
      '..0..',
      '.....'],
     ['.....',
      '..0..',
      '.00..',
      '..0..',
      '.....']]

shapes = [S, Z, I, O, J, L, T]
shape_colors = [(0, 255, 0), (255, 0, 0), (0, 255, 255), (255, 255, 0), (255, 165, 0), (0, 0, 255), (128, 0, 128)]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid


# 2. This is the convert_shape_format() function. It takes in a shape and converts it into a list of positions for the
#    game to understand.
# a) Create an empty list called positions
# b) Create a variable called format and set it equal to shape.shape[shape.rotation % len(shape.shape)]
# c) Create a for loop that runs for i and line in enumerate(format)
#    i.e. for i, line in enumerate(format)
# d) Within the for loop, Create a variable row and set it equal to list(line)
# e) Still within the for loop, create another for loop that runs for j and column in enumerate(row)
# f) Within this for loop, make an if statement that checks if column is equal to the string '0'
# g) Within the if statement, using the .append() function, append (shape.x + j, shape.y + i) to positions
# h) Outside of all the loops, create a new loop that runs for i and pos in enumerate(positions)
# i) Inside this loop, set the ith index of positions to equal (pos[0] - 2, pos[1] - 4)
# j) Finally, outside of this loop, return positions
def convert_shape_format(shape):
    positions = []
    format = shape.shape[shape.rotation % len(shape.shape)]
    for i,line in enumerate(format):
        row = list(line)
        for j,column in enumerate(row):
            if column == '0':
                positions.append((shape.x + j, shape.y + i))
    for i,pos in enumerate(positions):
        positions[i] = (pos[0] - 2, pos[1] - 4)
    return positions


# 3. This is the valid_space() function. It takes a shape and the grid and determines if the shape can fit there
# a) We have started this function for you. Follow step b onwards to finish the function
# b) Create a variable called formatted and set it equal to a call to convert_shape_format() with shape as the argument
# c) Create a for loop that runs for pos in formatted
# d) Inside the loop, make an if statement that checks if pos is not in accepted_pos
# e) Inside this if statement, make another if statement that checks if the 1st index of pos is greater than -1
# f) Inside this if statement, have the function return False
# g) Outside the for loop, have the function return True
def valid_space(shape, grid):
    accepted_pos = [[(j, i) for j in range(10) if grid[i][j] == (0,0,0)] for i in range(20)]
    accepted_pos = [j for sub in accepted_pos for j in sub]
    # Place b - g here
    formatted = convert_shape_format(shape)
    for pos in formatted:
        if not pos in accepted_pos:
            if pos[1] > -1:
                return False
    return True


# 4. This is the check_lost() function and it takes a list of positions as its argument. It checks if we have lost the
#    game
# a) Create a for loop that runs for pos in positions
# b) Set x and y equal to pos (i.e. x, y = pos)
# c) Make an if statement that checks if y is less than 1
# d) Inside the if statement return True
# e) Outside the for loop, return False
def check_lost(positions):
    for pos in positions:
        x,y = pos
        if y < 1:
            return True
    return False



def get_shape():
    global shapes, shape_colors
    return Piece(5, 0, random.choice(shapes))


def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("comicsans", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 -
                         (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))


# 1. This is the draw_grid() function. It draws the grey lines for the grid backdrop of the play area
# a) Create a variable called sx and set it equal to top_left_x
# b) Create a variable called sy and set it equal to top_left_y
# c) Create a for loop that runs for i in the range of the length of grid
# d) Within the for loop, call pygame's draw.line() function with the following parameters surface, (128,128,128),
#    (sx, sy + i * block_size), and (sx + play_width, sy + i * block_size)
# e) Also within the for loop, create another for loop that runs for j in the range the length of grid[i]
# f) Within this for loop, again call pygame's draw.line() function but use the following parameters instead: surface,
#    (128, 128, 128), (sx + j * block_size, sy), and (sx + j * block_size, sy + play_height)
def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx,sy + i * block_size),(sx + play_width,sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface,(128,128,128),(sx + j * block_size,sy),(sx + j * block_size,sy + play_height))


# 5. This is the clear_rows() function. It clears the completed rows from dropping blocks
# a) Create a variable inc and set it to 0
# b) Create a for loop that runs for i in range(len(grid)-1, -1, -1)
# c) Within the for loop, Create a variable row and set it equal to the ith index of grid
# d) Within the for loop, create an if statement that runs if (0,0,0) is not in row
# e) Within the if statement, increment inc by 1
# f) Next, Create a variable ind and set it to i
# g) Then, still within the for loop, create another for loop that runs for j in the range of the length of row
# h) Inside this loop, use a try statement
# i) In the try statement, use the del keyword to delete the (j, i)th index of locked
# j) Outside the try but within the second for loop, create an except statement
# k) Inside the except, use the keyword continue
# l) Outside of both for loops, create an if statement that checks if inc is greater than 0
# m) within this if statement, create a for loop that runs for key in sorted(list(locked), key=lambda x: x[1])[::-1]
# n) Inside this for loop set x and y equal to key (x, y = key)
# o) Next, make an if statement that checks if y is less than ind
# p) Within this if statement, set a variable newKey equal to (x, y + inc)
# q) Still within the if statement, set the index newKey of locked (locked[newKey]) equal to locked.pop(Key)
def clear_rows(grid, locked):
    inc = 0
    for i in range(len(grid)-1,-1,-1):
        row = grid[i]
        if not (0,0,0) in row:
            inc += 1
            ind = i
            for j in range(len(row)):
                try:
                    del locked[j,i]

                except:
                    continue
    if inc > 0:
        lsr.play()
        for key in sorted(list(locked),key=lambda p: p[1])[::-1]:
            x,y = key
            if y < ind:
                newKey = (x,y + inc)
                locked[newKey] = locked.pop(key)
    return inc



def draw_next_shape(shape, surface):
    font = pygame.font.SysFont('Consolas', 30)
    label = font.render('Next Shape', 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100
    format = shape.shape[shape.rotation % len(shape.shape)]

    for i, line in enumerate(format):
        row = list(line)
        for j, column in enumerate(row):
            if column == '0':
                pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))


def update_score(nscore):
    score = max_score()

    with open('scores.txt', 'w') as f:
        if int(score) > nscore:
            f.write(str(score))
        else:
            f.write(str(nscore))


def max_score():
    if not os.path.isfile("scores.txt"):
        with open("scores.txt","w+") as f:
            f.write("0")
        return 0
    with open('scores.txt', 'r') as f:
        lines = f.readlines()
        score = lines[0].strip()

    return score


def draw_window(surface, grid, score=0, last_score = 0):
    surface.fill((0, 0, 0))

    pygame.font.init()
    font = pygame.font.SysFont('Consolas', 60)
    label = font.render('Tetris', 1, (255, 255, 255))

    surface.blit(label, (top_left_x + play_width / 2 - (label.get_width() / 2), 30))

    # current score
    font = pygame.font.SysFont('Consolas', 30)
    label = font.render('Score: ' + str(score), 1, (255,255,255))

    sx = top_left_x + play_width + 50
    sy = top_left_y + play_height/2 - 100

    surface.blit(label, (sx + 20, sy + 160))
    # last score
    label = font.render('High Score: ' + last_score, 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + -50, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()


# 7. Here we are back at the main function. We will be making some alterations to make the functions we created work.
#    For each step, it will be clearly marked in the function where the code should be put.
# a) Create a variable called last_score and set it to a call to max_score()
# b) Create a variable called fall_speed and set it to 0.27
# c) Create a variable called level_time and set it to 0
# d) Create a variable called score and set it to 0
# e) Set the variable grid equal to a call to create_grid() with locked_positions as its argument
# f) Increment fall_time by a call to clock.get_rawtime()
# g) Increment level_time by a call to clock.get_rawtime()
# h) call clock.tick()
# i) Create an if statement that runs if level_time divided by 1000 is greater than 5
# j) Within the if statement, set level_time to 0
# k) Still within the if statement, create another if statement that runs if level_time is greater than 0.12
# l) Within this if statement, decrement level_time by 0.005
# m) Outside of the if statements, create a new if statement that runs if fall_time divided by 1000 is greater than
#    fall_speed
# n) Inside this if statement, set fall_time to 0
# o) Increment current_piece.y by 1
# p) Still within the if statement, create another if statement that runs via the following condition:
#    not(valid_space(current_piece, grid)) and current_piece.y > 0
# q) Inside this if statement, decrement current_piece.y by 1
# r) Next, set the variable change_piece to True
# s) Delete the call to quit()
# t) Outside of all the for loops and if statements, set shape_pos equal to a call to convert_shape_format() with
#    current_piece as its argument
# u) Create a for loop that runs for i in the range of the length of shape_pos
# v) Within the for looop, set x, y equal to the ith index of shape_pos
# w) Create an if statement that runs if y is greater than -1
# x) Within the if statement, set grid[y][x] equal to the color of the current piece (current_piece.color)
# y) Outside the for loop, create an if statement that runs if change_piece is true
# z) Inside this if statement, make a for loop that runs for pos in shape_pos
# A) Inside the for loop, set a variable p equal to the tuple (pos[0], pos[1])
# B) Next, set the pth index of locked_positions to current_piece.color
# C) Outside the for loop but within the if statement, set current_piece equal to next_piece
# D) Set next_piece equal to a call to get_shape
# E) set change_piece to False
# F) Increment score by 10 times a call to clear_rows() with grid and locked_positions as its arguments
# G) Change the arguments in the call to draw_window() such that they are win, grid, score, and last_score instead
# H) Below the call to draw_window, make a call to draw_next_shape() with the arguments next_piece and win
# I) Make a call to pygame's display.update() function
# J) Make an if statement that runs based on the output of a call to check_lost() with locked_positions as its argument
# K) Within the if statement, make a call to draw_text_middle() with the arguments win, "Game Over", 80, and
#    (255, 255, 255)
# L) Make a call to pygame's display.update() function
# M) Make a call to pygame's time.delay() function with 1500 as the argument
# N) Set run equal to False
# O) Make a call to update_score() with score as the parameter
def main(win):
    global grid
    # put a) here
    last_score = max_score()

    locked_positions = {}  # (x,y):(255,0,0)
    grid = create_grid(locked_positions)

    change_piece = False
    run = True
    current_piece = get_shape()
    next_piece = get_shape()
    clock = pygame.time.Clock()
    fall_time = 0
    # put steps b), c), and d) here
    fall_speed = 0.5
    level_time = 0
    score = 0

    while run:

        # put steps e) - r) here
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        if (level_time / 1000) < 5:
            level_time = 0
            if level_time > 0.12:
                level_time -= 0.005
        if (fall_time/1000) > fall_speed:
            fall_time = 0
            current_piece.y += 1
            if not(valid_space(current_piece, grid)) and current_piece.y > 0:
                current_piece.y -= 1
                change_piece = True

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.display.quit()
                pygame.quit()
                # step s) is here

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_DOWN:
                    # move shape down
                    current_piece.y += 1
                    if not valid_space(current_piece, grid):
                        current_piece.y -= 1

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                elif event.key == pygame.K_SPACE:
                    fall_speed = 0
        # put steps t) - F) here
        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                grid[y][x] = current_piece.color
        if change_piece:
            for pos in shape_pos:
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color
            fall_speed = 0.5
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            score += (10*clear_rows(grid,locked_positions))

        # follow step G) here
        draw_window(win,grid,score,last_score)
        # put steps H) - O) here
        draw_next_shape(next_piece,win)
        pygame.display.update()
        #score += (10 * clear_rows(grid, locked_positions))

        if check_lost(locked_positions):
            draw_text_middle(win,"Game Over",80,(255,255,255))
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            update_score(score)


# 6. This is the main_menu() function. It is used for creating a "main menu" for the game
# a) First up, make a variable called run and set it to True
# b) Next, create a while loop that runs while run is true
# c) Inside the while loop, call win.fill() using the parameter (0, 0, 0)
# d) Next, call draw_text_middle() with the parameters win, "Press Any Key to Play", 60, and (255, 255, 255)
# e) Call pygame's display.update() runction
# f) Create a for loop that runs for event in pygame.event.get()
# g) Inside the loop, make an if statement that checks if event.type() is equal to pygame.QUIT
# h) Inside the if statement, set run to False
# i) Outside the if statement but within the for loop, make another if statement that checks if the event type is equal
#    to pygame.KEYDOWN
# j) Inside this if statement, call main() with win as the argument
# k) Outside of the while loop call pygame.display.quit()
# l) Chance the final call to main in the code (at the very very bottom) to a main_menu() call with win as the argument
def main_menu(win):
    run = True
    while run:
        win.fill((0,0,0))
        draw_text_middle(win,"Press Any Key to Play",60,(255,255,255))
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                main(win)
    pygame.display.quit()


# 8. Edit the call to main below to instead call main_menu() with win as the argument
win = pygame.display.set_mode((s_width, s_height),pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')
main_menu(win)  # start game

# 9. Lastly, create a file called scores.txt at the same location as this file. In the file, put the number 0 and save
#    it. This will act as the database for the high score.

# CHALLENGES (These are optional and do not have solutions but are fun challenges for you to add to your game)
# 1. Change the background to another color or image
# 2. Add an instant drop if the player hits the space bar
# 3. Make it so the player can rotate the block either clockwise or counter-clockwise depending on if they hit z or x
# 4. Add background music
# 5. (EXTRA HARD) Make it multiplayer where one player uses arrows while the other uses WASD