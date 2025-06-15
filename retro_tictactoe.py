import pygame
import sys
import random
import time

# Initialize pygame
pygame.init()

# Screen dimensions
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Retro Tic-Tac-Toe")

# Colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)
GRAY = (128, 128, 128)

# Fonts
font_large = pygame.font.SysFont('Arial', 48, bold=True)
font_medium = pygame.font.SysFont('Arial', 32)
font_small = pygame.font.SysFont('Arial', 24)

# Game constants
BOARD_SIZE = 3
CELL_SIZE = 120
BOARD_OFFSET_X = (WIDTH - BOARD_SIZE * CELL_SIZE) // 2
BOARD_OFFSET_Y = (HEIGHT - BOARD_SIZE * CELL_SIZE) // 2

class TicTacToe:
    def __init__(self):
        self.reset()
    
    def reset(self):
        self.board = [['' for _ in range(BOARD_SIZE)] for _ in range(BOARD_SIZE)]
        self.current_player = 'X'
        self.winner = None
        self.game_over = False
        self.ai_enabled = True
        self.difficulty = "Medium"  # Default difficulty
    
    def make_move(self, row, col):
        if self.game_over or row < 0 or row >= BOARD_SIZE or col < 0 or col >= BOARD_SIZE:
            return False
        
        if self.board[row][col] == '':
            self.board[row][col] = self.current_player
            self.check_winner()
            self.current_player = 'O' if self.current_player == 'X' else 'X'
            return True
        
        return False
    
    def check_winner(self):
        # Check rows
        for row in range(BOARD_SIZE):
            if self.board[row][0] != '' and all(self.board[row][0] == self.board[row][i] for i in range(BOARD_SIZE)):
                self.winner = self.board[row][0]
                self.game_over = True
                return
        
        # Check columns
        for col in range(BOARD_SIZE):
            if self.board[0][col] != '' and all(self.board[0][col] == self.board[i][col] for i in range(BOARD_SIZE)):
                self.winner = self.board[0][col]
                self.game_over = True
                return
        
        # Check diagonals
        if self.board[0][0] != '' and all(self.board[0][0] == self.board[i][i] for i in range(BOARD_SIZE)):
            self.winner = self.board[0][0]
            self.game_over = True
            return
        
        if self.board[0][BOARD_SIZE-1] != '' and all(self.board[0][BOARD_SIZE-1] == self.board[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)):
            self.winner = self.board[0][BOARD_SIZE-1]
            self.game_over = True
            return
        
        # Check for draw
        if all(self.board[i][j] != '' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
            self.game_over = True
    
    def ai_move(self):
        if self.difficulty == "Hard":
            self.ai_move_hard()
        elif self.difficulty == "Medium":
            self.ai_move_medium()
        else:
            self.ai_move_easy()
    
    def ai_move_medium(self):
        # Medium difficulty: 70% chance to make the optimal move, 30% chance to make a random move
        if random.random() < 0.7:
            self.ai_move_hard()
        else:
            self.ai_move_easy()
    
    def ai_move_easy(self):
        # Simple AI: just pick a random empty cell
        empty_cells = [(i, j) for i in range(BOARD_SIZE) for j in range(BOARD_SIZE) if self.board[i][j] == '']
        if empty_cells:
            row, col = random.choice(empty_cells)
            self.make_move(row, col)
    
    def ai_move_hard(self):
        # Minimax AI
        best_score = float('-inf')
        best_move = None
        
        for i in range(BOARD_SIZE):
            for j in range(BOARD_SIZE):
                if self.board[i][j] == '':
                    self.board[i][j] = 'O'  # AI is always O
                    score = self.minimax(0, False)
                    self.board[i][j] = ''
                    
                    if score > best_score:
                        best_score = score
                        best_move = (i, j)
        
        if best_move:
            self.make_move(best_move[0], best_move[1])
    
    def minimax(self, depth, is_maximizing):
        # Check for terminal states
        result = self.check_game_state()
        if result is not None:
            return {'X': -10, 'O': 10, 'draw': 0}[result]
        
        if is_maximizing:
            best_score = float('-inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'O'
                        score = self.minimax(depth + 1, False)
                        self.board[i][j] = ''
                        best_score = max(score, best_score)
            return best_score
        else:
            best_score = float('inf')
            for i in range(BOARD_SIZE):
                for j in range(BOARD_SIZE):
                    if self.board[i][j] == '':
                        self.board[i][j] = 'X'
                        score = self.minimax(depth + 1, True)
                        self.board[i][j] = ''
                        best_score = min(score, best_score)
            return best_score
    
    def check_game_state(self):
        # Check rows
        for row in range(BOARD_SIZE):
            if self.board[row][0] != '' and all(self.board[row][0] == self.board[row][i] for i in range(BOARD_SIZE)):
                return self.board[row][0]
        
        # Check columns
        for col in range(BOARD_SIZE):
            if self.board[0][col] != '' and all(self.board[0][col] == self.board[i][col] for i in range(BOARD_SIZE)):
                return self.board[0][col]
        
        # Check diagonals
        if self.board[0][0] != '' and all(self.board[0][0] == self.board[i][i] for i in range(BOARD_SIZE)):
            return self.board[0][0]
        
        if self.board[0][BOARD_SIZE-1] != '' and all(self.board[0][BOARD_SIZE-1] == self.board[i][BOARD_SIZE-1-i] for i in range(BOARD_SIZE)):
            return self.board[0][BOARD_SIZE-1]
        
        # Check for draw
        if all(self.board[i][j] != '' for i in range(BOARD_SIZE) for j in range(BOARD_SIZE)):
            return 'draw'
        
        return None

    def draw(self, surface):
        # Draw board background
        board_rect = pygame.Rect(BOARD_OFFSET_X, BOARD_OFFSET_Y, CELL_SIZE * BOARD_SIZE, CELL_SIZE * BOARD_SIZE)
        pygame.draw.rect(surface, WHITE, board_rect)
        
        # Draw grid lines
        for i in range(1, BOARD_SIZE):
            # Horizontal lines
            pygame.draw.line(surface, BLACK, 
                            (BOARD_OFFSET_X, BOARD_OFFSET_Y + i * CELL_SIZE),
                            (BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE, BOARD_OFFSET_Y + i * CELL_SIZE),
                            3)
            # Vertical lines
            pygame.draw.line(surface, BLACK, 
                            (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y),
                            (BOARD_OFFSET_X + i * CELL_SIZE, BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE),
                            3)
        
        # Draw X's and O's
        for row in range(BOARD_SIZE):
            for col in range(BOARD_SIZE):
                if self.board[row][col] == 'X':
                    # Draw X
                    x_center = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                    y_center = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                    offset = CELL_SIZE // 3
                    
                    pygame.draw.line(surface, BLUE, 
                                    (x_center - offset, y_center - offset),
                                    (x_center + offset, y_center + offset),
                                    8)
                    pygame.draw.line(surface, BLUE, 
                                    (x_center + offset, y_center - offset),
                                    (x_center - offset, y_center + offset),
                                    8)
                
                elif self.board[row][col] == 'O':
                    # Draw O
                    x_center = BOARD_OFFSET_X + col * CELL_SIZE + CELL_SIZE // 2
                    y_center = BOARD_OFFSET_Y + row * CELL_SIZE + CELL_SIZE // 2
                    radius = CELL_SIZE // 3
                    
                    pygame.draw.circle(surface, RED, (x_center, y_center), radius, 8)
        
        # Draw current player indicator
        player_text = font_medium.render(f"Current Player: {self.current_player}", True, WHITE)
        surface.blit(player_text, (20, 20))
        
        # Draw AI status
        ai_text = font_medium.render(f"AI: {'ON' if self.ai_enabled else 'OFF'}", True, WHITE)
        surface.blit(ai_text, (WIDTH - 150, 20))
        
        # Draw difficulty if AI is enabled
        if self.ai_enabled:
            diff_text = font_medium.render(f"Difficulty: {self.difficulty}", True, WHITE)
            surface.blit(diff_text, (WIDTH - 250, 60))
        
        # Draw game over message
        if self.game_over:
            overlay = pygame.Surface((WIDTH, HEIGHT), pygame.SRCALPHA)
            overlay.fill((0, 0, 0, 180))  # Semi-transparent black
            surface.blit(overlay, (0, 0))
            
            if self.winner:
                message = f"Player {self.winner} wins!"
                color = BLUE if self.winner == 'X' else RED
            else:
                message = "It's a draw!"
                color = WHITE
            
            game_over_text = font_large.render(message, True, color)
            game_over_rect = game_over_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 - 50))
            surface.blit(game_over_text, game_over_rect)
            
            restart_text = font_medium.render("Press R to restart", True, WHITE)
            restart_rect = restart_text.get_rect(center=(WIDTH // 2, HEIGHT // 2 + 50))
            surface.blit(restart_text, restart_rect)

def draw_menu():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("RETRO TIC-TAC-TOE", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    button_width = 300
    button_height = 80
    button_margin = 30
    
    # Play vs AI button
    ai_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
    pygame.draw.rect(screen, BLUE, ai_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, ai_button, 3, border_radius=15)
    
    ai_text = font_medium.render("PLAY VS AI", True, WHITE)
    ai_text_rect = ai_text.get_rect(center=ai_button.center)
    screen.blit(ai_text, ai_text_rect)
    
    # Play vs Human button
    human_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + button_height + button_margin, 
                              button_width, button_height)
    pygame.draw.rect(screen, RED, human_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, human_button, 3, border_radius=15)
    
    human_text = font_medium.render("PLAY VS HUMAN", True, WHITE)
    human_text_rect = human_text.get_rect(center=human_button.center)
    screen.blit(human_text, human_text_rect)
    
    # Back button
    back_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + 2*(button_height + button_margin), 
                             button_width, button_height)
    pygame.draw.rect(screen, GRAY, back_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, back_button, 3, border_radius=15)
    
    back_text = font_medium.render("BACK", True, BLACK)
    back_text_rect = back_text.get_rect(center=back_button.center)
    screen.blit(back_text, back_text_rect)
    
    return ai_button, human_button, back_button

def draw_difficulty_menu():
    screen.fill(BLACK)
    
    # Draw title
    title = font_large.render("SELECT DIFFICULTY", True, WHITE)
    title_rect = title.get_rect(center=(WIDTH//2, HEIGHT//4))
    screen.blit(title, title_rect)
    
    # Draw buttons
    button_width = 300
    button_height = 80
    button_margin = 30
    
    # Easy button
    easy_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 - button_height - button_margin, 
                             button_width, button_height)
    pygame.draw.rect(screen, GREEN, easy_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, easy_button, 3, border_radius=15)
    
    easy_text = font_medium.render("EASY", True, BLACK)
    easy_text_rect = easy_text.get_rect(center=easy_button.center)
    screen.blit(easy_text, easy_text_rect)
    
    # Medium button
    medium_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2, button_width, button_height)
    pygame.draw.rect(screen, BLUE, medium_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, medium_button, 3, border_radius=15)
    
    medium_text = font_medium.render("MEDIUM", True, WHITE)
    medium_text_rect = medium_text.get_rect(center=medium_button.center)
    screen.blit(medium_text, medium_text_rect)
    
    # Hard button
    hard_button = pygame.Rect(WIDTH//2 - button_width//2, HEIGHT//2 + button_height + button_margin, 
                             button_width, button_height)
    pygame.draw.rect(screen, RED, hard_button, border_radius=15)
    pygame.draw.rect(screen, BLACK, hard_button, 3, border_radius=15)
    
    hard_text = font_medium.render("HARD", True, WHITE)
    hard_text_rect = hard_text.get_rect(center=hard_button.center)
    screen.blit(hard_text, hard_text_rect)
    
    return easy_button, medium_button, hard_button

def main():
    clock = pygame.time.Clock()
    game = TicTacToe()
    
    game_state = "menu"  # menu, difficulty, playing
    
    running = True
    while running:
        mouse_pos = pygame.mouse.get_pos()
        mouse_click = False
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Left mouse button
                    mouse_click = True
            
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    if game_state == "playing":
                        game_state = "menu"
                    else:
                        running = False
                
                if event.key == pygame.K_r and game.game_over:
                    game.reset()
        
        screen.fill(BLACK)
        
        if game_state == "menu":
            ai_button, human_button, back_button = draw_menu()
            
            if mouse_click:
                if ai_button.collidepoint(mouse_pos):
                    game_state = "difficulty"
                elif human_button.collidepoint(mouse_pos):
                    game.ai_enabled = False
                    game.reset()
                    game_state = "playing"
                elif back_button.collidepoint(mouse_pos):
                    running = False
        
        elif game_state == "difficulty":
            easy_button, medium_button, hard_button = draw_difficulty_menu()
            
            if mouse_click:
                if easy_button.collidepoint(mouse_pos):
                    game.difficulty = "Easy"
                    game.ai_enabled = True
                    game.reset()
                    game.difficulty = "Easy"  # Set again after reset to ensure it sticks
                    game_state = "playing"
                elif medium_button.collidepoint(mouse_pos):
                    game.difficulty = "Medium"
                    game.ai_enabled = True
                    game.reset()
                    game.difficulty = "Medium"  # Set again after reset to ensure it sticks
                    game_state = "playing"
                elif hard_button.collidepoint(mouse_pos):
                    game.difficulty = "Hard"
                    game.ai_enabled = True
                    game.reset()
                    game.difficulty = "Hard"  # Set again after reset to ensure it sticks
                    game_state = "playing"
        
        elif game_state == "playing":
            game.draw(screen)
            
            # Handle player moves
            if not game.game_over and game.current_player == 'X':  # Human is always X
                if mouse_click:
                    # Convert mouse position to board position
                    if BOARD_OFFSET_X <= mouse_pos[0] <= BOARD_OFFSET_X + BOARD_SIZE * CELL_SIZE and \
                       BOARD_OFFSET_Y <= mouse_pos[1] <= BOARD_OFFSET_Y + BOARD_SIZE * CELL_SIZE:
                        col = (mouse_pos[0] - BOARD_OFFSET_X) // CELL_SIZE
                        row = (mouse_pos[1] - BOARD_OFFSET_Y) // CELL_SIZE
                        game.make_move(row, col)
            
            # Handle AI moves
            if not game.game_over and game.current_player == 'O' and game.ai_enabled:
                # Add a small delay to make AI move visible
                pygame.display.flip()
                time.sleep(0.5)
                game.ai_move()
        
        pygame.display.flip()
        clock.tick(60)
    
    pygame.quit()
    sys.exit()
if __name__ == "__main__":
    main()
