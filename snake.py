import pygame
import random
from pygame.locals import *

# ==== GERA POSIÇÃO ALEATÓRIA NO GRID ====
def on_grid_random():
  x = random.randint(0, 59)
  y = random.randint(0, 59)
  return (x * 10, y * 10) # para uma posição múltipla de 10 para um perfeito alinhamento da cobra e da maçã

# ==== VERIFICA COLISÕES ENTRES CÉLULAS ====
def collision(c1, c2):
  return (c1[0] == c2[0]) and (c1[1] == c2[1])

# Função para reiniciar o jogo
def restart_game():
  global snake
  global apple_pos
  global my_direction
  snake = [(200, 200), (210, 200), (220, 200)]
  my_direction = K_LEFT
  apple_pos = on_grid_random()

# ==== DIREÇÕES ====
UP = 0
RIGHT = 1
DOWN = 2
LEFT = 3

# ==== INÍCIO ====
pygame.init()
# ==== JANELA ====
screen = pygame.display.set_mode((600, 600))
pygame.display.set_caption('Snake')

# ==== COBRA ====
snake = [(200, 200), (210, 200), (220, 200)]
snake_skin = pygame.Surface((10, 10))
snake_skin.fill((255, 255, 255))  # Cor da cobra
# direção inicial da cobra
my_direction = LEFT

# ==== MAÇÃ ====
apple_pos = on_grid_random()
apple = pygame.Surface((10, 10))
apple.fill((255, 0, 0))

clock = pygame.time.Clock()                     # Variável para limitar o FPS
font = pygame.font.Font('freesansbold.ttf', 18) # Variável para fonte
score = 0                                       # Variável para a pontuação

game_over = False
# ==== LOOP ====
while not game_over:
  clock.tick(15) # Para limitar o FPS
  # ==== EVENTOS ====
  for event in pygame.event.get():
    # ==== evento de fechar jogo ====
    if event.type == QUIT:
      pygame.quit()
    # ==== para controlar o movimento ====
    if event.type == KEYDOWN:
      if event.key == K_UP and my_direction != DOWN:
        my_direction = UP
      if event.key == K_DOWN and my_direction != UP:
        my_direction = DOWN
      if event.key == K_LEFT and my_direction != RIGHT:
        my_direction = LEFT
      if event.key == K_RIGHT and my_direction != LEFT:
        my_direction = RIGHT

  # ==== TESTANDO COLISÃO ====
  if collision(snake[0], apple_pos):
    apple_pos = on_grid_random() # gera nova posição para a maçã
    snake.append((0, 0))         # gera nova posição para a cobra
    score = score + 1            # pontuação

  # ==== Checa se a cobra colidiu com as bordas da janela ====
  if snake[0][0] == 600 or snake[0][1] == 600 or snake[0][0] < 0 or snake[0][1] < 0:
    game_over = True
    break

  # ==== Checa se a cobra colidiu consigo mesma =====
  for i in range(1, len(snake) - 1):
    if snake[0][0] == snake[i][0] and snake[0][1] == snake[i][1]:
      game_over = True
      break

  if game_over:
    break

  # ==== movimento do corpo da cobra ====
  for i in range(len(snake) - 1, 0, - 1):
    snake[i] = (snake[i - 1][0], snake[i - 1][1])

  # ==== movimento controlado da cobra ====
  if my_direction == UP:
    snake[0] = (snake[0][0], snake[0][1] - 10)
  if my_direction == DOWN:
    snake[0] = (snake[0][0], snake[0][1] + 10)
  if my_direction == RIGHT:
    snake[0] = (snake[0][0] + 10, snake[0][1])
  if my_direction == LEFT:
    snake[0] = (snake[0][0] - 10, snake[0][1])

  screen.fill((0, 0, 0))
  screen.blit(apple, apple_pos)

  for x in range(0, 600, 10):  # Cria linhas horizontais
    pygame.draw.line(screen, (40, 40, 40), (x, 0), (x, 600))
  for y in range(0, 600, 10):  # Cria linhas verticais
    pygame.draw.line(screen, (40, 40, 40), (0, y), (600, y))

  # Marcação de pontuação
  score_font = font.render('Score: %s' % (score), True, (255, 255, 255))
  score_rect = score_font.get_rect()
  score_rect.topleft = (600 - 120, 10)
  screen.blit(score_font, score_rect)

  for pos in snake:
    screen.blit(snake_skin, pos)  # Plotar a cobra

  pygame.display.update()

while True:
    game_over_font = pygame.font.Font('freesansbold.ttf', 75)
    game_over_screen = game_over_font.render('Game Over', True, (255, 255, 255))
    game_over_rect = game_over_screen.get_rect()
    game_over_rect.midtop = (600 / 2, 10)
    screen.blit(game_over_screen, game_over_rect)
    pygame.display.update()
    pygame.time.wait(500)
    while True:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
