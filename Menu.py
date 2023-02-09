import pygame
from load_image import load_image
import Game
from typing import List


class Menu:
    def __init__(self, surface: pygame.Surface, width: int, height: int, characters: tuple,
                 price: List[List[str]], balance: str, level: int, killed: List[str], bonus: List[str]) -> None:
        self.width = width
        self.height = height
        self.sfx = True
        self.music = True
        self.heroes = [pygame.transform.scale(load_image('img/Static/main_character.png'),
                                              (130, int(height // 5.9))),
                       pygame.transform.scale(load_image('img/Static/Ranger.png'),
                                              (180, int(height // 5.3))),
                       pygame.transform.scale(load_image('img/Static/Jill the fighter.png'),
                                              (130, int(height // 5.7))),
                       pygame.transform.scale(load_image('img/Static/Blood_Knight.png'),
                                              (135, int(height // 5.6))),
                       pygame.transform.scale(load_image('img/Static/The Knight.png'),
                                              (130, int(height // 5.5))),
                       pygame.transform.scale(load_image('img/Static/Elf_King.png'),
                                              (196, int(height // 5.8)))]
        self.coin = pygame.image.load('data/img/Static/coin.png')
        self.font = pygame.font.Font('data/fonts/at01.ttf', int(height // 17.28))
        self.price = price
        self.balance = balance # деньги
        self.cur_killed = '0'  # Количество убийств на данном уровне
        self.level = level
        self.killed = killed
        self.boss_killed = 3 ** (self.level // 5)
        self.bonus = bonus
        self.enemies_hp_now = str(self.level * 10 * self.boss_killed + int(self.bonus[self.level // 5]))
        self.gold = self.gold = str(int(str(self.level * 3 * self.boss_killed)) * 5)\
            if self.level % 5 == 0 else str(self.level * 3 * self.boss_killed)
        self.gold_now = self.gold
        self.time = '20'
        self.click_ratio = 1
        self.border_width = self.width - 60
        self.border_height = (self.height - 40) // 6.14
        self.btn_width = self.border_width // 4.7
        self.btn_height = self.border_height // 1.55
        self.buttons = []
        self.dps = sum(int(elem[1]) * int(elem[2]) for elem in price[1:])
        self.dmg = int(price[0][1]) * int(price[0][2])
        self.coin_x = 1.4
        self.coin_y = 1.4
        self.characters = characters
        self.boss = True if self.level % 5 == 0 else False
        self.drop = False
        self.coin_sound = pygame.mixer.Sound('data/sounds/collect_coin.wav')
        self.coin_sound.set_volume(0.3)
        self.draw_border(surface)
        self.draw_characters(surface)

    def draw_border(self, surface: pygame.Surface) -> None:
        self.rect = pygame.draw.rect(surface, (253, 217, 181), (0, 0, self.width, self.height))
        self.rect2 = pygame.draw.rect(surface, (205, 149, 117), (20, 20, self.width - 40, self.height - 40))
        self.rect_bottom = pygame.draw.rect(surface, (205, 149, 117), (surface.get_width() // 2,
                                                                       surface.get_height() // 1.09,
                                                                       surface.get_width() // 2, 90))

    def draw_characters(self, surface: pygame.Surface) -> None:
        for elem in self.heroes:
            if self.heroes.index(elem) > 1:
                if self.price[self.heroes.index(elem)][1] == '0' and self.price[self.heroes.index(elem) - 1][1] == '0':
                    break
            character = elem
            character_x = 5
            character_y = 20 + self.heroes.index(elem) * self.border_height
            self.character_border = pygame.draw.rect(surface, (121, 85, 61),
                                                     (30, 30 + self.heroes.index(elem) * self.border_height +
                                                      self.heroes.index(elem), self.border_width, self.border_height))
            character_btn_clr = \
                '#37178C' if int(self.balance) < int(self.price[self.heroes.index(elem)][0]) else '#6f47D7'
            self.character_btn_front = pygame.draw.rect(surface, character_btn_clr,
                                                        (self.border_width - self.btn_width, self.border_height -
                                                         self.btn_height + self.heroes.index(elem) *
                                                         self.border_height + self.heroes.index(elem),
                                                         self.btn_width, self.btn_height))
            self.character_btn_back = pygame.draw.rect(surface, '#000000', (self.border_width - self.btn_width,
                                                                            self.border_height - self.btn_height +
                                                                            self.heroes.index(elem) *
                                                                            self.border_height +
                                                                            self.heroes.index(elem), self.btn_width,
                                                                            self.btn_height), 5)
            text_price = self.font.render(self.price[self.heroes.index(elem)][0], True, '#FFD700')
            text_price_x = (self.border_width - self.btn_width) + self.width * 2 // 70
            text_price_y = self.border_height - self.btn_height + (self.heroes.index(elem) * self.border_height +
                                                                   self.heroes.index(elem) + self.btn_height // 2 -
                                                                   self.height // 40)
            surface.blit(text_price, (text_price_x, text_price_y))
            text_name = self.font.render(self.characters[self.heroes.index(elem)], True, '#ffffff')
            surface.blit(text_name, (character_x + self.character_border.w // 3,
                         character_y + self.character_border.h // 5))
            text_amount = self.font.render(f'Lvl {self.price[self.heroes.index(elem)][1]}', True, '#ffffff')
            surface.blit(text_amount, (character_x + self.character_border.w // 3,
                         character_y + self.character_border.h // 5 + self.height // 30 * 2))
            if self.heroes.index(elem) != 0:
                text_dmg = self.font.render(f'Dmg {int(self.price[self.heroes.index(elem)][2])}', True, '#ffffff')
            else:
                text_dmg = self.font.render(f'Click dmg'
                                            f' {int(self.price[self.heroes.index(elem)][2]) * self.click_ratio}',
                                            True, '#ffffff')
            surface.blit(text_dmg, (character_x + self.character_border.w // 3,
                                    character_y + self.character_border.h // 5 + self.height // 30))
            if self.character_btn_back not in self.buttons:
                self.buttons.append(self.character_btn_back)
            surface.blit(character, (character_x, character_y))
            if self.drop:
                surface.blit(self.coin, (surface.get_width() // self.coin_x, surface.get_height() // self.coin_y))

    def draw_stats(self, surface: pygame.Surface) -> None:
        text_balance = self.font.render(f'Gold: {self.balance}', True, '#FFD700')
        surface.blit(text_balance, (self.rect.width + 30, 3))
        text_click_damage = self.font.render(f'Click Damage: {self.dmg}', True, '#ffffff')
        surface.blit(text_click_damage, (self.rect.width + 30, 3 + self.height // 34.56))
        dps = int(int(self.dps)) if int(int(self.dps)) == float(int(self.dps))\
            else int(self.dps)
        text_dps = self.font.render(f'DPS: {dps}', True, '#ffffff')
        surface.blit(text_dps, (self.rect.width + 30, 3 + self.height // 34.56 * 2))
        text_killed = self.font.render(f'Killed: {self.cur_killed}', True, '#ffffff')
        surface.blit(text_killed, (self.rect.width + 30, 3 + self.height // 34.56 * 3))

    def draw_levels(self, surface: pygame.Surface) -> None:
        ratio = 3 if self.level != 1 else 2
        ratio_margin = 4 if self.level != 1 else 3
        margin = self.height // 172.8
        square_wh = self.height // 14.4
        levels_border_width = square_wh * ratio + margin * ratio_margin
        self.levels_border = pygame.draw.rect(surface, (121, 85, 61), (self.rect_bottom.centerx - levels_border_width
                                              // 2, self.rect_bottom.centery - square_wh // 2, levels_border_width,
                                                                       square_wh + 4))
        color = '#6f47D7' if len(self.killed) > self.level else '#808080'
        if self.level != 1:
            text_cur_level = self.font.render(f'{self.level}', True, '#FFD700')
            text_prev_level = self.font.render(f'{self.level - 1}', True, '#FFD700')
            text_next_level = self.font.render(f'{self.level + 1}', True, '#FFD700')
            self.cur_level_square = pygame.draw.rect(surface, '#37178C', (self.levels_border.centerx - square_wh // 2,
                                                                          self.levels_border.y + 2,
                                                                          square_wh, square_wh))
            self.prev_level_square = pygame.draw.rect(surface, '#6f47D7', (self.levels_border.centerx - square_wh // 2 -
                                                                           square_wh - margin,
                                                                           self.levels_border.y + 2,
                                                                           square_wh, square_wh))
            self.next_level_square = pygame.draw.rect(surface, color, (self.levels_border.centerx + square_wh // 2 +
                                                                       margin, self.levels_border.y + 2,
                                                                       square_wh, square_wh))
            surface.blit(text_cur_level, (self.cur_level_square.x + square_wh // 2 - text_cur_level.get_width() // 2,
                                          self.cur_level_square.y + text_cur_level.get_height() // 7))
            surface.blit(text_prev_level, (self.prev_level_square.x + square_wh // 2 - text_prev_level.get_width() // 2,
                                           self.prev_level_square.y + text_prev_level.get_height() // 7))
            surface.blit(text_next_level, (self.next_level_square.x + square_wh // 2 - text_next_level.get_width() // 2,
                                           self.next_level_square.y + text_next_level.get_height() // 7))
        else:
            text_cur_level = self.font.render(f'{self.level}', True, '#FFD700')
            text_next_level = self.font.render(f'{self.level + 1}', True, '#FFD700')
            self.cur_level_square = pygame.draw.rect(surface, '#37178C', (self.levels_border.x + margin,
                                                                          self.levels_border.y + 2,
                                                                          square_wh, square_wh))
            self.next_level_square = pygame.draw.rect(surface, color, (self.levels_border.x + square_wh + 2 * margin,
                                                                       self.levels_border.y + 2,
                                                                       square_wh, square_wh))
            surface.blit(text_cur_level, (self.cur_level_square.x + square_wh // 2 - text_cur_level.get_width() // 2,
                                          self.cur_level_square.y + text_cur_level.get_height() // 8))
            surface.blit(text_next_level, (self.next_level_square.x + square_wh // 2 - text_next_level.get_width() // 2,
                                           self.next_level_square.y + text_next_level.get_height() // 8))
        if self.boss:
            self.show_timer(surface)
        if self.time == '0':
            self.time = '20'
            Game.new_sprite()

    def draw_save_btn(self, surface: pygame.Surface) -> None:
        self.save_btn_back = pygame.draw.rect(surface, '#000000', (self.width * 2 - self.btn_width - 15, 5,
                                                                   self.btn_width + 10, self.btn_height + 10))
        self.save_btn_front = pygame.draw.rect(surface, '#6f47D7',
                                                        (self.width * 2 - self.btn_width - 10, 10,
                                                         self.btn_width, self.btn_height))
        save_btn_text = self.font.render('Saving', True, '#ffffff')
        surface.blit(save_btn_text, (self.width * 2 - self.btn_width - 10 + self.btn_width // 2 -
                                     save_btn_text.get_width() // 2, self.btn_height // 2 -
                                     save_btn_text.get_height() // 2.5))

    def btn_pressed(self, pos: tuple) -> tuple:
        for elem in self.buttons:
            if pos[0] in range(elem.x, elem.x + int(self.btn_width)) and pos[1] in range(elem.y, elem.y +
                                                                                         int(self.btn_height)):
                return True, elem
        return False, ''

    def verify_balance(self, btn: pygame.Rect) -> None:
        left = eval(f"{self.balance} - {self.price[self.buttons.index(btn)][0]}")
        if left >= 0:
            self.balance = str(left)
            price = self.price[self.buttons.index(btn)]
            price[0] = str(int(price[0]) + int(int(price[0]) * 0.07))
            price[1] = str(int(price[1]) + 1)
            if self.buttons.index(btn) == 0:
                price[0] = str(int(price[0]) + int(int(price[0]) * 0.2))
                self.click_ratio = int(price[1]) // 15 + 1 if int(price[1]) // 15 >= 1 else 1
                self.dmg = int(price[1]) * int(price[2]) * self.click_ratio
            else:
                self.dps += int(price[2])

    def verify_level(self, level: str) -> None:
        if level == 'next':
            if len(self.killed) > self.level:
                self.level += 1
            else:
                return
        elif level == 'prev':
            self.level -= 1
        self.cur_killed = self.killed[self.level - 1]
        self.boss_killed = 3 ** (self.level // 5)
        self.enemies_hp_now = str(self.level * 10 * self.boss_killed + int(self.bonus[self.level // 5]))
        self.gold = str(self.level * 3 * self.boss_killed)
        self.gold = str(int(str(self.level * 3 * self.boss_killed)) * 5)\
            if self.level % 5 == 0 else str(self.level * 3 * self.boss_killed)
        self.boss = True if self.level % 5 == 0 else False
        self.time = '20'
        Game.new_sprite()

    def show_timer(self, surface: pygame.Surface) -> None:
        font = pygame.font.Font('data/fonts/at01.ttf', int(self.height // 8.64))
        text_timer = font.render(f'{self.time}/20', True, '#000000')
        surface.blit(text_timer, (surface.get_width() // 1.4 - text_timer.get_width() // 3,
                                  surface.get_height() // 2.3))

    def collect_coin(self) -> None:
        if self.sfx:
            self.coin_sound.play()
        self.drop = False
        self.balance = str(int(self.balance) + int(self.gold_now))

    def draw_sound_buttons(self, surface: pygame.Surface) -> None:
        img_sfx = 'img/static/btn_sfx.png' if self.sfx else 'img/static/btn_sfx_off.png'
        img_music = 'img/static/btn_music.png' if self.music else 'img/static/btn_music_off.png'
        self.sfx_button = pygame.transform.scale(load_image(img_sfx),
                                                 (self.width // 11.5, self.height // 13))
        self.music_button = pygame.transform.scale(load_image(img_music),
                                                             (self.width // 11.5, self.height // 13))
        surface.blit(self.sfx_button, (self.width * 2 - self.sfx_button.get_width(), self.height -
                                       self.sfx_button.get_height()))
        surface.blit(self.music_button, (self.width * 2 - self.sfx_button.get_width() * 2, self.height -
                                         self.sfx_button.get_height()))
