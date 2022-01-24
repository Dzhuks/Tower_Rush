from scripts.constants import *


def start_screen(win: pygame.Surface):
    count_frames = 0
    speed = 2 / FPS
    intro_text = ["Котики, Люди, Школьники",
                  "Когда-то давно все они жили в мире, но все изменилось когда Поносенко всех переиграл и уничтожил",
                  "Только Амогус властелин всех мемов и рофлов мог остановить войну.",
                  "Но когда мир нуждался в амогусе больше всего он исчез.",
                  "Прошло десять лет и появился новый Амогус под именем Кличко, ",
                  "и хотя его искусство завтрашнего дня и арифметики было велико ему пристояло еще многому научится.",
                  "Но я верила что Кличко спасет мир."]
    font = pygame.font.Font(None, 30)
    fon = pygame.transform.scale(load_image('start_screen\\bg.png'), (SCREEN_WIDTH, SCREEN_HEIGHT))
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                terminate()
            elif event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return  # начинаем игру
        win.fill(BLACK)
        win.blit(fon, (0, 0))
        text_coord = win.get_height() - speed * count_frames
        for line in intro_text:
            string_rendered = font.render(line, True, ORANGE)
            intro_rect = string_rendered.get_rect(center=(SCREEN_WIDTH / 2, SCREEN_HEIGHT / 2))
            text_coord += 30
            intro_rect.y = text_coord
            text_coord += intro_rect.height
            win.blit(string_rendered, intro_rect)
        pygame.display.flip()
        count_frames += 1
        if text_coord <= 0:
            return
