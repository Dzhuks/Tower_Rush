from scripts.functions import *


def game_over():
    alpha = 0
    fon = load_image("end_game\\game_over.png")
    font = load_font("coldnightforalligators.otf", 60)
    background_music = "hello-darkness-my-old-friend-sound-effect.mp3"

    string_rendered = font.render("Переиграл   и   Уничтожил", True, BLOOD_RED)
    text_coord = screen.get_width() / 2 - string_rendered.get_width() / 2, 265
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

        screen.fill(BLACK)
        fon.set_alpha(alpha)
        string_rendered.set_alpha(alpha)
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, text_coord)
        pygame.display.flip()
        alpha += 1
        clock.tick(FPS)


def win():
    alpha = 0
    fon = load_image("end_game\\win_window.png")
    font = load_font("coldnightforalligators.otf", 40)
    win_sound = load_sound("z_uki-pobeda-2.mp3")
    win_sound.play()

    level_number, time, killed_enemies, tower_hp, status = save.get()
    win_text = [f"Время:\t{time}",
                f"Оставшееся здоровье у базы: {tower_hp}",
                "ЧЕЛ ХОРОШ"]

    clock = pygame.time.Clock()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру

        screen.fill(BLACK)
        fon.set_alpha(alpha)
        screen.blit(fon, (0, 0))
        text_coord = 50
        for line in win_text:
            string_rendered = font.render(line, 1, WHITE)
            string_rendered.set_alpha(alpha)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)
        pygame.display.flip()
        clock.tick(FPS)
        alpha += 1
