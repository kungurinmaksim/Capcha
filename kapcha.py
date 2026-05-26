import abc
import os
import random
import pygame
import colors


pygame.init()
pygame.font.init()

class State(abc.ABC):
    @abc.abstractmethod
    def handle_events(self , events):
        pass

    @abc.abstractmethod
    def update(self):
        pass

    @abc.abstractmethod
    def draw(self , screen):
        pass

class SplashScreen(State):
    def __init__(self):
        self.text = "Не ты ли робот?"
        self.surface = font.render(self.text , True , (255 , 255 , 255))

        self.hint = "Нажмите для продолжения"
        self.hint_surface = font.render(self.hint , True , (255 , 255 , 255))
        self.hint_visible = True
        self.hint_time = pygame.time.get_ticks()

    def handle_events(self , events):
        for event in  events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN or event.type == pygame.MOUSEBUTTONDOWN:
                return MenuScreen()
        return self

    def update(self):
        current_time = pygame.time.get_ticks()
        if current_time - self.hint_time > 800:
            self.hint_visible = not self.hint_visible
            self.hint_time = current_time

    def draw(self , screen):
        screen.fill(BACKGROUND)
        rect = self.surface.get_rect()
        rect.center = (size[0]//2 , size[1]//2 - 100)
        screen.blit(self.surface , rect)
        if self.hint_visible:
            hint_rect = self.hint_surface.get_rect()
            hint_rect.center = (size[0]//2 , size[1]//2 + 100)
            screen.blit(self.hint_surface, hint_rect)

class MenuScreen(State):
    def __init__(self):
        self.items = ["играть","Выбрать имя игрока","Выйти"]
        self.surfaces = [font.render(item, True, (255, 255, 255)) for item in self.items]
        self.selected = 0

    def handle_events(self , events):
        for event in  events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.prev()
                if event.key == pygame.K_DOWN:
                    self.next()
                if event.key == pygame.K_SPACE or event.key == pygame.K_RETURN:
                    return self.process_item()
        return self

    def update(self):
        pass

    def next(self):
        if self.selected < len(self.items) - 1:
            self.selected += 1

    def prev(self):
        if self.selected > 0:
            self.selected -= 1

    def process_item(self):
        if self.selected == 0:
            return GameScreen()
        if self.selected == 1:
            return NameScreen()
        if self.selected == 2:
            pygame.quit()
            exit()

    def draw(self , screen):
        screen.fill(BACKGROUND)
        for i, surface in enumerate(self.surfaces):
            rect =surface.get_rect()
            rect.centerx = screen.get_rect().centerx
            rect.top = screen.get_rect().top + 100 *(i+1)
            if i == self.selected:
                surface = font.render(self.items[i] , True , (255, 0, 0))
            screen.blit(surface , rect)

class NameScreen(State):
    def __init__(self):
        self.text = "Введите имя игрока"
        self.surface = font.render(self.text , True , (255 , 255 , 255))
        self.name = ""
        self.name_surface = None

    def handle_events(self , events):
        for event in  events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_BACKSPACE:
                    if len(self.name) > 0:
                        self.name = self.name[:-1]
                        self.name_surface = font.render(self.name , True , (255,255,255))
                elif event.key == pygame.K_RETURN:
                    global  player_name
                    player_name = self.name
                    return  MenuScreen()
                else:
                    if event.unicode.isalnum() and len(self.name) < 10:
                        self.name += event.unicode
                        self.name_surface = font.render(self.name , True , (255,255,255))
        return self

    def update(self):
        pass

    def draw(self , screen):
        screen.fill(BACKGROUND)
        rect = self.surface.get_rect()
        rect.centerx = screen.get_rect().centerx
        rect.top = screen.get_rect().top + 100
        screen.blit(self.surface , rect)
        if self.name_surface is not  None:
            name_rect = self.name_surface.get_rect()
            name_rect.centerx = screen.get_rect().centerx
            name_rect.top = screen.get_rect().top + 200
            screen.blit(self.name_surface , name_rect)

class GameScreen(State):
    def __init__(self):
        self.text = "Для возвращения нажмите пробел"
        self.surface = font.render(self.text , True , (255 , 255 , 255))
        self.name_surface = font.render(player_name , True , (255 , 255 , 255))
        self.swaps = 0
        self.selected = None
        self.pictures = os.listdir('pictures')
        self.picture = random.choice(self.pictures)
        self.image = pygame.image.load('pictures/' + self.picture)
        self.image_width, self.image_height = self.image.get_size()

        self.TITLE_WIDTH = self.image_width // COLS
        self.TITLE_HEIGHT = self.image_height // ROWS

        self.tiles = []

        for i in range(ROWS):
            for j in range(COLS):
                self.rect = pygame.Rect(j * self.TITLE_WIDTH, i * self.TITLE_HEIGHT, self.TITLE_WIDTH, self.TITLE_HEIGHT)
                self.tile = self.image.subsurface(self.rect)
                self.tiles.append(self.tile)

        self.origin_tiles = self.tiles.copy()
        random.shuffle(self.tiles)

        self.selected = None

    def handle_events(self , events):
        for event in  events:
            if event.type == pygame.QUIT:
                pygame.quit()
                exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE:
                    self.zero()
                    return MenuScreen()
            if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mouse_x, mouse_y = pygame.mouse.get_pos()
                for i in range(len(self.tiles)):
                    row = i // ROWS
                    col = i % COLS
                    x = col * (self.TITLE_WIDTH + MARGIN) + MARGIN
                    y = row * (self.TITLE_HEIGHT + MARGIN) + MARGIN

                    if x <= mouse_x <= x + self.TITLE_WIDTH and y <= mouse_y <= y + self.TITLE_HEIGHT:
                        if self.selected is not None and self.selected != i:
                            self.tiles[i], self.tiles[self.selected] = self.tiles[self.selected], self.tiles[i]
                            self.selected = None
                            self.swaps += 1
                        elif self.selected == i:
                            self.selected = None
                        else:
                            self.selected = i
        return self

    def draw(self , screen):
        screen.fill(BACKGROUND)
        rect = self.surface.get_rect()
        rect.center = (size[0]//2 , size[1]//2)
        rect.bottom = SCREEN_WIDTH
        screen.blit(self.surface , rect)
        name_rect = self.name_surface.get_rect()
        name_rect.left = screen.get_rect().right//1.5
        name_rect.top = screen.get_rect().top + 10
        screen.blit(self.name_surface, name_rect)
        self.draw_tiles()
        self.draw_swaps()
        if self.tiles == self.origin_tiles:
            self.game_over()


    def draw_tiles(self):
        for i in range(len(self.tiles)):
            tile = self.tiles[i]
            row = i // ROWS
            col = i % COLS
            x = col * (self.TITLE_WIDTH + MARGIN) + MARGIN
            y = row * (self.TITLE_HEIGHT + MARGIN) + MARGIN
            if i == selected:
                pygame.draw.rect(screen, (0, 255, 0),
                                 (x - MARGIN, y - MARGIN, self.TITLE_WIDTH + MARGIN * 2, self.TITLE_HEIGHT + MARGIN * 2))
            screen.blit(tile, (x, y))

    def game_over(self):
        font = pygame.font.SysFont('Arial', 64)
        text = font.render('Ура , картинка собрана!', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2)
        pygame.draw.rect(screen, (colors.GREEN), text_rect.inflate(4, 4))
        screen.blit(text, text_rect)

    def draw_swaps(self):
        font = pygame.font.SysFont('Arial', 64)
        text = font.render(f'колличество перестановок:{self.swaps}', True, (255, 255, 255))
        text_rect = text.get_rect()
        text_rect.center = (SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 100)
        pygame.draw.rect(screen, (colors.GREEN), text_rect.inflate(4, 4))
        screen.blit(text, text_rect)

    def update(self):
        pass

    def zero(self):
        self.pictures = os.listdir('pictures')
        self.picture = random.choice(self.pictures)
        self.image = pygame.image.load('pictures/' + self.picture)
        self.image_width, self.image_height = self.image.get_size()

        self.TITLE_WIDTH = self.image_width // COLS
        self.TITLE_HEIGHT = self.image_height // ROWS

        self.tiles = []

        for i in range(ROWS):
            for j in range(COLS):
                self.rect = pygame.Rect(j * self.TITLE_WIDTH, i * self.TITLE_HEIGHT, self.TITLE_WIDTH,
                                        self.TITLE_HEIGHT)
                self.tile = self.image.subsurface(self.rect)
                self.tiles.append(self.tile)

        self.origin_tiles = self.tiles.copy()
        random.shuffle(self.tiles)

        self.selected = None

SCREEN_WIDTH = 800
SCREEN_HEIGHT = 800
size = (SCREEN_WIDTH , SCREEN_HEIGHT)
screen = pygame.display.set_mode((SCREEN_WIDTH , SCREEN_HEIGHT))
pygame.display.set_caption("kapcha")
BACKGROUND = (colors.GREEN)
screen.fill(BACKGROUND)
FPS = 60
clock = pygame.time.Clock()

ROWS = 4
COLS = 4
MARGIN = 2

# pictures = os.listdir('pictures')
# picture = random.choice(pictures)
# image = pygame.image.load('pictures/' + picture)
# image_width , image_height = image.get_size()
#
# TITLE_WIDTH = image_width//COLS
# TITLE_HEIGHT = image_height//ROWS
#
# tiles = []
#
# for i in range(ROWS):
#     for j in range(COLS):
#         rect = pygame.Rect( j * TITLE_WIDTH, i * TITLE_HEIGHT, TITLE_WIDTH, TITLE_HEIGHT)
#         tile = image.subsurface(rect)
#         tiles.append(tile)
#
# origin_tiles = tiles.copy()
# random.shuffle(tiles)

selected = None



player_name = "АНОНИМ"
font = pygame.font.SysFont(None , 64)
state = SplashScreen()
#state = MenuScreen()

running = True
while running:
    events = pygame.event.get()
    state = state.handle_events(events)
    state.update()
    state.draw(screen)

#основная логика
#отрисовка обЪектов
    pygame.display.flip()
    clock.tick(FPS)