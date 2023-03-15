import sys
import pygame
import random

pygame.init()

# Screen dimensions and colors
WIDTH, HEIGHT = 800, 600
BACKGROUND_COLOR = (0, 0, 0)

# Grid dimensions
GRID_WIDTH, GRID_HEIGHT = 10, 20
GRID_CELL_SIZE = 25

# Tetromino colors and shapes
TETROMINO_COLORS = [
    (255, 0, 0),
    (0, 255, 0),
    (0, 0, 255),
    (255, 255, 0),
    (255, 0, 255),
    (0, 255, 255),
    (127, 127, 127),
]

TETROMINO_SHAPES = [
    [
        "1100",
        "1100",
    ],
    [
        "1000",
        "1000",
        "1100",
    ],
    [
        "0100",
        "0100",
        "1100",
    ],
    [
        "1000",
        "1100",
        "0100",
    ],
    [
        "0100",
        "1100",
        "1000",
    ],
    [
        "1100",
        "0110",
    ],
    [
        "0110",
        "1100",
    ],
]


# Tetromino class
class Tetromino:
    def __init__(self, x, y):
        self.x = x
        self.y = y
        self.shape = random.choice(TETROMINO_SHAPES)
        self.color = random.choice(TETROMINO_COLORS)

    def draw(self, screen):
        for y, row in enumerate(self.shape):
            for x, cell in enumerate(row):
                if cell == "1":
                    pygame.draw.rect(screen, self.color, (
                    (self.x + x) * GRID_CELL_SIZE, (self.y + y) * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))


def valid_move(tetromino, grid, x_offset=0, y_offset=0):
    for y, row in enumerate(tetromino.shape):
        for x, cell in enumerate(row):
            if cell == "1":
                new_x = tetromino.x + x + x_offset
                new_y = tetromino.y + y + y_offset

                if new_x < 0 or new_x >= GRID_WIDTH or new_y >= GRID_HEIGHT or grid[new_y][new_x]:
                    return False
    return True

# Game loop
def game_loop(screen):
    clock = pygame.time.Clock()

    grid = [[None for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
    tetromino = Tetromino(GRID_WIDTH // 2 - 2, 0)

    while True:
        screen.fill(BACKGROUND_COLOR)

        # Draw border
        pygame.draw.rect(screen, (255, 255, 255), (0, 0, GRID_WIDTH * GRID_CELL_SIZE, GRID_HEIGHT * GRID_CELL_SIZE), 2)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            # Arrow key controls
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT and valid_move(tetromino, grid, x_offset=-1):
                    tetromino.x -= 1
                elif event.key == pygame.K_RIGHT and valid_move(tetromino, grid, x_offset=1):
                    tetromino.x += 1
                elif event.key == pygame.K_DOWN and valid_move(tetromino, grid, y_offset=1):
                    tetromino.y += 1

        if valid_move(tetromino, grid, y_offset=1):
            tetromino.y += 1
        else:
            for y, row in enumerate(tetromino.shape):
                for x, cell in enumerate(row):
                    if cell == "1":
                        grid[tetromino.y + y][tetromino.x + x] = tetromino.color
            tetromino = Tetromino(GRID_WIDTH // 2 - 2, 0)

        # Draw grid
        for y, row in enumerate(grid):
            for x, cell in enumerate(row):
                if cell:
                    pygame.draw.rect(screen, cell,
                                     (x * GRID_CELL_SIZE, y * GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE))

        # Draw tetromino
        tetromino.draw(screen)

        pygame.display.flip()
        clock.tick(2)

if __name__ == "__main__":
    screen = pygame.display.set_mode((WIDTH, HEIGHT))
    pygame.display.set_caption("Simple Tetris-like Game")
    game_loop(screen)

