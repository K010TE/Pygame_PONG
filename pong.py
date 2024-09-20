import pygame
import sys

# Inicializando o Pygame
pygame.init()

# Definindo as cores
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
YELLOW = (255, 255, 0)

# Definindo as dimensões da tela
SCREEN_WIDTH = 800
SCREEN_HEIGHT = 600
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Pong")

# Definindo a velocidade do jogo
FPS = 60
clock = pygame.time.Clock()

# Definindo as propriedades do paddle (jogador)
PADDLE_WIDTH = 100
PADDLE_HEIGHT = 10
paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
paddle_y = SCREEN_HEIGHT - 40
paddle_speed = 7

# Definindo a bola
BALL_SIZE = 15
ball_x = paddle_x + PADDLE_WIDTH // 2  # Centraliza a bola inicialmente no paddle
ball_y = paddle_y - BALL_SIZE
ball_dx = 0
ball_dy = 0
initial_ball_speed = 5  # Velocidade inicial da bola
ball_speed = initial_ball_speed
speed_increment = 0.3  # Valor de incremento da velocidade

# Definindo o placar e vidas
score = 0
lives = 3
font = pygame.font.SysFont(None, 36)
large_font = pygame.font.SysFont(None, 72)

# Estados do jogo
game_active = False
game_over = False
menu_active = True  # Controla a exibição da tela de menu

# Função para desenhar o paddle
def draw_paddle(x, y):
    pygame.draw.rect(screen, WHITE, [x, y, PADDLE_WIDTH, PADDLE_HEIGHT])

# Função para desenhar a bola
def draw_ball(x, y):
    pygame.draw.circle(screen, WHITE, (x, y), BALL_SIZE)

# Função para exibir o placar
def draw_score():
    score_text = font.render(f"Score: {score}", True, WHITE)
    lives_text = font.render(f"Lives: {lives}", True, WHITE)
    screen.blit(score_text, (20, 10))
    screen.blit(lives_text, (SCREEN_WIDTH - 150, 10))

# Função para a tela de menu
def menu_screen():
    screen.fill(BLACK)

    # Título do jogo
    title = large_font.render("PONG", True, WHITE)
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, SCREEN_HEIGHT // 3))

    # Créditos
    credits = font.render("Desenvolvido por Itagiba Neto", True, WHITE)
    screen.blit(credits, (SCREEN_WIDTH // 2 - credits.get_width() // 2, SCREEN_HEIGHT - 50))

    # Botão "INICIAR"
    mouse_x, mouse_y = pygame.mouse.get_pos()
    
    # Fonte normal do botão
    font_normal = pygame.font.SysFont(None, 36)
    font_hover = pygame.font.SysFont(None, 48)

    # Texto padrão
    start_text = font_normal.render("INICIAR", True, WHITE)
    
    # Definir um retângulo maior para o botão "INICIAR"
    start_rect = pygame.Rect(SCREEN_WIDTH // 2 - 100, SCREEN_HEIGHT // 2 - 25, 400, 150)  # Área maior do click
    
    # Posição e tamanho do retângulo com base no tamanho do texto "INICIAR"
    start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))

    # Verificar se o mouse está sobre o retângulo do botão "INICIAR"
    if start_rect.collidepoint(mouse_x, mouse_y):
        # Se o mouse está sobre o texto, usa fonte maior e cor amarela
        start_text = font_hover.render("INICIAR", True, YELLOW)
        start_rect = start_text.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2))  # Recalcula o retângulo


    # Desenhar o texto "INICIAR" dentro do retângulo recalculado
    screen.blit(start_text, (start_rect.x, start_rect.y))

    pygame.display.flip()

# Função para a tela de game over
def game_over_screen():
    screen.fill(BLACK)
    game_over_text = font.render("GAME OVER", True, RED)
    restart_text = font.render("Pressione ESPAÇO ou click do mouse para ir ao menu", True, WHITE)
    screen.blit(game_over_text, (SCREEN_WIDTH // 2 - game_over_text.get_width() // 2, SCREEN_HEIGHT // 3))
    screen.blit(restart_text, (SCREEN_WIDTH // 2 - restart_text.get_width() // 2, SCREEN_HEIGHT // 2))
    pygame.display.flip()

# Função para resetar o jogo
def reset_game():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, score, lives, game_active, game_over, menu_active, ball_speed
    paddle_x = (SCREEN_WIDTH - PADDLE_WIDTH) // 2
    ball_x = paddle_x + PADDLE_WIDTH // 2  # Centraliza a bola no paddle
    ball_y = paddle_y - BALL_SIZE
    ball_dx = 0
    ball_dy = 0
    score = 0
    lives = 3
    ball_speed = initial_ball_speed  # Resetar a velocidade da bola
    game_active = False
    game_over = False
    menu_active = True

# Função para centralizar a bola no paddle
def center_ball_on_paddle():
    global ball_x, ball_y
    ball_x = paddle_x + PADDLE_WIDTH // 2
    ball_y = paddle_y - BALL_SIZE

# Função para iniciar o jogo
def start_game():
    global ball_dx, ball_dy, game_active
    if ball_dx == 0 and ball_dy == 0:  # Apenas redefinir velocidade da bola se for o início do jogo
        ball_dx = ball_speed
        ball_dy = -ball_speed  # Bola começará sempre subindo
    else:
        ball_dy = -abs(ball_dy)  # Garantir que a bola sempre comece subindo

    game_active = True

# Loop principal do jogo
def game_loop():
    global paddle_x, ball_x, ball_y, ball_dx, ball_dy, score, lives, game_active, game_over, menu_active

    while True:
        screen.fill(BLACK)

        # Eventos do jogo
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and not game_active and not game_over:
                    if menu_active:
                        menu_active = False
                        center_ball_on_paddle()
                    else:
                        start_game()
                elif event.key == pygame.K_SPACE and game_over:
                    reset_game()
            if event.type == pygame.MOUSEBUTTONDOWN:
                if event.button == 1:  # Botão esquerdo do mouse
                    if not game_active and not game_over:
                        if menu_active:
                            menu_active = False
                            center_ball_on_paddle()
                        else:
                            start_game()
                    elif game_over:
                        reset_game()

        # Movimentação do paddle com mouse
        mouse_x, _ = pygame.mouse.get_pos()
        paddle_x = mouse_x - PADDLE_WIDTH // 2

        # Centralizar a bola no paddle
        if not game_active:
            center_ball_on_paddle()

        # Limitar o movimento do paddle dentro da tela
        if paddle_x < 0:
            paddle_x = 0
        elif paddle_x + PADDLE_WIDTH > SCREEN_WIDTH:
            paddle_x = SCREEN_WIDTH - PADDLE_WIDTH

        # Se o jogo estiver ativo, mover a bola
        if game_active:
            ball_x += ball_dx
            ball_y += ball_dy

            # Colisão com as paredes
            if ball_x - BALL_SIZE < 0 or ball_x + BALL_SIZE > SCREEN_WIDTH:
                ball_dx = -ball_dx
            if ball_y - BALL_SIZE < 0:
                ball_dy = -ball_dy

            # Colisão com o paddle
            if paddle_y < ball_y + BALL_SIZE < paddle_y + PADDLE_HEIGHT and paddle_x < ball_x < paddle_x + PADDLE_WIDTH:
                ball_dy = -ball_dy
                score += 1
                

                # Aumentar a velocidade da bola após colisão com o paddle
                if ball_dx > 0:
                    ball_dx += speed_increment
                else:
                    ball_dx -= speed_increment

                if ball_dy > 0:
                    ball_dy += speed_increment
                else:
                    ball_dy -= speed_increment
                    

            # Se a bola passar pelo paddle, perder uma vida
            if ball_y > SCREEN_HEIGHT:
                lives -= 1
                center_ball_on_paddle()  # Centraliza a bola no paddle
                game_active = False  # Não redefine a velocidade da bola aqui

            # Verificar se o jogador perdeu
            if lives <= 0:
                game_over = True
                game_active = False

        # Desenhar paddle, bola e placar
        draw_paddle(paddle_x, paddle_y)
        draw_ball(ball_x, ball_y)
        draw_score()

        # Exibir tela de menu ou game over
        if menu_active:
            menu_screen()
        elif game_over:
            game_over_screen()

        # Atualizar a tela
        pygame.display.flip()
        clock.tick(FPS)

if __name__ == "__main__":
    game_loop()
