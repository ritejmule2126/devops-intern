import pygame
import random
import sys

# Initialize
pygame.init()

# Screen
WIDTH, HEIGHT = 800, 400
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Temple Run - Simple 2D")

# Colors
WHITE = (255, 255, 255)
BLACK = (255, 0, 0)
GOLD = (255, 215, 0)
RED = (200, 0, 0)

# Clock
clock = pygame.time.Clock()
FPS = 60

# Player
player_width, player_height = 40, 60
player_x, player_y = 100, HEIGHT - player_height - 50
player_vel_y = 0
gravity = 1
jump_power = -15
is_jumping = False

# Ground
ground_y = HEIGHT - 50

# Obstacles
obstacles = []
obstacle_width = 40
obstacle_height = 60
obstacle_speed = 8
spawn_rate = 1500  # milliseconds

# Score
score = 0
font = pygame.font.SysFont("Arial", 28)
pygame.time.set_timer(pygame.USEREVENT, spawn_rate)

def draw(player_rect, obstacles, score):
    screen.fill((80, 180, 80))
    pygame.draw.rect(screen, (50, 120, 50), (0, ground_y, WIDTH, 50))  # ground
    pygame.draw.rect(screen, GOLD, player_rect)
    for obs in obstacles:
        pygame.draw.rect(screen, RED, obs)
    score_text = font.render(f"Score: {score}", True, BLACK)
    screen.blit(score_text, (10, 10))
    pygame.display.update()

# Main loop
running = True
while running:
    clock.tick(FPS)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            pygame.quit()
            sys.exit()
        if event.type == pygame.USEREVENT:
            obs_x = WIDTH + random.randint(0, 200)
            obs_y = ground_y - obstacle_height
            obstacles.append(pygame.Rect(obs_x, obs_y, obstacle_width, obstacle_height))
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE and not is_jumping:
                player_vel_y = jump_power
                is_jumping = True

    # Player physics
    player_vel_y += gravity
    player_y += player_vel_y
    if player_y >= ground_y - player_height:
        player_y = ground_y - player_height
        is_jumping = False

    player_rect = pygame.Rect(player_x, player_y, player_width, player_height)

    # Move obstacles
    for obs in obstacles:
        obs.x -= obstacle_speed

    # Remove off-screen obstacles
    obstacles = [obs for obs in obstacles if obs.x + obstacle_width > 0]

    # Collision detection
    for obs in obstacles:
        if player_rect.colliderect(obs):
            pygame.quit()
            print(f"💀 Game Over! Final Score: {score}")
            sys.exit()

    # Increase score
    score += 1

    # Draw everything
    draw(player_rect, obstacles, score)
