import pygame

import random

from pygame.locals import *

text_file = open("WebDic.txt", "r")

word = ""
Wordlist = []
for letter in text_file.read():

    if letter != " ":
        word = word + letter
    else:
        Wordlist.append(word)
        word = ""

points_file_r = open("points.txt", "r")

num = ""
Pointslist = []
for n in points_file_r.read():

    if n != " ":
        num = num + n
    else:
        Pointslist.append(int(num))
        num = ""

if num != "":
    Pointslist.append(int(num))

Pointslist = sorted(Pointslist, reverse = True)

points_file_r.close()

pygame.init()

pygame.font.init()
word_font = pygame.font.SysFont("calibri", 36, bold = True)
number_font = pygame.font.SysFont("calibri", 54, bold = True)

IMAGE_MAIN = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteMain.png")
IMAGE_LIST = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteList.png")
IMAGE_BUTTON = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteButton.png")
IMAGE_SMALLBUTTON_ONE = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonOne.png")
IMAGE_SMALLBUTTON_TWO = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonTwo.png")
IMAGE_SMALLBUTTON_THREE = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonThree.png")
IMAGE_SMALLBUTTON_FOUR = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonFour.png")
IMAGE_SMALLBUTTON_FORFEIT = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonForfeit.png")
IMAGE_SMALLBUTTON_HINT = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonHint.png")
IMAGE_SMALLBUTTON_QUIT = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonQuit.png")
IMAGE_SMALLBUTTON_REPLAY = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteSmallButtonReplay.png")
IMAGE_INPUT = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteInput.png")
IMAGE_INDICATOR = pygame.image.load(r"C:\Users\Fran\Desktop\Code\Project WORD\WordpasteIndicator.png")

GREEN_LIGHT = (200, 255, 200)
RED = (255, 153, 153)

screen_width = 600
screen_height = 700
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Wordpaste")

class Rectangle:
    def __init__(self, width=0, height=0, color=(0, 0, 0)):
        self.width = width
        self.height = height
        self.color = color
        self.surface = pygame.Surface((self.width, self.height))
    def draw(self, x, y):
        self.surface.fill(self.color)
        screen.blit(self.surface, (x, y))

button = Rectangle(270, 80, (255, 255, 255))

word_list = Rectangle(400, 450, (255, 255, 255))

word_input = Rectangle(400, 100, (255, 255, 255))

small_button = Rectangle(70, 70, (255, 255, 255))

player_indicator_tab = Rectangle(400, 25, (255, 255, 255))

GAMESTATE_MENU = 0
GAMESTATE_PLAYERNUM = 1
GAMESTATE_NAMES = 2
GAMESTATE_GAME = 3
GAMESTATE_SCOREBOARD = 4
GAMESTATE_SINGLEPLAYER = 5
GAMESTATE_SINGLEPLAYER_SCOREBOARD = 6
current_state = GAMESTATE_MENU

leftclickdown = False
scroll_index = 0

input_text = ""
previous_word = ""
inputing_text = False
list_of_words = []

number_of_players = 0
list_of_names = []

current_player = 0
turn = 0

points = [0, 0, 0, 0]

number_of_hints = [0, 0, 0, 0]

running = True
while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        elif event.type == KEYDOWN:
            
            if event.key >= ord("a") and event.key <= ord("z") and inputing_text and len(input_text) < 19:
                input_text = input_text + chr(event.key)
            if event.key == K_BACKSPACE and inputing_text and len(input_text) > 0:
                input_text = input_text[:-1]                
            if event.key == K_RETURN and inputing_text and len(input_text) > 2:
                
                if current_state == GAMESTATE_GAME or current_state == GAMESTATE_SINGLEPLAYER:
                    
                    if (previous_word[-2:] == input_text[:2] or len(list_of_words) == 0) and input_text in Wordlist and input_text not in list_of_words:
                        list_of_words.append(input_text)
                        previous_word = input_text
                        input_text = ""
                        turn += 1
                        current_player = turn % number_of_players
                        
                        if current_state == GAMESTATE_SINGLEPLAYER:

                            Botlist = []
                            for i in Wordlist:
                                if (previous_word[-2:] == i[:2] or len(list_of_words) == 0) and i not in list_of_words:
                                    Botlist.append(i)

                            if len(Botlist) > 0:
                                random_word = Botlist[random.randint(0, len(Botlist) - 1)]                   
                                list_of_words.append(random_word)
                                previous_word = random_word
                            else:
                                print("No such word")
                    else:
                        if previous_word[-2:] != input_text[:2]:
                            print("The edges don't match")
                            word_input.color = RED
                        elif input_text not in Wordlist:
                            print("That's not a word")
                            word_input.color = RED
                        elif input_text in list_of_words:
                            print("Already used that one")
                            word_input.color = RED
                            
                elif current_state == GAMESTATE_NAMES:

                    if len(list_of_names) < number_of_players:
                        list_of_names.append(input_text)
                        input_text = ""
                    if len(list_of_names) == number_of_players:
                        current_state = GAMESTATE_GAME
                                
        elif event.type == MOUSEBUTTONDOWN:
            if event.button == 1:
                leftclickdown = True
            if event.button == 4 and len(list_of_words) > 11 and (len(list_of_words) - 11 - scroll_index) > 0:
                scroll_index += 1
            if event.button == 5 and len(list_of_words) > 11 and scroll_index > 0:
                scroll_index -= 1

    if current_state == GAMESTATE_MENU:

        screen.blit(IMAGE_MAIN, (0, 0))
        
        x_button = int((screen_width - button.width) / 2)
        y_button = int((screen_height - button.height) / 2) - 100
        button.draw(x_button, y_button)
        screen.blit(IMAGE_BUTTON, (x_button, y_button))
        
        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_button and x_mouse <= x_button + button.width and\
               y_mouse >= y_button and y_mouse <= y_button + button.height:
                   current_state = GAMESTATE_PLAYERNUM

    elif current_state == GAMESTATE_PLAYERNUM:

        screen.blit(IMAGE_MAIN, (0, 0))

        x_player1 = int((screen_width - small_button.width) / 2) - 150
        y_player1 = int((screen_height - small_button.height) / 2)
        small_button.draw(x_player1, y_player1)
        screen.blit(IMAGE_SMALLBUTTON_ONE, (x_player1, y_player1))

        x_player2 = int((screen_width - small_button.width) / 2) - 50
        y_player2 = int((screen_height - small_button.height) / 2)
        small_button.draw(x_player2, y_player2)
        screen.blit(IMAGE_SMALLBUTTON_TWO, (x_player2, y_player2))

        x_player3 = int((screen_width - small_button.width) / 2) + 50
        y_player3 = int((screen_height - small_button.height) / 2)
        small_button.draw(x_player3, y_player3)
        screen.blit(IMAGE_SMALLBUTTON_THREE, (x_player3, y_player3))

        x_player4 = int((screen_width - small_button.width) / 2) + 150
        y_player4 = int((screen_height - small_button.height) / 2)
        small_button.draw(x_player4, y_player4)
        screen.blit(IMAGE_SMALLBUTTON_FOUR, (x_player4, y_player4))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_player1 and x_mouse <= x_player1 + small_button.width and\
               y_mouse >= y_player1 and y_mouse <= y_player1 + small_button.height:
                   print("click")
                   number_of_players = 1
                   current_state = GAMESTATE_SINGLEPLAYER
            elif x_mouse >= x_player2 and x_mouse <= x_player2 + small_button.width and\
               y_mouse >= y_player2 and y_mouse <= y_player2 + small_button.height:
                   print("click")
                   number_of_players = 2
                   current_state = GAMESTATE_NAMES
            elif x_mouse >= x_player3 and x_mouse <= x_player3 + small_button.width and\
               y_mouse >= y_player3 and y_mouse <= y_player3 + small_button.height:
                   print("click")
                   number_of_players = 3
                   current_state = GAMESTATE_NAMES
            elif x_mouse >= x_player4 and x_mouse <= x_player4 + small_button.width and\
               y_mouse >= y_player4 and y_mouse <= y_player4 + small_button.height:
                   print("click")
                   number_of_players = 4
                   current_state = GAMESTATE_NAMES

    elif current_state == GAMESTATE_NAMES:

        screen.blit(IMAGE_MAIN, (0, 0))

        x_list = int((screen_width - word_list.width) / 2)
        y_list = int((screen_height - word_list.height) / 2) - 75
        word_list.draw(x_list, y_list)
        screen.blit(IMAGE_LIST, (x_list, y_list))

        x_input = int((screen_width - word_input.width) / 2)
        y_input = int((screen_height - word_input.height) / 2) + 250
        word_input.draw(x_input, y_input)
        screen.blit(IMAGE_INPUT, (x_input, y_input))

        text_surface = word_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (x_input + 25, y_input + 30))

        for i in range(min(len(list_of_names), number_of_players)):
            text_surface = word_font.render(list_of_names[i], True, (0, 0, 0))
            screen.blit(text_surface, (x_list + 25, y_list + 10 + i*40))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_input and x_mouse <= x_input + word_input.width and\
               y_mouse >= y_input and y_mouse <= y_input + word_input.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   inputing_text = True

    elif current_state == GAMESTATE_GAME:

        screen.blit(IMAGE_MAIN, (0, 0))
        
        x_list = int((screen_width - word_list.width) / 2)
        y_list = int((screen_height - word_list.height) / 2) - 75
        word_list.draw(x_list, y_list)
        screen.blit(IMAGE_LIST, (x_list, y_list))

        x_input = int((screen_width - word_input.width) / 2)
        y_input = int((screen_height - word_input.height) / 2) + 250
        word_input.draw(x_input, y_input)
        screen.blit(IMAGE_INPUT, (x_input, y_input))

        text_surface = word_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (x_input + 25, y_input + 30))

        x_forfeit = int((screen_width - small_button.width) / 2) + 250
        y_forfeit = int((screen_height - small_button.height) / 2) + 225
        small_button.draw(x_forfeit, y_forfeit)
        screen.blit(IMAGE_SMALLBUTTON_FORFEIT, (x_forfeit, y_forfeit))

        x_hint = int((screen_width - small_button.width) / 2) + 250
        y_hint = int((screen_height - small_button.height) / 2) + 125
        small_button.draw(x_hint, y_hint)
        screen.blit(IMAGE_SMALLBUTTON_HINT, (x_hint, y_hint))

        text_hint = number_font.render(str(5 - number_of_hints[current_player]), True, (255, 255, 255))
        screen.blit(text_hint, (x_hint + 20, y_hint + 10))

        x_player_indicator = int((screen_width - player_indicator_tab.width) / 2)
        y_player_indicator = int((screen_height - player_indicator_tab.height) / 2) + 180
        player_indicator_tab.draw(x_player_indicator, y_player_indicator)
        screen.blit(IMAGE_INDICATOR, (x_player_indicator, y_player_indicator))

        text_player = word_font.render(list_of_names[current_player], True, (0, 0, 0))
        screen.blit(text_player, (x_player_indicator + 20, y_player_indicator - 5))

        for i in range(min(len(list_of_words), 11)):
            if len(list_of_words) < 11:
                text_surface = word_font.render(list_of_words[i], True, (0, 0, 0))
                screen.blit(text_surface, (x_list + 25, y_list + 10 + i*40))
            else:
                text_surface = word_font.render(list_of_words[i + len(list_of_words) - 11 - scroll_index], True, (0, 0, 0))
                screen.blit(text_surface, (x_list + 25, y_list + 10 + i*40))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_input and x_mouse <= x_input + word_input.width and\
               y_mouse >= y_input and y_mouse <= y_input + word_input.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   inputing_text = True

            if x_mouse >= x_forfeit and x_mouse <= x_forfeit + small_button.width and\
               y_mouse >= y_forfeit and y_mouse <= y_forfeit + small_button.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   loser = list_of_names[current_player]
                   points[current_player] -= 1
                   current_state = GAMESTATE_SCOREBOARD

            if x_mouse >= x_hint and x_mouse <= x_hint + small_button.width and\
               y_mouse >= y_hint and y_mouse <= y_hint + small_button.height:
                   print("click")
                   if number_of_hints[current_player] <= 4:
                       word_input.color = GREEN_LIGHT

                       Hintlist = []
                       for i in Wordlist:
                           if (previous_word[-2:] == i[:2] or len(list_of_words) == 0) and i not in list_of_words:
                                Hintlist.append(i)

                       if len(Hintlist) > 0:
                            random_word = Hintlist[random.randint(0, len(Hintlist) - 1)]                   
                            list_of_words.append(random_word)
                            previous_word = random_word
                            turn += 1
                            current_player = turn % number_of_players
                            number_of_hints[current_player] += 1
                       else:
                            print("No such word")

                   else:
                       print("No more hints")

    elif current_state == GAMESTATE_SCOREBOARD:

        screen.blit(IMAGE_MAIN, (0, 0))

        x_list = int((screen_width - word_list.width) / 2)
        y_list = int((screen_height - word_list.height) / 2) - 75
        word_list.draw(x_list, y_list)
        screen.blit(IMAGE_LIST, (x_list, y_list))

        x_again = int((screen_width - small_button.width) / 2) - 100
        y_again = int((screen_height - small_button.height) / 2) + 250
        small_button.draw(x_again, y_again)
        screen.blit(IMAGE_SMALLBUTTON_REPLAY, (x_again, y_again))

        x_quit = int((screen_width - small_button.width) / 2) + 100
        y_quit = int((screen_height - small_button.height) / 2) + 250
        small_button.draw(x_quit, y_quit)
        screen.blit(IMAGE_SMALLBUTTON_QUIT, (x_quit, y_quit))

        for i in range(number_of_players):
            
            names_surface = word_font.render(list_of_names[i], True, (0, 0, 0))
            screen.blit(names_surface, (x_list + 25, y_list + 10 + i*40))
        
            points_surface = word_font.render(str(points[i]), True, (0, 0, 0))
            screen.blit(points_surface, (screen_width - x_list - 50, y_list + 10 + i*40))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_again and x_mouse <= x_again + word_input.width and\
               y_mouse >= y_again and y_mouse <= y_again + word_input.height:
                   print("click")
                   print("Number of turns:", turn)
                   word_input.color = GREEN_LIGHT
                   list_of_words = []
                   previous_word = ""
                   turn = 0
                   current_state = GAMESTATE_GAME

            if x_mouse >= x_quit and x_mouse <= x_quit + word_input.width and\
               y_mouse >= y_quit and y_mouse <= y_quit + word_input.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   list_of_words = []
                   list_of_names = []
                   points = [0, 0, 0, 0]
                   previous_word = ""
                   turn = 0
                   current_state = GAMESTATE_MENU

    elif current_state == GAMESTATE_SINGLEPLAYER:

        screen.blit(IMAGE_MAIN, (0, 0))

        x_list = int((screen_width - word_list.width) / 2)
        y_list = int((screen_height - word_list.height) / 2) - 75
        word_list.draw(x_list, y_list)
        screen.blit(IMAGE_LIST, (x_list, y_list))

        x_input = int((screen_width - word_input.width) / 2)
        y_input = int((screen_height - word_input.height) / 2) + 250
        word_input.draw(x_input, y_input)
        screen.blit(IMAGE_INPUT, (x_input, y_input))

        x_forfeit = int((screen_width - small_button.width) / 2) + 250
        y_forfeit = int((screen_height - small_button.height) / 2) + 225
        small_button.draw(x_forfeit, y_forfeit)
        screen.blit(IMAGE_SMALLBUTTON_FORFEIT, (x_forfeit, y_forfeit))

        text_surface = word_font.render(input_text, True, (0, 0, 0))
        screen.blit(text_surface, (x_input + 25, y_input + 30))

        for i in range(min(len(list_of_words), 11)):
            if len(list_of_words) < 11:
                text_surface = word_font.render(list_of_words[i], True, (0, 0, 0))
                screen.blit(text_surface, (x_list + 25, y_list + 10 + i*40))
            else:
                text_surface = word_font.render(list_of_words[i + len(list_of_words) - 11 - scroll_index], True, (0, 0, 0))
                screen.blit(text_surface, (x_list + 25, y_list + 10 + i*40))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_input and x_mouse <= x_input + word_input.width and\
               y_mouse >= y_input and y_mouse <= y_input + word_input.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   inputing_text = True

            if x_mouse >= x_forfeit and x_mouse <= x_forfeit + small_button.width and\
               y_mouse >= y_forfeit and y_mouse <= y_forfeit + small_button.height:
                    print("click")

                    points_file_w = open("points.txt", "w")

                    word_input.color = GREEN_LIGHT
                    for i in range(len(Pointslist)):
                        if turn >= Pointslist[i]:
                            Pointslist.insert(i, turn)
                            break
                    Pointslist.pop()
                    Pointslist = Pointslist[:10]

                    for i in Pointslist:
                        points_file_w.write(str(i) + " ")
                    
                    points_file_w.close()
                   
                    current_state = GAMESTATE_SINGLEPLAYER_SCOREBOARD

    elif current_state == GAMESTATE_SINGLEPLAYER_SCOREBOARD:

        screen.blit(IMAGE_MAIN, (0, 0))

        x_list = int((screen_width - word_list.width) / 2)
        y_list = int((screen_height - word_list.height) / 2) - 75
        word_list.draw(x_list, y_list)
        screen.blit(IMAGE_LIST, (x_list, y_list))

        x_again = int((screen_width - small_button.width) / 2) - 100
        y_again = int((screen_height - small_button.height) / 2) + 250
        small_button.draw(x_again, y_again)
        screen.blit(IMAGE_SMALLBUTTON_REPLAY, (x_again, y_again))

        x_quit = int((screen_width - small_button.width) / 2) + 100
        y_quit = int((screen_height - small_button.height) / 2) + 250
        small_button.draw(x_quit, y_quit)
        screen.blit(IMAGE_SMALLBUTTON_QUIT, (x_quit, y_quit))

        for i in range(len(Pointslist)):
        
            points_surface = word_font.render(str(Pointslist[i]), True, (0, 0, 0))
            screen.blit(points_surface, (screen_width - x_list - 50, y_list + 10 + i*40))

        if leftclickdown:
            x_mouse = pygame.mouse.get_pos()[0]
            y_mouse = pygame.mouse.get_pos()[1]
            if x_mouse >= x_again and x_mouse <= x_again + small_button.width and\
               y_mouse >= y_again and y_mouse <= y_again + small_button.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   list_of_words = []
                   previous_word = ""
                   turn = 0
                   current_state = GAMESTATE_SINGLEPLAYER

            if x_mouse >= x_quit and x_mouse <= x_quit + small_button.width and\
               y_mouse >= y_quit and y_mouse <= y_quit + small_button.height:
                   print("click")
                   word_input.color = GREEN_LIGHT
                   list_of_words = []
                   list_of_names = []
                   previous_word = ""
                   turn = 0
                   current_state = GAMESTATE_MENU

    pygame.display.flip()

    leftclickdown = False

text_file.close()

pygame.quit()
