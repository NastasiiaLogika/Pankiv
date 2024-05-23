import pygame
import random
import sys

# Ініціалізація Pygame
pygame.init()

# Колір
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Розміри екрану
WIDTH, HEIGHT = 800, 600

# Розмір і кількість дірок
NUM_HOLES_PER_ROW = 3
NUM_ROWS = 3
HOLE_SIZE = 100
HOLES_MARGIN_X = 50
HOLES_MARGIN_Y = 50

# Розмір бобра
BEAVER_SIZE = 80

# Розмір молотка
HAMMER_SIZE = 80

# Швидкість з'явлення бобра
BEAVER_SPEED = 1000

# Очки гравця
score = 0

# Створення екрану
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Whack-a-Beaver!")

# Завантаження зображень
background_img = pygame.image.load("background.jpg")
background_img = pygame.transform.scale(background_img, (WIDTH, HEIGHT))
beaver_img = pygame.image.load("beaver.png")
beaver_img = pygame.transform.scale(beaver_img, (BEAVER_SIZE, BEAVER_SIZE))
hammer_img = pygame.image.load("hammer.png")
hammer_img = pygame.transform.scale(hammer_img, (HAMMER_SIZE, HAMMER_SIZE))
hole_img = pygame.image.load("hole.png")
hole_img = pygame.transform.scale(hole_img, (HOLE_SIZE, HOLE_SIZE))

# Функція для відображення молотка
def display_hammer(x, y):
    screen.blit(hammer_img, (x - HAMMER_SIZE // 2, y - HAMMER_SIZE // 2))

# Функція для відображення дирки
def display_hole(x, y):
    screen.blit(hole_img, (x, y))

# Функція для визначення області, де можна клікати на бобра
def beaver_rect(x, y):
    return pygame.Rect(x, y, BEAVER_SIZE, BEAVER_SIZE)

# Функція для визначення, чи клікнули на бобра
def check_click_on_beaver(beaver_x, beaver_y, click_x, click_y):
    beaver_rect = pygame.Rect(beaver_x, beaver_y, BEAVER_SIZE, BEAVER_SIZE)
    return beaver_rect.collidepoint(click_x, click_y)

# Час, коли бобер з'явиться на іншому місці
next_beaver_time = pygame.time.get_ticks() + BEAVER_SPEED

# Приховання системного курсору миші
pygame.mouse.set_visible(False)

# Основний цикл гри
running = True
while running:
    screen.fill(WHITE)

    # Відображення фону
    screen.blit(background_img, (0, 0))

    # Обробка подій
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Обробка кліків миші
        if event.type == pygame.MOUSEBUTTONDOWN:
            click_x, click_y = pygame.mouse.get_pos()
            for hole_x, hole_y in holes:
                if hole_x <= click_x <= hole_x + HOLE_SIZE and hole_y <= click_y <= hole_y + HOLE_SIZE:
                    if 'beaver_x' in locals() and 'beaver_y' in locals():
                        if check_click_on_beaver(beaver_x, beaver_y, click_x, click_y):
                            score += 1
                            if score >= 25:
                                # Перемога
                                font = pygame.font.Font(None, 72)
                                win_text = font.render("You Win!", True, WHITE)
                                screen.blit(win_text, ((WIDTH - win_text.get_width()) // 2, (HEIGHT - win_text.get_height()) // 2))
                                pygame.display.flip()
                                pygame.time.wait(2000)  # Затримка на 2 секунди
                                running = False
                            else:
                                # Вибір нового місця для бобра
                                holes.remove((beaver_x - (HOLE_SIZE - BEAVER_SIZE) // 2, beaver_y - (HOLE_SIZE - BEAVER_SIZE) // 2))
                    else:
                        score -= 1

    # Вивід дірок на екран
    holes = []
    for i in range(NUM_ROWS):
        for j in range(NUM_HOLES_PER_ROW):
            hole_x = j * (WIDTH // NUM_HOLES_PER_ROW) + HOLES_MARGIN_X
            hole_y = i * (HEIGHT // NUM_ROWS) + HOLES_MARGIN_Y
            display_hole(hole_x, hole_y)
            holes.append((hole_x, hole_y))

    # Перевірка часу для появи нового бобра
    current_time = pygame.time.get_ticks()
    if current_time >= next_beaver_time:
        if holes:
            beaver_x, beaver_y = random.choice(holes)
            beaver_x += (HOLE_SIZE - BEAVER_SIZE) // 2
            beaver_y += (HOLE_SIZE - BEAVER_SIZE) // 2
            next_beaver_time = current_time + BEAVER_SPEED

    # Відображення бобра
    if 'beaver_x' in locals() and 'beaver_y' in locals():
        screen.blit(beaver_img, (beaver_x, beaver_y))

    # Відображення молотка
    display_hammer(*pygame.mouse.get_pos())

    # Відображення очків
    font = pygame.font.Font(None, 36)
    text = font.render("Score: " + str(score), True, WHITE)
    screen.blit(text, (10, 10))

    pygame.display.update()

pygame.quit()
sys.exit()