import os
import random
import pygame
pygame.init()

def draw_tiles():
    for i in range(len(tiles)):
        tile = tiles[i]
        row = i//ROWS
        col = i % COLS
        x = col * (TITLE_WIDTH + MARGIN) + MARGIN
        y = row * (TITLE_HEIGHT + MARGIN) + MARGIN
        if i == selected:
            pygame.draw.rect(screen,(0 , 255 , 0) , (x - MARGIN , y - MARGIN , TITLE_WIDTH + MARGIN * 2 , TITLE_HEIGHT + MARGIN * 2))
        screen.blit(tile , (x , y))

def game_over():
    font = pygame.font.SysFont('Arial' , 64)
    text = font.render('Ура , картинка собрана!' , True , (255 , 255 , 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2)
    pygame.draw.rect(screen , (0,0,0) , text_rect.inflate(4 , 4))
    screen.blit(text , text_rect)

def draw_swaps():
    font = pygame.font.SysFont('Arial' , 64)
    text = font.render(f'колличество перестановок:{swaps}' , True , (255 , 255 , 255))
    text_rect = text.get_rect()
    text_rect.center = (SCREEN_WIDTH//2 , SCREEN_HEIGHT//2 + 100)
    pygame.draw.rect(screen , (0,0,0) , text_rect.inflate(4 , 4))
    screen.blit(text , text_rect)

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
ROWS = 4
COLS = 4
MARGIN = 2

screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("пазл")
BACKGROUND = (0,0,0)

FPS = 60
clock = pygame.time.Clock()
pictures = os.listdir('pictures')
picture = random.choice(pictures)
image = pygame.image.load('pictures/' + picture)
image_width , image_height = image.get_size()

TITLE_WIDTH = image_width//COLS
TITLE_HEIGHT = image_height//ROWS


tiles = []
for i in range(ROWS):
    for j in range(COLS):
        rect = pygame.Rect( j * TITLE_WIDTH, i * TITLE_HEIGHT, TITLE_WIDTH, TITLE_HEIGHT)
        tile = image.subsurface(rect)
        tiles.append(tile)

origin_tiles = tiles.copy()
random.shuffle(tiles)

selected = None
swaps = 0


running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            pygame.quit()
            exit()
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            mouse_x , mouse_y = pygame.mouse.get_pos()
            for i in range(len(tiles)):
                row = i // ROWS
                col = i % COLS
                x = col * (TITLE_WIDTH + MARGIN) + MARGIN
                y = row * (TITLE_HEIGHT + MARGIN) + MARGIN

                if x <= mouse_x <= x + TITLE_WIDTH and y <= mouse_y <= y + TITLE_HEIGHT:
                    if selected is not  None and selected != i:
                        tiles[i], tiles[selected] = tiles[selected] , tiles[i]
                        selected = None
                        swaps += 1
                    elif selected == i:
                        selected = None
                    else:
                        selected = i
#основная логика

#отрисовка обЪектов
    screen.fill(BACKGROUND)
    draw_tiles()
    draw_swaps()
    if tiles == origin_tiles:
        game_over()
    pygame.display.flip()
    clock.tick(FPS)