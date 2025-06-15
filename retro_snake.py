import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
GRID_SIZE = 20
GRID_WIDTH = WIDTH // GRID_SIZE
GRID_HEIGHT = HEIGHT // GRID_SIZE

screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Snake")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
DARK_GREEN = (0, 150, 0)

# Fonts
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

# Directions
UP = (0, -1)
DOWN = (0, 1)
LEFT = (-1, 0)
RIGHT = (1, 0)

class Snake:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.length = 3
        self.positions = [(GRID_WIDTH // 2, GRID_HEIGHT // 2)]
        self.direction = RIGHT
        self.score = 0
        self.grow_to = 3  # Initial length
        self.is_alive = True
    
    def get_head_position(self):
        return self.positions[0]
    
    def update(self):
        if not self.is_alive:
            return
        
        head = self.get_head_position()
        x, y = self.direction
        new_head = ((head[0] + x) % GRID_WIDTH, (head[1] + y) % GRID_HEIGHT)
        
        # Check for collision with self
        if new_head in self.positions[1:]:
            self.is_alive = False
            return
        
        # Move snake
        self.positions.insert(0, new_head)
        
        # Grow snake if needed
        if len(self.positions) > self.grow_to:
            self.positions.pop()
    
    def change_direction(self, direction):
        # Prevent 180 degree turns
        if (direction[0] * -1, direction[1] * -1) == self.direction:
            return
        self.direction = direction
    
    def grow(self):
        self.grow_to += 1
        self.score += 1
    
    def draw(self, surface):
        for i, pos in enumerate(self.positions):
            color = GREEN if i == 0 else DARK_GREEN  # Head is lighter green
            rect = pygame.Rect(pos[0] * GRID_SIZE, pos[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, color, rect)
            pygame.draw.rect(surface, BLACK, rect, 1)

class Food:
    def __init__(self, snake_positions):
        self.position = self.randomize_position(snake_positions)
    
    def randomize_position(self, snake_positions):
        position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        while position in snake_positions:
            position = (random.randint(0, GRID_WIDTH - 1), random.randint(0, GRID_HEIGHT - 1))
        return position
    
    def draw(self, surface):
        rect = pygame.Rect(self.position[0] * GRID_SIZE, self.position[1] * GRID_SIZE, GRID_SIZE, GRID_SIZE)
        pygame.draw.rect(surface, RED, rect)
        pygame.draw.rect(surface, BLACK, rect, 1)

def draw_grid(surface):
    for y in range(0, HEIGHT, GRID_SIZE):
        for x in range(0, WIDTH, GRID_SIZE):
            rect = pygame.Rect(x, y, GRID_SIZE, GRID_SIZE)
            pygame.draw.rect(surface, BLACK, rect, 1)

def draw_menu():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("RETRO SNAKE", True, GREEN)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    instructions = [
        "Use ARROW KEYS to control the snake",
        "Eat the red food to grow",
        "Don't hit yourself!",
        "",
        "Press SPACE to start",
        "Press ESC to quit"
    ]
    
    for i, line in enumerate(instructions):
        text = font_medium.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 40))
        screen.blit(text, text_rect)

def draw_game_over(score):
    overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
    overlay.fill((0, 0, 0, 180))  # Semi-transparent black
    screen.blit(overlay, (0, 0))
    
    # Draw game over message
    game_over = font_large.render("GAME OVER", True, RED)
    game_over_rect = game_over.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(game_over, game_over_rect)
    
    # Draw score
    score_text = font_medium.render(f"Final Score: {score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    # Draw restart instructions
    restart = font_medium.render("Press R to restart", True, WHITE)
    restart_rect = restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(restart, restart_rect)
    
    quit_text = font_medium.render("Press ESC to quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
    screen.blit(quit_text, quit_rect)

def main():
    clock = pygame.time.Clock()
    snake = Snake()
    food = Food(snake.positions)
    
    game_state = "menu"  # menu, playing, game_over
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_state == "menu":
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        snake = Snake()
                        food = Food(snake.positions)
                
                elif game_state == "playing":
                    if event.key == pygame.K_UP:
                        snake.change_direction(UP)
                    elif event.key == pygame.K_DOWN:
                        snake.change_direction(DOWN)
                    elif event.key == pygame.K_LEFT:
                        snake.change_direction(LEFT)
                    elif event.key == pygame.K_RIGHT:
                        snake.change_direction(RIGHT)
                
                elif game_state == "game_over":
                    if event.key == pygame.K_r:
                        game_state = "playing"
                        snake = Snake()
                        food = Food(snake.positions)
        
        if game_state == "menu":
            draw_menu()
        
        elif game_state == "playing":
            # Update game state
            snake.update()
            
            # Check for food collision
            if snake.get_head_position() == food.position:
                snake.grow()
                food = Food(snake.positions)
            
            # Check for game over
            if not snake.is_alive:
                game_state = "game_over"
            
            # Draw everything
            screen.fill(BLACK)
            draw_grid(screen)
            snake.draw(screen)
            food.draw(screen)
            
            # Draw score
            score_text = font_small.render(f"Score: {snake.score}", True, WHITE)
            screen.blit(score_text, (10, 10))
        
        elif game_state == "game_over":
            draw_game_over(snake.score)
        
        pygame.display.flip()
        
        # Control game speed based on snake length
        speed = 5 + min(15, snake.score // 5)  # Increase speed as score increases
        clock.tick(speed)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
