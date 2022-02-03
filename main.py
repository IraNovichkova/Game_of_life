import pygame
from math import floor

DISPLAY_WIDTH = 640
DISPLAY_HEIGHT = 480
CELL = 20
CELL_COUNT_WIDTH, CELL_COUNT_HEIGHT = \
    DISPLAY_WIDTH // CELL, DISPLAY_HEIGHT // CELL
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GREEN = pygame.Color('chartreuse4')
gameDisplay = pygame.display.set_mode((DISPLAY_WIDTH, DISPLAY_HEIGHT))


def draw_grid():
    for x in range(0, DISPLAY_WIDTH, CELL):
        pygame.draw.line(gameDisplay, GREEN,
                         (x, 0), (x, DISPLAY_HEIGHT))
    for y in range(0, DISPLAY_HEIGHT, CELL):
        pygame.draw.line(gameDisplay, GREEN,
                         (0, y), (DISPLAY_WIDTH, y))


def generation():
    mat_generation = [[0 for _ in range(CELL_COUNT_WIDTH)]
                      for __ in range(CELL_COUNT_HEIGHT)]
    for i in range(CELL // 2, (DISPLAY_WIDTH - CELL // 2) + 1, CELL):
        for j in range(CELL // 2, (DISPLAY_HEIGHT - CELL // 2) + 1, CELL):
            if gameDisplay.get_at((i, j)) == BLACK:
                mat_generation[(j + 1) // CELL][(i + 1) // CELL] = 1
            elif gameDisplay.get_at((i, j)) == WHITE:
                mat_generation[(j + 1) // CELL][(i + 1) // CELL] = 0
    return mat_generation


def next_generation(generation):
    new_generation = [[0 for _ in range(CELL_COUNT_WIDTH)] for __ in range(CELL_COUNT_HEIGHT)]
    endstr = CELL_COUNT_WIDTH - 1
    endcolumn = CELL_COUNT_HEIGHT - 1
    for i in range(CELL_COUNT_HEIGHT):
        for j in range(CELL_COUNT_WIDTH):
            neighbors = 0
            if i + 1 <= endcolumn:
                neighbors += generation[i + 1][j]
                if j + 1 <= endstr:
                    neighbors += generation[i + 1][j + 1]
                if j - 1 >= 0:
                    neighbors += generation[i + 1][j - 1]
            if j + 1 <= endstr:
                neighbors += generation[i][j + 1]
            if i - 1 >= 0:
                neighbors += generation[i - 1][j]
                if j - 1 >= 0:
                    neighbors += generation[i - 1][j - 1]
                if j + 1 <= endstr:
                    neighbors += generation[i - 1][j + 1]
            if j - 1 >= 0:
                neighbors += generation[i][j - 1]
            if generation[i][j] == 0 and neighbors == 3:
                new_generation[i][j] = 1
            elif generation[i][j] == 1 and (neighbors == 2 or neighbors == 3):
                new_generation[i][j] = 1
    return new_generation


def draw_generation():
    cur = pygame.mouse.get_pos()
    click = pygame.mouse.get_pressed()
    color = gameDisplay.get_at(pygame.mouse.get_pos())
    if click[0] and color == WHITE:
        pygame.draw.rect(gameDisplay, BLACK, [CELL * floor(cur[0] / CELL) + 1,
                                              CELL * floor(cur[1] / CELL) + 1,
                                              CELL - 1, CELL - 1])
    elif click[2] and color == BLACK:
        pygame.draw.rect(gameDisplay, WHITE, [CELL * floor(cur[0] / CELL) + 1,
                                              CELL * floor(cur[1] / CELL) + 1,
                                              CELL - 1, CELL - 1])


def draw_new_generation(a):
    for i in range(len(a)):
        for j in range(len(a[0])):
            if a[i][j] == 1 and gameDisplay.get_at((CELL * j + 1,
                                                    CELL * i + 1)) != BLACK:
                pygame.draw.rect(gameDisplay, BLACK,
                                 [CELL * j + 1,
                                  CELL * i + 1,
                                  CELL - 1, CELL - 1])
            elif a[i][j] == 0 and gameDisplay.get_at((CELL * j + 1,
                                                      CELL * i + 1)) != WHITE:
                pygame.draw.rect(gameDisplay, WHITE,
                                 [CELL * j + 1,
                                  CELL * i + 1,
                                  CELL - 1, CELL - 1])


def empty():
    for i in range(CELL_COUNT_HEIGHT):
        for j in range(CELL_COUNT_WIDTH):
            pygame.draw.rect(gameDisplay, WHITE,
                             [CELL * j + 1,
                              CELL * i + 1,
                              CELL - 1, CELL - 1])


def func(n):
    clock = pygame.time.Clock()
    key = pygame.key.get_pressed()
    if key[pygame.K_RIGHT]:
        draw_new_generation(next_generation(generation()))
        clock.tick(n)


def game_loop(n):
    pygame.init()
    pygame.display.set_caption('Game of life')
    gameDisplay.fill(WHITE)
    draw_grid()
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            draw_generation()
            if event.type == pygame.KEYDOWN and \
                    event.key == pygame.K_SPACE:
                empty()
        func(n)
        pygame.display.update()


def welcome():
    text1 = 'Добро пожаловать. Добро пожаловать в Game of Life.'
    text2 = 'Сами вы её выбрали или её выбрали за вас,'
    text3 = 'это лучшая игра из оставшихся.'
    text4 = 'Описание: при нажатии левой кнопкой мыши '
    text5 = 'клетки оживают, при нажатии правой -- погибают.'
    text6 = 'Пробел -- все клетки умирают. '
    text7 = 'Стрелка вправо -- следующее поколение.'
    text8 = 'Введите целое число от 1 до 100. 1 -- медленная '
    text9 = 'скорость протекания жизни, 10 -- норм, 100 -- мгновенная.'
    user_text = 'скорость жизни = '
    input_rect = pygame.Rect(180, 360, 140, 32)
    color_active = pygame.Color('lightskyblue3')
    color_passive = pygame.Color('chartreuse4')

    pygame.init()
    pygame.display.set_caption('Game of life')
    gameDisplay.fill(WHITE)
    draw_grid()
    base_font = pygame.font.Font(None, 32)
    active = False
    finished = False
    while not finished:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                finished = True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    game_loop(int(user_text[17:]))
                    finished = True
            if event.type == pygame.MOUSEBUTTONDOWN:
                if input_rect.collidepoint(event.pos):
                    active = True
                else:
                    active = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    user_text = user_text[:-1]
                else:
                    user_text += event.unicode
        if active:
            color = color_active
        else:
            color = color_passive
        pygame.draw.rect(gameDisplay, color, input_rect)

        textsurface1 = base_font.render(text1,
                                        True, pygame.Color('chartreuse4'))
        textsurface2 = base_font.render(text2,
                                        True, pygame.Color('chartreuse4'))
        textsurface3 = base_font.render(text3,
                                        True, pygame.Color('chartreuse4'))
        textsurface4 = base_font.render(text4, True, (0, 0, 0))
        textsurface5 = base_font.render(text5, True, (0, 0, 0))
        textsurface6 = base_font.render(text6, True, (0, 0, 0))
        textsurface7 = base_font.render(text7, True, (0, 0, 0))
        textsurface8 = base_font.render(text8, True, (0, 0, 0))
        textsurface9 = base_font.render(text9, True, (0, 0, 0))

        gameDisplay.blit(textsurface1, (21, 21))
        gameDisplay.blit(textsurface2, (61, 61))
        gameDisplay.blit(textsurface3, (81, 101))

        gameDisplay.blit(textsurface4, (10, 160))
        gameDisplay.blit(textsurface5, (10, 180))
        gameDisplay.blit(textsurface6, (10, 200))
        gameDisplay.blit(textsurface7, (10, 220))

        gameDisplay.blit(textsurface8, (10, 300))
        gameDisplay.blit(textsurface9, (10, 320))

        base_font.render(user_text, True, (255, 255, 255))
        text_surface = base_font.render(user_text,
                                        True, (255, 255, 255))
        gameDisplay.blit(text_surface, (input_rect.x + 5,
                                        input_rect.y + 5))
        input_rect.w = max(100, text_surface.get_width() + 10)
        pygame.display.flip()
    pygame.quit()


if __name__ == "__main__":
    welcome()
