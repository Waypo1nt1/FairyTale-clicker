# Импорт библиотек и файлов
import pygame
import Game
import SaveMenu
import sqlite3
import ast
import random
import webbrowser
from load_image import load_image


if __name__ == '__main__':
    pygame.init()  # Инициализация pygame
    WIDTH, HEIGHT = 1280, 720
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Установка размеров окна
    pygame.display.set_caption('Fairy Tale clicker')  # Установка названия окна
    running = True
    btn_width = 270
    btn_height = 100
    # Отрисовка кнопок
    btn_game = pygame.draw.rect(screen, (121, 85, 61), (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 - btn_height * 2,
                                                        btn_width, btn_height))
    btn_options = pygame.draw.rect(screen, (121, 85, 61), (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 - btn_height + 5,
                                                           btn_width, btn_height))
    btn_quit = pygame.draw.rect(screen, (121, 85, 61),
                                (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 + 10, btn_width, btn_height))
    github = pygame.transform.scale(load_image('img/static/github.png'), (50, 50))  # Инициализация лого github'а
    logo = load_image('img/static/logo.png')  # Лого игры
    font = pygame.font.Font('data/fonts/at01.ttf', 50)  # Шрифт
    texts = ['New game', 'Load', 'Quit']  # Список с текстами на кнопках (для дальнейшего использования в цикле)
    btns = [btn_game, btn_options, btn_quit]  # Список с кнопками (для дальнейшего использования в цикле)
    sound_hover = pygame.mixer.Sound('data/sounds/menu_hover.mp3')  # Звук при наведении на одну из кнопок
    sound_hover.set_volume(0.1)  # Установка громкости
    music_id = random.randint(0, 2)  # id для случайной музыки при каждом запуске
    if music_id == 0:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu1.wav')
    elif music_id == 1:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu2.wav')
    elif music_id == 2:
        main_menu_music = pygame.mixer.Sound('data/music/main_menu3.wav')
    main_menu_music.set_volume(0.1)  # Установка громкости
    main_menu_music.play(-1)  # play с бесконечным повтором
    game = False  # Переменная, отвечающая за начало игры
    played = False  # Переменная для hover'а (отслеживание, был ли сыгран звук hover'а или нет)
    btn_played = ''  # Кнопка, для которой played = True
    save_menu = False  # Открыто ли меню загрузки
    data = False  # Были ли загружены данные
    while running:
        pos = pygame.mouse.get_pos()  # Получение позиции курсора
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Событие выхода
                running = False
            if event.type == pygame.KEYDOWN:  # Событие нажатия на кнопку
                if event.key == pygame.K_ESCAPE:  # Escape
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Событие нажатия на мышь
                if event.button == 1:  # Левая кнопка мыши
                    if btn_game.collidepoint(pos):  # Пересечение позиции мыши с btn_game
                        game = True
                    elif btn_options.collidepoint(pos):  # Пересечение позиции мыши с btn_options
                        savemenu = SaveMenu.SaveMenu(WIDTH, HEIGHT, False)  # Инициализация меню загрузки
                        savemenu.show_menu(screen)  # Отрисовка меню загрузки
                        save_menu = True  # Меню загрузки открыто
                    elif btn_quit.collidepoint(pos):  # Пересечение позиции мыши с btn_quit
                        running = False  # Выход из цикла (для остановки работы программы)
                    if save_menu:  # Если открыто меню загрузки
                        if savemenu.close_btn.collidepoint(pos):  # Пересечение позиции мыши с close_btn
                            save_menu = False  # Меню загрузки закрыто
                        for btn in savemenu.buttons:  # Прохождение по кнопкам меню загрузки
                            if btn.collidepoint(pos):
                                if savemenu.res[savemenu.buttons.index(btn)][0]:  # Если есть данные в бд
                                    con = sqlite3.connect('data/db/saves.db')  # Подключение к бд
                                    # Получение всех данных по соотвутствующему id (индекс кнопки + 1)
                                    res = con.execute('''SELECT * from saves WHERE id = ?''',
                                                      (int(savemenu.buttons.index(btn) + 1),)).fetchall()
                                    res = res[0]
                                    # Присвоение переменным полученных значений из бд
                                    # ast.literal_eval преобразовывает строку в список
                                    price, balance, level, killed, bonus =\
                                        ast.literal_eval(res[0]), res[1], int(res[2]),\
                                        ast.literal_eval(res[3]), ast.literal_eval(res[4])
                                    data = True  # Были получены данные
                                    break
                    if github.get_rect(topleft=(WIDTH - github.get_width() - 3,
                                                HEIGHT - github.get_height() - 3)).collidepoint(pos) and not save_menu:
                        webbrowser.open('https://github.com/Waypo1nt1')  # Открытие ссылки
            if event.type == pygame.MOUSEMOTION:  # Событие движения мыши
                if save_menu:  # Если открыто меню загрузки
                    if savemenu.close_btn.collidepoint(pos):  # Пересечение позиции мыши с close_btn
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Смена курсора на руку
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Смена курсора на стрелку
                elif github.get_rect(topleft=(WIDTH - github.get_width() - 3,
                                              HEIGHT - github.get_height() - 3)).collidepoint(pos):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)

            if data:
                break
        if data:
            break
        screen.fill('#7C2335')  # Заливка экрана
        if save_menu:  # Если открыто меню загрузки
            savemenu.show_menu(screen)  # Отрисовка меню загрузки
        if not save_menu:
            for ind, btn in enumerate(btns):
                # При наведении на кнопку цвет кнопки и текста меняется
                if btn.collidepoint(pos):
                    if not played:
                        played = True
                        btn_played = btn
                        sound_hover.play()
                    btn_color = (253, 217, 181)
                    color = '#7908AA'
                else:
                    if btn == btn_played:
                        played = False
                    btn_color = '#854826'
                    color = '#FFD700'
                pygame.draw.rect(screen, btn_color, (WIDTH // 2 - btn_width // 2, HEIGHT // 1.5 -
                                                     btn_height * (2 - ind) + 5 * ind,
                                                     btn_width, btn_height))
                screen.blit(font.render(texts[ind], True, color),
                            (WIDTH // 2 - btn_width // 4, HEIGHT // 1.5 - btn_height
                             * (2 - ind) + 5 * ind + btn_height // 2 - 25))  # Отрисовка текста
                screen.blit(logo, (WIDTH // 2 - logo.get_width() // 2, 10))  # Отрисовка лого игры
        # Отрисовка лого github'а
        screen.blit(github, (WIDTH - github.get_width() - 3, HEIGHT - github.get_height() - 3))
        pygame.display.flip()  # Обновление экрана
        if game:
            break
    pygame.quit()  # Выход
    if running:
        if data:
            Game.play(price, balance, level, killed, bonus)
        else:
            Game.play()
