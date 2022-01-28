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
    DEATH_ANIMATION = load_image("sprites\\death_animation")
    DEATH_ANIMATION_ROWS = 5
    DEATH_ANIMATION_COLUMNS = 1

    def __init__(self, name, x, y, *groups):
        super(Unit, self).__init__(*groups)

        self.name = name

        self.con = sqlite3.connect(DATABASE)
        cur = self.con.cursor()

        animation = load_image(cur.execute(f"SELECT image FROM units WHERE name={name}").fetchall()[0][0])
        rows, columns = cur.execute(f"SELECT rows, columns FROM units WHERE name={name}").fetchall()[0]

        self.frames = self.cut_sheet(animation, rows, columns)
        self.cur_frame = 0
        self.image = self.frames[self.cur_frame]
        self.rect = self.image.get_rect().move(x, y)

        self.cur_death_frame = -1
        self.death_frames = self.cut_sheet(Unit.DEATH_ANIMATION, Unit.DEATH_ANIMATION_ROWS, Unit.DEATH_ANIMATION_COLUMNS)

        self.range = self.rect.copy()
        self.range.width += cur.execute(f"SELECT range FROM units WHERE name={name}").fetchall()[0][0]

        self.hp = cur.execute(f"SELECT hp FROM units WHERE name={name}").fetchall()[0][0]

        self.damage = cur.execute(f"SELECT damage FROM units WHERE name={name}").fetchall()[0][0]

        speed = cur.execute(f"SELECT speed FROM units WHERE name={name}").fetchall()[0][0]
        self.time_for_move = FPS // speed

        self.tba = 0
        self.speed = -1

        self.cost = cur.execute(f"SELECT cost FROM units WHERE name={name}").fetchall()[0][0]
        self.money = cur.execute(f"SELECT money FROM units WHERE name={name}").fetchall()[0][0]

        self.alive = True
        self.iteration = 0

    def cut_sheet(self, sheet: pygame.Surface, rows, columns):
        frames = []
        size = width, height = sheet.get_width() // rows, sheet.get_height() // columns
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
        self.tba = 0
        if self.iteration % self.time_for_move:
            self.rect.x += self.speed
            self.cur_frame = (self.cur_frame + 1) % len(self.frames)
            self.image = self.frames[self.cur_frame]

    def attack(self, group: list):
        self.cur_frame = 0
        self.tba -= 1
        if self.tba == 0:
            for unit in group:
                unit.defense(self.damage)
            cur = self.con.cursor()
            self.tba = cur.execute(f"SELECT TBA FROM units WHERE name={self.name}").fetchall()[0][0]

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

        if not pygame.sprite.spritecollideany(self, PLAYER_SPRITES):
            if not pygame.sprite.spritecollideany(self, TOWER_SPRITES):
                self.move()
                return

        collided_enemy_units = pygame.sprite.spritecollide(self, PLAYER_SPRITES, False, collided=hitbox_collision)
        collided_enemy_tower = pygame.sprite.spritecollide(self, TOWER_SPRITES, False, collided=hitbox_collision)
        self.attack(collided_enemy_tower + collided_enemy_units)


class EnemyUnit(Unit):
    def __init__(self, name, x, y, *groups):
        super(EnemyUnit, self).__init__(name, x, y, *groups)
        self.speed = 1
        self.range.width -= 2 * self.range.width + self.rect.width

    def update(self, *args) -> None:
        self.iteration += 1
        if not self.alive:
            self.update_death()
            return

        if not pygame.sprite.spritecollideany(self, PLAYER_SPRITES):
            if not pygame.sprite.spritecollideany(self, TOWER_SPRITES):
                self.move()
                return

        collided_player_units = pygame.sprite.spritecollide(self, PLAYER_SPRITES, False, collided=hitbox_collision)
        collided_player_tower = pygame.sprite.spritecollide(self, TOWER_SPRITES, False, collided=hitbox_collision)
        self.attack(collided_player_tower + collided_player_units)
