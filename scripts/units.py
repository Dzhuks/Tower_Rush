import sqlite3
import random

import pygame.sprite
from scripts.constants import *


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


class Unit(pygame.sprite.Sprite):
    DEATH_ANIMATION = load_image("sprites\\death_animation.png")
    DEATH_ANIMATION_ROWS = 5
    DEATH_ANIMATION_COLUMNS = 1

    def __init__(self, name, tower, *groups):
        super(Unit, self).__init__(*groups)

        self.name = name

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        animation = load_image(cur.execute(f"SELECT animation FROM units WHERE name=\"{name}\"").fetchall()[0][0])
        rows, columns = cur.execute(f"SELECT rows, columns FROM units WHERE name=\"{name}\"").fetchall()[0]

        self.frames = self.cut_sheet(animation, rows, columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect()
        self.rect.x = tower.rect.x + tower.rect.width / 2
        self.rect.y = tower.rect.bottom - self.rect.height

        self.x_pos = self.rect.x

        self.cur_death_frame = -1
        self.death_frames = self.cut_sheet(Unit.DEATH_ANIMATION, Unit.DEATH_ANIMATION_ROWS, Unit.DEATH_ANIMATION_COLUMNS)

        self.range = self.rect.copy()
        self.move_range()

        self.hp = cur.execute(f"SELECT hp FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.damage = cur.execute(f"SELECT damage FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.speed = -cur.execute(f"SELECT speed FROM units WHERE name=\"{name}\"").fetchall()[0][0] / FPS

        self.tba = 0

        self.cost = cur.execute(f"SELECT cost FROM units WHERE name=\"{name}\"").fetchall()[0][0]
        self.money = cur.execute(f"SELECT money FROM units WHERE name=\"{name}\"").fetchall()[0][0]

        self.alive = True
        self.iteration = 0

    def cut_sheet(self, sheet: pygame.Surface, rows, columns):
        frames = []
        size = width, height = sheet.get_width() // columns, sheet.get_height() // rows
        for j in range(rows):
            for i in range(columns):
                frame_location = (width * i, height * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, size)))
        return frames

    def update_death(self):
        self.cur_death_frame += 1
        if self.cur_death_frame >= len(self.death_frames):
            self.kill()
            del self
        else:
            self.image = self.death_frames[self.cur_death_frame]

    def move(self):
        self.x_pos += self.speed
        self.rect.x = int(self.x_pos)
        self.move_range()
        if self.iteration % 6 == 0:
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def move_range(self):
        cur = self.con.cursor()
        self.range = self.rect.copy()
        self.range.x -= cur.execute(f"SELECT range FROM units WHERE name=\"{self.name}\"").fetchall()[0][0]

    def attack(self, group: list):
        self.cur_frame = 0
        if self.tba <= 0:
            for unit in group:
                unit.defense(self.damage)
            cur = self.con.cursor()
            self.tba = cur.execute(f"SELECT TBA FROM units WHERE name=\"{self.name}\"").fetchall()[0][0] * FPS

    def create_particles(self, position):
        # количество создаваемых частиц
        particle_count = 20
        # возможные скорости
        numbers = range(-5, 6)
        for _ in range(particle_count):
            Particle(position, random.choice(numbers), random.choice(numbers))

    def defense(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False
        self.create_particles(self.rect.center)

    def get_money(self):
        if self.alive:
            return 0
        money, self.money = self.money, 0
        return

    def update(self, *args) -> None:
        self.iteration += 1
        if not self.alive:
            self.update_death()
            return

        self.tba = max(0, self.tba - 1)

        if pygame.sprite.spritecollideany(self, ENEMIES_SPRITES, collided=hitbox_collision):
            collided_enemy_units = pygame.sprite.spritecollide(self, ENEMIES_SPRITES, False, collided=hitbox_collision)
            self.attack(collided_enemy_units)
            return
        self.move()


class EnemyUnit(Unit):
    def __init__(self, name, x, y, *groups):
        super(EnemyUnit, self).__init__(name, x, y, *groups)
        self.speed = -self.speed
        self.range.width -= 2 * self.range.width + self.rect.width

    def move_range(self):
        cur = self.con.cursor()
        self.range = self.rect.copy()
        self.range.x += cur.execute(f"SELECT range FROM units WHERE name=\"{self.name}\"").fetchall()[0][0]

    def update(self, *args) -> None:
        self.iteration += 1
        if not self.alive:
            self.update_death()
            return

        self.tba = max(0, self.tba - 1)

        if pygame.sprite.spritecollideany(self, PLAYER_SPRITES, collided=hitbox_collision):
            collided_enemy_units = pygame.sprite.spritecollide(self, PLAYER_SPRITES, False, collided=hitbox_collision)
            self.attack(collided_enemy_units)
            return
        self.move()
