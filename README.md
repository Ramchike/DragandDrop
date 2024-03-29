![Pygame](https://www.leixue.com/uploads/2019/07/Pygame.png)
# Описание игры

"Убей мой блок" - это простая физическая игра, в которой игроку предоставляется возможность создавать и уничтожать блоки. Цель игры заключается в том, чтобы использовать физические законы для уничтожения блоков и создания новых структур.

# Возможности игрока

- **Добавлять блоки:** Нажимая на кнопку "Добавить блок", игрок может создавать новые блоки на экране. Эти блоки могут быть различных размеров, цветов и иметь разные свойства.

- **Перемещать блоки:** Используя мышь, игрок может перетаскивать блоки по экрану, чтобы располагать их в нужном месте.

- **Уничтожать блоки:** Блоки могут взаимодействовать с полом и лавой. Если блок сталкивается с полом, он отскакивает от него. Если блок падает в лаву он теряет здоровье, затем распадается на еще одни блоки в конце уничтожается.

# **Документация к игре**

## 1. **Классы:**
   - `Button`: Класс, представляющий кнопку в пользовательском интерфейсе.
   - `Floor`: Класс, представляющий пол на экране игры.
   - `Block`: Класс, представляющий блок на экране игры.

## 2. **Методы:**
   - `Button.__init__(self, x, y, image, text="", hover_color=(255,255,255))`: Инициализирует кнопку с заданными координатами, изображением, текстом и цветом при наведении.
   - `Button.draw(self)`: Отображает кнопку на экране.
   - `Button.is_clicked(self, pos)`: Проверяет, была ли нажата кнопка в указанных координатах.
   - `Floor.__init__(self, color, width, height, xpos, ypos)`: Инициализирует пол с заданными параметрами.
   - `Block.__init__(self, color, width, height, x, y, bounce, max_health)`: Инициализирует блок с заданными параметрами.
   - `Block.update(self, floor, lava, blocks)`: Обновляет состояние блока на основе его взаимодействия с полом и лавой.

## 3. **Переменные:**
   - `screen`: Переменная, представляющая экран игры.
   - `all_sprites`: Группа спрайтов, содержащая все спрайты на экране.
   - `blocks`: Группа спрайтов, содержащая все блоки на экране.
   - `floor`: Обьект класса `Floor`, представляющий пол на экране.
   - `lava`: Обьект класса `Floor`, представляющий лаву на экране.
   - `buttons`: Список объектов класса `Button`, представляющих кнопки на экране.

## 4. **Главный игровой цикл:**
   - Обработка событий: проверка нажатий кнопок мыши, перемещение блоков.
   - Обновление всех спрайтов.
   - Отрисовка всех спрайтов и кнопок на экране.
   - Отображение изменений на экране.
   - Ограничение частоты кадров.
