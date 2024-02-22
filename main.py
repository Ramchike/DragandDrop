import pygame
import sys

# Инициализация Pygame
pygame.init()

# Определение констант для цветов
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Определение размеров окна
WIDTH, HEIGHT = 800, 600

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("физика дерьма")

# Создание класса для пола
class Floor(pygame.sprite.Sprite):
    def __init__(self, color, width, height):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = 0
        self.rect.y = HEIGHT - height

# Создание класса для блоков
class Block(pygame.sprite.Sprite):
    def __init__(self, color, width, height, x, y, bounce):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.1  # Гравитация
        self.bounce = bounce  # Коэффициент столкновения
        self.dragging = False  # Переменная, определяющая, можно ли поднимать блок
        self.taken = False  # Переменная, определяющая, взят ли блок

    def update(self, floor, blocks):
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.velocity.y += self.gravity
            self.rect.move_ip(self.velocity)
            # Проверка столкновения с полом
            if self.rect.colliderect(floor.rect):
                self.rect.bottom = floor.rect.top
                self.velocity.y *= -self.bounce  # Отскок от пола

            # Проверка столкновений с другими блоками
            for block in blocks:
                if block != self and self.rect.colliderect(block.rect):
                    # Если произошло столкновение, отменяем перемещение и применяем коэффициент столкновения
                    self.rect.x -= self.velocity.x
                    self.rect.y -= self.velocity.y
                    self.velocity.x *= self.bounce
                    self.velocity.y *= self.bounce
                    break

# Создание всех спрайтов и групп спрайтов
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
floor = Floor(BLACK, WIDTH, 20)
for i in range(3):
    block = Block(BLACK, 50, 50, 100 + i * 200, 200, 0.5)  # Устанавливаем коэффициент столкновения для блоков
    all_sprites.add(block)
    blocks.add(block)
all_sprites.add(floor)

# Создание объекта Clock для управления частотой кадров
clock = pygame.time.Clock()

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # При нажатии кнопки мыши, поднимаем блок, если курсор находится над ним
            for block in blocks:
                if block.rect.collidepoint(event.pos) and not block.dragging:
                    block.dragging = True
                    pygame.mouse.set_cursor(*pygame.cursors.tri_left)
                    block.taken = True
        elif event.type == pygame.MOUSEBUTTONUP:
            # При отпускании кнопки мыши, опускаем блок
            for block in blocks:
                block.dragging = False
                block.taken = False
                pygame.mouse.set_cursor(*pygame.cursors.arrow)

    # Проверка наведения на блок и смена курсора
    for block in blocks:
        if block.rect.collidepoint(pygame.mouse.get_pos()) and not block.taken:
            pygame.mouse.set_cursor(*pygame.cursors.broken_x)
            break
    else:
        pygame.mouse.set_cursor(*pygame.cursors.arrow)

    # Обновление всех спрайтов
    all_sprites.update(floor, blocks)

    # Очистка экрана
    screen.fill(WHITE)

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Отображение всех изменений на экране
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(60)

# Завершение Pygame
pygame.quit()
sys.exit()
