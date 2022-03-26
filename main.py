import pygame
import random

pygame.init()

WIDTH_WINDOW = 600
HEIGHT_WINDOW = 600
TITLE_WINDOW = "GAME SNAKE"
BACKGROUND_COLOR_WINDOW = (0, 0, 0)
SNAKE_COLOR = (0, 255, 89)
APPLE_COLOR = (255, 40, 47)
SCORE_COLOR = (255, 255, 255)
head_size = 50
font = pygame.font.SysFont("Arial", 50)
position_head_x = 0
position_head_y = 0
snake = [(position_head_x,position_head_y)]
score = 0
FPS = 60

screen = pygame.display.set_mode([WIDTH_WINDOW, HEIGHT_WINDOW])
pygame.display.set_caption(TITLE_WINDOW)


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color=color)
        self.rect = self.image.get_rect()

    def position(self, position_head_x, position_head_y):
        self.rect.x = position_head_x
        self.rect.y = position_head_y

    def movement_player(self, x_direction, y_direction):
        self.rect.x += x_direction
        self.rect.y += y_direction

    def update(self):
        self.rect.x += 1



class Food(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color=color)
        self.rect = self.image.get_rect()

    def random_position(self):
        self.rect.x = random.randrange(WIDTH_WINDOW - 100)
        self.rect.y = random.randrange(HEIGHT_WINDOW - 100)


sprites_group = pygame.sprite.Group()
all_sprites_group = pygame.sprite.Group()

food = Food(width=head_size, height=head_size, color=APPLE_COLOR)
food.random_position()
sprites_group.add(food)
all_sprites_group.add(food)

player = Player(width=head_size, height=head_size, color=SNAKE_COLOR)
player.position(position_head_x=position_head_x, position_head_y=position_head_y)
all_sprites_group.add(player)

def draw_snake_tail():
    [pygame.draw.rect(screen, SNAKE_COLOR, (block_x, block_y, head_size, head_size)) for block_x,block_y in snake]

Close_Window = False
clock = pygame.time.Clock()

while not Close_Window:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Close_Window = True
    screen.fill(BACKGROUND_COLOR_WINDOW)
    all_sprites_group.draw(screen)
    all_sprites_group.update()
    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_UP]:
        player.movement_player(0, -1)

    if key_pressed[pygame.K_DOWN]:
        player.movement_player(0, 1)

    if key_pressed[pygame.K_RIGHT]:
        player.movement_player(1, 0)

    if key_pressed[pygame.K_LEFT]:
        player.movement_player(-1, 0)

    if key_pressed[pygame.K_w]:
        player.movement_player(0, -1)

    if key_pressed[pygame.K_a]:
        player.movement_player(0, 1)

    if key_pressed[pygame.K_s]:
        player.movement_player(1, 0)
    if key_pressed[pygame.K_d]:
        player.movement_player(-1, 0)

    sprites_collision = pygame.sprite.spritecollide(player, sprites_group, False)
    if food in sprites_collision:
        score += 1
        food.random_position()
        draw_snake_tail()
        pygame.display.flip()

    show_score = font.render("Score:" + str(score), True, SCORE_COLOR)
    screen.blit(show_score,[220,0])
    pygame.display.update()
    clock.tick(FPS)