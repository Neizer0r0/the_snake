from random import choice, randint
import sys

import pygame as pg

# Константы для размеров поля и сетки:
SCREEN_WIDTH, SCREEN_HEIGHT = 640, 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Направления движения:
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Кортеж всех направлений движения:
list_direction = (UP, DOWN, LEFT, RIGHT)

# Цвет фона - черный:
BOARD_BACKGROUND_COLOR = (0, 0, 0)

# Цвет границы ячейки
BORDER_COLOR = (93, 216, 228)

# Цвет яблока
APPLE_COLOR = (255, 0, 0)

# Цвет змейки
SNAKE_COLOR = (0, 255, 0)

# Скорость движения змейки:
SPEED = 8

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для Змейки и Яблока"""

    def __init__(self, body_color=None):
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = body_color

    def draw(self):
        """Метод отрисовки родительского класса"""
        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)


class Apple(GameObject):
    """Класс создания Яблока"""

    def __init__(self, body_color=None):
        super().__init__(body_color)
        self.body_color = APPLE_COLOR
        self.position = None

    def randomize_position(self, snake_positions):
        """Метод создания рандомных координат для яблока на игровом поле"""
        while True:
            self.position = (
                randint(0, ((SCREEN_WIDTH - 1) // GRID_SIZE)) * GRID_SIZE,
                randint(0, ((SCREEN_HEIGHT - 1) // GRID_SIZE)) * GRID_SIZE
            )

            if self.position not in (
                    (SCREEN_WIDTH // 2),
                    (SCREEN_HEIGHT // 2)
            ):
                if self.position not in snake_positions:
                    break

    def draw(self):
        """Метод отрисовки яблока"""
        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс создания Змейки"""

    def __init__(self, body_color=None):
        super().__init__(body_color)
        self.reset()
        self.next_direction = None
        self.body_color = SNAKE_COLOR
        self.last = None

    def update_direction(self):
        """Метод для смены движения головы змейки"""
        if self.next_direction:
            self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Метод определения движения и увеличения змейки"""
        head_x, head_y = self.get_head_position()
        head_x = (
            (head_x + self.direction[0] * GRID_SIZE) % SCREEN_WIDTH)
        head_y = (
            (head_y + self.direction[1] * GRID_SIZE) % SCREEN_HEIGHT)
        self.positions.insert(0, (head_x, head_y))
        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""
        rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)
        # Затирание последнего сегмента
        if self.last:
            last_rect = pg.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)

    def get_head_position(self):
        """Метод получения координат головы змейки"""
        return self.positions[0]

    def reset(self):
        """Метод сбрасывания змейки в начальное состояние"""
        self.length = 1
        self.positions = [(self.position)]
        self.direction = choice(list_direction)


def handle_keys(game_object):
    """Метод считывания и обработки ввода пользователя"""
    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise sys.exit
        elif event.type == pg.KEYDOWN:
            if event.key == pg.K_UP and game_object.direction != DOWN:
                game_object.next_direction = UP
            elif event.key == pg.K_DOWN and game_object.direction != UP:
                game_object.next_direction = DOWN
            elif event.key == pg.K_LEFT and game_object.direction != RIGHT:
                game_object.next_direction = LEFT
            elif event.key == pg.K_RIGHT and game_object.direction != LEFT:
                game_object.next_direction = RIGHT


def main():
    """Инициализация игры"""
    pg.init()

    snake = Snake()
    apple = Apple()
    apple.randomize_position(snake.positions)
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position(snake.positions)

        if snake.get_head_position() in snake.positions[4:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)
            apple.randomize_position(snake.positions)

        snake.draw()
        apple.draw()
        pg.display.update()


if __name__ == '__main__':
    main()
