#!/usr/bin/python3

import random, copy, sys, pygame, time
from pygame.locals import *
from button import *

BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
FPS = 60


START_FLAG = True
CHATBOX_WIDTH = 900
CHATBOX_HEIGHT = 150
OPTION_WIDTH = 200
OPTION_HEIGHT = 50
GAMESTATE = 'INGAME'
TEXT_WIDTH = 60
TEXT_HEIGHT = 560
count = 0
option_list = []
FLAGS = [False] * 5
OINDEX = 0
OSCRIPTS = []
OCOUNT = 0
BAD_END_FLAG = False

""""
start gamestate: 
load the white album bg pic
the game start button
"""


def start_gamestate(surface):
    BGImg = pygame.image.load('wa_pic.jpg').convert()
    start_button = button(WHITE, 570, 500, 180, 40, '画面をクリックでスタート')
    surface.blit(BGImg, (0, 0))
    start_button.draw(surface, WHITE)

    return start_button


def draw_chatbox(surface):
    s = pygame.Surface((CHATBOX_WIDTH, CHATBOX_HEIGHT))
    s.set_alpha(128)
    s.fill(WHITE)
    surface.blit(s,(50,550))


""""
second gamestate should first load the bg pic: shinkai makoto.
Then komatsu and then the chatbox.
Then the first line of scripts.
"""


def second_gamestate(surface, option_index):
    global FLAGS, BAD_END_FLAG
    if option_index == -1 or (option_index == 0 and BAD_END_FLAG):
        surface.fill(BLACK)
        BGImg = pygame.image.load('bg1.jpg')
        surface.blit(BGImg, (0, 0))

        KIMG = pygame.image.load('komatu.png')
        surface.blit(KIMG, (800, 300))
        draw_chatbox(surface)
    elif option_index == 0 or (option_index == 1 and BAD_END_FLAG):
        surface.fill(BLACK)
        BGImg = pygame.image.load('bg2.jpg')
        surface.blit(BGImg, (0, 0))

        KIMG = pygame.image.load('komatu.png')
        surface.blit(KIMG, (800, 300))
        draw_chatbox(surface)
    else:
        surface.fill(BLACK)
        BGImg = pygame.image.load('bg3.jpg')
        surface.blit(BGImg, (0, 0))

        KIMG = pygame.image.load('komatu.png')
        surface.blit(KIMG, (800, 300))
        draw_chatbox(surface)
        FLAGS = [False] * 5


    for i in range(len(FLAGS)):
        if FLAGS[i]:
            RIMG = pygame.image.load('pic{}.png'.format(i))
            if i == 0:
                surface.blit(RIMG, (400, 9))
            elif i == 1:
                surface.blit(RIMG, (400, -100))


def main():
    global START_FLAG, GAMESTATE, count, option_list
    pygame.init()
    fpsClock = pygame.time.Clock()
    DISPLAYSURF = pygame.display.set_mode((1280, 720), 0, 32)
    pygame.display.set_caption('ホワイトアルバム')
    play()
    f = open('script.txt', 'r')
    scripts = f.readlines()
    print(scripts)
    fontObj = pygame.font.Font('fonts/07gothic.ttf', 24)
    option_index = -1

    while True:  # main game loop
        if START_FLAG:
            print("starting game...")
            start_gamestate(DISPLAYSURF)
            START_FLAG = False
        for event in pygame.event.get():
            pos = pygame.mouse.get_pos()
            if event.type == QUIT:
                pygame.quit()
                sys.exit()
            elif event.type == pygame.MOUSEBUTTONDOWN:
                if GAMESTATE == 'CHOOSING':
                    for i in range(3):
                        if option_list[i].isOver(pos) and option_index != -1:
                            print(i)
                            GAMESTATE = "INGAME"
                            f.close()
                            f = open('scripts/BA{}{}.txt'.format(option_index, i), 'r')
                            scripts = f.readlines()
                            count = 0
                            reset_screen(DISPLAYSURF, fontObj, scripts, option_index)
                else:
                    option_index = reset_screen(DISPLAYSURF, fontObj, scripts, option_index)
        pygame.display.update()
        fpsClock.tick(FPS)
    f.close()


def reset_screen(surface, fontObj, scripts, option_index):
    global count
    second_gamestate(surface, option_index)
    option_index = print_script(surface, fontObj, scripts, option_index)
    count += 1
    return option_index


def print_script(surface, fontObj, scripts, option_index):
    global count, GAMESTATE, FLAGS, OSCRIPTS, OCOUNT, OINDEX, BAD_END_FLAG
    BAD_END_FLAG = False
    cur_script = scripts[count][:-1]
    if cur_script.startswith('option'):
        OINDEX, OSCRIPTS, OCOUNT = int(cur_script[6]), scripts[count+1: count+4], count+3
        option_index = int(cur_script[6])
        print("get into option")
        GAMESTATE = 'CHOOSING'
        show_options(surface, scripts[count+1: count+4])
        count += 3
        return option_index
    elif cur_script.startswith('pic'):
        tmp_text_surface = fontObj.render('............................................', 0, BLACK)
        surface.blit(tmp_text_surface, [TEXT_WIDTH, TEXT_HEIGHT])
        FLAGS = [False] * 5
        FLAGS[int(cur_script[3])] = True
        return option_index
    elif cur_script.startswith('BAD_END'):
        BAD_END_FLAG = True
        GAMESTATE = 'CHOOSING'
        show_options(surface, OSCRIPTS)
        count = OCOUNT
        return OINDEX
    elif cur_script.startswith('BADEND'):
        time.sleep(1)
        pygame.quit()
        sys.exit()
    else:
        if len(cur_script) > 37:
            multi = 0
            cur_scriptlist = [cur_script[i: i + 37] for i in range(0, len(cur_script), 37)]
            for chunk in cur_scriptlist:
                tmp_text_surface = fontObj.render(chunk, 0, BLACK)
                surface.blit(tmp_text_surface, [TEXT_WIDTH, TEXT_HEIGHT + 30 * multi])
                multi += 1
        else:
            tmp_text_surface = fontObj.render(cur_script, 0, BLACK)
            surface.blit(tmp_text_surface, [TEXT_WIDTH, TEXT_HEIGHT])
        return option_index


def show_options(surface, option_texts):
    global option_list
    print(option_texts)
    option_list = [button(WHITE, 600, 200 + i * 100, OPTION_WIDTH, OPTION_HEIGHT, option_texts[i][:-1])
                   for i in range(3)]
    for i in option_list:
        i.draw(surface, WHITE)
    return option_list


def play():
    pygame.mixer.init()
    pygame.mixer.music.load("wg.wav")
    pygame.mixer.music.play(-1, 0)


if __name__ == '__main__':
    main()
