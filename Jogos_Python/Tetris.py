import pygame
import random

# Configurações do jogo
SCREEN_WIDTH = 300
SCREEN_HEIGHT = 600
BLOCK_SIZE = 30
FPS = 30

# Cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
GRAY = (128, 128, 128)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
YELLOW = (255, 255, 0)
CYAN = (0, 255, 255)
MAGENTA = (255, 0, 255)
SHADOW_COLOR = (100, 100, 100, 100)  # Cor da sombra

# Formas dos blocos
SHAPES = [
    [[1, 1, 1],
     [0, 1, 0]],

    [[0, 2, 2],
     [2, 2, 0]],

    [[3, 3],
     [3, 3]],

    [[0, 0, 4],
     [4, 4, 4]],

    [[5, 0],
     [5, 0],
     [5, 5]],

    [[6, 0],
     [6, 0],
     [6, 0],
     [6, 0]],

    [[7, 7, 0],
     [0, 7, 7]]
]

# Inicializa o Pygame
pygame.init()
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
clock = pygame.time.Clock()

def draw_block(x, y, color):
    pygame.draw.rect(screen, BLACK, (x * BLOCK_SIZE, y * BLOCK_SIZE, BLOCK_SIZE, BLOCK_SIZE))
    pygame.draw.rect(screen, color, (x * BLOCK_SIZE + 2, y * BLOCK_SIZE + 2, BLOCK_SIZE - 4, BLOCK_SIZE - 4))

def draw_grid():
    for x in range(SCREEN_WIDTH // BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (x * BLOCK_SIZE, 0), (x * BLOCK_SIZE, SCREEN_HEIGHT))
    for y in range(SCREEN_HEIGHT // BLOCK_SIZE):
        pygame.draw.line(screen, GRAY, (0, y * BLOCK_SIZE), (SCREEN_WIDTH, y * BLOCK_SIZE))

def draw_shape(shape, x, y, color):
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                draw_block(x + col_index, y + row_index, color)

def check_collision(board, shape, x, y):
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                if x + col_index < 0 or x + col_index >= SCREEN_WIDTH // BLOCK_SIZE:
                    return True
                if y + row_index >= SCREEN_HEIGHT // BLOCK_SIZE:
                    return True
                if board[y + row_index][x + col_index]:
                    return True
    return False

def merge_shape(board, shape, x, y):
    for row_index, row in enumerate(shape):
        for col_index, cell in enumerate(row):
            if cell:
                board[y + row_index][x + col_index] = cell

def clear_lines(board):
    lines_cleared = 0
    for row_index, row in enumerate(board):
        if all(cell != 0 for cell in row):
            del board[row_index]
            board.insert(0, [0] * (SCREEN_WIDTH // BLOCK_SIZE))
            lines_cleared += 1
    return lines_cleared

def draw_border():
    pygame.draw.rect(screen, BLACK, (0, 0, SCREEN_WIDTH, SCREEN_HEIGHT), 5)

def draw_score(score):
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"Score: {score}", True, WHITE)
    screen.blit(score_text, (10, 10))

def rotate_shape(shape, x, y):
    rotated_shape = [[shape[j][i] for j in range(len(shape))] for i in range(len(shape[0]) - 1, -1, -1)]
    # Verificar se o bloco rotacionado está dentro dos limites da tela
    if x + len(rotated_shape[0]) > SCREEN_WIDTH // BLOCK_SIZE:
        return shape  # Se estiver fora, retorna a forma original sem rotacionar
    if y + len(rotated_shape) > SCREEN_HEIGHT // BLOCK_SIZE:
        return shape  # Se estiver fora, retorna a forma original sem rotacionar
    return rotated_shape  # Se estiver dentro, retorna o bloco rotacionado

def draw_shadow(board, current_shape, current_shape_x, current_shape_y):
    shadow_y = current_shape_y
    while not check_collision(board, current_shape, current_shape_x, shadow_y + 1):
        shadow_y += 1
    shadow_shape = [row[:] for row in current_shape]
    draw_shape(shadow_shape, current_shape_x, shadow_y, SHADOW_COLOR)

def show_game_over(score):
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    game_over_text = font.render("Game Over", True, RED)
    score_text = font.render(f"Score: {score}", True, WHITE)
    game_over_rect = game_over_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 30))
    score_rect = score_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 30))
    screen.blit(game_over_text, game_over_rect)
    screen.blit(score_text, score_rect)
    font = pygame.font.Font(None, 24)
    restart_text = font.render("Pressione F para recomeçar", True, WHITE)
    restart_rect = restart_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 70))
    screen.blit(restart_text, restart_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_f:
                    return

def show_start_screen():
    screen.fill(BLACK)
    font = pygame.font.Font(None, 36)
    start_text = font.render("Press Enter", True, WHITE)
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))
    screen.blit(start_text, start_rect)
    pygame.display.flip()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                quit()
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    return

def draw_intro_animation():
    intro_board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    for _ in range(30):  # Gerar 30 quadros de animação
        screen.fill(BLACK)
        draw_border()
        draw_grid()
        for row_index, row in enumerate(intro_board):
            for col_index, cell in enumerate(row):
                if cell:
                    draw_block(col_index, row_index, WHITE)
        for i in range(3):
            current_shape = random.choice(SHAPES)
            current_shape_x = random.randint(0, SCREEN_WIDTH // BLOCK_SIZE - len(current_shape[0]))
            current_shape_y = -len(current_shape)
            shape_color = random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA])
            while not check_collision(intro_board, current_shape, current_shape_x, current_shape_y + 1):
                current_shape_y += 1
            merge_shape(intro_board, current_shape, current_shape_x, current_shape_y)
            draw_shape(current_shape, current_shape_x, current_shape_y, shape_color)
        pygame.display.flip()
        pygame.time.wait(100)

def main():
    show_start_screen()

    draw_intro_animation()

    board = [[0] * (SCREEN_WIDTH // BLOCK_SIZE) for _ in range(SCREEN_HEIGHT // BLOCK_SIZE)]
    next_shape = random.choice(SHAPES)
    current_shape = random.choice(SHAPES)
    current_shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
    current_shape_y = 0
    shape_color = random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA])
    score = 0
    last_drop_time = pygame.time.get_ticks()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_a:  # Mudar para a tecla 'A' para rotacionar
                    current_shape = rotate_shape(current_shape, current_shape_x, current_shape_y)
                elif event.key == pygame.K_UP:  # Rotacionar usando a seta para cima
                    current_shape = rotate_shape(current_shape, current_shape_x, current_shape_y)
                elif event.key == pygame.K_SPACE:
                    while not check_collision(board, current_shape, current_shape_x, current_shape_y + 1):
                        current_shape_y += 1

        keys = pygame.key.get_pressed()
        if keys[pygame.K_LEFT]:
            if not check_collision(board, current_shape, current_shape_x - 1, current_shape_y):
                current_shape_x -= 1
        if keys[pygame.K_RIGHT]:
            if not check_collision(board, current_shape, current_shape_x + 1, current_shape_y):
                current_shape_x += 1
        if keys[pygame.K_DOWN]:
            if not check_collision(board, current_shape, current_shape_x, current_shape_y + 1):
                current_shape_y += 1

        current_time = pygame.time.get_ticks()
        if current_time - last_drop_time > 500:  # Intervalo de queda de 0.5 segundos
            if not check_collision(board, current_shape, current_shape_x, current_shape_y + 1):
                current_shape_y += 1
                last_drop_time = current_time

        screen.fill(BLACK)
        draw_border()
        draw_grid()
        draw_shadow(board, current_shape, current_shape_x, current_shape_y)
        draw_shape(current_shape, current_shape_x, current_shape_y, shape_color)

        # Desenhar o próximo bloco na tela
        draw_shape(next_shape, SCREEN_WIDTH // BLOCK_SIZE + 1, 3, shape_color)

        if check_collision(board, current_shape, current_shape_x, current_shape_y + 1):
            if current_shape_y == 0:  # Verifica se o jogo acabou
                show_game_over(score)
                main()
            merge_shape(board, current_shape, current_shape_x, current_shape_y)
            lines_cleared = clear_lines(board)
            if lines_cleared:
                score += lines_cleared * 10
            current_shape = next_shape
            next_shape = random.choice(SHAPES)
            current_shape_x = SCREEN_WIDTH // BLOCK_SIZE // 2 - len(current_shape[0]) // 2
            current_shape_y = 0
            shape_color = random.choice([RED, BLUE, GREEN, YELLOW, CYAN, MAGENTA])
            last_drop_time = pygame.time.get_ticks()

        for row_index, row in enumerate(board):
            for col_index, cell in enumerate(row):
                if cell:
                    draw_block(col_index, row_index, shape_color)

        draw_score(score)
        pygame.display.flip()
        clock.tick(FPS)

    pygame.quit()

if __name__ == "__main__":
    main()
