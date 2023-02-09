import random
import pygame
from load_image import load_image
import sys
from SaveMenu import SaveMenu
from AnimatedSprite import AnimatedSprite
from Menu import Menu


def new_sprite() -> None:
    global entity, sound_dmg, sound_dead
    if already:
        entity.off = True
        entity.kill()
    ent_id = random.randint(0, 3)
    if not menu.boss:
        health_all = random.randint(int(menu.enemies_hp_now),
                                    int(menu.enemies_hp_now) + int(menu.enemies_hp_now) // 5)
    else:
        health_all = random.randint(int(menu.enemies_hp_now) * 10,
                                    int(menu.enemies_hp_now) * 10 + int(menu.enemies_hp_now) // 3)
    gold = random.randint(int(menu.gold), int(int(menu.gold) * 1.5))
    if ent_id == 0:
        entity = AnimatedSprite(load_image('img/Sprites/Slime_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Slime_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Slime_dead Sprite Sheet.png'), 4, 1, 4, 1, 7, 1, WIDTH // 1.5,
                                HEIGHT // 1.73, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/slime_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/slime_dead.mp3')
    elif ent_id == 1:
        entity = AnimatedSprite(load_image('img/Sprites/Cobra_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Cobra_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Cobra_dead Sprite Sheet.png'), 8, 1, 4, 1, 6, 1, WIDTH // 1.45,
                                HEIGHT // 1.83, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/cobra_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/cobra_dead.mp3')
        sound_dead.set_volume(0.1)
    elif ent_id == 2:
        entity = AnimatedSprite(load_image('img/Sprites/Imp_afk Sprite Sheet.png'),
                                load_image('img/Sprites/Imp_dmg Sprite Sheet.png'),
                                load_image('img/Sprites/Imp_dead Sprite Sheet.png'), 7, 1, 4, 1, 6, 1, WIDTH // 1.45,
                                HEIGHT // 1.7, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/imp_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/imp_dead.mp3')
        sound_dead.set_volume(0.1)
    elif ent_id == 3:
        entity = AnimatedSprite(load_image('img/Sprites/Kobold_afk Priest Sprite Sheet.png'),
                                load_image('img/Sprites/Kobold_dmg Priest Sprite Sheet.png'),
                                load_image('img/Sprites/Kobold_dead Priest Sprite Sheet.png'), 4, 1, 4, 1, 7, 1,
                                WIDTH // 1.45, HEIGHT // 1.75, all_sprites, health_all, gold)
        sound_dmg = pygame.mixer.Sound('data/sounds/imp_dmg.mp3')
        sound_dead = pygame.mixer.Sound('data/sounds/imp_dead.mp3')
        sound_dead.set_volume(0.1)
    sound_dmg.set_volume(0.1)
    all_sprites.add(entity)


def run() -> None:
    global already
    running = True
    already = False
    new_sprite()
    already = True
    savemenu = SaveMenu(WIDTH, HEIGHT, True)
    save_menu = False
    messagebox = False
    music = False
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                enemy_x = entity.get_position()[0]
                enemy_y = entity.get_position()[1]
                if event.button == 1:
                    if event.pos[0] in \
                        range(enemy_x, enemy_x + entity.get_size()[0]) and event.pos[1] in \
                            range(enemy_y, enemy_y + entity.get_size()[1]) and not (save_menu or messagebox):
                        entity.damage(menu, sound_dmg)
                    elif menu.btn_pressed(event.pos)[0] and not (save_menu or messagebox):
                        btn = menu.btn_pressed(event.pos)[1]
                        menu.verify_balance(btn)
                    elif menu.next_level_square.collidepoint(event.pos) and not (save_menu or messagebox):
                        menu.verify_level('next')
                    elif menu.level > 1:
                        if menu.prev_level_square.collidepoint(event.pos) and not (save_menu or messagebox):
                            menu.verify_level('prev')
                    if menu.sfx_button.get_rect(topleft=(menu.width * 2 - menu.sfx_button.get_width(),
                                                         menu.height -
                                                         menu.sfx_button.get_height())).collidepoint(event.pos):
                        menu.sfx = False if menu.sfx else True
                    if menu.music_button.get_rect(topleft=(menu.width * 2 - menu.sfx_button.get_width() * 2,
                                                           menu.height -
                                                           menu.sfx_button.get_height())).collidepoint(event.pos):
                        menu.music = False if menu.music else True

                    if menu.save_btn_front.collidepoint(event.pos) and not messagebox:
                        save_menu = True
                    if save_menu:
                        savemenu.show_menu(screen)
                        if savemenu.close_btn.collidepoint(event.pos):
                            save_menu = False
                        else:
                            for btn in savemenu.buttons:
                                if btn.collidepoint(event.pos):
                                    save_menu = False
                                    messagebox = True if savemenu.res[savemenu.buttons.index(btn)][0] else False
                                    if messagebox:
                                        savemenu.show_messagebox(screen, btn)
                                    else:
                                        savemenu.save_game(menu, 'data/db/saves.db', btn)
                    if messagebox:
                        btn = savemenu.cur_btn
                        if savemenu.btn_no_back.collidepoint(event.pos):
                            messagebox = False
                        elif savemenu.btn_yes_back.collidepoint(event.pos):
                            messagebox = False
                            savemenu.save_game(menu, 'data/db/saves.db', btn)
            if event.type == pygame.MOUSEMOTION:
                if entity.rect.collidepoint(event.pos) and not (save_menu or messagebox):
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                else:
                    pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
                if menu.coin.get_rect(topleft=(screen.get_width() //
                                               menu.coin_x, screen.get_height() //
                                               menu.coin_y)).collidepoint(event.pos) and menu.drop:
                    menu.collect_coin()
                if save_menu:
                    if savemenu.close_btn.collidepoint(event.pos):
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_HAND)
                    else:
                        pygame.mouse.set_cursor(pygame.SYSTEM_CURSOR_ARROW)
            if event.type == pygame.USEREVENT:
                entity.dps_damage(menu, sound_dead)
                if menu.boss:
                    menu.time = str(int(menu.time) - 1)
        screen.blit(image_bg, (0, 0))
        screen.blit(image_platform, (screen.get_width() // 1.9, screen.get_height() // 1.9))
        menu.draw_border(screen)
        menu.draw_characters(screen)
        menu.draw_stats(screen)
        menu.draw_levels(screen)
        menu.draw_save_btn(screen)
        menu.draw_sound_buttons(screen)
        all_sprites.draw(screen)
        character_sprites.draw(screen)
        if not entity.off:
            entity.update()
        entity.get_health(screen)
        if save_menu:
            savemenu.show_menu(screen)
        btn = savemenu.cur_btn
        if messagebox:
            savemenu.show_messagebox(screen, btn)
        if menu.music and not music:
            music = True
            music_id = random.randint(0, 2)
            if music_id == 0:
                ingame_music = pygame.mixer.Sound('data/music/ingame1.wav')
            elif music_id == 1:
                ingame_music = pygame.mixer.Sound('data/music/ingame2.wav')
            elif music_id == 2:
                ingame_music = pygame.mixer.Sound('data/music/ingame3.wav')
            ingame_music.set_volume(0.1)
            ingame_music.play(-1)
        elif not menu.music:
            music = False
            ingame_music.stop()
        clock.tick(fps)
        pygame.display.flip()


def play(price=[['10', '1', '1'], ['50', '0', '5'], ['200', '0', '20'], ['1000', '0', '100'], ['10000', '0', '800'],
                ['50000', '0', '10000']],
         balance='0', level=1, killed=['0'], bonus=['0']):
    global WIDTH, HEIGHT, screen, clock, fps, menu, all_sprites, character_sprites, image_bg, image_platform
    pygame.init()
    info = pygame.display.Info()
    WIDTH, HEIGHT = info.current_w, info.current_h
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    all_sprites = pygame.sprite.Group()
    character_sprites = pygame.sprite.Group()
    pygame.display.set_caption('Fairy Tale clicker')
    image_bg = pygame.transform.scale(load_image('img/Static/background.png'), (WIDTH, HEIGHT))
    image_platform = pygame.transform.scale(load_image('img/Static/platform_grass.png'), (WIDTH // 2.5, HEIGHT // 2))
    clock = pygame.time.Clock()
    fps = 13
    characters = ('Click Master', 'Forest Ranger', 'Jill the Fighter', 'Blood Knight', 'Imperial knight', 'Elf king')
    menu = Menu(screen, WIDTH // 2, HEIGHT, characters, price, balance, level, killed, bonus)
    all_sprites.draw(screen)
    character_sprites.draw(screen)
    pygame.time.set_timer(pygame.USEREVENT, 1000)
    run()
    pygame.quit()
    sys.exit()
