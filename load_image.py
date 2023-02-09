# Импорт библиотек
import os
import sys
import pygame


def load_image(name: str, colorkey=None) -> pygame.Surface:
    fullname = os.path.join('data', name)  # Полный путь к файлу
    if not os.path.isfile(fullname):  # Если путь пустой
        print(f"Файл с изображением '{fullname}' не найден")
        sys.exit()  # Выход
    image = pygame.image.load(fullname)
    if colorkey is not None:  # Если был указан colorkey
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)  # Переданный цвет colorkey станет прозрачным
    else:
        image = image.convert_alpha()  # Изображение уже прозрачно
    return image
