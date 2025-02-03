import pygame
import random
import math
from pygame.math import Vector2

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
screen = pygame.display.set_mode((0, 0), pygame.FULLSCREEN)
screen_size = screen.get_size()
pygame.display.set_caption('COBRINHA')

def get_direction_and_distance(target:Vector2, self_pos:Vector2):
    direction = target - self_pos
    distance = direction.length()

    return (direction, distance)

# Comida
class Food():
    def __init__(self, screen:pygame.Surface, pos:Vector2, color=WHITE):
        self.screen = screen
        self.pos = pos
        self.color = color
        self.radius = 10
        self.eaten = False
    
    def draw(self):
        if not self.eaten:
            pygame.draw.circle(self.screen, self.color, self.pos, self.radius)

# Cada segmento da cobra
class Segments:
    def __init__(self, screen:pygame.Surface, head:bool, radius:int, pos:Vector2, color=WHITE):
        self.screen = screen
        self.ishead = head
        self.radius = radius
        self.color = color
        self.pos = pos
    
    def draw(self):
        pygame.draw.circle(self.screen, self.color, self.pos, self.radius, self.radius // 8)


    # Colisão do Segmento
    def collision(self, target:Food):
        screen_size = self.screen.get_size()

        distance = get_direction_and_distance(target.pos, self.pos)[1]

        if distance <= target.radius + self.radius and self.ishead:
            target.eaten = True
            

        if self.pos.x > self.radius or self.pos.x < screen_size[0] - self.radius:
            self.pos.x = max(self.radius, min(self.pos.x, screen_size[0] - self.radius))
        if self.pos.y < self.radius or self.pos.y > screen_size[1] - self.radius:
            self.pos.y = max(self.radius, min(self.pos.y, screen_size[1] - self.radius))

    # Faz o segmento seguir determinado objeto
    def move(self, target:Vector2, easing=0.5):
        direction, distance = get_direction_and_distance(target, self.pos)

        if distance > self.radius:
            self.pos += direction * easing


# Criar o corpo da cobra
def create_body(screen:pygame.Surface, size:int, radius:int):
    screen_size = screen.get_size()
    pos = Vector2(random.randint(50, screen_size[0] - 50), random.randint(50, screen_size[1] - 50))
    snake = [Segments(screen, True, radius, pos)]

    for i in range(size):
        new_pos = pos - Vector2(i * radius * 1.5, 0)
        snake.append(Segments(screen, False, radius - i, new_pos))
    
    return snake

def main():
    pygame.init()
    pygame.font.init()
    font = pygame.font.Font(None, 36)
    snake = create_body(screen, 0, 20)
    food = Food(screen, Vector2(random.randint(50, screen_size[0] - 50), random.randint(50, screen_size[1] - 50)))
    clock = pygame.time.Clock()
    running = True
    eat_count = 0

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
        
        mouse_pos = Vector2(pygame.mouse.get_pos())
        screen.fill(BLACK)

        for i, segment in enumerate(snake):
            segment.collision(food)
            if segment.ishead:
                segment.move(mouse_pos, easing=0.03)
            else:
                segment.move(snake[i-1].pos)
            if food.eaten:
                snake.append(Segments(screen, False, snake[i-1].radius, Vector2(0, 0)))
                food.pos = Vector2(random.randint(50, screen_size[0] - 50), random.randint(50, screen_size[1] - 50))
                food.eaten = False
                eat_count += 1
            segment.draw()
        food.draw()
        text_surface = font.render(f"Comeu {eat_count}", True, WHITE)
        screen.blit(text_surface, (screen_size[0] // 2.1, screen_size[1] - 50))
        
        pygame.display.flip()
        clock.tick(60)


if __name__ == "__main__":
    main()