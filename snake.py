"""
Snake game implementation using Pygame.
"""
import random
import pygame
from pygame.locals import (  # type: ignore
    K_UP, K_DOWN, K_LEFT, K_RIGHT, QUIT, KEYDOWN
)

# Game constants
SCREEN_WIDTH = 640
SCREEN_HEIGHT = 480
GRID_SIZE = 20
GRID_WIDTH = SCREEN_WIDTH // GRID_SIZE
GRID_HEIGHT = SCREEN_HEIGHT // GRID_SIZE

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

# Colors
BOARD_BACKGROUND_COLOR = (0, 0, 0)
SNAKE_COLOR = (0, 255, 0)
APPLE_COLOR = (255, 0, 0)
WHITE = (255, 255, 255)


class GameObject:
    """Base class for game objects."""

    def __init__(self, position=None, body_color=None):
        """Initialize game object.
        
        Args:
            position: Starting position of object
            body_color: Color of object
        """
        if position is None:
            position = ((SCREEN_WIDTH // 2), (SCREEN_HEIGHT // 2))
        self.position = position
        self.body_color = body_color

    def draw(self, surface):
        """Draw object on surface.
        
        Args:
            surface: Surface to draw on
        """
        pass


class Apple(GameObject):
    """Apple class - target for snake."""

    def __init__(self):
        """Initialize apple with random position."""
        super().__init__()
        self.body_color = APPLE_COLOR
        self.randomize_position()

    def randomize_position(self):
        """Set random position for apple."""
        x = random.randint(0, GRID_WIDTH - 1) * GRID_SIZE
        y = random.randint(0, GRID_HEIGHT - 1) * GRID_SIZE
        self.position = (x, y)

    def draw(self, surface):
        """Draw apple on surface.
        
        Args:
            surface: Surface to draw on
        """
        rect = pygame.Rect(self.position, (GRID_SIZE, GRID_SIZE))
        pygame.draw.rect(surface, self.body_color, rect)
        pygame.draw.rect(surface, WHITE, rect, 1)


class Snake(GameObject):
    """Snake class - player character."""

    def __init__(self):
        """Initialize snake."""
        super().__init__()
        self.body_color = SNAKE_COLOR
        self.reset()

    def reset(self):
        """Reset snake to initial state."""
        self.length = 1
        center_x = (SCREEN_WIDTH // 2) // GRID_SIZE * GRID_SIZE
        center_y = (SCREEN_HEIGHT // 2) // GRID_SIZE * GRID_SIZE
        self.positions = [(center_x, center_y)]
        self.direction = RIGHT
        self.next_direction = None
        self.last = None

    def get_head_position(self):
        """Get position of snake's head.
        
        Returns:
            tuple: Head position coordinates
        """
        return self.positions[0]

    def update_direction(self):
        """Update snake's movement direction."""
        if self.next_direction:
            # Prevent moving in opposite direction
            opposite_direction = (
                self.next_direction[0] * -1,
                self.next_direction[1] * -1
            )
            if opposite_direction != self.direction:
                self.direction = self.next_direction
            self.next_direction = None

    def move(self):
        """Move snake one step forward."""
        self.last = self.positions[-1] if self.positions else None
        head = self.get_head_position()
        x, y = head
        dx, dy = self.direction
        new_x = (x + dx * GRID_SIZE) % SCREEN_WIDTH
        new_y = (y + dy * GRID_SIZE) % SCREEN_HEIGHT
        new_head = (new_x, new_y)

        # Check collision with self
        if new_head in self.positions[:-1]:
            self.reset()
            return

        self.positions.insert(0, new_head)
        if len(self.positions) > self.length:
            self.positions.pop()

    def draw(self, surface):
        """Draw snake on surface.
        
        Args:
            surface: Surface to draw on
        """
        if self.last:
            last_rect = pygame.Rect(self.last, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, BOARD_BACKGROUND_COLOR, last_rect)

        for position in self.positions:
            rect = pygame.Rect(position, (GRID_SIZE, GRID_SIZE))
            pygame.draw.rect(surface, self.body_color, rect)
            pygame.draw.rect(surface, WHITE, rect, 1)


def handle_keys(snake):
    """Handle keyboard input for snake control.
    
    Args:
        snake: Snake object to control
    """
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
    """Main game function containing game loop."""
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    pygame.display.set_caption('Snake Game')
    snake = Snake()
    apple = Apple()
    base_speed = 5

    while True:
        handle_keys(snake)
        snake.update_direction()
        snake.move()

        # Check apple collision
        if snake.get_head_position() == apple.position:
            snake.length += 1
            apple.randomize_position()
            # Ensure apple doesn't spawn on snake
            while apple.position in snake.positions:
                apple.randomize_position()
            # Increase speed
            if snake.length % 1 == 0:
                base_speed += 0.5

        screen.fill(BOARD_BACKGROUND_COLOR)
        snake.draw(screen)
        apple.draw(screen)
        pygame.display.update()
        clock.tick(base_speed)


if __name__ == '__main__':
    main()
