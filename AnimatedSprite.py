import pygame
import Game
import random
import Menu


class AnimatedSprite(pygame.sprite.Sprite):
    def __init__(self, sheet_afk: pygame.Surface, sheet_dmg: pygame.Surface, sheet_dead: pygame.Surface, columns: int,
                 rows: int, columns2: int, rows2: int, columns3: int, rows3: int, x: float, y: float,
                 sprite: pygame.sprite.Group, health_all: int = 10, gold: int = 3) -> None:
        super().__init__(sprite)
        self.frames = []
        self.dmg_frames = []
        self.dead_frames = []
        self.cut_sheet(sheet_afk, sheet_dmg, sheet_dead, columns, rows, columns2, rows2, columns3, rows3)
        self.cur_frame = 0
        self.cur_dmg_frame = 0
        self.cur_dead_frame = 0
        self.c = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.rect.move(x, y)
        self.rect2 = self.rect2.move(x, y)
        self.rect3 = self.rect3.move(x, y)
        self.not_damaged = True
        self.dead = False
        self.can_damage = True
        self.off = False
        self.health_all = health_all
        self.health_r = self.health_all
        self.gold = gold

    def cut_sheet(self, sheet_afk: pygame.Surface, sheet_dmg: pygame.Surface, sheet_dead: pygame.Surface,
                  columns: int, rows: int, columns2: int, rows2: int, columns3: int, rows3: int) -> None:
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

    def update(self) -> None:
        if self.not_damaged and not self.dead:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]
        elif self.dead:
            if self.cur_dead_frame + 1 == len(self.dead_frames):
                self.c += 1
                if self.c == 5:
                    self.c = 0
                    self.dead = False
                    self.health_r = self.health_all
                    self.cur_dead_frame = 0
                    self.kill()
                    self.off = True
                    Game.new_sprite()

            else:
                self.can_damage = False
                self.cur_dead_frame = (self.cur_dead_frame + 1) % len(self.dead_frames)
                self.image = self.dead_frames[self.cur_dead_frame]
        else:
            if self.cur_dmg_frame + 1 == len(self.dmg_frames):
                self.not_damaged = True
                self.cur_dmg_frame = 0
            else:
                self.cur_dmg_frame = (self.cur_dmg_frame + 1) % len(self.dmg_frames)
                self.image = self.dmg_frames[self.cur_dmg_frame]

    def damage(self, data: Menu.Menu, sound_dmg: pygame.mixer.Sound) -> None:
        if self.can_damage:
            self.not_damaged = False
            self.health_r = str(int(self.health_r) - data.dmg)
            if int(self.health_r) < 0:
                self.health_r = '0'
            if data.sfx:
                sound_dmg.play()

    def dps_damage(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:
        if self.can_damage:
            self.health_r = str(int(self.health_r) - data.dps)
            if int(self.health_r) < 0:
                self.health_r = '0'
            self.check_for_death(data, sound_dead)

    def check_for_death(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:
        if int(float(self.health_r)) <= 0:
            self.ent_dead(data, sound_dead)

    def ent_dead(self, data: Menu.Menu, sound_dead: pygame.mixer.Sound) -> None:
        self.dead = True
        if data.drop:
            data.collect_coin()
        data.cur_killed = str(int(data.cur_killed) + 1)
        data.killed[data.level - 1] = data.cur_killed
        data.gold_now = self.gold
        if data.sfx:
            sound_dead.stop()
            sound_dead.play()
        data.drop = True
        data.coin_x = random.uniform(1.3, 1.5)
        data.coin_y = random.uniform(1.4, 1.6)
        if (int(data.killed[data.level - 1]) >= 10 or (int(data.killed[data.level - 1]) >= 1 and data.boss))\
                and len(data.killed) == data.level:
            data.killed.append('0')
            if data.level % 5 == 4:
                data.bonus.append('0')
        if data.boss:
            if data.killed[data.level - 1] == '1':
                data.bonus[data.level // 5] = f'{int(data.bonus[data.level // 5]) + int(data.enemies_hp_now) // 2}'
            data.time = '21'
        self.health_r = '0'

    def get_position(self) -> tuple:
        return self.rect.x, self.rect.y

    def get_size(self) -> tuple:
        return self.rect.size

    def get_health(self, surface: pygame.Surface) -> None:
        font = pygame.font.Font('data/fonts/at01.ttf', 100)
        text_health = font.render(f"{self.health_r}/{self.health_all}", True, '#FB000D')
        surface.blit(text_health, (surface.get_width() // 1.4 - text_health.get_width() //
                                   3, surface.get_height() // 1.3))
