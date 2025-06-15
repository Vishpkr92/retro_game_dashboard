import pygame
import sys
import random

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Pong")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
BLUE = (0, 120, 255)
RED = (255, 50, 50)
DARK_GRAY = (40, 40, 40)
LIGHT_GRAY = (150, 150, 150)

# Game objects
PADDLE_WIDTH = 15
PADDLE_HEIGHT = 100
BALL_SIZE = 15
BALL_SPEED_X = 7
BALL_SPEED_Y = 7
PADDLE_SPEED = 8

# Fonts
font = pygame.font.SysFont('Arial', 32)
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 20)

class Paddle:
    def __init__(self, x, y, is_player=False):
        self.rect = pygame.Rect(x, y, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.speed = 0
        self.score = 0
        self.is_player = is_player
    
    def move(self):
        self.rect.y += self.speed
        # Keep paddle on screen
        if self.rect.top < 0:
            self.rect.top = 0
        if self.rect.bottom > HEIGHT:
            self.rect.bottom = HEIGHT
    
    def draw(self):
        color = BLUE if self.is_player else RED
        pygame.draw.rect(screen, color, self.rect)
        # Add a 3D effect with a border
        pygame.draw.rect(screen, WHITE, self.rect, 2)

class Ball:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.rect = pygame.Rect(WIDTH // 2 - BALL_SIZE // 2, HEIGHT // 2 - BALL_SIZE // 2, BALL_SIZE, BALL_SIZE)
        self.speed_x = BALL_SPEED_X * random.choice([-1, 1])
        self.speed_y = BALL_SPEED_Y * random.choice([-1, 1])
    
    def move(self, player_paddle, ai_paddle):
        self.rect.x += self.speed_x
        self.rect.y += self.speed_y
        
        # Bounce off top and bottom
        if self.rect.top <= 0 or self.rect.bottom >= HEIGHT:
            self.speed_y *= -1
        
        # Score points
        if self.rect.left <= 0:
            ai_paddle.score += 1
            self.reset()
        if self.rect.right >= WIDTH:
            player_paddle.score += 1
            self.reset()
        
        # Paddle collisions
        if self.rect.colliderect(player_paddle.rect) or self.rect.colliderect(ai_paddle.rect):
            self.speed_x *= -1
            # Add some randomness to bounce
            self.speed_y += random.uniform(-1, 1)
            if abs(self.speed_y) > 10:
                self.speed_y = 10 if self.speed_y > 0 else -10
    
    def draw(self):
        # Draw ball with a gradient effect
        pygame.draw.ellipse(screen, WHITE, self.rect)
        # Add a small highlight
        highlight = pygame.Rect(self.rect.x + 2, self.rect.y + 2, BALL_SIZE // 3, BALL_SIZE // 3)
        pygame.draw.ellipse(screen, (255, 255, 200), highlight)

def draw_game(player_paddle, ai_paddle, ball):
    # Draw background with a gradient effect
    screen.fill(BLACK)
    
    # Draw court markings
    # Center line
    pygame.draw.aaline(screen, LIGHT_GRAY, (WIDTH // 2, 0), (WIDTH // 2, HEIGHT))
    
    # Center circle
    pygame.draw.circle(screen, LIGHT_GRAY, (WIDTH // 2, HEIGHT // 2), 50, 1)
    
    # Draw player side label
    player_label = font_small.render("PLAYER", True, BLUE)
    screen.blit(player_label, (WIDTH // 4 - player_label.get_width() // 2, HEIGHT - 30))
    
    # Draw AI side label
    ai_label = font_small.render("AI", True, RED)
    screen.blit(ai_label, (3 * WIDTH // 4 - ai_label.get_width() // 2, HEIGHT - 30))
    
    # Draw paddles and ball
    player_paddle.draw()
    ai_paddle.draw()
    ball.draw()
    
    # Draw scores
    player_score = font.render(str(player_paddle.score), True, BLUE)
    ai_score = font.render(str(ai_paddle.score), True, RED)
    screen.blit(player_score, (WIDTH // 4, 20))
    screen.blit(ai_score, (3 * WIDTH // 4, 20))

def ai_movement(ai_paddle, ball):
    # Simple AI: follow the ball
    if ball.rect.centery < ai_paddle.rect.centery:
        ai_paddle.speed = -PADDLE_SPEED
    elif ball.rect.centery > ai_paddle.rect.centery:
        ai_paddle.speed = PADDLE_SPEED
    else:
        ai_paddle.speed = 0
    
    # Make AI imperfect
    if random.random() < 0.05:  # 5% chance to make a mistake
        ai_paddle.speed = 0

def draw_menu():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("RETRO PONG", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw instructions
    instructions = [
        "Use UP and DOWN arrow keys to move your paddle",
        "First to 5 points wins!",
        "Press SPACE to start",
        "Press ESC to quit"
    ]
    
    for i, line in enumerate(instructions):
        text = font_medium.render(line, True, WHITE)
        text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//2 + i * 50))
        screen.blit(text, text_rect)

def draw_game_over(player_paddle, ai_paddle):
    screen.fill(BLACK)
    
    if player_paddle.score >= 5:
        message = "YOU WIN!"
    else:
        message = "GAME OVER"
    
    # Draw message
    text = font_large.render(message, True, WHITE)
    text_rect = text.get_rect(center=(WIDTH//2, HEIGHT//3))
    screen.blit(text, text_rect)
    
    # Draw final score
    score_text = font_medium.render(f"Final Score: {player_paddle.score} - {ai_paddle.score}", True, WHITE)
    score_rect = score_text.get_rect(center=(WIDTH//2, HEIGHT//2))
    screen.blit(score_text, score_rect)
    
    # Draw instructions
    restart = font_medium.render("Press SPACE to play again", True, WHITE)
    restart_rect = restart.get_rect(center=(WIDTH//2, HEIGHT//2 + 60))
    screen.blit(restart, restart_rect)
    
    quit_text = font_medium.render("Press ESC to quit", True, WHITE)
    quit_rect = quit_text.get_rect(center=(WIDTH//2, HEIGHT//2 + 120))
    screen.blit(quit_text, quit_rect)

def main():
    clock = pygame.time.Clock()
    
    # Create game objects
    player_paddle = Paddle(50, HEIGHT // 2 - PADDLE_HEIGHT // 2, is_player=True)
    ai_paddle = Paddle(WIDTH - 50 - PADDLE_WIDTH, HEIGHT // 2 - PADDLE_HEIGHT // 2, is_player=False)
    ball = Ball()
    
    game_state = "menu"  # menu, playing, game_over
    
    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            # Keyboard events
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                
                if game_state == "menu" or game_state == "game_over":
                    if event.key == pygame.K_SPACE:
                        game_state = "playing"
                        player_paddle.score = 0
                        ai_paddle.score = 0
                        ball.reset()
                
                if game_state == "playing":
                    if event.key == pygame.K_UP:
                        player_paddle.speed = -PADDLE_SPEED
                    if event.key == pygame.K_DOWN:
                        player_paddle.speed = PADDLE_SPEED
            
            if event.type == pygame.KEYUP:
                if game_state == "playing":
                    if event.key == pygame.K_UP and player_paddle.speed < 0:
                        player_paddle.speed = 0
                    if event.key == pygame.K_DOWN and player_paddle.speed > 0:
                        player_paddle.speed = 0
        
        if game_state == "menu":
            draw_menu()
        
        elif game_state == "playing":
            # Update game objects
            player_paddle.move()
            ai_movement(ai_paddle, ball)
            ai_paddle.move()
            ball.move(player_paddle, ai_paddle)
            
            # Draw everything
            draw_game(player_paddle, ai_paddle, ball)
            
            # Check for game over
            if player_paddle.score >= 5 or ai_paddle.score >= 5:
                game_state = "game_over"
        
        elif game_state == "game_over":
            draw_game_over(player_paddle, ai_paddle)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
