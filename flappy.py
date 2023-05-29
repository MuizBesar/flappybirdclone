import pygame
import random

# Game dimensions
WIDTH = 288
HEIGHT = 512

# Bird dimensions
BIRD_WIDTH = 34
BIRD_HEIGHT = 24

# Pipe dimensions
PIPE_WIDTH = 52
PIPE_HEIGHT = 320
PIPE_GAP = 100
PIPE_VELOCITY = 2

# Colors
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)

# Initialize Pygame
pygame.init()

# Create the game window
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Flappy Bird")

# Load images
bird_img = pygame.image.load("bird.png")
pipe_img = pygame.image.load("pipe.png")
background_img = pygame.image.load("background.png")

# Scale images
bird_img = pygame.transform.scale(bird_img, (BIRD_WIDTH, BIRD_HEIGHT))
pipe_img = pygame.transform.scale(pipe_img, (PIPE_WIDTH, PIPE_HEIGHT))

# Rotate the top pipe image vertically
flipped_pipe_img = pygame.transform.rotate(pipe_img, 180)

# Bird class
class Bird(pygame.sprite.Sprite):
    def __init__(self):
        super().__init__()
        self.image = bird_img
        self.rect = self.image.get_rect()
        self.rect.x = 50
        self.rect.y = HEIGHT // 2
        self.velocity = 0

        # Adjust the hitbox size
        self.rect.width = 24
        self.rect.height = 18

    def update(self):
        self.velocity += 0.2
        self.rect.y += self.velocity

    def flap(self):
        self.velocity = -4

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))
        
# Pipe class
class Pipe(pygame.sprite.Sprite):
    def __init__(self, x, y, flipped=False):
        super().__init__()
        if flipped:
            self.image = flipped_pipe_img
        else:
            self.image = pipe_img
        self.rect = self.image.get_rect()
        self.rect.x = x
        self.rect.y = y
        self.passed = False

    def update(self):
        self.rect.x -= PIPE_VELOCITY

    def draw(self, window):
        window.blit(self.image, (self.rect.x, self.rect.y))

# Score class
class Score:
    def __init__(self):
        self.value = 0
        self.font = pygame.font.Font(None, 50)
        self.text = self.font.render(str(self.value), True, WHITE)
        self.rect = self.text.get_rect(center=(WIDTH // 2, 50))

    def increment(self):
        self.value += 0.5
        self.text = self.font.render(str(self.value), True, WHITE)

    def draw(self, window):
        window.blit(self.text, self.rect)

# Create bird, pipes, and score
bird = Bird()
pipes = pygame.sprite.Group()
spawn_pipe_event = pygame.USEREVENT + 1
pygame.time.set_timer(spawn_pipe_event, 1500)
score = Score()

# Game loop
clock = pygame.time.Clock()
running = True

while running:
    clock.tick(60)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                bird.flap()
        elif event.type == spawn_pipe_event:
            gap_y = random.randint(50, HEIGHT - PIPE_GAP - 50)
            top_pipe = Pipe(WIDTH, gap_y - PIPE_HEIGHT, flipped=True)
            bottom_pipe = Pipe(WIDTH, gap_y + PIPE_GAP)
            pipes.add(top_pipe, bottom_pipe)

    window.blit(background_img, (0, 0))

    bird.update()
    bird.draw(window)

    if pygame.sprite.spritecollide(bird, pipes, False):
        running = False

    if bird.rect.y > HEIGHT or bird.rect.y < 0:
        running = False

    pipes.update()
    pipes.draw(window)

    # Check if bird passes through a pair of pipes
    for pipe in pipes:
        if pipe.rect.right < bird.rect.left and not pipe.passed:
            pipe.passed = True
            score.increment()

    score.draw(window)

    pygame.display.flip()

# Quit the game
pygame.quit()
