import pygame
import random

# Initialize Pygame
pygame.init()

# Set up the game window
width, height = 640, 480
screen = pygame.display.set_mode((width, height))
pygame.display.set_caption("Snake Game")

# Define colors
black = (0, 0, 0)
white = (255, 255, 255)
red = (255, 0, 0)

# Set up the game clock
clock = pygame.time.Clock()

# Define the Snake class
class Snake:
    def __init__(self):
        self.size = 1
        self.elements = [[100, 100]]
        self.direction = "right"
        self.speed = 5

    def draw(self):
        for i, element in enumerate(self.elements):
            color = (255 - (255 * i // self.size), 255 - (255 * i // self.size), 255 - (255 * i // self.size))
            pygame.draw.rect(screen, color, (element[0], element[1], 10, 10))

    def move(self):
        head = self.elements[0]
        if self.direction == "right":
            new_head = [head[0] + self.speed, head[1]]
        elif self.direction == "left":
            new_head = [head[0] - self.speed, head[1]]
        elif self.direction == "up":
            new_head = [head[0], head[1] - self.speed]
        elif self.direction == "down":
            new_head = [head[0], head[1] + self.speed]

        self.elements.insert(0, new_head)
        if len(self.elements) > self.size:
            self.elements.pop()

    def grow(self):
        self.size += 1
        self.speed += 0.5

    def collides_with(self, food):
        head = self.elements[0]
        return head[0] < food.position[0] + 10 and head[0] + 10 > food.position[0] and head[1] < food.position[1] + 10 and head[1] + 10 > food.position[1]

# Define the Food class
class Food:
    def __init__(self):
        self.position = [random.randrange(0, width - 10, 10), random.randrange(0, height - 10, 10)]

    def draw(self):
        pygame.draw.rect(screen, red, (self.position[0], self.position[1], 10, 10))

# Set up the game objects
snake = Snake()
food = Food()
score = 0

# Game loop
running = True
game_over = False
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_RIGHT and snake.direction != "left":
                snake.direction = "right"
            elif event.key == pygame.K_LEFT and snake.direction != "right":
                snake.direction = "left"
            elif event.key == pygame.K_UP and snake.direction != "down":
                snake.direction = "up"
            elif event.key == pygame.K_DOWN and snake.direction != "up":
                snake.direction = "down"
            elif event.key == pygame.K_SPACE and game_over:
                game_over = False
                snake = Snake()
                food = Food()
                score = 0

    screen.fill(black)

    if not game_over:
        snake.move()
        snake.draw()
        food.draw()

        if snake.collides_with(food):
            snake.grow()
            food = Food()
            score += 1

        if snake.elements[0][0] < 0 or snake.elements[0][0] >= width or snake.elements[0][1] < 0 or snake.elements[0][1] >= height:
            game_over = True
    else:
        font = pygame.font.Font(None, 36)
        text = font.render("Game Over! Press Space to Retry", True, white)
        text_rect = text.get_rect(center=(width // 2, height // 2))
        screen.blit(text, text_rect)

    font = pygame.font.Font(None, 24)
    score_text = font.render("Score: " + str(score), True, white)
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
