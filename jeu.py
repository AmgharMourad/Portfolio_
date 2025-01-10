import pygame
import random

# Initialiser Pygame
pygame.init()

# Dimensions de la fenêtre
WIDTH, HEIGHT = 800, 600
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Jeu de Parcours")

# Couleurs
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 0, 0)
GREEN = (0, 255, 0)
BLUE = (0, 0, 255)

# Constantes
PLAYER_SIZE = 30
OBSTACLE_SIZE = 30
TARGET_SIZE = 40
PLAYER_SPEED = 5
OBSTACLE_SPEED = 3

# Initialiser le joueur
player = {'x': 50, 'y': HEIGHT // 2, 'width': PLAYER_SIZE, 'height': PLAYER_SIZE}

# Initialiser les obstacles
def create_obstacles(num):
    obstacles = []
    for _ in range(num):
        obstacles.append({
            'x': random.randint(100, WIDTH - OBSTACLE_SIZE),
            'y': random.randint(0, HEIGHT - OBSTACLE_SIZE),
            'width': OBSTACLE_SIZE,
            'height': OBSTACLE_SIZE,
            'dx': random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED]),
            'dy': random.choice([-OBSTACLE_SPEED, OBSTACLE_SPEED])
        })
    return obstacles

obstacles = create_obstacles(5)

# Initialiser la cible
target = {'x': WIDTH - TARGET_SIZE - 20, 'y': random.randint(0, HEIGHT - TARGET_SIZE), 'width': TARGET_SIZE, 'height': TARGET_SIZE}

# Jeu principal
def main():
    clock = pygame.time.Clock()
    running = True

    while running:
        window.fill(WHITE)

        # Gérer les événements
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False

        # Récupérer les touches pressées
        keys = pygame.key.get_pressed()
        if keys[pygame.K_UP] and player['y'] > 0:
            player['y'] -= PLAYER_SPEED
        if keys[pygame.K_DOWN] and player['y'] < HEIGHT - PLAYER_SIZE:
            player['y'] += PLAYER_SPEED
        if keys[pygame.K_LEFT] and player['x'] > 0:
            player['x'] -= PLAYER_SPEED
        if keys[pygame.K_RIGHT] and player['x'] < WIDTH - PLAYER_SIZE:
            player['x'] += PLAYER_SPEED

        # Mettre à jour les obstacles
        for obstacle in obstacles:
            obstacle['x'] += obstacle['dx']
            obstacle['y'] += obstacle['dy']

            # Rebonds sur les bords
            if obstacle['x'] <= 0 or obstacle['x'] >= WIDTH - OBSTACLE_SIZE:
                obstacle['dx'] *= -1
            if obstacle['y'] <= 0 or obstacle['y'] >= HEIGHT - OBSTACLE_SIZE:
                obstacle['dy'] *= -1

        # Dessiner le joueur
        pygame.draw.rect(window, BLUE, (player['x'], player['y'], player['width'], player['height']))

        # Dessiner les obstacles
        for obstacle in obstacles:
            pygame.draw.rect(window, RED, (obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height']))

        # Dessiner la cible
        pygame.draw.rect(window, GREEN, (target['x'], target['y'], target['width'], target['height']))

        # Vérifier les collisions avec les obstacles
        player_rect = pygame.Rect(player['x'], player['y'], player['width'], player['height'])
        for obstacle in obstacles:
            obstacle_rect = pygame.Rect(obstacle['x'], obstacle['y'], obstacle['width'], obstacle['height'])
            if player_rect.colliderect(obstacle_rect):
                font = pygame.font.Font(None, 74)
                text = font.render("Perdu !", True, RED)
                window.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
                pygame.display.flip()
                pygame.time.wait(2000)
                running = False

        # Vérifier si le joueur atteint la cible
        target_rect = pygame.Rect(target['x'], target['y'], target['width'], target['height'])
        if player_rect.colliderect(target_rect):
            font = pygame.font.Font(None, 74)
            text = font.render("Gagné !", True, GREEN)
            window.blit(text, (WIDTH // 2 - 100, HEIGHT // 2 - 50))
            pygame.display.flip()
            pygame.time.wait(2000)
            running = False

        # Mettre à jour l'écran
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()
