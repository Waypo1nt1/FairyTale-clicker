# Импорт библиотек и файлов
import random
import pygame
from load_image import load_image
import sys
from SaveMenu import SaveMenu
from AnimatedSprite import AnimatedSprite
from Menu import Menu


def new_sprite() -> None:
    global entity, sound_dmg, sound_dead
    if already:  # Если уже была инициализирована сущность
        entity.off = True
        entity.kill()  # "Убийство" сущности
    ent_id = random.randint(0, 3)  # Случайный id для случайного спрайта
    if not menu.boss:  # Если сущность не является боссом
        # Расчет здоровья сущности
        health_all = random.randint(int(menu.enemies_hp_now),
                                    int(menu.enemies_hp_now) + int(menu.enemies_hp_now) // 5)
    else:
        # Расчет здоровья босса
        health_all = random.randint(int(menu.enemies_hp_now) * 10,
                                    int(menu.enemies_hp_now) * 10 + int(menu.enemies_hp_now) // 3)
    gold = random.randint(int(menu.gold), int(int(menu.gold) * 1.5))  # Расчет выпадаемого золота
    if ent_id == 0:
        # Инициализация сущности (класс AnimatedSprite)
        entity = AnimatedSprite(load_image('img/Sprites/Slime_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Slime_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Slime_dead Sprite Sheet.png'), 4, 1, 4, 1, 7, 1, WIDTH // 1.5,
                                HEIGHT // 1.73, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/slime_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/slime_dead.mp3')
    elif ent_id == 1:
        # Инициализация сущности (класс AnimatedSprite)
        entity = AnimatedSprite(load_image('img/Sprites/Cobra_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Cobra_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Cobra_dead Sprite Sheet.png'), 8, 1, 4, 1, 6, 1, WIDTH // 1.45,
                                HEIGHT // 1.83, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/cobra_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/cobra_dead.mp3')
        sound_dead.set_volume(0.1)
    elif ent_id == 2:
        # Инициализация сущности (класс AnimatedSprite)
        entity = AnimatedSprite(load_image('img/Sprites/Imp_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Imp_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Imp_dead Sprite Sheet.png'), 7, 1, 4, 1, 6, 1, WIDTH // 1.45,
                                HEIGHT // 1.7, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/imp_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/imp_dead.mp3')
        sound_dead.set_volume(0.1)
    elif ent_id == 3:
        # Инициализация сущности (класс AnimatedSprite)
        entity = AnimatedSprite(load_image('img/Sprites/Kobold_afk Priest Sprite Sheet.png'),
                                load_image('img/Sprites/Kobold_dmg Priest Sprite Sheet.png'),
                                load_image('img/Sprites/Kobold_dead Priest Sprite Sheet.png'), 4, 1, 4, 1, 7, 1,
                                WIDTH // 1.45, HEIGHT // 1.75, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/imp_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/imp_dead.mp3')
        sound_dead.set_volume(0.1)
    sound_dmg.set_volume(0.1)
    all_sprites.add(entity)  # Добавление спрайта в группу спрайтов


def run() -> None:
    global already
    running = True
    already = False  # Сущность еще не была инициализирована
    new_sprite()  # Новая сущность
    already = True  # Сущность была инициализирована
    savemenu = SaveMenu(WIDTH, HEIGHT, True)  # Инициализация меню сохранений
    save_menu = False  # Меню сохранений не было открыто
    messagebox = False  # Окно сообщения не было открыто
    music = False  # Музыка не играет
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:  # Событие выхода
                running = False
            if event.type == pygame.KEYDOWN:  # Событие нажатия на кнопку
                if event.key == pygame.K_ESCAPE:  # Escape
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:  # Событие нажатия на мышь
                enemy_x = entity.get_position()[0]  # Получение координат сущности
                enemy_y = entity.get_position()[1]
                if event.button == 1:  # Левая кнопка мыши
                    # Пересечение позиции мыши с сущностью
                    if event.pos[0] in \
                        range(enemy_x, enemy_x + entity.get_size()[0]) and event.pos[1] in \
                            range(enemy_y, enemy_y + entity.get_size()[1]) and not (save_menu or messagebox):
                        entity.damage(menu, sound_dmg)  # Вызов получения урона сущности с переданным звуком
                    # Если позиция мыши пересекается с кнопкой меню, и не открыто меню сохранений или окно сообщения
                    elif menu.btn_pressed(event.pos)[0] and not (save_menu or messagebox):
                        btn = menu.btn_pressed(event.pos)[1]
                        menu.verify_balance(btn)
                    # Пересечение позиции мыши с next_level_square
                    elif menu.next_level_square.collidepoint(event.pos) and not (save_menu or messagebox):
                        menu.verify_level('next')  # Проверка для перехода на следующий уровень
                    elif menu.level > 1:  # Если уровень больше 1 (тогда появляется предыдущий уровень)
                        # Пересечение позиции мыши с prev_level_square
                        if menu.prev_level_square.collidepoint(event.pos) and not (save_menu or messagebox):
                            menu.verify_level('prev')  # Проверка для перехода на прошлый уровень
                    # Пересечение позиции мыши с sfx_button
                    if menu.sfx_button.get_rect(topleft=(menu.width * 2 - menu.sfx_button.get_width(),
                                                         menu.height -
                                                         menu.sfx_button.get_height())).collidepoint(event.pos):
                        menu.sfx = False if menu.sfx else True  # Переключение состояния sfx
                    # Пересечение позиции мыши с music_button
                    if menu.music_button.get_rect(topleft=(menu.width * 2 - menu.sfx_button.get_width() * 2,
                                                           menu.height -
                                                           menu.sfx_button.get_height())).collidepoint(event.pos):
                        menu.music = False if menu.music else True  # Переключение состояния music
                    # Пересечение позиции мыши с save_btn_front (При этом не открыто окно сообщения)
                    if menu.save_btn_front.collidepoint(event.pos) and not messagebox:
                        save_menu = True  # Меню сохранений открыто
                    if save_menu:  # Если открыто меню сохранений
                        savemenu.show_menu(screen)  # Отрисовка меню сохранений
                        if savemenu.close_btn.collidepoint(event.pos):  # Пересечение позиции мыши с close_btn
                            save_menu = False  # Меню сохранений закрыто
                        else:
                            for btn in savemenu.buttons:
                                if btn.collidepoint(event.pos):
                                    save_menu = False  # Меню сохранений закрыто
                                    # Окно сообщений появится если данные в бд уже есть (перезапись сохранения)
                                    messagebox = True if savemenu.res[savemenu.buttons.index(btn)][0] else False
                                    if messagebox:
                                        savemenu.show_messagebox(screen, btn)  # Отрисовка окна сообщения
                                    else:
                                        savemenu.save_game(menu, 'data/db/saves.db', btn)  # Сохранение данных в бд
                    if messagebox:  # Логика кнопок "yes" и "no" при открытом окне сообщения
                        btn = savemenu.cur_btn
                        if savemenu.btn_no_back.collidepoint(event.pos):
                            messagebox = False
                        elif savemenu.btn_yes_back.collidepoint(event.pos):
                            messagebox = False
                            savemenu.save_game(menu, 'data/db/saves.db', btn)  # Сохранение данных в бд
            if event.type == pygame.MOUSEMOTION:  # Событие движения мыши
                # Пересечение позиции мыши с сущностью (если не открыто меню сохранений или окно сообщения)
                if entity.rect.collidepoint(event.pos) and not (save_menu or messagebox):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)  # Смена курсора на руку
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)  # Смена курсора на стрелку
                # Пересечение позиции мыши с coin
                if menu.coin.get_rect(topleft=(screen.get_width() //
                                               menu.coin_x, screen.get_height() //
                                               menu.coin_y)).collidepoint(event.pos) and menu.drop:
                    menu.collect_coin()  # Вызов метода сбора монетки
                if save_menu:
                    if savemenu.close_btn.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.USEREVENT:  # Пользовательское событие, созданное таймером (каждые 1000мс)
                entity.dps_damage(menu, sound_dead)  # Урон в секунду
                if menu.boss:  # Если сущность - босс
                    menu.time = str(int(menu.time) - 1)  # Уменьшение времени на таймере убийства босса
        screen.blit(image_bg, (0, 0))  # Отрисовка фона
        screen.blit(image_platform, (screen.get_width() // 1.9, screen.get_height() // 1.9))  # Отрисовка платформы
        menu.draw_border(screen)  # Отрисовка границ меню
        menu.draw_characters(screen)  # Отрисовка персонажей
        menu.draw_stats(screen)  # Отрисовка статистики
        menu.draw_levels(screen)  # Отрисовка уровней для переключения
        menu.draw_save_btn(screen)  # Отрисовка кнопки сохранения
        menu.draw_sound_buttons(screen)  # Отрисовка кнопок звука
        all_sprites.draw(screen)  # Отрисовка спрайтов на экране (сущности)
        if not entity.off:  # Если сущность не выключена (не мертва)
            entity.update()  # Обновление сущности
        entity.get_health(screen)  # Отрисовка здоровья сущности на экране
        if save_menu:  # Если меню сохранений открыто
            savemenu.show_menu(screen)  # Отрисовка меню сохранений
        btn = savemenu.cur_btn  # Нажатая кнопка сохранений (для получения индекса кнопки для id в бд)
        if messagebox:  # Если окно сообщения открыто
            savemenu.show_messagebox(screen, btn)  # Отрисовка окна сообщений
        if menu.music and not music:  # Если музыка включена и ещё не начала проигрываться
            music = True  # Музыка начала проигрываться
            music_id = random.randint(0, 2)  # id для случайной музыки
            if music_id == 0:
                ingame_music = pygame.mixer.Sound('data/music/ingame1.wav')
            elif music_id == 1:
                ingame_music = pygame.mixer.Sound('data/music/ingame2.wav')
            elif music_id == 2:
                ingame_music = pygame.mixer.Sound('data/music/ingame3.wav')
            ingame_music.set_volume(0.1)  # Установка громкости
            ingame_music.play(-1) # play с бесконечным повтором
        elif not menu.music:  # Если музыка начала проигрываться и должна закончиться
            music = False
            ingame_music.stop()  # Остановка музыки
        clock.tick(fps)
        pygame.display.flip() # Обновление экрана


def play(price=[['10', '1', '1'], ['50', '0', '5'], ['200', '0', '20'], ['1000', '0', '100'], ['10000', '0', '800'],
                ['50000', '0', '10000']],
         balance='0', level=1, killed=['0'], bonus=['0']):
    # Базовые значения - начало игры (вместо них могут вставляться данные из бд)
    global WIDTH, HEIGHT, screen, clock, fps, menu, all_sprites, image_bg, image_platform
    pygame.init()  # Инициализация pygame
    info = pygame.display.Info()  # Получение длины и высоты экрана
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))  # Установка размеров окна
    all_sprites = pygame.sprite.Group()  # Создание группы спрайтов
    pygame.display.set_caption('Fairy Tale clicker')  # Установка названия окна
    image_bg = pygame.transform.scale(load_image('img/Static/background.png'), (WIDTH, HEIGHT))  # Фон
    image_platform = pygame.transform.scale(load_image('img/Static/platform_grass.png'), (WIDTH // 2.5, HEIGHT // 2))
    clock = pygame.time.Clock()
    fps = 13  # фпс
    # Персонажи (текст в border'ах персонажей)
    characters = ('Click Master', 'Forest Ranger', 'Jill the Fighter', 'Blood Knight', 'Imperial knight', 'Elf king')
    # Инициализация меню
    menu = Menu(screen, WIDTH // 2, HEIGHT, characters, price, balance, level, killed, bonus)
    all_sprites.draw(screen) # Отрисовка спрайтов на экране (сущности)
    pygame.time.set_timer(pygame.USEREVENT, 1000)  # Таймер для dps'а и времени у босса
    run()  # Работа игры
    pygame.quit()  # Выход из pygame'а
    sys.exit()  # Конец работы программы
