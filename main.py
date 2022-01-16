import pygame
import sys
import os


def terminate():
    pygame.quit()
    sys.exit()


def load_image(name, colorkey=None):
    fullname = os.path.join('data', name)
    # если файл не существует, то выходим
    if not os.path.isfile(fullname):
        print(f"Файл с изображением '{fullname}' не найден")
        terminate()
    image = pygame.image.load(fullname)
    if colorkey is not None:
        image = image.convert()
        if colorkey == -1:
            colorkey = image.get_at((0, 0))
        image.set_colorkey(colorkey)
    else:
        image = image.convert_alpha()
    return image


class Game:
    def __init__(self, caption, width, height, frame_rate):
        pygame.init()
        self.size = self.width, self.height = width, height
        self.fps = frame_rate
        self.screen = pygame.display.set_mode(self.size)
        pygame.display.set_caption(caption)
        self.clock = pygame.time.Clock()
        self.game_over = False
        self.win = False

    def update(self):
        pass

    def draw(self):
        pass

    def handle_events(self):
        pass

    def run(self):
        while not self.game_over or not self.win:
            self.handle_events()
            self.update()
            self.draw()
            pygame.display.flip()
            self.clock.tick(self.fps)
        if self.game_over:
            pass
        elif self.win:
            pass
        terminate()


if __name__ == '__main__':
    game = Game("Tower Rush", 600, 400, 50)
    game.run()
