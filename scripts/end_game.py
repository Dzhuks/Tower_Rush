from scripts.functions import *


# функция проигрыша
def game_over():
    alpha = 0  # прозрачность
    fon = load_image("end_game\\game_over.png")  # фон
    font = load_font("coldnightforalligators.otf", 60)  # шрифт

    background_music = "hello-darkness-my-old-friend-sound-effect.mp3"  # фоновая музыка
    play_background_music(background_music)

    # текст
    string_rendered = font.render("Переиграл   и   Уничтожил", True, BLOOD_RED)
    text_coord = screen.get_width() / 2 - string_rendered.get_width() / 2, 265
    string_rendered = pygame.transform.scale(string_rendered, (string_rendered.get_width(), 100))

    clock = pygame.time.Clock()  # игровые часы

    # цикл
    while True:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()
                return  # завершаем игру

        # меняем прозрачность screen
        screen.fill(BLACK)
        fon.set_alpha(alpha)
        string_rendered.set_alpha(alpha)
        screen.blit(fon, (0, 0))
        screen.blit(string_rendered, text_coord)
        pygame.display.flip()
        alpha += 1
        clock.tick(FPS)


# функция показа результата пользователя при окончание уровня
def win():
    alpha = 0
    fon = load_image("end_game\\win_window.png")
    font = load_font("coldnightforalligators.otf", 40)

    win_sound = load_sound("z_uki-pobeda-2.mp3")  # звук победы
    win_sound.play()

    # получение данных с последней игры
    level_number, time, tower_hp, status = save.get()
    # текст окна
    win_text = [f"Время:\t{time}",
                f"Оставшееся здоровье у базы: {tower_hp}",
                "ЧЕЛ ХОРОШ"]

    clock = pygame.time.Clock()

    # цикл
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return

        # делаем blit на screen
        screen.fill(BLACK)
        fon.set_alpha(alpha)
        screen.blit(fon, (0, 0))

        text_coord = 50  # координата текста
        for line in win_text:
            # накладываем поверхность с текстом на screen
            string_rendered = font.render(line, 1, WHITE)
            string_rendered.set_alpha(alpha)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 10
            intro_rect.top = text_coord
            intro_rect.x = 10
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip() # сменяем кадр
        clock.tick(FPS)
        alpha += 1
