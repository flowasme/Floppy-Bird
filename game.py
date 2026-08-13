import pygame, random, time, sys, os
from pygame.locals import *
import cv2
import numpy as np
import hands  

# VARIABLES
SCREEN_WIDHT = 400
CAM_WIDTH = 640 
SCREEN_HEIGHT = 600
TOTAL_WIDTH = SCREEN_WIDHT + CAM_WIDTH 

# Calculate proper 16:9 camera height and vertical offset for letterboxing
CAM_HEIGHT = int(CAM_WIDTH * (720 / 1280)) 
CAM_Y_OFFSET = (SCREEN_HEIGHT - CAM_HEIGHT) // 2 

SPEED = 20
GRAVITY = 2.5
GAME_SPEED = 15

GROUND_WIDHT = 2 * SCREEN_WIDHT
GROUND_HEIGHT= 100

PIPE_WIDHT = 80
PIPE_HEIGHT = 500

PIPE_GAP = 150

pygame.mixer.init()

# AUDIO VARIABLES
wing_sound = pygame.mixer.Sound('assets/audio/wing.wav')
hit_sound = pygame.mixer.Sound('assets/audio/hit.wav')

if os.path.exists('assets/audio/point.wav'):
    point_sound = pygame.mixer.Sound('assets/audio/point.wav')
else:
    point_sound = pygame.mixer.Sound('assets/audio/point.ogg')

theme_song = 'assets/audio/theme_song.mp3'

# HIGHSCORE FILE LOGIC
def get_highscore():
    if os.path.exists("highscore.txt"):
        with open("highscore.txt", "r") as file:
            try:
                return int(file.read())
            except:
                return 0
    return 0

def save_highscore(score_to_save):
    with open("highscore.txt", "w") as file:
        file.write(str(score_to_save))

# SPRITES & SCORE RENDERING
pygame.init()
screen = pygame.display.set_mode((TOTAL_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption('Flappy Bird Tracking')

BACKGROUND = pygame.image.load('assets/sprites/background-day.png')
BACKGROUND = pygame.transform.scale(BACKGROUND, (SCREEN_WIDHT, SCREEN_HEIGHT))
BEGIN_IMAGE = pygame.image.load('assets/sprites/message.png').convert_alpha()
GAMEOVER_IMAGE = pygame.image.load('assets/sprites/gameover.png').convert_alpha()

# Load Number Sprites 0-9
NUMBER_SPRITES = [pygame.image.load(f'assets/sprites/{i}.png').convert_alpha() for i in range(10)]

def draw_score(surface, score_val, center_x, top_y):
    score_str = str(score_val)
    total_width = sum([NUMBER_SPRITES[int(char)].get_width() for char in score_str])
    current_x = center_x - total_width // 2
    for char in score_str:
        img = NUMBER_SPRITES[int(char)]
        surface.blit(img, (current_x, top_y))
        current_x += img.get_width()


class Bird(pygame.sprite.Sprite):
    def __init__(self):
        pygame.sprite.Sprite.__init__(self)
        self.images =  [pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-midflap.png').convert_alpha(),
                        pygame.image.load('assets/sprites/bluebird-downflap.png').convert_alpha()]
        self.speed = SPEED
        self.current_image = 0
        self.image = pygame.image.load('assets/sprites/bluebird-upflap.png').convert_alpha()
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = SCREEN_WIDHT / 6
        self.rect[1] = SCREEN_HEIGHT / 2

    def update(self, target_y=None):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]
        if target_y is not None:
            self.rect[1] = target_y
        else:
            self.speed += GRAVITY
            self.rect[1] += self.speed

    def bump(self):
        self.speed = -SPEED

    def begin(self):
        self.current_image = (self.current_image + 1) % 3
        self.image = self.images[self.current_image]


class Pipe(pygame.sprite.Sprite):
    def __init__(self, inverted, xpos, ysize):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/pipe-green.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (PIPE_WIDHT, PIPE_HEIGHT))
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.inverted = inverted
        self.passed = False 

        if inverted:
            self.image = pygame.transform.flip(self.image, False, True)
            self.rect[1] = - (self.rect[3] - ysize)
        else:
            self.rect[1] = SCREEN_HEIGHT - ysize

        self.mask = pygame.mask.from_surface(self.image)

    def update(self):
        self.rect[0] -= GAME_SPEED


class Ground(pygame.sprite.Sprite):
    def __init__(self, xpos):
        pygame.sprite.Sprite.__init__(self)
        self.image = pygame.image.load('assets/sprites/base.png').convert_alpha()
        self.image = pygame.transform.scale(self.image, (GROUND_WIDHT, GROUND_HEIGHT))
        self.mask = pygame.mask.from_surface(self.image)
        self.rect = self.image.get_rect()
        self.rect[0] = xpos
        self.rect[1] = SCREEN_HEIGHT - GROUND_HEIGHT
        
    def update(self):
        self.rect[0] -= GAME_SPEED


def is_off_screen(sprite):
    return sprite.rect[0] < -(sprite.rect[2])

def get_random_pipes(xpos):
    size = random.randint(100, 300)
    pipe = Pipe(False, xpos, size)
    pipe_inverted = Pipe(True, xpos, SCREEN_HEIGHT - size - PIPE_GAP)
    return pipe, pipe_inverted

def reset_game():
    bird.rect[0] = SCREEN_WIDHT / 6
    bird.rect[1] = SCREEN_HEIGHT / 2
    bird.speed = SPEED
    bird.current_image = 0
    pipe_group.empty()
    for i in range(2):
        pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
        pipe_group.add(pipes[0])
        pipe_group.add(pipes[1])
    return 0


# GROUPS SETUP
bird_group = pygame.sprite.Group()
bird = Bird()
bird_group.add(bird)

ground_group = pygame.sprite.Group()
for i in range (2):
    ground = Ground(GROUND_WIDHT * i)
    ground_group.add(ground)

pipe_group = pygame.sprite.Group()
for i in range (2):
    pipes = get_random_pipes(SCREEN_WIDHT * i + 800)
    pipe_group.add(pipes[0])
    pipe_group.add(pipes[1])

clock = pygame.time.Clock()

# INITIAL STATES
score = 0
high_score = get_highscore()
state = "WAIT" # The game loops through "WAIT", "PLAY", and "GAMEOVER" states

while True:
    clock.tick(15)
    
    # Process camera logic first regardless of game state
    target_y = None
    success, cam_frame, coords = hands.process_frame()
    if success and coords is not None:
        target_y = int((coords[1] / hands.h) * SCREEN_HEIGHT)

    # Event handling based on state
    for event in pygame.event.get():
        if event.type == QUIT:
            hands.release_camera()
            pygame.quit()
            sys.exit()
        if event.type == KEYDOWN:
            if event.key == K_SPACE or event.key == K_UP:
                if state == "WAIT":
                    bird.bump()
                    wing_sound.play()
                    state = "PLAY"
                    pygame.mixer.music.load(theme_song)
                    pygame.mixer.music.play(-1)
                elif state == "PLAY":
                    bird.bump()
                    wing_sound.play()
                elif state == "GAMEOVER":
                    score = reset_game()
                    state = "WAIT"

    # Always draw background on the left
    screen.blit(BACKGROUND, (0, 0))

    # --- STATE: WAIT SCREEN ---
    if state == "WAIT":
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        bird.begin()
        ground_group.update()

        bird_group.draw(screen)
        ground_group.draw(screen)
        screen.blit(BEGIN_IMAGE, (120, 150))
        
        # Draw highscore at the top using sprites
        draw_score(screen, high_score, SCREEN_WIDHT // 2, 50)

    # --- STATE: PLAYING ---
    elif state == "PLAY":
        if is_off_screen(ground_group.sprites()[0]):
            ground_group.remove(ground_group.sprites()[0])
            new_ground = Ground(GROUND_WIDHT - 20)
            ground_group.add(new_ground)

        if is_off_screen(pipe_group.sprites()[0]):
            pipe_group.remove(pipe_group.sprites()[0])
            pipe_group.remove(pipe_group.sprites()[0])
            pipes = get_random_pipes(SCREEN_WIDHT * 2)
            pipe_group.add(pipes[0])
            pipe_group.add(pipes[1])

        # Check Score
        for pipe in pipe_group:
            if not pipe.inverted and not pipe.passed: 
                if pipe.rect[0] + PIPE_WIDHT < bird.rect[0]:
                    pipe.passed = True
                    score += 1
                    point_sound.play()

        bird.update(target_y)
        ground_group.update()
        pipe_group.update()

        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)

        # Draw current score using sprites
        draw_score(screen, score, SCREEN_WIDHT // 2, 50)

        # Collision Check
        if (pygame.sprite.groupcollide(bird_group, ground_group, False, False, pygame.sprite.collide_mask) or
                pygame.sprite.groupcollide(bird_group, pipe_group, False, False, pygame.sprite.collide_mask)):
            pygame.mixer.music.stop() 
            hit_sound.play()
            
            # Highscore logic
            if score > high_score:
                high_score = score
                save_highscore(high_score)
                
            state = "GAMEOVER"

    # --- STATE: GAME OVER ---
    elif state == "GAMEOVER":
        # Draw static elements in the background
        pipe_group.draw(screen)
        ground_group.draw(screen)
        bird_group.draw(screen)

        # Draw GAMEOVER overlay centered
        go_rect = GAMEOVER_IMAGE.get_rect(center=(SCREEN_WIDHT // 2, SCREEN_HEIGHT // 3))
        screen.blit(GAMEOVER_IMAGE, go_rect)

        # Draw Score and Highscore using sprites
        draw_score(screen, score, SCREEN_WIDHT // 2, SCREEN_HEIGHT // 2)
        draw_score(screen, high_score, SCREEN_WIDHT // 2, SCREEN_HEIGHT // 2 + 50)


    # Obscure the right side with solid black (fixes z-index issue and creates letterbox)
    pygame.draw.rect(screen, (0, 0, 0), (SCREEN_WIDHT, 0, CAM_WIDTH, SCREEN_HEIGHT))
    
    # Render webcam preview
    if success:
        cam_frame_rgb = cv2.cvtColor(cam_frame, cv2.COLOR_BGR2RGB)
        cam_surface = pygame.surfarray.make_surface(cam_frame_rgb.swapaxes(0, 1))
        cam_surface = pygame.transform.scale(cam_surface, (CAM_WIDTH, CAM_HEIGHT))
        screen.blit(cam_surface, (SCREEN_WIDHT, CAM_Y_OFFSET))

    pygame.display.update()