import pygame.mixer_music
from scripts.menu import *
from scripts.functions import *
from scripts.game import Game


# главное меню
class MainMenu(Menu):
    def __init__(self):
        bg = load_image('main_menu\\main_menu.png')  # фон
        super(MainMenu, self).__init__(bg, 0, 0)  # вызываем родительскии класс

        start_btn_img = load_image('main_menu\\start_button.png')
        start_btn_x = self.rect.width / 2 - start_btn_img.get_width() / 2
        start_btn_y = self.rect.height / 2 - start_btn_img.get_height() / 2
        self.start_btn = Button("start button", start_btn_img, start_btn_x, start_btn_y)
        self.buttons.add(self.start_btn)
        self.buttons.draw(self.bg)

    def run(self, window: pygame.Surface):
        background_music = "honor-and-sword-main-11222.mp3"  # фоновая музыка
        play_background_music(background_music)

        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.mixer.music.stop()
                    running = False

                if event.type == pygame.MOUSEBUTTONDOWN:
                    # check if hit start btn

                    if self.start_btn.is_clicked(event.pos):
                        # начинаем игру
                        pygame.mixer.music.stop()
                        game = Game()
                        game.run(window)
                        break

            # рисуем на экране
            window.fill(pygame.color.Color("black"))
            window.blit(self.bg, self.rect.topleft)
            pygame.display.flip()

        pygame.quit()
