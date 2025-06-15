import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 30
GRID_WIDTH = 10
GRID_HEIGHT = 20
GRID_OFFSET_X = (WIDTH - GRID_WIDTH * GRID_SIZE) // 2
GRID_OFFSET_Y = (HEIGHT - GRID_HEIGHT * GRID_SIZE) // 2

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Tetris")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GRAY = (128, 128, 128)
CYAN = (0, 255, 255)
BLUE = (0, 0, 255)
ORANGE = (255, 165, 0)
YELLOW = (255, 255, 0)
GREEN = (0, 255, 0)
PURPLE = (128, 0, 128)
RED = (255, 0, 0)

# Tetromino shapes
SHAPES = [
    [[1, 1, 1, 1]],  # I
    [[1, 1, 1], [0, 1, 0]],  # T
    [[1, 1, 1], [1, 0, 0]],  # L
    [[1, 1, 1], [0, 0, 1]],  # J
    [[1, 1], [1, 1]],  # O
    [[0, 1, 1], [1, 1, 0]],  # S
    [[1, 1, 0], [0, 1, 1]]   # Z
]

# Colors for each shape
SHAPE_COLORS = [CYAN, PURPLE, ORANGE, BLUE, YELLOW, GREEN, RED]

# Fonts
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

class Tetromino:
    def __init__(self):
        self.shape_index = random.randint(0, len(SHAPES) - 1)
        self.shape = SHAPES[self.shape_index]
        self.color = SHAPE_COLORS[self.shape_index]
        self.x = GRID_WIDTH // 2 - len(self.shape[0]) // 2
        self.y = 0
    
    def rotate(self):
        # Transpose the shape matrix to rotate it
        rotated = list(zip(*self.shape[::-1]))
        # Convert tuples to lists
        rotated = [list(row) for row in rotated]
        return rotated
    
    def try_rotate(self, grid):
        rotated = self.rotate()
        if not self.collision(self.x, self.y, rotated, grid):
            self.shape = rotated
    
    def collision(self, x, y, shape, grid):
        for i in range(len(shape)):
            for j in range(len(shape[i])):
                if shape[i][j]:
                    if (y + i >= GRID_HEIGHT or 
                        x + j < 0 or 
                        x + j >= GRID_WIDTH or 
                        (y + i >= 0 and grid[y + i][x + j])):
                        return True
        return False

class Game:
    def __init__(self):
        self.grid = [[0 for _ in range(GRID_WIDTH)] for _ in range(GRID_HEIGHT)]
        self.current_piece = Tetromino()
        self.next_piece = Tetromino()
        self.game_over = False
        self.score = 0
        self.level = 1
        self.lines_cleared = 0
        self.fall_speed = 0.5  # seconds per grid cell
        self.fall_timer = 0
    
    def new_piece(self):
        self.current_piece = self.next_piece
        self.next_piece = Tetromino()
        
        # Check if game is over
        if self.collision(self.current_piece.x, self.current_piece.y, self.current_piece.shape):
            self.game_over = True
    
    def collision(self, x, y, shape):
        return self.current_piece.collision(x, y, shape, self.grid)
    
    def lock_piece(self):
        for i in range(len(self.current_piece.shape)):
            for j in range(len(self.current_piece.shape[i])):
                if self.current_piece.shape[i][j]:
                    if self.current_piece.y + i >= 0:  # Only lock if on grid
                        self.grid[self.current_piece.y + i][self.current_piece.x + j] = self.current_piece.color
        
        self.clear_lines()
        self.new_piece()
    
    def clear_lines(self):
        lines_to_clear = []
        for i in range(GRID_HEIGHT):
            if all(self.grid[i]):
                lines_to_clear.append(i)
        
        for line in lines_to_clear:
            del self.grid[line]
            self.grid.insert(0, [0 for _ in range(GRID_WIDTH)])
        
        # Update score and level
        if lines_to_clear:
            self.lines_cleared += len(lines_to_clear)
            self.score += [100, 300, 500, 800][min(len(lines_to_clear) - 1, 3)] * self.level
            self.level = self.lines_cleared // 10 + 1
            self.fall_speed = max(0.05, 0.5 - (self.level - 1) * 0.05)
    
    def move(self, dx, dy):
        if not self.collision(self.current_piece.x + dx, self.current_piece.y + dy, self.current_piece.shape):
            self.current_piece.x += dx
            self.current_piece.y += dy
            return True
        return False
    
    def drop(self):
        while self.move(0, 1):
            pass
        self.lock_piece()
    
    def update(self, dt):
        if self.game_over:
            return
        
        self.fall_timer += dt
        if self.fall_timer >= self.fall_speed:
            self.fall_timer = 0
            if not self.move(0, 1):
                self.lock_piece()
    
    def draw(self, surface):
        # Draw grid background
        pygame.draw.rect(surface, GRAY, (GRID_OFFSET_X - 2, GRID_OFFSET_Y - 2, 
                                        GRID_WIDTH * GRID_SIZE + 4, GRID_HEIGHT * GRID_SIZE + 4), 2)
        
        # Draw grid cells
        for y in range(GRID_HEIGHT):
            for x in range(GRID_WIDTH):
                if self.grid[y][x]:
                    pygame.draw.rect(surface, self.grid[y][x], 
                                    (GRID_OFFSET_X + x * GRID_SIZE, GRID_OFFSET_Y + y * GRID_SIZE, 
                                     GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw current piece
        if not self.game_over:
            for i in range(len(self.current_piece.shape)):
                for j in range(len(self.current_piece.shape[i])):
                    if self.current_piece.shape[i][j]:
                        pygame.draw.rect(surface, self.current_piece.color, 
                                        (GRID_OFFSET_X + (self.current_piece.x + j) * GRID_SIZE, 
                                         GRID_OFFSET_Y + (self.current_piece.y + i) * GRID_SIZE, 
                                         GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw next piece preview
        next_piece_x = WIDTH - 150
        next_piece_y = 100
        
        # Draw next piece label
        next_label = font_small.render("NEXT:", True, WHITE)
        surface.blit(next_label, (next_piece_x, next_piece_y - 30))
        
        # Draw next piece
        for i in range(len(self.next_piece.shape)):
            for j in range(len(self.next_piece.shape[i])):
                if self.next_piece.shape[i][j]:
                    pygame.draw.rect(surface, self.next_piece.color, 
                                    (next_piece_x + j * GRID_SIZE, 
                                     next_piece_y + i * GRID_SIZE, 
                                     GRID_SIZE - 1, GRID_SIZE - 1))
        
        # Draw score and level
        score_text = font_small.render(f"SCORE: {self.score}", True, WHITE)
        level_text = font_small.render(f"LEVEL: {self.level}", True, WHITE)
        lines_text = font_small.render(f"LINES: {self.lines_cleared}", True, WHITE)
        
        surface.blit(score_text, (50, 100))
        surface.blit(level_text, (50, 140))
        surface.blit(lines_text, (50, 180))
        
        # Draw game over
        if self.game_over:
            game_over_surf = font_large.render("GAME OVER", True, RED)
            game_over_rect = game_over_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            surface.blit(game_over_surf, game_over_rect)
            
            restart_surf = font_medium.render("Press R to restart", True, WHITE)
            restart_rect = restart_surf.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            surface.blit(restart_surf, restart_rect)

def draw_menu():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("RETRO TETRIS", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    instructions = [
        "LEFT/RIGHT: Move piece",
        "UP: Rotate piece",
        "DOWN: Soft drop",
        "SPACE: Hard drop",
        "",
        "Press SPACE to start",
        "Press ESC to quit"
    ]
    
    for i, line in enumerate(instructions):
        text = font_medium.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 40))
        screen.blit(text, text_rect)

def main():
    clock = pygame.time.Clock()
    game = Game()
    
    game_state = "menu"  # menu, playing, game_over
    
    # Key repeat for movement
    pygame.key.set_repeat(200, 100)
    
    running = True
    while running:
        dt = clock.tick(60) / 1000.0  # Convert to seconds
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        game = Game()
                
                elif game_state == "playing":
                    if event.key == pygame.K_LEFT:
                        game.move(-1, 0)
                    if event.key == pygame.K_RIGHT:
                        game.move(1, 0)
                    if event.key == pygame.K_DOWN:
                        game.move(0, 1)
                    if event.key == pygame.K_UP:
                        game.current_piece.try_rotate(game.grid)
                    if event.key == pygame.K_SPACE:
                        game.drop()
                
                if game.game_over and event.key == pygame.K_r:
                    game = Game()
                    game_state = "playing"
        
        screen.fill(BLACK)
        
        if game_state == "menu":
            draw_menu()
        elif game_state == "playing":
            game.update(dt)
            game.draw(screen)
            
            if game.game_over:
                game_state = "game_over"
        elif game_state == "game_over":
            game.draw(screen)
        
        pygame.display.flip()
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
