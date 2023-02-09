# Импорт библиотек и файлов
import pygame
import Game
import random
import Menu


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet_afk: pygame.Surface, sheet_dmg: pygame.Surface, sheet_dead: pygame.Surface, columns: int,
                 rows: int, columns2: int, rows2: int, columns3: int, rows3: int, x: float, y: float,
                 sprite: pygame.sprite.Group, health_all: int = 10, gold: int = 3) -> None:
        super().__init__(sprite)  # Вызов конструктора родительского класса Sprite
        self.frames = []  # Список idle кадров
        self.dmg_frames = []  # Список dmg кадров
        self.dead_frames = []  # Список dead кадров
        self.cut_sheet(sheet_afk, sheet_dmg, sheet_dead, columns, rows, columns2, rows2, columns3, rows3)  # Обрезка
        self.cur_frame = 0  # Данный idle кадр
        self.cur_dmg_frame = 0  # Данный idle кадр
        self.cur_dead_frame = 0  # Данный idle кадр
        self.c = 0  # counter
        self.image = self.frames[self.cur_frame]  # Данное изображение
        self.rect = self.rect.move(x, y)  # rect'ы для обрезки
        self.rect2 = self.rect2.move(x, y)
        self.rect3 = self.rect3.move(x, y)
        self.not_damaged = True  # Сущность не получает урон
        self.dead = False  # Сущность жива
        self.can_damage = True  # Сущности можно наносить урон
        self.off = False  # Сущность включена
        self.health_all = health_all  # Полное здоровье сущности
        self.health_r = self.health_all  # Текущее здоровье сущности
        self.gold = gold  # Количество выпадаемого золота с сущности

    def cut_sheet(self, sheet_afk: pygame.Surface, sheet_dmg: pygame.Surface, sheet_dead: pygame.Surface,
                  columns: int, rows: int, columns2: int, rows2: int, columns3: int, rows3: int) -> None:  # Обрезка,
        # добавление кадров в списки кадров
        self.rect = pygame.Rect(0, 0, sheet_afk.get_width() // columns,
                                sheet_afk.get_height() // rows)
        self.rect2 = pygame.Rect(0, 0, sheet_dmg.get_width() // columns2,
                                 sheet_dmg.get_height() // rows2)
        self.rect3 = pygame.Rect(0, 0, sheet_dead.get_width() // columns3,
                                 sheet_dead.get_height() // rows3)

        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                self.frames.append(sheet_afk.subsurface(pygame.Rect(
                    frame_location, self.rect.size)))

        for j in range(rows2):
            for i in range(columns2):
                frame_location = (self.rect2.w * i, self.rect2.h * j)
                self.dmg_frames.append(sheet_dmg.subsurface(pygame.Rect(
                    frame_location, self.rect2.size)))

        for j in range(rows3):
            for i in range(columns3):
                frame_location = (self.rect3.w * i, self.rect3.h * j)
                self.dead_frames.append(sheet_dead.subsurface(pygame.Rect(
                    frame_location, self.rect3.size)))

    def update(self) -> None: # Обновление кадров
        if self.not_damaged and not self.dead:  # Состояние idle
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)  # Обновление текущего кадра
            self.image = self.frames[self.cur_frame]  # Изменение текущего показываемого изображения
        elif self.dead:  # Состояние dead
            if self.cur_dead_frame + 1 == len(self.dead_frames):  # Если кадр - последний
                self.c += 1  # Задержка смерти сущности
                if self.c == 5:
                    self.c = 0
                    self.dead = False  # Сущность снова жива
                    self.health_r = self.health_all
                    self.cur_dead_frame = 0
                    self.kill()
                    self.off = True
                    Game.new_sprite()  # Новая сущность

            else:  # Обновление текущего кадра
                self.can_damage = False  # Нельзя наносить урон сущности
                self.cur_dead_frame = (self.cur_dead_frame + 1) % len(self.dead_frames)
                self.image = self.dead_frames[self.cur_dead_frame]
        else:  # Состояние dmg
            if self.cur_dmg_frame + 1 == len(self.dmg_frames):  # Последний кадр
                self.not_damaged = True  # Сущность не получает урон
                self.cur_dmg_frame = 0
            else:
                self.cur_dmg_frame = (self.cur_dmg_frame + 1) % len(self.dmg_frames) # Обновление текущего кадра
                self.image = self.dmg_frames[self.cur_dmg_frame]

    def damage(self, data: Menu.Menu, sound_dmg: pygame.mixer.Sound) -> None:  # Получение урона от клика
        if self.can_damage:
            self.not_damaged = False
            self.health_r = str(int(self.health_r) - data.dmg)
            if int(self.health_r) < 0:
                self.health_r = '0'
            if data.sfx:
                sound_dmg.play()

    def dps_damage(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:  # Получение урона от dps
        if self.can_damage:  # Если сущности можно наносить урон
            self.health_r = str(int(self.health_r) - data.dps)  # Изменение здоровья (меньше на урон от dps)
            if int(self.health_r) < 0:
                self.health_r = '0'
            self.check_for_death(data, sound_dead)  # Проверка на смерть сущности

    def check_for_death(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:
        if int(float(self.health_r)) <= 0:  # Если здоровья нет
            self.ent_dead(data, sound_dead)

    def ent_dead(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:
        self.dead = True  # Сущность мертва
        if data.drop:  # Если на земле лежала прошлая монетка
            data.collect_coin()
        data.cur_killed = str(int(data.cur_killed) + 1)  # Увеличения текущего количества убитых сущностей
        data.killed[data.level - 1] = data.cur_killed
        data.gold_now = self.gold
        if data.sfx:  # Если включены sfx
            sound_dead.stop()
            sound_dead.play()
        data.drop = True  # Монетка падает на землю
        data.coin_x = random.uniform(1.3, 1.5)  # Случайное положение монетки
        data.coin_y = random.uniform(1.4, 1.6)
        if (int(data.killed[data.level - 1]) >= 10 or (int(data.killed[data.level - 1]) >= 1 and data.boss))\
                and len(data.killed) == data.level:  # Если текущий уровень - максимальный и убито 10 врагов
            data.killed.append('0')
            if data.level % 5 == 4:
                data.bonus.append('0')
        if data.boss:  # Если текущий враг был боссом
            if data.killed[data.level - 1] == '1':  # Если убийство босса происходит в первый раз
                data.bonus[data.level // 5] = f'{int(data.bonus[data.level // 5]) + int(data.enemies_hp_now) // 2}'
            data.time = '21'  # Возврат таймера в начальное значение (станет 20 после 1 тика таймера)
        self.health_r = '0'

    def get_position(self) -> tuple:
        return self.rect.x, self.rect.y  # Получение координат сущности

    def get_size(self) -> tuple:  # Получение размеров сущности
        return self.rect.size

    def get_health(self, surface: pygame.Surface) -> None:  # Отрисовка здоровья сущности
        font = pygame.font.Font('data/fonts/at01.ttf', 100)
        text_health = font.render(f"{self.health_r}/{self.health_all}", True, '#FB000D')
        surface.blit(text_health, (surface.get_width() // 1.4 - text_health.get_width() //
                                   3, surface.get_height() // 1.3))
