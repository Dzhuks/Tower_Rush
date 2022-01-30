from scripts.constants import *


def start_screen(win: pygame.Surface):
    count_frames = 0
    speed = 1 / FPS
    fon = pygame.transform.scale(load_image('credits\\start_screen.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    font = pygame.font.Font(None, 18)
    intro_text = ["Котики. Люди. Школьники.",
                  "Когда-то давно все эти расы жили в мире.",
                  "Но всё изменилось, когда Поносенко всех переиграл и уничтожил.",
                  "Только Амогус, властелин всех мемов и рофлов, мог остановить Поносенко.",
                  "Но когда мир нуждался в амогусе больше всего он исчез.",
                  "Прошло десять лет, и мы с Маратом нашли нового Амогуса, в маге жука по имени Джук.",
                  "И хотя его искусство покорения жука было велико, ему предстояло ещё многому научиться.",
                  "Но я верила, что Джук спасёт мир."]
    background_music = "cinematic-dramatic-11120.mp3"
    play_background_music(background_music)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                pygame.mixer.music.stop()
                return  # начинаем игру
        win.fill(BLACK)
        win.blit(fon, (0, 0))
        text_coord = win.get_height() - speed * count_frames
        for line in intro_text:
            string_rendered = font.render(line, True, ORANGE)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 25
            intro_rect.y = text_coord
            text_coord += intro_rect.height
            win.blit(string_rendered, intro_rect)
        pygame.display.flip()
        count_frames += 1
        if text_coord <= 0:
            pygame.mixer.music.stop()
            return


def end_screen(win):
    pass