import pygame
import sys
from config import *

# Инициализация Pygame
pygame.init()

# Создание экрана
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Убей мой блок")

title_menu = pygame.image.load(TITLE_IMG).convert_alpha()
button_add = pygame.image.load(BUTTON_ADD).convert_alpha()

class Button:
    """
    Класс, представляющий кнопку в пользовательском интерфейсе. 
    Он содержит методы для отображения кнопки на экране, проверки нажатия на кнопку.
    """

    def __init__(self, x, y, image, text="", hover_color=(255,255,255)):
        self.image = image
        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)
        self.text = text
        self.hovered = False
        self.hover_image = self.image.copy()
        
    def draw(self):
        screen.blit(self.image, (self.rect.x, self.rect.y))
        
    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)
    
# Создание класса для пола
class Floor(pygame.sprite.Sprite):
    def __init__(self, color, width, height, xpos, ypos):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = xpos
        self.rect.y = ypos

# Создание класса для блоков
class Block(pygame.sprite.Sprite):
    """
    Класс, представляющий блок (квадрат) физически и в пользовательском интерфейсе. 
    Он содержит один основной метод для обновления блока (отрисовка, состояния, жизни).
    """


    def __init__(self, color, width, height, x, y, bounce, max_health):
        super().__init__()
        self.image = pygame.Surface([width, height])
        self.original_image = self.image.copy()
        self.image.fill(color)
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.velocity = pygame.math.Vector2(0, 0)
        self.gravity = 0.1  # Гравитация
        self.bounce = bounce  # Коэффициент столкновения
        self.dragging = False  # Переменная, определяющая, можно ли поднимать блок
        self.taken = False  # Переменная, определяющая, взят ли блок
        self.health = max_health  # Жизни блока
        self.max_health = max_health  # Максимальное количество жизней
        self.hit_strength = 0  # Сила удара

    def update(self, floor, lava, blocks):
        if self.dragging:
            self.rect.center = pygame.mouse.get_pos()
        else:
            self.velocity.y += self.gravity
            self.rect.move_ip(self.velocity)

            # Проверка столкновения с полом
            if self.rect.colliderect(floor.rect):
                self.rect.bottom = floor.rect.top
                self.hit_strength = abs(self.velocity.y)
                self.velocity.y *= -self.bounce  # Отскок от пола

            # Проверка столкновения с лавой
            if self.rect.colliderect(lava.rect):
                self.health -= 1
                if self.health <= 0:
                    self.kill()
                else:
                    # Изменение цвета в зависимости от количества жизней
                    self.image = pygame.Surface([self.rect.width, self.rect.height])
                    color = YELLOW if self.health > self.max_health // 2 else RED
                    self.image.fill(color)
                    self.rect = self.image.get_rect(center=self.rect.center)

                    # Проверка разделения блока на две части
                    if self.rect.width > 10 and len(blocks) < 8:
                        new_width = self.rect.width // 2
                        new_height = self.rect.height // 2
                        new_x = self.rect.x + new_width // 2
                        new_y = self.rect.y + new_height // 2
                        # Создание новых блоков
                        block1 = Block(color, new_width, new_height, new_x, new_y, self.bounce, self.max_health // 2)
                        block2 = Block(color, new_width, new_height, self.rect.x, self.rect.y, self.bounce, self.max_health // 2)
                        blocks.add(block1, block2)
                        all_sprites.add(block1, block2)
                        self.kill()

# Создание всех спрайтов и групп спрайтов
all_sprites = pygame.sprite.Group()
blocks = pygame.sprite.Group()
floor = Floor(BLACK, WIDTH, 20, 0, HEIGHT - 20)
lava = Floor(RED, WIDTH//2, 30, 0, HEIGHT - 30)
for i in range(3):
    block = Block(YELLOW, 50, 50, 100 + i * 200, 200, 0.5, 1000)  # Устанавливаем коэффициент столкновения для блоков
    all_sprites.add(block)
    blocks.add(block)
all_sprites.add(floor, lava)

# Создание объекта Clock для управления частотой кадров
clock = pygame.time.Clock()

# Создание кнопок
buttons = [
    Button(751, 64, button_add),
    Button(196, 17, title_menu)
]

# Основной игровой цикл
running = True
while running:
    # Обработка событий
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.MOUSEBUTTONDOWN:
            # При нажатии кнопки мыши, проверяем попадание в кнопку и добавляем новый блок
            if buttons[0].is_clicked(event.pos):
                new_block = Block(YELLOW, 50, 50, WIDTH // 2, 50, 0.5, 1000)
                all_sprites.add(new_block)
                blocks.add(new_block)
            else:
                # Если нажатие произошло не на кнопке, проверяем попадание в блоки
                for block in blocks:
                    if block.rect.collidepoint(event.pos):
                        block.dragging = True
                        block.taken = True
        elif event.type == pygame.MOUSEMOTION:  # Обработка движения мыши
            # Перемещение блоков, если они подняты
            for block in blocks:
                if block.dragging:
                    block.rect.center = pygame.mouse.get_pos()
        elif event.type == pygame.MOUSEBUTTONUP:  # Обработка отпускания кнопки мыши
            # Опускание блоков после их перетаскивания
            for block in blocks:
                if block.dragging:
                    block.dragging = False
                    block.taken = False
                    pygame.mouse.set_cursor(*pygame.cursors.broken_x)
                else:
                    pygame.mouse.set_cursor(*pygame.cursors.arrow)


    screen.fill(WHITE)
    # Обновление всех спрайтов
    all_sprites.update(floor, lava, blocks)

    for button in buttons:
        button.draw()

    # Отрисовка всех спрайтов
    all_sprites.draw(screen)

    # Отображение всех изменений на экране
    pygame.display.flip()

    # Ограничение частоты кадров
    clock.tick(60)

pygame.quit()
sys.exit()
