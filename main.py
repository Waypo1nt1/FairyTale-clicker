import pygame
import Game
import SaveMenu
import sqlite3
import ast
import random
from load_image import load_image
import webbrowser


if __name__ == '__main__':
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption('Fairy Tale clicker')
    running = True
    btn_width = 270
    btn_height = 100
    screen.fill((205, 149, 117))
    btn_game = pygame.draw.rect(screen, (121, 85, 61), (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 - btn_height * 2,
                                                        btn_width, btn_height))
    btn_options = pygame.draw.rect(screen, (121, 85, 61), (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 - btn_height + 5,
                                                           btn_width, btn_height))
    btn_quit = pygame.draw.rect(screen, (121, 85, 61),
                                (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 + 10, btn_width, btn_height))
    github = pygame.transform.scale(load_image('img/static/github.png'), (50, 50))
    logo = load_image('img/static/logo.png')
    font = pygame.font.Font('data/fonts/at01.ttf', 50)
    text_price = font.render('Start', True, '#FFD700')
    texts = ['New game', 'Load', 'Quit']
    btns = [btn_game, btn_options, btn_quit]
    pygame.display.flip()
    sound_hover = pygame.mixer.Sound('data/sounds/menu_hover.mp3')
    sound_hover.set_volume(0.1)
    music_id = random.randint(0, 2)
    if music_id == 0:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu1.wav')
    elif music_id == 1:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu2.wav')
    elif music_id == 2:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu3.wav')
    main_menu_music.set_volume(0.1)
    main_menu_music.play(-1)
    game = False
    played = False
    btn_played = ''
    save_menu = False
    data = False
    while running:
        pos = pygame.mouse.get_pos()
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    if btn_game.collidepoint(pos):
                        game = True
                    elif btn_options.collidepoint(pos):
                        savemenu = SaveMenu.SaveMenu(WIDTH, HEIGHT, False)
                        savemenu.show_menu(screen)
                        save_menu = True
                    elif btn_quit.collidepoint(pos):
                        running = False
                    if save_menu:
                        if savemenu.close_btn.collidepoint(pos):
                            save_menu = False
                        for btn in savemenu.buttons:
                            if btn.collidepoint(pos):
                                if savemenu.res[savemenu.buttons.index(btn)][0]:
                                    con = sqlite3.connect('data/db/saves.db')
                                    res = con.execute('''SELECT * from saves WHERE id = ?''',
                                                      (int(savemenu.buttons.index(btn) + 1),)).fetchall()
                                    res = res[0]
                                    price, balance, level, killed, bonus =\
                                        ast.literal_eval(res[0]), res[1], int(res[2]),\
                                        ast.literal_eval(res[3]), ast.literal_eval(res[4])
                                    data = True
                                    break
                    if github.get_rect(topleft=(WIDTH - github.get_width() - 3,
                                                HEIGHT - github.get_height() - 3)).collidepoint(pos) and not save_menu:
                        webbrowser.open('https://github.com/Waypo1nt1')

            if event.type == pygame.MOUSEMOTION:
                if save_menu:
                    if savemenu.close_btn.collidepoint(pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                elif github.get_rect(topleft=(WIDTH - github.get_width() - 3,
                                              HEIGHT - github.get_height() - 3)).collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if data:
                break
        if data:
            break
        screen.fill('#7C2335') # (205, 149, 117)
        if save_menu:
            savemenu.show_menu(screen)
        if not save_menu:
            #pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            for ind, btn in enumerate(btns):
                if btn.collidepoint(pos):
                    if not played:
                        played = True
                        btn_played = btn
                        sound_hover.play()
                    btn = pygame.draw.rect(screen, (253, 217, 181), (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 -
                                                                     btn_height * (2 - ind) + 5 * ind,
                                                                     btn_width, btn_height))
                    color = '#7908AA'
                else:
                    if btn == btn_played:
                        played = False
                    btn = pygame.draw.rect(screen, '#854826', (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 -
                                                               btn_height * (2 - ind) + 5 * ind,
                                                               btn_width, btn_height)) # 121, 85, 61
                    color = '#FFD700'
                screen.blit(font.render(texts[ind], True, color),
                            (WIDTH // 2 - btn_width // 4, HEIGHT // 1.5 - btn_height
                             * (2 - ind) + 5 * ind + btn_height // 2 - 25))
                screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 10))
        screen.blit(github, (WIDTH - github.get_width() - 3, HEIGHT - github.get_height() - 3))
        pygame.display.flip()
        if game:
            break
    pygame.quit()
    if running:
        if data:
            Game.play(price, balance, level, killed, bonus)
        else:
            Game.play()
