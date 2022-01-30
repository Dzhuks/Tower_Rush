import time
import csv

from scripts.menu import BuyMenu, PauseButton, SoundOnButton
from scripts.tower import *
from scripts.end_game import *
from scripts.credits import *


class Game:
    def __init__(self):
        self.con = sqlite3.connect(DATABASE)

        # обьявление ключевых переменных (деньги, пауза, музыкальная пауза, текущая итерация, время начало игры)
        self.money = 0
        self.pause = False
        self.music_pause = False
        self.iteration = 0
        self.start_time = time.time()

        # меню покупок
        self.menu = BuyMenu()

        # кнопка паузы и остановки музыки
        self.buttons = pygame.sprite.Group()
        self.pause_button = PauseButton("pause_button", 0, 0, self.buttons, ALL_SPRITES)
        self.sound_on_off = SoundOnButton("sound_on_off", 50, 0, self.buttons, ALL_SPRITES)

        # последний уровень игрока
        self.cur_level = save.last_save()
        if self.cur_level is None:
            self.cur_level = 1

        # загрузка уровня
        self.render_level()

        # загрузка уровня с врагами
        self.levels = {}
        self.render_enemies()

    # функция обнуления всех переменных
    def zeroing_out(self):
        clear_sprites()
        self.money = 0
        self.iteration = 0
        self.start_time = time.time()  # время начало игры

    # сохранение прогресса игрока
    def save_progress(self, status):
        level = self.cur_level   # текущий уровень
        period = convert_time_to_string(time.time() - self.start_time)  # разница во времени
        tower_hp = self.player_tower.cur_hp  # оставшееся здоровье
        save.save(level, period, tower_hp, status)  # сохраняем

    # загружаем уровни врагов
    def render_enemies(self):
        # открываем levels.csv
        with open("data\\levels.csv", "r") as csvfile:
            reader = csv.reader(csvfile, delimiter=';', quotechar='"')
            next(reader)
            for item in reader:
                self.levels[int(item[0])] = {}
                for i in item[1:]:
                    name, value = i.split(":")
                    time, delta = map(int, value[1:-1].split(", "))
                    self.levels[int(item[0])][name] = (time, delta)

    # загрузка уровня
    def render_level(self):
        self.zeroing_out()  # обнуление

        cur = self.con.cursor()
        que = f"""
        SELECT level_name, bg, background_music, enemy_tower_id, player_tower_id FROM levels 
            WHERE level_number={self.cur_level}"""
        result = cur.execute(que).fetchall()

        # если следущего уровня нету, то показываем финальный экран
        if not result:
            self.cur_level -= 1
            self.save_progress("win")
            end_screen()
            return

        # имя уровня, фон, вражеская башня, башня игрока
        level_name, background, background_music, enemy_tower_id, player_tower_id = result[0]
        self.level_name = level_name
        self.bg = load_image(background)
        self.enemy_tower = EnemyTower(enemy_tower_id, ENEMIES_SPRITES, ALL_SPRITES)
        self.player_tower = PlayerTower(player_tower_id, PLAYER_SPRITES, ALL_SPRITES)

        # включаем фоновую музыку
        play_background_music(background_music, self.music_pause)

        # добавляем кнопки в ALL_SPRITES
        ALL_SPRITES.add(self.pause_button)
        ALL_SPRITES.add(self.sound_on_off)

    # функция спавна юнита
    def spawn(self, name, cost):
        # если денег хватает, то спавнить юнита в башне
        if self.money >= cost:
            self.money -= cost
            self.player_tower.spawn(name)

    # функция генерация врагов
    def gen_enemies(self):
        enemies = self.levels[self.cur_level]  # враги в уровне
        for enemy in enemies.keys():
            # время спавна и частота спавна
            spawn_time, frequency = enemies[enemy]
            spawn_time *= FPS
            frequency *= FPS

            # если частота равна -1, то спавнить только один раз
            if self.iteration == spawn_time:
                self.enemy_tower.spawn(enemy)
            if self.iteration > spawn_time and frequency != -1:
                if self.iteration % frequency == 0:
                    self.enemy_tower.spawn(enemy)

    # рисовать на холсте деньги
    def draw_money_string(self, window):
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(f"{self.money}$", True, DARK_GREEN)
        window.blit(string_rendered, (window.get_width() - string_rendered.get_width(), 0))

    # функция рисования на холсте
    def draw(self, window):
        window.fill(BLACK)
        window.blit(self.bg, (0, 0))

        # рисуем спрайты
        ALL_SPRITES.draw(window)
        ENEMIES_SPRITES.draw(window)
        PLAYER_SPRITES.draw(window)

        self.menu.draw(window)

        self.draw_money_string(window)
        font = pygame.font.Font(None, 30)
        string_rendered = font.render(self.level_name, True, ORANGE)
        window.blit(string_rendered, (window.get_width() / 2 - string_rendered.get_width() / 2, 0))

        self.buttons.draw(window)

    # функция
    def run(self, window):
        running = True
        clock = pygame.time.Clock()

        # основной игровой цикл
        while running:
            # если в паузе, то не реагировать на нажатие. Кроме нажатие на кнопки паузы и остановки музыки
            if self.pause:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        self.buttons.update(event)
                        self.pause = self.pause_button.pause
                        self.music_pause = self.sound_on_off.pause
            else:
                self.iteration += 1

                # увеличить количество денег каждый третий кадр
                if self.iteration % 3 == 0:
                    self.money += 1

                # обработка событий
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False

                    # если нажата одна из иконок с персонажем, то вызывать функцию spawn
                    if event.type == pygame.MOUSEBUTTONDOWN:
                        if self.menu.get_clicked(event.pos) is not None:
                            self.spawn(*self.menu.get_clicked(event.pos))
                        else:
                            self.buttons.update(event)
                            self.pause = self.pause_button.pause
                            self.music_pause = self.sound_on_off.pause

                # если вражеская башня разрущена, то перейти на следующий уровень
                if not self.enemy_tower.is_whole:
                    self.save_progress("win")
                    self.cur_level += 1
                    win()
                    self.render_level()

                # если башня игрока разрущена, то показать окно окончание игры
                if not self.player_tower.is_whole:
                    self.save_progress("lose")
                    game_over()
                    running = False
                    break

                # спавним врагов
                self.gen_enemies()

                # обновляем юнитов
                ALL_SPRITES.update()

                # получаем деньги с поверженных врагов
                for sprite in ENEMIES_SPRITES.sprites():
                    self.money += sprite.get_money()

                # рисуем на холсте
                self.draw(window)

            pygame.display.flip()
            clock.tick(FPS)
