import sqlite3
import random

import pygame.sprite
from scripts.functions import *


# класс частицы
class Particle(pygame.sprite.Sprite):
    # сгенерируем частицы разного размера
    fire = [load_image("sprites\\star.png")]
    for scale in (5, 10, 20):
        fire.append(pygame.transform.scale(fire[0], (scale, scale)))

    def __init__(self, pos, dx, dy):
        super().__init__(ALL_SPRITES)
        self.image = random.choice(self.fire)
        self.rect = self.image.get_rect()

        # у каждой частицы своя скорость — это вектор
        self.velocity = [dx, dy]
        # и свои координаты
        self.rect.x, self.rect.y = pos

        # гравитация будет одинаковой (значение константы)
        self.gravity = GRAVITY

    def update(self):
        # применяем гравитационный эффект:
        # движение с ускорением под действием гравитации
        self.velocity[1] += self.gravity
        # перемещаем частицу
        self.rect.x += self.velocity[0]
        self.rect.y += self.velocity[1]
        # убиваем, если частица ушла за экран
        if self.rect.width > SCREEN_WIDTH or self.rect.height > SCREEN_HEIGHT:
            self.kill()
            del self


def hitbox_collision(sprite1, sprite2):
    """Check if the hitbox of the first sprite collides with the
    rect of the second sprite.

    `spritecollide` will pass the player object as `sprite1`
    and the sprites in the enemies group as `sprite2`.
    """
    return sprite1.range.colliderect(sprite2.rect)


# вырезаем кадры анимации
def cut_sheet(sheet: pygame.Surface, rows, columns):
    frames = []
    size = width, height = sheet.get_width() // columns, sheet.get_height() // rows
    for j in range(rows):
        for i in range(columns):
            frame_location = (width * i, height * j)
            frames.append(sheet.subsurface(pygame.Rect(frame_location, size)))
    return frames


# класс юнита
class Unit(pygame.sprite.Sprite):
    # переменные общий для всех юнитов (изображение смерти, скорость летучести, звук удара, смерти
    death_image = load_image("sprites\\death_animation.png")
    FLY = -30 / FPS
    hit_sound = load_sound("inecraft_hit_sound.mp3")
    death_sound = load_sound("inecraft_death.mp3")

    def __init__(self, name, tower, *groups):
        super(Unit, self).__init__(*groups)

        self.name = name

        # связываемся с бд
        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        # кадры анимация
        animation = load_image(cur.execute(f"SELECT animation FROM units WHERE name=\"{name}\"").fetchall()[0][0])
        rows, columns = cur.execute(f"SELECT rows, columns FROM units WHERE name=\"{name}\"").fetchall()[0]
        self.frames = cut_sheet(animation, rows, columns)
        self.cur_frame = 0  # текущии кадр

        # определям image, rect
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = tower.rect.x + tower.rect.width / 2
        self.rect.y = tower.rect.bottom - self.rect.height

        # координаты юнита. Нужны для вещественных значений, так как rect принимает только уелые значения
        self.x_pos = self.rect.x
        self.y_pos = self.rect.y

        # дальность
        self.range = self.rect.copy()
        self.move_range()

        # характеристики юнита
        self.hp = cur.execute(f"SELECT hp FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.damage = cur.execute(f"SELECT damage FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.speed = -cur.execute(f"SELECT speed FROM units WHERE name=\"{name}\"").fetchall()[0][0] / FPS

        self.tba = 0

        self.cost = cur.execute(f"SELECT cost FROM units WHERE name=\"{name}\"").fetchall()[0][0]
        self.money = cur.execute(f"SELECT money FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.alive = True
        self.iteration = 0

    # функция смерти. При смерти перемещать изображение смерти наверх
    def death(self):
        self.image = Unit.death_image
        self.y_pos += Unit.FLY
        self.rect.y = int(self.y_pos)

    # функция передвижения
    def move(self):
        self.x_pos += self.speed
        self.rect.x = int(self.x_pos)
        self.move_range()

    # функция для перемещения дальности
    def move_range(self):
        cur = self.con.cursor()
        self.range = self.rect.copy()
        self.range.x -= cur.execute(f"SELECT range FROM units WHERE name=\"{self.name}\"").fetchall()[0][0]

    # функция атаки
    def attack(self, group: list):
        if self.tba <= 0:  # если tba(Time Between Attack) равен 0, то атаковать
            for unit in group:
                unit.defense(self.damage)
            cur = self.con.cursor()
            self.tba = cur.execute(f"SELECT TBA FROM units WHERE name=\"{self.name}\"").fetchall()[0][0] * FPS

    # при получение урона генерировать частицы
    def create_particles(self, position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))

    # функция принятия урона
    def defense(self, damage):
        """
        Если юнит мертв, то удалить его из всех групп, добавить в группу DEAD_SPRITES и издать звук смерти
        Иначе издать звук получения урона
        """

        if self.hp > 0 >= self.hp - damage:
            self.alive = False
            self.kill()
            DEAD_SPRITES.add(self)
            ALL_SPRITES.add(self)
            Unit.death_sound.play()
        else:
            Unit.hit_sound.play()
            self.create_particles(self.rect.center)
        self.hp -= damage

    # функция обновления
    def update(self, *args) -> None:
        self.iteration += 1
        if not self.alive:  # если юнит мертв, то вызвать функцию death()
            self.death()
            return

        self.tba = max(0, self.tba - 1)  # уменьшить время атаки

        # каждый десятый кадр обновлять анимацию
        if self.iteration % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        # если юнит сталкивается с врагами атаковать его, иначе продолжить двигаться
        if pygame.sprite.spritecollideany(self, ENEMIES_SPRITES, collided=hitbox_collision):
            collided_enemy_units = pygame.sprite.spritecollide(self, ENEMIES_SPRITES, False, collided=hitbox_collision)
            self.attack(collided_enemy_units)
            return

        self.move()


# класс вражеского юнита
class EnemyUnit(Unit):
    def __init__(self, name, tower, *groups):
        super(EnemyUnit, self).__init__(name, tower, *groups)
        # изменить на противоположную скорость и дальность
        self.speed = -self.speed
        self.range.width -= 2 * self.range.width + self.rect.width

    # переопределяем функцию move_range
    def move_range(self):
        cur = self.con.cursor()
        self.range = self.rect.copy()
        self.range.x += cur.execute(f"SELECT range FROM units WHERE name=\"{self.name}\"").fetchall()[0][0]

    # функция получение денег с поверженного врага
    def get_money(self):
        if self.alive:
            return 0

        money = self.money
        self.money = 0
        return money

    # функция обновления состояние вражеского юнита
    def update(self, *args) -> None:
        self.iteration += 1
        if not self.alive:
            self.death()
            return

        self.tba = max(0, self.tba - 1)

        if self.iteration % 10 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

        if pygame.sprite.spritecollideany(self, PLAYER_SPRITES, collided=hitbox_collision):
            collided_enemy_units = pygame.sprite.spritecollide(self, PLAYER_SPRITES, False, collided=hitbox_collision)
            self.attack(collided_enemy_units)
            return

        self.move()


# класс Босса. Отличается тем, что при выходе вызывает музыку
class Boss(EnemyUnit):
    background_music = "Rick_Astley_-_Never_Gonna_Give_You_Up_(musmore.com).mp3"

    def __init__(self, name, tower, *groups):
        super(Boss, self).__init__(name, tower, *groups)
        play_background_music(Boss.background_music)
