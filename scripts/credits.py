from scripts.functions import *


# стартовое окно
def start_screen():
    count_frames = 0  # количество кадр после начала
    speed = 1 / FPS  # скорость прокрутки текста
    fon = pygame.transform.scale(load_image('credits\\start_screen.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))  # фон

    font = pygame.font.Font(None, 18)
    # краткий сюжет игры
    intro_text = ["Котики. Люди. Школьники.",
                  "Когда-то давно все эти расы жили в мире.",
                  "Но всё изменилось, когда Понасенко всех переиграл и уничтожил.",
                  "Только Амогус, властелин всех мемов и рофлов, мог остановить Понасенко.",
                  "Но когда мир нуждался в амогусе больше всего он исчез.",
                  "Прошло десять лет, и мы с Маратом нашли нового Амогуса, в маге жука по имени Джук.",
                  "И хотя его искусство покорения жука было велико, ему предстояло ещё многому научиться.",
                  "Но я верила, что Джук спасёт мир."]

    # фоновая музыка
    background_music = "cinematic-dramatic-11120.mp3"
    play_background_music(background_music)

    # начальный цикл
    while True:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                return  # начинаем игру

        # рисование на screen
        screen.fill(BLACK)
        screen.blit(fon, (0, 0))  #

        # координата начального текста
        text_coord = screen.get_height() - speed * count_frames
        for line in intro_text:
            # размещаем поверхность с текстом на screen
            string_rendered = font.render(line, True, ORANGE)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 25
            intro_rect.y = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        pygame.display.flip()
        count_frames += 1
        if text_coord <= 0:  # при выходе текста за экран завершить работу
            pygame.mixer.music.stop()
            return


# окно завершение
def end_screen():
    count_frames = 0  # количество кадр после начала
    speed = 1.5 / FPS  # скорость прокрутки текста
    fon = pygame.transform.scale(load_image('credits\\end_screen.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))  # фон

    # текст финального окна
    font = load_font("Boncegro FF 4F.otf", 15)
    intro_text = ["И вот, армия Амогуса все таки смогла победить Понасенкова и его союзников",
                  "Понасенкова забрали санитары в дурку, все мемы были отправлены на перевоспитание",
                  "Наконец, в этот мир вернулся баланс и справедливость",
                  "И отныне, все расы жили в мире и спокойствии",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  "",
                  ]

    final_font = load_font("coldnightforalligators.otf", 28)
    final_text = "Пока Школьники не начали спорить про Майнкрафт..."

    # фоновая музыка
    background_music = "spokojnoj-nochi.mp3"
    play_background_music(background_music)

    # финальный цикл
    while True:
        # обработка событий
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                terminate()

        screen.fill(BLACK)
        screen.blit(fon, (0, 0))

        # координата начального текста
        text_coord = screen.get_height() - speed * count_frames
        for line in intro_text:
            # размещаем поверхность с текстом на screen
            string_rendered = font.render(line, True, ORANGE)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 25
            intro_rect.y = text_coord
            text_coord += intro_rect.height
            screen.blit(string_rendered, intro_rect)

        # для финальной строки отдельная обработка
        final_rendered = final_font.render(final_text, True, ORANGE)
        intro_rect = final_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
        text_coord += 25
        intro_rect.y = text_coord
        text_coord += intro_rect.height
        screen.blit(final_rendered, intro_rect)

        pygame.display.flip()
        count_frames += 1
        if text_coord <= 0:  # при выходе текста за экран завершить работу
            pygame.mixer.music.stop()
            return
