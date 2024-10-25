from random import choice, randint
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
SPEED = 12

# Настройка игрового окна:
screen = pg.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT), 0, 32)

# Заголовок окна игрового поля:
pg.display.set_caption('Змейка')

# Настройка времени:
clock = pg.time.Clock()


class GameObject:
    """Родительский класс для Змейки и Яблока"""

    def __init__(self) -> None:
        self.position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.body_color = None

    def draw(self):
        pass


class Apple(GameObject):
    """Класс создания Яблока"""

    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.position = self.randomize_position()

    def randomize_position(self):
        """Метод создания рандомных координат для яблока на игровом поле"""

        self.position = (
            randint(0, ((SCREEN_WIDTH - 1) // 20)) * GRID_SIZE,
            randint(0, ((SCREEN_HEIGHT - 1) // 20)) * GRID_SIZE
        )

        if self.position not in ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2)):
            return self.position

    def draw(self):
        """Метод отрисовки яблока"""

        rect = pg.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, rect)
        pg.draw.rect(screen, BORDER_COLOR, rect, 1)


class Snake(GameObject):
    """Класс создания Змейки"""

    def __init__(self):
        super().__init__()
        self.length = 1
        self.positions = [(self.position)]
        self.direction = choice(list_direction)
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

        now_position = self.get_head_position()
        if self.direction == RIGHT:
            if now_position[0] > SCREEN_WIDTH:
                self.positions.insert(0, (0, self.get_head_position()[1]))

            else:
                new_posiotion_head = (
                    (now_position[0] + GRID_SIZE),
                    now_position[1]
                )
                self.positions.insert(0, new_posiotion_head)

        elif self.direction == LEFT:
            if now_position[0] < 0:
                self.positions.insert(0, (620, self.get_head_position()[1]))

            else:
                new_posiotion_head = (
                    (now_position[0] - GRID_SIZE),
                    now_position[1]
                )
                self.positions.insert(0, new_posiotion_head)

        elif self.direction == DOWN:
            if now_position[1] > SCREEN_HEIGHT:
                self.positions.insert(0, (self.get_head_position()[0], 0))

            else:
                new_posiotion_head = (
                    now_position[0],
                    (now_position[1] + GRID_SIZE)
                )
                self.positions.insert(0, new_posiotion_head)

        elif self.direction == UP:
            if now_position[1] < 0:
                self.positions.insert(0, (self.get_head_position()[0], 480))

            else:
                new_posiotion_head = (
                    now_position[0],
                    (now_position[1] - GRID_SIZE)
                )
                self.positions.insert(0, new_posiotion_head)

        if len(self.positions) > self.length:
            self.last = self.positions[-1]
            self.positions.pop()

    def draw(self):
        """Метод отрисовки змейки на игровом поле"""

        for position in self.positions[:-1]:
            rect = pg.Rect(position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, self.body_color, rect)
            pg.draw.rect(screen, BORDER_COLOR, rect, 1)

        # Отрисовка головы змейки
        head_rect = pg.Rect(self.positions[0], (GRID_SIZE, GRID_SIZE))
        pg.draw.rect(screen, self.body_color, head_rect)
        pg.draw.rect(screen, BORDER_COLOR, head_rect, 1)
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
        while self.positions:
            self.positions.pop()
        self.positions.append(self.position)
        self.direction


def handle_keys(game_object):
    """Метод считывания и обработки ввода пользователя"""

    for event in pg.event.get():
        if event.type == pg.QUIT:
            pg.quit()
            raise SystemExit
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

    apple = Apple()
    snake = Snake()
    while True:
        clock.tick(SPEED)
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        apple.draw()
        snake.draw()

        if snake.get_head_position() == apple.position:
            snake.length += 1
            last_rect = pg.Rect(apple.position, (GRID_SIZE, GRID_SIZE))
            pg.draw.rect(screen, BOARD_BACKGROUND_COLOR, last_rect)
            apple.randomize_position()

        if snake.get_head_position() in snake.positions[1:]:
            snake.reset()
            screen.fill(BOARD_BACKGROUND_COLOR)

        pg.display.update()


if __name__ == '__main__':
    main()
