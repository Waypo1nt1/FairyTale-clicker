import pygame
import sqlite3
import ast
import Menu


class SaveMenu:
    def __init__(self, width: int, height: int, save: bool) -> None:
        self.width = width // 1.5  # Ширина
        self.height = height // 1.5  # Высота
        self.buttons = list()
        self.text = 'Save' if save else 'Load'  # Текст на кнопке - Если находимся в главном меню, то Load,
                                                # а если в игре, то Save
        self.font1 = pygame.font.Font('data/fonts/at01.ttf', int(self.height // 11.52))  # Подгружаем шрифты
        self.font2 = pygame.font.Font('data/fonts/at01.ttf', int(self.height // 14.4))
        self.font3 = pygame.font.Font('data/fonts/at01.ttf', int(self.height // 8.22))
        self.res = list()
        self.cur_btn = 0

    def show_menu(self, surface: pygame.Surface) -> None:
        menu_x = self.width * 1.5 // 2 - self.width // 2
        menu_y = self.height * 1.5 // 2 - self.height // 2
        border_width = self.width - 60
        border_height = self.height // 4.5
        btn_width = self.width * 1.5 // 10.24
        btn_height = self.height * 1.5 // 17.28
        self.menu = pygame.draw.rect(surface, (253, 217, 181), (menu_x, menu_y, self.width, self.height))
        self.inmenu = pygame.draw.rect(surface, (205, 149, 117), (menu_x + 20, menu_y + 20,
                                                                  self.width - 40, self.height - 40))
        con = sqlite3.connect('data/db/saves.db')
        self.res = list(con.execute('''SELECT * from saves'''))
        con.close()
        for elem in self.res:
            self.save_border = pygame.draw.rect(surface, (121, 85, 61),
                                                (menu_x + 30, menu_y + self.height // 19.2 + (elem[5] - 1) *
                                                 border_height + elem[5] - 1, border_width, border_height))
            text_save = self.font3.render(f'Save {elem[5]}', True, '#ffffff')
            surface.blit(text_save, (menu_x + 35, menu_y + 35 + (elem[5] - 1) * border_height + elem[5] - 1 -
                                     text_save.get_height() // 4))
            save_btn_clr = '#6f47D7'
            self.save_btn_front = pygame.draw.rect(surface, save_btn_clr,
                                                   (menu_x + border_width - btn_width, menu_y + self.height // 19.2 +
                                                    (elem[5] - 1) * border_height + elem[5] - 1 +
                                                    border_height // 2 - btn_height // 2,
                                                    btn_width, btn_height))
            self.save_btn_back = pygame.draw.rect(surface, '#000000', (menu_x + border_width - btn_width, menu_y +
                                                                       self.height // 19.2 +
                                                                       (elem[5] - 1) * border_height + elem[5] - 1 +
                                                                       border_height // 2 - btn_height // 2,
                                                                       btn_width, btn_height), 5)
            text_save_btn = self.font2.render(f'{self.text}', True, '#ffffff')
            surface.blit(text_save_btn, (self.save_btn_front.x + btn_width // 2 - text_save_btn.get_width() // 2,
                                         self.save_btn_front.y + btn_height // 4 - text_save_btn.get_height() // 5))
            if self.save_btn_back not in self.buttons:
                self.buttons.append(self.save_btn_back)
            if elem[0]:
                pass
                text_info_game = self.font1.render(f'Level: {elem[2]} Gold: {elem[1]}', True, '#ffffff')
                text_info_stats = self.font1.render(
                    f'Dps: {sum(int(elem2[1]) * int(elem2[2]) for elem2 in ast.literal_eval(elem[0])[1:])} '
                    f'Click Damage: {ast.literal_eval(elem[0])[0][1]}',
                    True, '#ffffff')
                surface.blit(text_info_game, (menu_x + 35, menu_y + 35 + (elem[5] - 1) * border_height + elem[5] - 1 -
                                              text_save.get_height() // 3 + text_save.get_height()))
                surface.blit(text_info_stats, (menu_x + 35, menu_y + 35 + (elem[5] - 1) * border_height + elem[5] - 1 -
                                               text_save.get_height() // 1.5 + text_save.get_height() * 2))
            else:
                text_info = self.font1.render('No data found', True, '#ffffff')
                surface.blit(text_info, (menu_x + 35, menu_y + 35 + (elem[5] - 1) * border_height + elem[5] - 1 -
                                         text_save.get_height() // 4 + text_save.get_height()))
        self.close_btn = pygame.draw.rect(surface, '#6f47D7', (menu_x + self.width - self.height // 19.2 - 1,
                                                               menu_y + 1, self.height // 19.2, self.height // 19.2))
        self.close_btn_back = pygame.draw.rect(surface, '#000000', (menu_x + self.width - self.height // 19.2 - 2,
                                                                    menu_y, self.height // 19.2 + 2,
                                                                    self.height // 19.2 + 2), 1)
        self.close_btn_left_line = pygame.draw.line(surface, '#ffffff', (menu_x + self.width - self.height // 19.2 + 1,
                                                                         menu_y + 3),
                                                    (menu_x + self.width - 5, menu_y + self.height // 19.2 - 3), 3)
        self.close_btn_right_line = pygame.draw.line(surface, '#ffffff', (menu_x + self.width - 5, menu_y + 3),
                                                     (menu_x + self.width - self.height // 19.2 + 1,
                                                      menu_y + self.height // 19.2 - 3), 3)

    def show_messagebox(self, surface: pygame.Surface, btn: pygame.Rect) -> None:
        self.cur_btn = btn
        window_width = self.width * 1.5 // 3.41
        window_height = self.height * 1.5 // 3.456
        self.window = pygame.draw.rect(surface, (253, 217, 181), (self.width * 1.5 // 2 - window_width // 2,
                                                                  self.height * 1.5 // 2 - window_height // 2,
                                                                  window_width, window_height))
        self.btn_yes_front = pygame.draw.rect(surface, '#6f47D7', (self.window.centerx - self.window.width // 4 - 75,
                                                                   self.window.centery + self.window.height // 4 - 25,
                                                                   150, 50))
        self.btn_yes_back = pygame.draw.rect(surface, '#000000', (self.btn_yes_front.x, self.btn_yes_front.y,
                                                                  150, 50), 5)
        self.btn_no_front = pygame.draw.rect(surface, '#6f47D7', (self.window.centerx + self.window.width // 4 - 75,
                                                                  self.window.centery + self.window.height // 4 - 25,
                                                                  150, 50))
        self.btn_no_back = pygame.draw.rect(surface, '#000000', (self.btn_no_front.x, self.btn_no_front.y,
                                                                 150, 50), 5)
        text_warning = self.font3.render('Overwrite your save?', True, '#000000')
        surface.blit(text_warning, (self.window.centerx - text_warning.get_width() // 2,
                                    self.window.centery - text_warning.get_height()))
        text_yes = self.font1.render('Yes', True, '#ffffff')
        surface.blit(text_yes, (self.btn_yes_front.centerx - text_yes.get_width() // 2,
                                self.btn_yes_front.centery - text_yes.get_height() // 1.5))
        text_no = self.font1.render('No', True, '#ffffff')
        surface.blit(text_no, (self.btn_no_front.centerx - text_no.get_width() // 2,
                               self.btn_no_front.centery - text_no.get_height() // 1.5))

    def save_game(self, data: Menu.Menu, db: str, btn: pygame.Rect):
        con = sqlite3.connect(db)
        res = con.execute('''
        UPDATE saves
        SET dmg = ?, balance = ?, max_level = ?, killed_each_level = ?, bonus_hp = ?
        WHERE id = ?''', (str(data.price), int(data.balance), len(data.killed),
                          str(data.killed), str(data.bonus), self.buttons.index(btn) + 1))
        con.commit()
        con.close()
