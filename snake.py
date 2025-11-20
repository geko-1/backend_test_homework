import pygame
import random
from pygame.locals import (
    K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, KEYDOWN
)

SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)


class GameObject:
    def __init__(self, position=None, body_color=None):
        if position is None:
            position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        pass


class Apple(GameObject):
    def __init__(self):
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)
    
    def draw(self, surface):
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, (255, 255, 255), rect, 1)


class Snake(GameObject):
    def __init__(self):
        super().__init__()    
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        self.length = 1
        center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None
    
    def get_head_position(self):
        return self.positions[0]
    
    def update_direction(self):
        if self.next_direction:
            if ((self.next_direction[0] * -1, self.next_direction[1] * -1)
                    != self.direction):
                self.direction = self.next_direction
            self.next_direction = None
    
    def move(self):
        self.last = self.positions[-1] if self.positions else None
        head = self.get_head_position()
        x, y = head 
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)
        if new_head in self.positions[:-1]:
            self.reset()
            return 
        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()
    
    def draw(self, surface):
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)
        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, (255, 255, 255), rect, 1)


def handle_keys(snake):
    for event in pygame.event.get():
        if event.type == QUIT:
            pygame.quit()
            exit()
        elif event.type == KEYDOWN:
            if event.key == K_UP:
                snake.next_direction = UP
            elif event.key == K_DOWN:
                snake.next_direction = DOWN
            elif event.key == K_LEFT:
                snake.next_direction = LEFT
            elif event.key == K_RIGHT:
                snake.next_direction = RIGHT


def main():
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Изгиб Питона')
    snake = Snake()
    apple = Apple()
    base_speed = 5
    
    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()
        
        if snake.get_head_position() == apple.position:
            snake.length += 1  
            apple.randomize_position() 
            while apple.position in snake.positions:
                apple.randomize_position()
            if snake.length % 1 == 0:
                base_speed += 0.5
                
        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(base_speed)


if __name__ == '__main__':
    main()
