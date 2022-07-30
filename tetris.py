import pygame
import random
import os
import sys
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
    font = pygame.font.SysFont("Consolas", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 -
                         (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
def draw_text(surface,text,size,color,x,y):
    font = pygame.font.SysFont("Colsolas",size)
    label = font.render(text,False,color)
    surface.blit(label,(x,y))


def draw_grid(surface, grid):
    sx = top_left_x
    sy = top_left_y
    for i in range(len(grid)):
        pygame.draw.line(surface,(128,128,128),(sx,sy + i * block_size),(sx + play_width,sy + i * block_size))
        for j in range(len(grid[i])):
            pygame.draw.line(surface,(128,128,128),(sx + j * block_size,sy),(sx + j * block_size,sy + play_height))


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

    surface.blit(label, (sx + -80, sy + 160))

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)

    draw_grid(surface, grid)
    #pygame.display.update()

def main(win):
    global grid
    paused = False
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
                sys.exit()
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
                    fall_speed = 0

                elif event.key == pygame.K_UP:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                elif event.key == pygame.K_q:
                    run = False
                    update_score(score)
                elif event.key == pygame.K_ESCAPE and not paused:
                    paused = True
                    ofs = fall_speed
                    fall_speed = 100000
                elif event.key == pygame.K_ESCAPE and paused:
                    paused = False
                    fall_speed = ofs
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
            pscore = clear_rows(grid,locked_positions)
            if pscore == 1:
                score += 10
            elif pscore == 2:
                score += 25
            elif pscore == 3:
                score += 50
            elif pscore == 4:
                score += 100

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


def main_menu(win):
    im = pygame.image.load("logo.png")
    run = True
    while run:
        win.fill((0,0,0))
        win.blit(im,(s_width/2-(im.get_rect().width/2),0))
        draw_text_middle(win,"PyTetris",60,(255,255,255))
        draw_text(win,"Press Enter to begin",60,(255,255,255),0,500)
        pygame.display.update()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    main(win)
                elif event.key == pygame.K_ESCAPE:
                    sys.exit()
    pygame.display.quit()
    sys.exit()

win = pygame.display.set_mode((s_width, s_height),pygame.FULLSCREEN)
pygame.display.set_caption('Tetris')
pygame.mouse.set_visible(False)
pygame.display.set_icon(pygame.image.load("logo.png"))
main_menu(win)  # start game
