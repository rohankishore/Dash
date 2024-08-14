import math

import pygame
from pygame.locals import *

import Obstacle
import Player


class LaserGrid(pygame.sprite.Sprite):
    def __init__(self, x, y, width, height, on_time, off_time):
        super().__init__()
        self.image_on = pygame.Surface((width, height))
        self.image_on.fill((255, 0, 0))  # Red color for the laser
        self.image_off = pygame.Surface((width, height))
        self.image_off.fill((0, 0, 0))  # Black color for when the laser is off
        self.image = self.image_on

        self.rect = self.image.get_rect()
        self.rect.topleft = (x, y)

        self.on_time = on_time
        self.off_time = off_time
        self.timer = 0
        self.laser_on = True

    def update(self):
        self.timer += 1

        if self.laser_on and self.timer > self.on_time:
            self.laser_on = False
            self.timer = 0
            self.image = self.image_off
        elif not self.laser_on and self.timer > self.off_time:
            self.laser_on = True
            self.timer = 0
            self.image = self.image_on


pygame.init()

# create the game window
game_width = 1000
game_height = 550
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption('Dash')

# game variables
score = 0
speed = 3

start_screen_image = pygame.image.load("images/bg/banner.png").convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (game_width, game_height))


def start_screen():
    # Display the start screen image
    game.blit(start_screen_image, (0, 0))

    pygame.mixer.music.load("music/intro_music.mp3")
    pygame.mixer.music.play(0)

    # Display a "Press any key to start" message
    font = pygame.font.Font(pygame.font.get_default_font(), 32)
    text = font.render('Press any key to start', True, (255, 255, 255))
    text_rect = text.get_rect(center=(game_width / 2, game_height - 50))
    game.blit(text, text_rect)

    pygame.display.update()

    # Wait for the player to press a key
    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN:
                pygame.mixer.music.stop()  # stop the music playback
                pygame.mixer.music.unload()  # unload music from mixer
                waiting = False


def show_story():
    story_texts = [
        "In a world where obstacles are everywhere,",
        "a lone runner must dash through danger,",
        "avoiding every obstacle in their path,",
        "to achieve the highest score and prove their skill.",
        "Are you ready to take on the challenge?"
    ]

    for text in story_texts:
        show_story_screen(text)


def show_story_screen(text):
    showing_story = True
    while showing_story:
        game.fill((0, 0, 0))  # Background color (black)

        # Display the story text
        font = pygame.font.Font(pygame.font.get_default_font(), 24)
        story_text = font.render(text, True, (255, 255, 255))
        text_rect = story_text.get_rect(center=(game_width / 2, game_height / 2))
        game.blit(story_text, text_rect)

        instructions_text = font.render('Press SPACE to continue', True, (200, 200, 200))
        instructions_rect = instructions_text.get_rect(center=(game_width / 2, game_height / 2 + 50))
        game.blit(instructions_text, instructions_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                showing_story = False


# game loop
clock = pygame.time.Clock()
fps = 90

# show_story()




# Show the start screen
start_screen()

quit = False

while not quit:
    # Load the music and sounds
    pygame.mixer.music.load("music/game_bgm.mp3")

    # Set the number of channels
    pygame.mixer.set_num_channels(10)  # default is 8

    # Play the sounds on different channels
    bgm_channel = pygame.mixer.Channel(0)
    running_channel = pygame.mixer.Channel(1)

    bgm_channel.play(pygame.mixer.Sound('music/game_bgm.mp3'))

    # Set volumes
    bgm_channel.set_volume(0.1)  # Set the background music to 50% volume

    # If you want to control the volume of the music being played by pygame.mixer.music
    pygame.mixer.music.set_volume(0.3)  # Set the music volume to 30%

    pygame.mixer.music.play(0)
    sky = pygame.image.load('images/bg/sky.png').convert_alpha()
    num_bg_tiles = math.ceil(game_width / sky.get_width()) + 1

    # set the images for the parallax background
    bgs = []
    bgs.append(pygame.image.load('images/bg/bg.png').convert_alpha())

    # for the parallax effect, determine how much each layer will scroll
    parallax = []
    for x in range(len(bgs)):
        parallax.append(0)

    # create the player
    player = Player.Player()

    # create the obstacle
    obstacles_group = pygame.sprite.Group()
    obstacle = Obstacle.Obstacle()
    laser_grid = LaserGrid(x=game_width, y=200, width=100, height=10, on_time=60, off_time=60)
    obstacles_group.add(laser_grid)
    obstacles_group.add(obstacle)

    # load the heart images for representing health
    heart_sprites = []
    heart_sprite_index = 0
    for i in range(8):
        heart_sprite = pygame.image.load(f'images/heart/heart{i}.png').convert_alpha()
        scale = 30 / heart_sprite.get_height()
        new_width = heart_sprite.get_width() * scale
        new_height = heart_sprite.get_height() * scale
        heart_sprite = pygame.transform.scale(heart_sprite, (new_width, new_height))
        heart_sprites.append(heart_sprite)

    # game loop
    clock = pygame.time.Clock()
    fps = 90
    quit = False
    while not quit:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                quit = True

            # press SPACE to jump
            if event.type == KEYDOWN and event.key == K_SPACE or event.type == KEYDOWN and event.key == K_UP or event.type == KEYDOWN and event.key == K_w:
                player.jump()

        # draw the sky
        for i in range(num_bg_tiles):
            game.blit(sky, (i * sky.get_width(), 0))

        # draw each background layer
        for i in range(len(bgs)):

            bg = bgs[i]

            for j in range(num_bg_tiles):
                game.blit(bg, (j * bg.get_width() + parallax[i], 0))

        # update how much each layer will scroll
        for i in range(len(parallax)):

            # top layer should scroll faster
            parallax[i] -= i + 1

            if abs(parallax[i]) > bgs[i].get_width():
                parallax[i] = 0

        # draw the player
        player.draw()

        # update the sprite and position of the player
        player.update()

        # draw the obstacle
        obstacle.draw()

        # update the position of the obstacle
        obstacle.update()

        # add to score and reset the obstacle when it goes off screen
        if obstacle.x < obstacle.image.get_width() * -1:

            score += 1
            obstacle.reset()

            # increase the speed after clearing 2 obstacles
            # but the max it can go up to is 10
            if score % 2 == 0 and speed < 10:
                speed += 1

        # Handle collisions between player and obstacles
        if pygame.sprite.spritecollide(player, obstacles_group, True, pygame.sprite.collide_mask):
            player.health -= 1
            player.invincibility_frame = 30

            # remove obstacle and replace with a new one
            obstacles_group.remove(obstacle)
            obstacle = Obstacle.Obstacle()
            obstacles_group.add(laser_grid)
            obstacles_group.add(obstacle)

        # display a heart per remaining health
        for life in range(player.health):
            heart_sprite = heart_sprites[int(heart_sprite_index)]
            x_pos = 10 + life * (heart_sprite.get_width() + 10)
            y_pos = 10
            game.blit(heart_sprite, (x_pos, y_pos))

        # increment the index for the next heart sprite
        # use 0.1 to make the sprite change after 10 frames
        heart_sprite_index += 0.1

        # set index back to 0 after the last heart sprite is drawn
        if heart_sprite_index >= len(heart_sprites):
            heart_sprite_index = 0

        # display the score
        black = (0, 0, 0)
        white = "#FFFFFF"
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Score: {score}', True, white)
        text_rect = text.get_rect()
        text_rect.center = (game_width - 50, 20)
        game.blit(text, text_rect)

        pygame.display.update()

        # gameover
        gameover = player.health == 0
        while gameover and not quit:
            pygame.mixer.music.stop()
            red = (255, 0, 0)
            pygame.draw.rect(game, red, (0, 50, game_width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Game over. Play again? (Enter Y or N)', True, black)
            text_rect = text.get_rect()
            text_rect.center = (game_width / 2, 100)
            game.blit(text, text_rect)

            for event in pygame.event.get():

                if event.type == QUIT:
                    quit = True

                # get the player's input (Y or N)
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        pygame.mixer.music.play(0)
                        gameover = False
                        speed = 3
                        score = 0
                        player = Player()
                        obstacle = Obstacle()
                        obstacles_group.empty()
                        obstacles_group.add(obstacle)
                    elif event.key == K_n:
                        quit = True

            pygame.display.update()

    pygame.quit()
