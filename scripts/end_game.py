from scripts.constants import *


def game_over(win: pygame.Surface):
    alpha = 0
    fon = load_image("end_game\\game_over.png")
    font = load_font("coldnightforalligators.otf", 60)
    background_music = "hello-darkness-my-old-friend-sound-effect.mp3"

    string_rendered = font.render("Переиграл   и   Уничтожил", True, BLOOD_RED)
    text_coord = win.get_width() / 2 - string_rendered.get_width() / 2, 265
    string_rendered = pygame.transform.scale(string_rendered, (string_rendered.get_width(), 100))

    play_background_music(background_music)

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
                return  # начинаем игру

        win.fill(BLACK)
        fon.set_alpha(alpha)
        string_rendered.set_alpha(alpha)
        win.blit(fon, (0, 0))
        win.blit(string_rendered, text_coord)
        pygame.display.flip()
        alpha += 1
        clock.tick(FPS)


def win(win):
    pass
