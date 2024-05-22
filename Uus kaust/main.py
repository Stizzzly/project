import pygame
import random

pygame.init()

WIDTH = 1268
HEIGHT = 768
FPS = 30
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flying Plane")
clock = pygame.time.Clock()

plane1_image = pygame.transform.scale(pygame.image.load("plen1.png").convert_alpha(), (300, 100))
plane2_image = pygame.transform.scale(pygame.image.load("plen2.png").convert_alpha(), (300, 200))
arrow_image = pygame.transform.scale(pygame.image.load("arrow.png").convert_alpha(), (50, 50))
fon_image = pygame.transform.scale(pygame.image.load("fon.jpg").convert(), (WIDTH, HEIGHT))
start_image = pygame.transform.scale(pygame.image.load("start.jpg").convert(), (WIDTH, HEIGHT))
hangar_image = pygame.transform.scale(pygame.image.load("hangar.jpg").convert(), (WIDTH, HEIGHT))
game_over_image = pygame.image.load("finish.jpg")

class Plane(pygame.sprite.Sprite):
    def __init__(self, image):
        pygame.sprite.Sprite.__init__(self)
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.centerx = WIDTH // 4
        self.rect.centery = HEIGHT // 2
        self.speedy = 0

    def update(self):
        self.speedy = 0
        keystate = pygame.key.get_pressed()
        if keystate[pygame.K_UP]:
            self.speedy = -5
        if keystate[pygame.K_DOWN]:
            self.speedy = 5
        self.rect.y += self.speedy
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT

class Column(pygame.sprite.Sprite):
    def __init__(self, x, y, height):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.transform.scale(pygame.image.load("bashi.jpg").convert(), (50, height))
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.passed = False  # Flag to track if plane passed this column

    def update(self):
        self.rect.x -= 5
        if self.rect.right < 0:
            self.kill()

def select_plane():
    selected_plane = "plane1"
    arrow_x = WIDTH // 3  # Initial position of the arrow
    while True:
        screen.blit(hangar_image, (0, 0))
        plane1_rect = plane1_image.get_rect(center=(WIDTH // 3, HEIGHT // 2))
        plane2_rect = plane2_image.get_rect(center=(2 * WIDTH // 3, HEIGHT // 2))
        screen.blit(plane1_image, plane1_rect)
        screen.blit(plane2_image, plane2_rect)
        arrow_rect = arrow_image.get_rect(center=(arrow_x, HEIGHT // 2 - 100))  # Set arrow position
        screen.blit(arrow_image, arrow_rect)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RIGHT:
                    if selected_plane == "plane1":
                        selected_plane = "plane2"
                        arrow_x = 2 * WIDTH // 3  # Move arrow to the right plane
                elif event.key == pygame.K_LEFT:
                    if selected_plane == "plane2":
                        selected_plane = "plane1"
                        arrow_x = WIDTH // 3  # Move arrow to the left plane
                elif event.key == pygame.K_RETURN:
                    return selected_plane

def create_columns(column1_x, column2_x):
    column_gap = 259
    max_column_height = 600
    top_height_1 = random.randint(200, min(HEIGHT - column_gap - 200, max_column_height // 2))
    bottom_height_1 = min(HEIGHT - top_height_1 - column_gap, max_column_height // 2)
    top_height_2 = random.randint(200, min(HEIGHT - column_gap - 200, max_column_height // 2))
    bottom_height_2 = min(HEIGHT - top_height_2 - column_gap, max_column_height // 2)

    top_column_1 = Column(column1_x, 0, top_height_1)
    bottom_column_1 = Column(column1_x, HEIGHT - bottom_height_1, bottom_height_1)
    top_column_2 = Column(column2_x, 0, top_height_2)
    bottom_column_2 = Column(column2_x, HEIGHT - bottom_height_2, bottom_height_2)

    all_sprites.add(top_column_1)
    all_sprites.add(bottom_column_1)
    all_sprites.add(top_column_2)
    all_sprites.add(bottom_column_2)

    columns.add(top_column_1)
    columns.add(bottom_column_1)
    columns.add(top_column_2)
    columns.add(bottom_column_2)

all_sprites = pygame.sprite.Group()
columns = pygame.sprite.Group()
points = 0
plane = None
game_started = False
game_over = False

font = pygame.font.SysFont(None, 36)
title_font = pygame.font.SysFont(None, 72)

while True:
    clock.tick(FPS)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            quit()
        if event.type == pygame.KEYDOWN:
            if not game_started:
                if event.key == pygame.K_r:
                    plane_type = select_plane()
                    if plane_type == "plane1":
                        plane = Plane(plane1_image)
                    elif plane_type == "plane2":
                        plane = Plane(plane2_image)
                    all_sprites.add(plane)
                    game_started = True
                    game_over = False
                    points = 0
                    columns.empty()  # Clear all columns
                    all_sprites.empty()
                    all_sprites.add(plane)
            elif game_over and event.key == pygame.K_r:
                game_started = False  # Reset the game

    if not game_started:
        screen.blit(start_image, (0, 0))
        title_text = title_font.render("Flying Plane", True, WHITE)
        press_enter_text = font.render("Press R to start", True, WHITE)
        screen.blit(title_text, (WIDTH // 2 - title_text.get_width() // 2, HEIGHT // 3))
        screen.blit(press_enter_text, (WIDTH // 2 - press_enter_text.get_width() // 2, HEIGHT // 2))
        pygame.display.flip()
        continue

    if not game_over and len(columns) < 4:
        create_columns(WIDTH, WIDTH + 500)

    all_sprites.update()

    for column in columns:
        if pygame.sprite.collide_rect(plane, column):
            game_over = True
            break

    for column in columns:
        if column.rect.right < plane.rect.left and not column.passed:
            column.passed = True
            points += 1

    screen.blit(fon_image, (0, 0))
    all_sprites.draw(screen)
    if game_over:
        screen.blit(game_over_image, (WIDTH // 2 - game_over_image.get_width() // 2,
                                      HEIGHT // 2 - game_over_image.get_height() // 2))
        restart_text = font.render("Press R to restart", True, WHITE)
        screen.blit(restart_text, (WIDTH // 2 - restart_text.get_width() // 2, HEIGHT // 2 + 100))
    score_text = font.render("Points: " + str(points), True, WHITE)
    screen.blit(score_text, (WIDTH - score_text.get_width() - 10, 10))
    pygame.display.flip()
