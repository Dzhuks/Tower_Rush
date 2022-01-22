import sqlite3

import pygame.sprite
from main import load_image
from scripts.constants import *


def hitbox_collision(sprite1, sprite2):
    """Check if the hitbox of the first sprite collides with the
    rect of the second sprite.

    `spritecollide` will pass the player object as `sprite1`
    and the sprites in the enemies group as `sprite2`.
    """
    return sprite1.range.colliderect(sprite2.rect)


class Unit(pygame.sprite.Sprite):
    def __init__(self, name, x, y):
        super(Unit, self).__init__()

        self.name = name

        self.con = sqlite3.connect("data\\stats_db.db")
        cur = self.con.cursor()

        self.image = load_image(cur.execute(f"SELECT image FROM units WHERE name={name}").fetchall()[0][0])
        self.hp = cur.execute(f"SELECT hp FROM units WHERE name={name}").fetchall()[0][0]
        self.damage = cur.execute(f"SELECT damage FROM units WHERE name={name}").fetchall()[0][0]
        self.speed = cur.execute(f"SELECT speed FROM units WHERE name={name}").fetchall()[0][0]
        self.time_for_move = FPS // self.speed
        self.cost = cur.execute(f"SELECT cost FROM units WHERE name={name}").fetchall()[0][0]
        self.money = cur.execute(f"SELECT money FROM units WHERE name={name}").fetchall()[0][0]

        self.moving_animation = cur.execute(f"SELECT moving_animation FROM units WHERE name={name}").fetchall()[0][0]
        self.moving_animation = load_image(self.moving_animation)

        self.is_moving = True
        self.cur_moving_frame = -1
        self.move_frames = self.cut_sheet(self.moving_animation)

        self.attack_animation = cur.execute(f"SELECT attack_animation FROM units WHERE name={name}").fetchall()[0][0]
        self.attack_animation = load_image(self.attack_animation)

        self.is_attacking = False
        self.cur_attacking_frame = -1
        self.attack_frames = self.cut_sheet(self.attack_animation)

        self.death_animation = cur.execute(f"SELECT death_animation FROM units WHERE name={name}").fetchall()[0][0]
        self.death_animation = load_image(self.death_animation)

        self.is_alive = True
        self.cur_death_frame = -1
        self.death_frames = self.cut_sheet(self.death_animation)

        self.rect = self.image.get_rect()
        self.rect.move(x, y)

        self.range = cur.execute(f"SELECT range FROM units WHERE name={name}").fetchall()[0][0]
        self.range = pygame.rect.Rect((x, y, self.rect.width + self.range, self.rect.height))

        self.iteration = 0
        self.can_get_money = True

    def cut_sheet(self, sheet: pygame.Surface):
        frames = []
        rows = sheet.get_width() // self.rect.w
        columns = sheet.get_height() // self.rect.h
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.w * i, self.rect.h * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames

    def attacked(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.is_alive = False

    def update_death(self):
        self.cur_death_frame += 1
        if self.cur_death_frame > len(self.death_frames):
            self.kill()
            del self
        else:
            self.image = self.death_frames[self.cur_death_frame]

    def update_attacking(self):
        self.cur_attacking_frame = (self.cur_attacking_frame + 1) % len(self.attack_frames)
        self.image = self.attack_frames[self.cur_attacking_frame]

    def update_moving(self):
        self.cur_moving_frame = (self.cur_moving_frame + 1) % len(self.move_frames)
        self.image = self.move_frames[self.cur_moving_frame]

    def get_money(self):
        if self.is_alive:
            return 0
        if self.can_get_money:
            self.can_get_money = False
            return self.money
        return 0

    def attack(self, group: list):
        for sprite in group:
            sprite.attacked(self.damage)


class EnemyUnit(Unit):
    def update(self, *args) -> None:
        self.iteration += 1
        if not self.is_alive:
            self.update_death()
            return
        collided_player_units = pygame.sprite.spritecollide(self, PLAYER_SPRITES, False, collided=hitbox_collision)
        collided_player_tower = pygame.sprite.spritecollide(self, TOWER_SPRITES, False, collided=hitbox_collision)
        if len(collided_player_units) == len(collided_player_tower) == 0:
            self.move()
            self.update_moving()
        else:
            self.attack(collided_player_tower)
            self.attack(collided_player_units)
            self.update_attacking()

    def move(self):
        if self.iteration % self.time_for_move == 0:
            self.rect.x += self.speed


class PlayerUnit(Unit):
    def update(self, *args) -> None:
        self.iteration += 1
        if not self.is_alive:
            self.update_death()
            return
        collided_player_units = pygame.sprite.spritecollide(self, ENEMIES_SPRITES, False, collided=hitbox_collision)
        collided_player_tower = pygame.sprite.spritecollide(self, TOWER_SPRITES, False, collided=hitbox_collision)
        if len(collided_player_units) == len(collided_player_tower) == 0:
            self.move()
            self.update_moving()
        else:
            self.attack(collided_player_tower)
            self.attack(collided_player_units)
            self.update_attacking()

    def move(self):
        if self.iteration % self.time_for_move == 0:
            self.rect.x -= self.speed
