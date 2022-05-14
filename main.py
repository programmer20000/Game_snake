import pygame
import random
from time import sleep

pygame.init()

WIDTH_WINDOW = (600)
HEIGHT_WINDOW = (600)
TITLE_WINDOW = "GAME SNAKE"
BACKGROUND_COLOR_WINDOW = (0, 0, 0)
SNAKE_COLOR = (0, 255, 89)
APPLE_COLOR = (255, 40, 47)
SCORE_COLOR = (255, 255, 255)
head_size = 22
font = pygame.font.SysFont("Arial", 40)
position_head_x = 0
position_head_y = 0
snake = [[position_head_x, position_head_y], (300, 300)]
score = 0
FPS = 20
background_image = pygame.image.load("background_image/background_image.png")

screen = pygame.display.set_mode([WIDTH_WINDOW, HEIGHT_WINDOW])
pygame.display.set_caption(TITLE_WINDOW)

pygame.mixer.music.load("music/Snake Game - Theme Song.mp3")
pygame.mixer.music.play(-1)


class Player(pygame.sprite.Sprite):
    def __init__(self, width, height, color):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color=color)
        self.rect = self.image.get_rect()

        self.length = 0
        self.speed = 10

        self.x, self.y = 0, 0

    def position(self, position_head_x, position_head_y):
        self.rect.x = position_head_x
        self.rect.y = position_head_y

    def movement_player(self, x_direction, y_direction):
        self.rect.x += x_direction * self.speed
        self.rect.y += y_direction * self.speed

    def snake_tails(self):
        snake.append([self.rect.x, self.rect.y])

    def draw_tails(self):
        if len(snake) > self.length:
            del snake[0]
        for i in snake:
            pygame.draw.rect(screen, SNAKE_COLOR, (i[0], i[1], head_size, head_size))

    def update(self):
        snake.append([self.rect.x, self.rect.y])
        self.draw_tails()
        self.movement_player(self.x, self.y)
        pygame.display.update()


class Food(Player):
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

Close_Window = False
clock = pygame.time.Clock()

while not Close_Window:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            Close_Window = True

    if player.rect.x > WIDTH_WINDOW or player.rect.y > HEIGHT_WINDOW:
        pygame.mixer.music.load("music/music_by_game_over.mp3")
        pygame.mixer.music.play(0)
        sleep(1)
        Close_Window = True

    screen.fill(BACKGROUND_COLOR_WINDOW)
    screen.blit(background_image, [0, 0])
    all_sprites_group.draw(screen)
    all_sprites_group.update()

    key_pressed = pygame.key.get_pressed()

    if key_pressed[pygame.K_UP]:
        player.x = 0
        player.y = -1

    if key_pressed[pygame.K_DOWN]:
        player.x = 0
        player.y = 1

    if key_pressed[pygame.K_RIGHT]:
        player.x = 1
        player.y = 0

    if key_pressed[pygame.K_LEFT]:
        player.x = -1
        player.y = 0

    if key_pressed[pygame.K_w]:
        player.x = -1
        player.y = 0

    if key_pressed[pygame.K_a]:
        player.x = 0
        player.y = 1

    if key_pressed[pygame.K_s]:
        player.x = 1
        player.y = 0
    if key_pressed[pygame.K_d]:
        player.x = -1
        player.y = 0

    if key_pressed[pygame.K_ESCAPE]:
        Close_Window = True

    sprites_collision = pygame.sprite.spritecollide(player, sprites_group, False)
    if food in sprites_collision:
        player.snake_tails()
        player.length += 1
        score += 1
        food.random_position()

    show_score = font.render("Score:" + str(score), True, SCORE_COLOR)
    screen.blit(show_score, [220, 0])
    show_score = font.render("length:" + str(player.length), True, SCORE_COLOR)
    screen.blit(show_score, [10, 0])
    pygame.display.update()
    clock.tick(FPS)
