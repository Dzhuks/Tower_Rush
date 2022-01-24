import sqlite3

import pygame.sprite
from scripts.constants import *


def hitbox_collision(sprite1, sprite2):
    """Check if the hitbox of the first sprite collides with the
    rect of the second sprite.

    `spritecollide` will pass the player object as `sprite1`
    and the sprites in the enemies group as `sprite2`.
    """
    return sprite1.range.colliderect(sprite2.rect)


class Unit(pygame.sprite.Sprite):
    def __init__(self, name, x, y, *groups):
        super(Unit, self).__init__(*groups)

        self.name = name

        self.con = sqlite3.connect("data\\stats_db.db")
        cur = self.con.cursor()

        self.image = load_image(cur.execute(f"SELECT image FROM units WHERE name={name}").fetchall()[0][0])
        self.rect = self.image.get_rect()
        self.rect.move(x, y)

        self.range = self.rect.copy()
        self.range.width += cur.execute(f"SELECT range FROM units WHERE name={name}").fetchall()[0][0]

        self.hp = cur.execute(f"SELECT hp FROM units WHERE name={name}").fetchall()[0][0]

        self.damage = cur.execute(f"SELECT damage FROM units WHERE name={name}").fetchall()[0][0]
        speed = cur.execute(f"SELECT speed FROM units WHERE name={name}").fetchall()[0][0]
        self.time_for_move = FPS // speed
        self.speed = 1
        self.cost = cur.execute(f"SELECT cost FROM units WHERE name={name}").fetchall()[0][0]
        self.money = cur.execute(f"SELECT money FROM units WHERE name={name}").fetchall()[0][0]

        moving_animation = cur.execute(f"SELECT moving_animation FROM units WHERE name={name}").fetchall()[0][0]
        moving_animation = load_image(moving_animation)
        self.cur_moving_frame = -1
        self.move_frames = self.cut_sheet(moving_animation)

        attack_animation = cur.execute(f"SELECT attack_animation FROM units WHERE name={name}").fetchall()[0][0]
        attack_animation = load_image(attack_animation)
        self.cur_attacking_frame = -1
        self.attack_frames = self.cut_sheet(attack_animation)

        death_animation = cur.execute(f"SELECT death_animation FROM units WHERE name={name}").fetchall()[0][0]
        death_animation = load_image(death_animation)
        self.cur_death_frame = -1
        self.death_frames = self.cut_sheet(death_animation)

        self.alive = True
        self.iteration = 0

    def cut_sheet(self, sheet: pygame.Surface):
        frames = []
        rows = sheet.get_width() // self.rect.width
        columns = sheet.get_height() // self.rect.height
        for j in range(rows):
            for i in range(columns):
                frame_location = (self.rect.width * i, self.rect.height * j)
                frames.append(sheet.subsurface(pygame.Rect(frame_location, self.rect.size)))
        return frames

    def update_death(self):
        self.cur_death_frame += 1
        if self.cur_death_frame > len(self.death_frames):
            self.kill()
            del self
        else:
            self.image = self.death_frames[self.cur_death_frame]

    def move(self):
        self.cur_attacking_frame = 0
        if self.iteration % self.time_for_move:
            self.rect.x += self.speed
            self.cur_moving_frame = (self.cur_moving_frame + 1) % len(self.move_frames)
            self.image = self.move_frames[self.cur_moving_frame]

    def attack(self, group: list):
        self.cur_moving_frame = 0
        self.cur_attacking_frame = self.cur_attacking_frame + 1
        self.image = self.attack_frames[self.cur_attacking_frame]
        if self.cur_attacking_frame == len(self.attack_frames) - 1:
            self.cur_attacking_frame = 0
            for unit in group:
                unit.defense(self.damage)

    def defense(self, damage):
        self.hp -= damage
        if self.hp <= 0:
            self.alive = False

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
        self.speed = -1
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
