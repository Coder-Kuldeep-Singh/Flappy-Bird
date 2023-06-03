import pygame
import sys
import random

# Game Variables
SCREEN_WIDTH, SCREEN_HEIGHT = 400, 600
GRAVITY = 0.25
BIRD_JUMP = -8
GAP_SIZE = 150
PIPE_WIDTH = 100
PIPE_VELOCITY = 3
PIPE_FREQ = 1200  # The frequency of pipe generation (lower value -> more difficult)
# Set the timer for switching the background
BACKGROUND_SWITCH_TIME = 10000  # 10 seconds in milliseconds



class Bird(pygame.sprite.Sprite):
    def __init__(self, bird_image):
        super().__init__()
        self.image = bird_image
        self.rect = self.image.get_rect(center=(100, SCREEN_HEIGHT // 2))
        self.velocity = 0

    def update(self):
        self.velocity += GRAVITY
        self.rect.y += self.velocity

    def jump(self):
        self.velocity = BIRD_JUMP

class Pipe(pygame.sprite.Sprite):
    def __init__(self, position, pipe_image):
        super().__init__()
        self.image = pipe_image
        self.rect = self.image.get_rect(midbottom=position)

    def update(self):
        self.rect.x -= PIPE_VELOCITY
        if self.rect.right < 0:
            self.kill()

def create_pipe(pipe_image):
    gap_y = random.randint(GAP_SIZE + 50, SCREEN_HEIGHT - GAP_SIZE - 50)  # Random y-coordinate for the gap
    bottom_pipe = Pipe((SCREEN_WIDTH, SCREEN_HEIGHT), pipe_image)  # Bottom pipe starts from the bottom of the screen
    bottom_pipe.rect.top = gap_y + GAP_SIZE // 2  # Reset the top of the bottom pipe to the bottom of the gap
    top_pipe = Pipe((SCREEN_WIDTH, 0), pygame.transform.flip(pipe_image, False, True))  # Top pipe starts from the top of the screen
    top_pipe.rect.bottom = gap_y - GAP_SIZE // 2  # Reset the bottom of the top pipe to the top of the gap
    return bottom_pipe, top_pipe

def display_message(message):
    pygame.font.init()
    font = pygame.font.Font(None, 30)  # Adjust the size of the font as needed
    text = font.render(message, 1, (255, 255, 255))
    screen.blit(text, (SCREEN_WIDTH // 2 - text.get_width() // 2, SCREEN_HEIGHT // 2 - text.get_height() // 2))


def game_over():
    display_message("Game Over! Press any key to play again.")
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                main()

def pause():
    display_message("Paused. Press any key to continue.")
    pygame.display.update()
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.KEYDOWN:
                return

def main():
    global PIPE_FREQ

    score = 0

    bird_group = pygame.sprite.Group()
    pipe_group = pygame.sprite.Group()

    bird = Bird(bird_image)
    bird_group.add(bird)

    pygame.time.set_timer(pygame.USEREVENT, PIPE_FREQ)
    pygame.time.set_timer(pygame.USEREVENT + 1, BACKGROUND_SWITCH_TIME)

    while True:
        is_daytime = True  # Start with daytime
        for event in pygame.event.get():
            if event.type == pygame.USEREVENT + 1:
                is_daytime = not is_daytime  # Switch between day and night
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()
            if event.type == pygame.MOUSEBUTTONDOWN:
                bird.jump()
            if event.type == pygame.USEREVENT:
                pipes = create_pipe(pipe_image)
                pipe_group.add(pipes)
                score += 1  # Increase score when a new pipe is generated
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_p:  # Pause the game when 'p' is pressed
                    pause()

        if is_daytime:
            screen.blit(day_image, (0, 0))
        else:
            screen.blit(night_image, (0, 0))

        bird_group.draw(screen)
        bird_group.update()

        pipe_group.draw(screen)
        pipe_group.update()

        # Display the score
        score_display = score_font.render(str(score), True, (255, 255, 255))
        screen.blit(score_display, (SCREEN_WIDTH - 50, 50))

        # Collision
        if pygame.sprite.spritecollideany(bird_group.sprites()[0], pipe_group):
          game_over()
          
        # Collision with top or bottom of the screen
        if bird.rect.top <= 0 or bird.rect.bottom >= SCREEN_HEIGHT:
          game_over()

        pygame.display.update()
        clock.tick(120)

# Initialize Pygame
pygame.init()

# Create the game window
screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))

# Game Clock
clock = pygame.time.Clock()

# Load game sprites
bird_image = pygame.image.load('bird.png').convert_alpha()  # Add your path to bird image
pipe_image = pygame.image.load('pipe-green.png').convert_alpha()  # Add your path to pipe image
pipe_heights = [(i * 50) + 200 for i in range(5)]
day_image = pygame.image.load('background-day.png').convert()  # Add your path to day image
day_image = pygame.transform.scale(day_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
night_image = pygame.image.load('background-night.png').convert()  # Add your path to night image
night_image = pygame.transform.scale(night_image, (SCREEN_WIDTH, SCREEN_HEIGHT))


# Score font
score_font = pygame.font.Font(None, 50)

main()

