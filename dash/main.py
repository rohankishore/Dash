import math
import pygame
from pygame.locals import *

import Obstacle
import Player

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
obstacles_cleared = 0  # Counter for obstacles cleared
level = 1  # Start with level 1

start_screen_image = pygame.image.load("images/bg/banner.png").convert_alpha()
start_screen_image = pygame.transform.scale(start_screen_image, (game_width, game_height))

board_image = pygame.image.load("images/obstacles/board.png").convert_alpha()  # Load the board image
board_image = pygame.transform.scale(board_image, (game_width, game_height))  # Scale it if needed


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


def show_board(level):
    font = pygame.font.Font(pygame.font.get_default_font(), 48)
    text = font.render(f'Level {level}', True, (255, 255, 255))
    text_rect = text.get_rect(center=(game_width / 2, game_height / 2))

    # Draw the board image
    game.blit(board_image, (0, 0))
    game.blit(text, text_rect)
    pygame.display.update()
    pygame.time.wait(2000)  # Show the board image for 2 seconds


# game loop
clock = pygame.time.Clock()
fps = 90

# Show the start screen
start_screen()

quit = False

while not quit:
    # Load the music and sounds
    pygame.mixer.music.load("music/game_bgm.mp3")

    # Set the number of channels
    pygame.mixer.set_num_channels(10)  # Increase number of audio channels

    # Play the sounds on different channels
    bgm_channel = pygame.mixer.Channel(0)
    running_channel = pygame.mixer.Channel(1)

    bgm_channel.play(pygame.mixer.Sound('music/game_bgm.mp3'))

    # Set volumes
    bgm_channel.set_volume(0.1)  # Set the background music to 10% volume
    pygame.mixer.music.set_volume(0.3)  # Set the music volume to 30%

    pygame.mixer.music.play(0)
    sky = pygame.image.load('images/bg/sky.png').convert_alpha()
    num_bg_tiles = math.ceil(game_width / sky.get_width()) + 1

    # Set the images for the parallax background
    bgs = []
    bgs.append(pygame.image.load('images/bg/bg.png').convert_alpha())

    # For the parallax effect, determine how much each layer will scroll
    parallax = []
    for x in range(len(bgs)):
        parallax.append(0)

    # Create the player
    player = Player.Player()

    # Create the obstacle
    obstacles_group = pygame.sprite.Group()
    obstacle = Obstacle.Obstacle()
    obstacles_group.add(obstacle)

    # Load the heart images for representing health
    heart_sprites = []
    heart_sprite_index = 0
    for i in range(8):
        heart_sprite = pygame.image.load(f'images/heart/heart{i}.png').convert_alpha()
        scale = 30 / heart_sprite.get_height()
        new_width = heart_sprite.get_width() * scale
        new_height = heart_sprite.get_height() * scale
        heart_sprite = pygame.transform.scale(heart_sprite, (new_width, new_height))
        heart_sprites.append(heart_sprite)

    # Game loop
    clock = pygame.time.Clock()
    fps = 90
    quit = False
    while not quit:
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.mixer.music.stop()
                quit = True

            # Press SPACE to jump
            if event.type == KEYDOWN and event.key == K_SPACE or event.type == KEYDOWN and event.key == K_UP or event.type == KEYDOWN and event.key == K_w:
                player.jump()

        # Draw the sky
        for i in range(num_bg_tiles):
            game.blit(sky, (i * sky.get_width(), 0))

        # Draw each background layer
        for i in range(len(bgs)):
            bg = bgs[i]
            for j in range(num_bg_tiles):
                game.blit(bg, (j * bg.get_width() + parallax[i], 0))

        # Update how much each layer will scroll
        for i in range(len(parallax)):
            # Top layer should scroll faster
            parallax[i] -= i + 1
            if abs(parallax[i]) > bgs[i].get_width():
                parallax[i] = 0

        # Draw the player
        player.draw()

        # Update the sprite and position of the player
        player.update()

        # Draw the obstacle
        obstacle.draw()

        # Update the position of the obstacle
        obstacle.update()

        # Add to score and reset the obstacle when it goes off screen
        if obstacle.x < obstacle.image.get_width() * -1:
            score += 1
            obstacles_cleared += 1  # Increment obstacles cleared
            obstacle.reset()

            # Increase the speed after clearing 2 obstacles
            # but the max it can go up to is 10
            if score % 2 == 0 and speed < 10:
                speed += 1

            # Show the board image every 10 obstacles cleared
            if obstacles_cleared % 10 == 0:
                level += 1  # Increase the level
                show_board(level)  # Pass the current level to the function

        # Handle collisions between player and obstacles
        if pygame.sprite.spritecollide(player, obstacles_group, True, pygame.sprite.collide_mask):
            player.health -= 1
            player.invincibility_frame = 30

            # Remove obstacle and replace with a new one
            obstacles_group.remove(obstacle)
            obstacle = Obstacle.Obstacle()
            obstacles_group.add(obstacle)

        # Display a heart per remaining health
        for life in range(player.health):
            heart_sprite = heart_sprites[int(heart_sprite_index)]
            x_pos = 10 + life * (heart_sprite.get_width() + 10)
            y_pos = 10
            game.blit(heart_sprite, (x_pos, y_pos))

        # Increment the index for the next heart sprite
        # Use 0.1 to make the sprite change after 10 frames
        heart_sprite_index += 0.1

        # Set index back to 0 after the last heart sprite is drawn
        if heart_sprite_index >= len(heart_sprites):
            heart_sprite_index = 0

        # Display the score and level
        black = (0, 0, 0)
        white = "#FFFFFF"
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text_score = font.render(f'Score: {score}', True, white)
        text_rect_score = text_score.get_rect()
        text_rect_score.center = (game_width - 50, 20)

        text_level = font.render(f'Level: {level}', True, white)
        text_rect_level = text_level.get_rect()
        text_rect_level.center = (game_width - 50, 40)

        game.blit(text_score, text_rect_score)
        game.blit(text_level, text_rect_level)

        pygame.display.update()

        # Game over
        gameover = player.health == 0
        while gameover and not quit:
            pygame.mixer.music.stop()
            red = (255, 0, 0)
            pygame.draw.rect(game, red, (0, 50, game_width, 100))
            font = pygame.font.Font(pygame.font.get_default_font(), 16)
            text = font.render('Game over. Play again? (Enter Y or N)', True, white)
            text_rect = text.get_rect()
            text_rect.center = (game_width / 2, 100)
            game.blit(text, text_rect)

            for event in pygame.event.get():
                if event.type == QUIT:
                    quit = True

                # Get the player's input (Y or N)
                if event.type == KEYDOWN:
                    if event.key == K_y:
                        pygame.mixer.music.play(0)
                        gameover = False
                        speed = 3
                        score = 0
                        obstacles_cleared = 0  # Reset the counter
                        level = 1  # Reset the level
                        player = Player.Player()
                        obstacle = Obstacle.Obstacle()
                        obstacles_group.empty()
                        obstacles_group.add(obstacle)
                    elif event.key == K_n:
                        quit = True

            pygame.display.update()

    pygame.quit()
