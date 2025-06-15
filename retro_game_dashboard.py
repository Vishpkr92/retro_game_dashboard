import pygame
import sys
import subprocess
import os

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Game Dashboard")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
YELLOW = (255, 255, 0)
PURPLE = (128, 0, 128)
ORANGE = (255, 165, 0)

# Fonts
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

class Button:
    def __init__(self, x, y, width, height, color, text, text_color=BLACK, hover_color=None):
        self.rect = pygame.Rect(x, y, width, height)
        self.color = color
        self.text = text
        self.text_color = text_color
        self.hover_color = hover_color or self.lighten_color(color)
        self.is_hovered = False
        
    def lighten_color(self, color):
        r, g, b = color
        return min(r + 30, 255), min(g + 30, 255), min(b + 30, 255)
        
    def draw(self, surface):
        color = self.hover_color if self.is_hovered else self.color
        pygame.draw.rect(surface, color, self.rect, border_radius=15)
        pygame.draw.rect(surface, BLACK, self.rect, 3, border_radius=15)
        
        text_surf = font_medium.render(self.text, True, self.text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)
        
    def check_hover(self, pos):
        self.is_hovered = self.rect.collidepoint(pos)
        return self.is_hovered
        
    def is_clicked(self, pos, click):
        return self.rect.collidepoint(pos) and click

def draw_dashboard():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("RETRO GAME DASHBOARD", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, 80))
    screen.blit(title, title_rect)
    
    # Draw game buttons
    buttons = []
    
    # Pong Button
    pong_button = Button(WIDTH//2 - 150, 180, 300, 80, RED, "PONG", WHITE)
    pong_button.draw(screen)
    buttons.append(("pong", pong_button))
    
    # Tetris Button
    tetris_button = Button(WIDTH//2 - 150, 280, 300, 80, GREEN, "TETRIS", WHITE)
    tetris_button.draw(screen)
    buttons.append(("tetris", tetris_button))
    
    # Snake Button
    snake_button = Button(WIDTH//2 - 150, 380, 300, 80, BLUE, "SNAKE", WHITE)
    snake_button.draw(screen)
    buttons.append(("snake", snake_button))
    
    # Tic-tac-toe Button
    ttt_button = Button(WIDTH//2 - 150, 480, 300, 80, YELLOW, "TIC-TAC-TOE", BLACK)
    ttt_button.draw(screen)
    buttons.append(("tictactoe", ttt_button))
    
    return buttons

def launch_game(game_name):
    game_file = f"retro_{game_name}.py"
    if os.path.exists(game_file):
        try:
            subprocess.Popen([sys.executable, game_file])
        except Exception as e:
            print(f"Error launching {game_name}: {e}")
    else:
        print(f"Game file {game_file} not found!")

def main():
    clock = pygame.time.Clock()
    running = True
    
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:
                    mouse_click = True
        
        buttons = draw_dashboard()
        
        # Check button interactions
        for game_name, button in buttons:
            button.check_hover(mouse_pos)
            if button.is_clicked(mouse_pos, mouse_click):
                launch_game(game_name)
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()

if __name__ == "__main__":
    main()
