import pygame
import random
import os
import sys
import datetime
import requests
import urllib.request
import json
import logging
import ast

pygame.font.init()
pygame.mixer.init()

s_width = 1280
s_height = 720
play_width = 300  # meaning 300 // 10 = 30 width per block
play_height = 600  # meaning 600 // 20 = 20 height per block
block_size = 30

top_left_x = (s_width - play_width) // 2
top_left_y = s_height - play_height
win = pygame.display.set_mode((s_width, s_height))
pygame.display.set_caption('Tetris')

def draw_text_middle(surface, text, size, color):
    font = pygame.font.SysFont("Consolas", size, bold=True)
    label = font.render(text, 1, color)
    surface.blit(label, (top_left_x + play_width /2 -
                         (label.get_width()/2), top_left_y + play_height/2 - label.get_height()/2))
draw_text_middle(win,"Enderbyte Programs",60,(255,255,255))
pygame.display.update()

CWD = os.getcwd()
ASSETSDIR = CWD + "/t22assets"
STRIPPED = False
if not os.path.isdir(ASSETSDIR):
    os.mkdir(ASSETSDIR)
DATADIR = ASSETSDIR + "/data.json"
defaultdata = {
    "config" : {
        "mute" : False,
        "fullscreen" : False,
        "grid" : True
    },
    "stats" : {
        "highscore" : 0,
        "linescleared" : 0,
        "points" : 0,
        "highestlevel": 0,
        "gamesplayed" : 0,
        "wellclears" : 0,
        "tetris" : 0
    },
    "saves" : [
        {
            "empty" : True
        }
     for i in range(5)]
}
DATA = defaultdata
if not os.path.isfile(DATADIR):
    with open(DATADIR,"w+") as f:
        f.write(json.dumps(defaultdata))
else:
    with open(DATADIR) as f:
        try:
            DATA = json.load(f)
        except:
            f.write(defaultdata)
#Making sure data is not corrupt
if "config" in DATA:
    if not "mute" in DATA["config"]:
        DATA["config"]["mute"] = False
    if not "fullscreen" in DATA["config"]:
        DATA["config"]["fullscreen"] = False
    if not "grid" in DATA["config"]:
        DATA["config"]["grid"] = True
else:
    DATA["config"] = {
        "mute" : False,
        "fullscreen" : False,
        "grid" : True
    }
if "stats" in DATA:
    e = ["highscore","linescleared","points","highestlevel","gamesplayed","wellclears","tetris"]
    for k in e:
        if not k in DATA["stats"]:
            DATA["stats"][k] = 0
else:
    DATA["stats"] = {
        "highscore" : 0,
        "linescleared" : 0,
        "points" : 0,
        "highestlevel": 0,
        "gamesplayed" : 0,
        "wellclears" : 0,
        "tetris" : 0
    }
if not "saves" in DATA:
    DATA["saves"] = [{"empty":True} for i in range(5)]

class Button():
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.ogcol = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text
        self.juston = False
        self.on = False

    def draw(self, win, outline=None):
        # Call this method to draw the button on the screen
        if outline:
            pygame.draw.rect(win, outline, (self.x - 2, self.y - 2, self.width + 4, self.height + 4), 0)

        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)

        if self.text != '':
            font = pygame.font.SysFont('Consolas', 24)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (
            self.x + (self.width / 2 - text.get_width() / 2), self.y + (self.height / 2 - text.get_height() / 2)))

    def isOver(self, ev):
        pos = pygame.mouse.get_pos()

        # Pos is the mouse position or a tuple of (x,y) coordinates
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_HAND))
                self.color = (128, 128, 128)
                self.on = True

            else:
                self.color = self.ogcol
                self.on = False

        else:
            self.color = self.ogcol
            self.on = False

        if not self.on and self.juston:
            pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
        self.juston = self.on

        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pos[0] > self.x and pos[0] < self.x + self.width:
                    if pos[1] > self.y and pos[1] < self.y + self.height:
                        return True

if DATA["config"]["fullscreen"]:
    win = pygame.display.set_mode((s_width, s_height),pygame.FULLSCREEN)
    FULLSCREEN = True
else:
    FULLSCREEN = False
if DATA["config"]["mute"]:
    MUTE = True
else:
    MUTE = False

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
shape_stats = [0,0,0,0,0,0,0]


class Piece(object):
    def __init__(self, x, y, shape):
        self.x = x
        self.y = y
        self.shape = shape
        self.color = shape_colors[shapes.index(shape)]
        self.rotation = 0
    def incstat(self):
        shape_stats[shapes.index(self.shape)] += 1


def create_grid(locked_positions={}):
    grid = [[(0,0,0) for _ in range(10)] for _ in range(20)]

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            if (j, i) in locked_positions:
                c = locked_positions[(j,i)]
                grid[i][j] = c
    return grid

def parsedate(dat):
    return {
        "year" : dat.year,
        "month" : dat.month,
        "day" : dat.day,
        "hour" : dat.hour,
        "minute" : dat.minute,
        "second" : dat.second
    }
def loaddate(dat):
    return datetime.datetime(
        dat["year"],
        dat["month"],
        dat["day"],
        dat["hour"],
        dat["minute"],
        dat["second"]
    )
def parsepiece(dat):
    return {
        "x" : dat.x,
        "y" : dat.y,
        "shape" : dat.shape,
        "rotation" : dat.rotation
    }
def loadpiece(dat):
    result = Piece(dat["x"],dat["y"],dat["shape"])
    result.rotation = dat["rotation"]
    return result

class GameSave:
    def __init__(self,rawdata):
        try:
            if rawdata["empty"]:
                self.empty = True
            else:
                self.empty = False
            if not self.empty:
                self.score = rawdata["score"]
                self.level = rawdata["level"]
                self.curpiece = loadpiece(rawdata["pieces"]["cp"])
                self.nextpiece = loadpiece(rawdata["pieces"]["np"])
                if rawdata["pieces"]["hp"] is not None:
                    self.holdpiece = loadpiece(rawdata["pieces"]["hp"])
                else:
                    self.holdpiece = None
                self.lp = ast.literal_eval(rawdata["board"])
                self.bp = rawdata["blockplaced"]
                self.time = loaddate(rawdata["time"])
                self.gtime = loaddate(rawdata["gtime"])
                self.lc = rawdata["linescleared"]
                self.lclevel = rawdata["lc_level"]
                self.selected = False
        except:
            self.empty = True
    def play(self,saveaddress):
        main(win,self.level,self.lclevel,self.lc,self.lp,self.curpiece,self.nextpiece,self.holdpiece,self.bp,self.score,saveaddress)
    def display(self,win,x,y,ev):

        for event in ev:
            if event.type == pygame.MOUSEBUTTONDOWN:
                if pygame.mouse.get_pos()[0] > x and pygame.mouse.get_pos()[1] > y and pygame.mouse.get_pos()[1] < y + 100:
                    self.selected = True
                else:
                    self.selected = False

        if not self.empty:
            draw_text(win,str(self.time),28,(255,255,255),0+x,0+y)
            draw_text(win,"Level: "+str(self.level),28,(255,255,255),200+x,0+y)
            draw_text(win,"Score: "+str(self.score),28,(255,255,255),0+x,30+y)
            if self.selected:
                pygame.draw.rect(win,(0,128,0),(500+x,20+y,25,25))
        else:
            draw_text(win,"Empty save",28,(255,255,255),0+x,0+y)
#TODO Finish gamesave class

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
        if not MUTE:
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

def draw_hold(shape, surface):
    font = pygame.font.SysFont('Consolas', 30)
    label = font.render('Hold', 1, (255,255,255))

    sx = 200
    sy = 200
    if shape is not None:
        format = shape.shape[shape.rotation % len(shape.shape)]
        shape.x = 5
        shape.y = 0
        for i, line in enumerate(format):
            row = list(line)
            for j, column in enumerate(row):
                if column == '0':
                    pygame.draw.rect(surface, shape.color, (sx + j*block_size, sy + i*block_size, block_size, block_size), 0)

    surface.blit(label, (sx + 10, sy - 30))

def writeappdata():
    with open(DATADIR,"w+") as f:
        f.write(json.dumps(DATA))

def update_score(nscore):

    if int(nscore) > DATA["stats"]["highscore"]:
        DATA["stats"]["highscore"] = nscore
        writeappdata()

def max_score():
    return DATA["stats"]["highscore"]

DEBUG = False
def draw_window(surface, grid, score=0, last_score = 0):
    global _wctick
    global ttick
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
    label = font.render('High Score: ' + str(last_score), 1, (255,255,255))

    sx = top_left_x - 200
    sy = top_left_y + 200

    surface.blit(label, (sx + -80, sy + 160))
    draw_text(win,parsedtime,48,(255,255,255),0,0)
    draw_text(win,"Level: " + str(level),30,(255,255,255),0,50)
    draw_text(win,"Lines Left: " + str(requirement-lines_cleared),30,(255,255,255),0,100)
    draw_text(win, "Lines Cleared: " + str(lc),30,(255,255,255),0,150)
    draw_text(win,"Blocks Placed: "+str(bp),30,(255,255,255),0,200)

    if DEBUG:
        draw_text(win,str(shape_stats),30,(255,255,255),0,250)
        draw_text(win,"FPS: "+str(round(clock.get_fps())),30,(255,255,255),0,300)

    for i in range(len(grid)):
        for j in range(len(grid[i])):
            pygame.draw.rect(surface, grid[i][j], (top_left_x + j*block_size, top_left_y + i*block_size, block_size, block_size), 0)

    pygame.draw.rect(surface, (255, 0, 0), (top_left_x, top_left_y, play_width, play_height), 5)
    if DATA["config"]["grid"]:
        draw_grid(surface, grid)
    if paused:
        draw_text_middle(win, "You are Paused", 60, (255, 255, 255))
    if _wctick > 0:
        if _wctick > 100:
            _wctick = 0
        else:
            _wctick += 1
            draw_text_middle(win,"Well Cleared",60,(255,255,255))
    if ttick > 0:
        if ttick > 100:
            ttick = 0
        else:
            ttick += 1
            draw_text_middle(win,"TETRIS",60,(255,255,255))
    #pygame.display.update()
level = 1
def main(win,slevel = 1,lc_level = 0, linesclear = 0, lockedpos = {},cp=None,np=None,hp=None,blockplace=0,sscore=0,saveaddress=-1):
    pygame.mouse.set_visible(False)
    global grid
    global level
    global requirement
    global lines_cleared
    global lc
    global bp
    global parsedtime
    global holdpiece
    global paused
    global _wctick
    global ttick
    global DEBUG
    global clock
    global shape_stats
    global DATA
    level = slevel
    DATA["stats"]["gamesplayed"] += 1
    holdpiece = hp
    lc = linesclear
    bp = blockplace
    paused = False
    # put a) here
    last_score = max_score()
    locked_positions = lockedpos
    grid = create_grid(locked_positions)
    shape_stats = [0,0,0,0,0,0,0]
    change_piece = False
    run = True
    if cp is None:
        current_piece = get_shape()
    else:
        current_piece = cp
    if np is None:
        next_piece = get_shape()
    else:
        next_piece = np
    clock = pygame.time.Clock()
    fall_time = 0
    # put steps b), c), and d) here
    fall_speed = 0.5 - (level * 0.02)
    level_time = 0
    score = sscore
    requirement = 4 + ((level - 1) * 4)
    lines_cleared = lc_level
    _linetick = 0
    _ctick = 0
    _gamestart = datetime.datetime.now()
    _wctick = 0
    ttick = 0
    wc = False
    while run:

        # put steps e) - r) here
        grid = create_grid(locked_positions)
        fall_time += clock.get_rawtime()
        level_time += clock.get_rawtime()
        clock.tick()
        _parsedtime = round((datetime.datetime.now() - _gamestart).total_seconds())
        parsedtime = datetime.datetime(2022,1,1,_parsedtime // 3600,(_parsedtime % 3600) // 60, (_parsedtime % 3600) % 60).strftime("%H:%M:%S")
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
                writeappdata()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
                # step s) is here

            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and not paused:
                    current_piece.x -= 1
                    if not valid_space(current_piece, grid):
                        current_piece.x += 1

                elif event.key == pygame.K_RIGHT and not paused:
                    current_piece.x += 1
                    if not valid_space(current_piece, grid):
                        current_piece.x -= 1

                elif event.key == pygame.K_UP and not paused:
                    # rotate shape
                    current_piece.rotation = current_piece.rotation + 1 % len(current_piece.shape)
                    if not valid_space(current_piece, grid):
                        current_piece.rotation = current_piece.rotation - 1 % len(current_piece.shape)
                elif event.key == pygame.K_q:
                    if saveaddress < 0:
                        kq = confirm(win,"Are you sure you want to quit without saving?")
                        if kq:
                            run = False
                            pygame.mouse.set_visible(True)
                    if saveaddress > -1:
                        run = False
                        update_score(score)
                        writeappdata()
                        pygame.mouse.set_visible(True)
                        DATA["saves"][saveaddress] = {
                            "empty": False,
                            "score": score,
                            "level": level,
                            "board": str(locked_positions),
                            "lc_level": lines_cleared,
                            "linescleared": lc,
                            "blockplaced": bp,
                            "time": parsedate(datetime.datetime.now()),
                            "gtime": parsedate(
                                datetime.datetime(2022, 1, 1, _parsedtime // 3600, (_parsedtime % 3600) // 60,
                                                  (_parsedtime % 3600) % 60)),
                            "pieces": {
                                "cp": parsepiece(current_piece),
                                "np": parsepiece(next_piece),
                                "hp": None
                            }
                        }
                        if holdpiece is not None:
                            DATA["saves"][saveaddress]["pieces"]["hp"] = parsepiece(holdpiece)
                elif event.key == pygame.K_s:
                    if saveaddress < 0:
                        _i = -1
                        for save in DATA["saves"]:
                            _i += 1
                            if save["empty"]:
                                break
                        DATA["saves"][_i] = {
                            "empty" : False,
                            "score" : score,
                            "level" : level,
                            "board" : str(locked_positions),
                            "lc_level" : lines_cleared,
                            "linescleared" : lc,
                            "blockplaced" : bp,
                            "time" : parsedate(datetime.datetime.now()),
                            "gtime" : parsedate(datetime.datetime(2022,1,1,_parsedtime // 3600,(_parsedtime % 3600) // 60, (_parsedtime % 3600) % 60)),
                            "pieces" : {
                                "cp" : parsepiece(current_piece),
                                "np" : parsepiece(next_piece),
                                "hp" : None
                            }
                        }
                        if holdpiece is not None:
                            DATA["saves"][_i]["pieces"]["hp"] = parsepiece(holdpiece)
                        saveaddress = _i
                    else:
                        DATA["saves"][saveaddress] = {
                            "empty": False,
                            "score": score,
                            "level": level,
                            "board": str(locked_positions),
                            "lc_level": lines_cleared,
                            "linescleared": lc,
                            "blockplaced": bp,
                            "time": parsedate(datetime.datetime.now()),
                            "gtime": parsedate(
                                datetime.datetime(2022, 1, 1, _parsedtime // 3600, (_parsedtime % 3600) // 60,
                                                  (_parsedtime % 3600) % 60)),
                            "pieces": {
                                "cp": parsepiece(current_piece),
                                "np": parsepiece(next_piece),
                                "hp": None
                            }
                        }
                        if holdpiece is not None:
                            DATA["saves"][saveaddress]["pieces"]["hp"] = parsepiece(holdpiece)
                elif event.key == pygame.K_ESCAPE and not paused:
                    paused = True
                    ofs = fall_speed
                    fall_speed = 100000# Technically if you left it for a few hours it would drop
                elif event.key == pygame.K_ESCAPE and paused:
                    paused = False
                    fall_speed = ofs
                elif event.key == pygame.K_SLASH and holdpiece is None and not paused:
                    holdpiece = current_piece
                    current_piece = next_piece
                    next_piece = get_shape()
                elif event.key == pygame.K_SLASH and holdpiece is not None and not paused:
                    _hp = holdpiece
                    holdpiece = current_piece
                    current_piece = _hp
                elif event.key == pygame.K_DOWN:
                    current_piece.y += 1
                    if not valid_space(current_piece,grid):
                        current_piece.y -= 1
                elif event.key == pygame.K_F3 and not DEBUG:
                    DEBUG = True
                elif event.key == pygame.K_F3 and DEBUG:
                    DEBUG = False
        ki = pygame.key.get_pressed()

        if ki[pygame.K_DOWN]:

            _linetick += 1
            if _linetick > 50:
                fall_speed = 0
                _linetick = -50 #Debounce
        else:
            _linetick = 0
        # put steps t) - F) here

        shape_pos = convert_shape_format(current_piece)
        for i in range(len(shape_pos)):
            x,y = shape_pos[i]
            if y > -1:
                try:
                    grid[y][x] = current_piece.color
                except:
                    pass
        if change_piece:
            bp += 1
            wc = False
            for pos in shape_pos:
                p = (pos[0],pos[1])
                locked_positions[p] = current_piece.color
            current_piece.incstat()
            fall_speed = 0.5 - (level * 0.02)
            if fall_speed < 0:
                fall_speed = 0
            requirement = 4 + ((level - 1) * 4)
            current_piece = next_piece
            next_piece = get_shape()
            change_piece = False
            pscore = clear_rows(grid,locked_positions)
            oscore = score
            if pscore == 1:
                score += 10
            elif pscore == 2:
                score += 25
            elif pscore == 3:
                score += 50
            elif pscore == 4:
                score += 100
                ttick = 1
                DATA["stats"]["tetris"] += 1
            lines_cleared += pscore
            DATA["stats"]["points"] += (score-oscore)
            DATA["stats"]["linescleared"] += pscore
            lc += pscore
            if lines_cleared > (requirement - 1):
                level += 1
                if level > DATA["stats"]["highestlevel"]:
                    DATA["stats"]["highestlevel"] = level
                lines_cleared = 0

        # follow step G) here
        draw_window(win,grid,score,last_score)
        # put steps H) - O) here
        draw_next_shape(next_piece,win)
        draw_hold(holdpiece,win)
        pygame.display.update()
        clock.tick()
        #score += (10 * clear_rows(grid, locked_positions))

        if check_lost(locked_positions):
            draw_text_middle(win,"Game Over",80,(255,255,255))
            writeappdata()
            pygame.display.update()
            pygame.time.delay(1500)
            run = False
            level = 0
            lines_cleared = 0
            update_score(score)
            pygame.mouse.set_visible(True)
        empty = True
        if not wc and bp > 0:
            for row in grid[16:20]:
                for line in row:
                    for block in line:
                        if block == 0:
                            pass
                        else:
                            empty = False
        else:
            empty = False
        if empty:
            score += 200
            wc = True
            DATA["stats"]["wellclears"] += 1
            _wctick = 1
    main_menu(win)

def main_menu(win):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    if not STRIPPED:
        im = pygame.image.load(ASSETSDIR + "/background.jpg")
    run = True
    b = Button((0,255,0),s_width/2 - 50,100,200,100,"Play")
    b2 = Button ((255,0,0),s_width/2 - 50,600,200,100,"Quit")
    b3 = Button((0,128,128),s_width/2 - 50,300,200,100,"Options")
    b4 = Button((0,128,128),s_width/2 - 50,450,200,100,"Statistics")
    while run:
        win.fill((0,0,0))
        if not STRIPPED:
            win.blit(im,(s_width/2-(im.get_rect().width/2),30))
        draw_text(win,"Tetris 22",60,(255,255,255),(s_width/2 - 50),0)

        draw_text(win,"1.0 (Yay!)",30,(255,255,255),0,0)
        b.draw(win)
        b2.draw(win)
        b3.draw(win)
        b4.draw(win)

        pygame.display.update()
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                run = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    playmen(win)
                elif event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_o:
                    settingsm(win)
                elif event.key == pygame.K_s:
                    vmem(win)
        if b.isOver(ev):
            playmen(win)
        elif b2.isOver(ev):
            run = False
        elif b3.isOver(ev):
            settingsm(win)
        elif b4.isOver(ev):
            vmem(win)

    pygame.display.quit()
    pygame.quit()
    writeappdata()
    sys.exit()

def settingsm(win):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    global MUTE
    global FULLSCREEN
    run = True
    b = Button((0, 128, 128), 50, 0, 300, 100, "Toggle Fullscreen")
    b1 = Button((0, 128, 128), 50, 150, 300, 100, "Toggle Sounds")
    b2 = Button((0, 128, 128), 50, 600, 300, 100, "Back to Menu")
    b3 = Button((0, 128, 128), 50, 300, 300, 100, "Delete Highscore")
    b4 = Button((0, 128, 128), 50, 450, 300, 100, "Toggle Grid (" + str(DATA["config"]["grid"]) + ")")
    while run:
        win.fill((0,0,0))
        draw_text_middle(win,"Configuration Menu",60,(255,255,255))
        b.draw(win)
        b1.draw(win)
        b2.draw(win)
        b3.draw(win)
        b4.draw(win)
        pygame.display.update()
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_f and not FULLSCREEN:
                    FULLSCREEN = True
                    DATA["config"]["fullscreen"] = True
                    pygame.display.set_mode((1280,720),pygame.FULLSCREEN)
                    pygame.time.delay(1000)
                elif event.key == pygame.K_f and FULLSCREEN:
                    FULLSCREEN = False
                    DATA["config"]["fullscreen"] = False
                    pygame.display.set_mode((1280,720))
                    pygame.time.delay(1000)
                elif event.key == pygame.K_m and not MUTE:
                    MUTE = True
                    DATA["config"]["mute"] = True
                    pygame.mixer.music.stop()
                    pygame.time.delay(200)
                elif event.key == pygame.K_m and MUTE:
                    MUTE = False
                    DATA["config"]["mute"] = False
                    pygame.mixer.music.play(-1)
                    pygame.time.delay(200)
                elif event.key == pygame.K_r:
                    x = confirm(win,"Are you sure that you want to delete the highscore")
                    if x:
                        DATA["stats"]["highscore"] = 0
                        writeappdata()
        if b.isOver(ev) and not FULLSCREEN:
            FULLSCREEN = True
            DATA["config"]["fullscreen"] = True
            pygame.display.set_mode((1280, 720), pygame.FULLSCREEN)
            pygame.time.delay(1000)
        elif b.isOver(ev) and FULLSCREEN:
            FULLSCREEN = False
            DATA["config"]["fullscreen"] = False
            pygame.display.set_mode((1280, 720))
            pygame.time.delay(1000)
        elif b1.isOver(ev) and not MUTE:
            MUTE = True
            DATA["config"]["mute"] = True
            pygame.mixer.music.stop()
            pygame.time.delay(200)
        elif b1.isOver(ev) and MUTE:
            MUTE = False
            DATA["config"]["mute"] = False
            pygame.mixer.music.play(-1)
            pygame.time.delay(200)
        elif b2.isOver(ev):
            run = False
        elif b3.isOver(ev):
            x = confirm(win, "Are you sure that you want to delete the highscore")
            if x:
                DATA["stats"]["highscore"] = 0
                writeappdata()
        elif b4.isOver(ev) and not DATA["config"]["grid"]:
            DATA["config"]["grid"] = True
            b4 = Button((0, 128, 128), 50, 450, 300, 100, "Toggle Grid (" + str(DATA["config"]["grid"]) + ")")
        elif b4.isOver(ev) and DATA["config"]["grid"]:
            DATA["config"]["grid"] = False
            b4 = Button((0, 128, 128), 50, 450, 300, 100, "Toggle Grid (" + str(DATA["config"]["grid"]) + ")")
    writeappdata()

def vmem(win):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    global DATA
    run = True
    b = Button((255,0,0),50,500,200,75,"Reset")
    b1 = Button((0,128,128),50,650,200,75,"Back")
    while run:
        win.fill((0,0,0))
        inc = -1
        for k in DATA["stats"]:
            inc += 1
            draw_text(win,k + " : " + str(DATA["stats"][k]),36,(255,255,255),0,inc*50)
        b.draw(win)
        b1.draw(win)
        pygame.display.update()
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
                elif event.key == pygame.K_r:
                    if confirm(win,"Are you sure you want to reset stats?"):
                        for k in DATA["stats"]:
                            DATA["stats"][k] = 0
                        writeappdata()
        if b.isOver(ev):
            if confirm(win, "Are you sure you want to reset stats?"):
                for k in DATA["stats"]:
                    DATA["stats"][k] = 0
                writeappdata()
        elif b1.isOver(ev):
            run = False

def playmen(win):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    saves = [GameSave(x) for x in DATA["saves"]]
    run = True
    b = Button((0,255,0),50,600,200,50,"New Game")
    b1 = Button((0,128,128),300,600,200,50,"Back")
    b2 = Button((0,128,0),550,600,200,50,"Play Selected")
    b3 = Button((255,0,0),800,600,200,50,"Delete")
    while run:
        win.fill((0,0,0))
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        inc = -1

        b.draw(win)
        b1.draw(win)
        b2.draw(win)
        b3.draw(win)

        if b.isOver(ev):
            hasemoty = 0
            for save in saves:
                if not save.empty:
                    hasemoty += 1
            p = False
            if hasemoty == len(saves):
                p = confirm(win,"No empty saves. New game?")
            if p or hasemoty < len(saves):
                newgamemen(win)
        elif b1.isOver(ev):
            run = False
        elif b2.isOver(ev):
            try:
                ince = -1
                for save in saves:
                    ince += 1
                    if save.selected:
                        save.play(ince)
            except:
                pass
        elif b3.isOver(ev):
            incd = -1
            for save in saves:
                incd += 1
                if save.selected:
                    del DATA["saves"][incd]
                    DATA["saves"].insert(incd,{"empty":True})
                    saves[incd].empty = True
        for save in saves:
            inc += 1
            save.display(win,0,inc*100,ev)
        pygame.display.update()

def newgamemen(win):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    run = True
    b = Button((0,255,0),50,0,200,100,"Easy")
    b1 = Button((255,255,0),50,150,200,100,"Moderate")
    b2 = Button((255,128,0),50,300,200,100,"Difficult")
    b3 = Button((255,0,0),50,450,200,100,"Ridiculous")
    b4 = Button((0,128,128),50,600,200,100,"Back")
    while run:
        win.fill((0, 0, 0))
        ev = pygame.event.get()
        for event in ev:
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    run = False
        b1.draw(win)
        b2.draw(win)
        b.draw(win)
        b3.draw(win)
        b4.draw(win)
        pygame.display.update()
        if b4.isOver(ev):
            run = False
        elif b.isOver(ev):
            main(win,lockedpos={})
        elif b1.isOver(ev):
            main(win,8,lockedpos={})
        elif b2.isOver(ev):
            main(win,15,lockedpos={})
        elif b3.isOver(ev):
            main(win,25,lockedpos={})

def confirm(win,msg):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    run = True
    while run:
        win.fill((0,0,128))
        draw_text_middle(win,msg + " [Y/N]",36,(255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_y:
                    return True
                elif event.key == pygame.K_n:
                    return False
        pygame.display.update()

def display_message(win,msg):
    pygame.mouse.set_cursor(pygame.cursors.Cursor(pygame.SYSTEM_CURSOR_ARROW))
    run = True
    while run:
        win.fill((0,128,0))
        draw_text_middle(win,msg,36,(255,255,255))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                writeappdata()
                pygame.mixer.music.stop()
                pygame.display.quit()
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return
        pygame.display.update()

def checkinternet(website,timeout):

    try:
        # requesting URL
        request = requests.get(website, timeout=timeout)
        return True

    # catching exception
    except (requests.ConnectionError, requests.Timeout) as exception:
        return False

if "-s" in sys.argv or "--stripped" in sys.argv:
    STRIPPED = True
else:
    STRIPPED = False

if not STRIPPED:

    if not checkinternet("https://github.com",5) and (not os.path.isfile(ASSETSDIR + "/logo.png") or not os.path.isfile(ASSETSDIR + "/tetris.mp3") or not os.path.isfile(ASSETSDIR + "/laser.wav") or not os.path.isfile(ASSETSDIR + "/background.jpg")):
        win.fill((0,0,255))
        draw_text_middle(win,"Failed to download missing assets. Tetris will quit in 5 seconds",30,(255,255,255))
        pygame.display.update()
        pygame.time.delay(5000)
        sys.exit(-1)

    if not os.path.isfile(ASSETSDIR + "/logo.png"):
        urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/pytetris/raw/main/logo.png",ASSETSDIR + "/logo.png")

    pygame.display.set_icon(pygame.image.load(ASSETSDIR + "/logo.png"))
    if not os.path.isfile(ASSETSDIR + "/Tetris.mp3"):
        urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/pytetris/raw/main/Tetris.mp3",ASSETSDIR + "/tetris.mp3")
    if not os.path.isfile(ASSETSDIR + "/laser.wav"):
        urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/pytetris/raw/main/laser.wav",ASSETSDIR + "/laser.wav")
    music = pygame.mixer.music.load(ASSETSDIR + "/tetris.mp3")
    if not os.path.isfile(ASSETSDIR + "/background.jpg"):
        urllib.request.urlretrieve("https://github.com/Enderbyte-Programs/pytetris/raw/main/background.jpg",ASSETSDIR + "/background.jpg")
    if not MUTE:
        pygame.mixer.music.play(-1)
    lsr = pygame.mixer.Sound(ASSETSDIR + "/laser.wav")

main_menu(win)  # start game
