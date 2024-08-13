import pygame
from pygame.locals import *
import random
import math

pygame.init()

# create the game window
game_width = 1000
game_height = 400
size = (game_width, game_height)
game = pygame.display.set_mode(size)
pygame.display.set_caption('Dash')

# game variables
score = 0
speed = 3


class Player(pygame.sprite.Sprite):
    def __init__(self):

        pygame.sprite.Sprite.__init__(self)

        self.height = 150
        self.x = 25
        self.y = game_height - self.height
        self.action = 'running'
        self.health = 3

        # load the running sprites
        self.running_sprites = []
        self.running_sprite_index = 0
        for i in range(10):
            running_sprite = pygame.image.load(f'images/running/run{i}.png').convert_alpha()
            scale = self.height / running_sprite.get_height()
            new_width = running_sprite.get_width() * scale
            new_height = running_sprite.get_height() * scale
            running_sprite = pygame.transform.scale(running_sprite, (new_width, new_height))
            self.running_sprites.append(running_sprite)

        # load the jumping sprites
        self.jumping_sprites = []
        self.jumping_sprite_index = 0
        for i in range(10):
            jumping_sprite = pygame.image.load(f'images/jumping/jump{i}.png').convert_alpha()
            scale = self.height / jumping_sprite.get_height()
            new_width = jumping_sprite.get_width() * scale
            new_height = jumping_sprite.get_height() * scale
            jumping_sprite = pygame.transform.scale(jumping_sprite, (new_width, new_height))
            self.jumping_sprites.append(jumping_sprite)

        # set the initial sprite rect
        self.rect = self.running_sprites[self.running_sprite_index].get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # number of frames player is invincible after getting hurt
        self.invincibility_frame = 0

    def draw(self):
        ''' draw the sprite based on the character action and index '''

        if self.action == 'running':
            running_sprite = self.running_sprites[int(self.running_sprite_index)]

            # add invincibility effect when hurt
            if self.invincibility_frame > 0:
                self.invincibility_frame -= 1
            if self.invincibility_frame % 10 == 0:
                game.blit(running_sprite, (self.x, self.y))

        elif self.action == 'jumping' or self.action == 'landing':
            jumping_sprite = self.jumping_sprites[int(self.jumping_sprite_index)]

            # add invincibility effect when hurt
            if self.invincibility_frame > 0:
                self.invincibility_frame -= 1
            if self.invincibility_frame % 10 == 0:
                game.blit(jumping_sprite, (self.x, self.y))

    def update(self):
        ''' update the sprite index so the next sprite image is drawn '''
        ''' also update the y position when jumping or landing '''

        if self.action == 'running':

            # increment the sprite index by 0.2
            # so it takes 5 frames to get to the next index
            self.running_sprite_index += 0.2

            # go back to index 0 after the last sprite image is drawn
            if self.running_sprite_index >= len(self.running_sprites):
                self.running_sprite_index = 0

            # update the rect
            self.rect = self.running_sprites[int(self.running_sprite_index)].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            # update the mask for collision detection
            self.mask = pygame.mask.from_surface(self.running_sprites[int(self.running_sprite_index)])

        elif self.action == 'jumping' or self.action == 'landing':

            # increment the sprite index by 0.2
            # so it takes 5 frames to get to the next index
            self.jumping_sprite_index += 0.2

            # go back to index 0 after the last sprite image is drawn
            if self.jumping_sprite_index >= len(self.jumping_sprites):
                self.jumping_sprite_index = 0

            # move position up if jumping or down if landing
            if self.action == 'jumping':
                self.y -= 2

                # change to landing when peak of jump is reached
                if self.y <= game_height - self.height * 1.5:
                    self.action = 'landing'

            elif self.action == 'landing':
                self.y += 2

                # change to running when character touches the ground
                if self.y == game_height - self.height:
                    self.action = 'running'

            # update the rect
            self.rect = self.jumping_sprites[int(self.jumping_sprite_index)].get_rect()
            self.rect.x = self.x
            self.rect.y = self.y

            # update the mask for collision detection
            self.mask = pygame.mask.from_surface(self.jumping_sprites[int(self.jumping_sprite_index)])

    def jump(self):
        ''' make the player go to jumping action when not already jumping or landing '''
        if self.action not in ['jumping', 'landing']:
            self.action = 'jumping'


class Obstacle(pygame.sprite.Sprite):

    def __init__(self):
        pygame.sprite.Sprite.__init__(self)

        # load images used for the obstacles
        self.obstacle_images = []
        for image_name in ['rock1', 'rock2', 'rock3', 'spikes']:
            image = pygame.image.load(f'images/obstacles/{image_name}.png').convert_alpha()
            scale = 50 / image.get_width()
            new_width = image.get_width() * scale
            new_height = image.get_height() * scale
            image = pygame.transform.scale(image, (new_width, new_height))
            self.obstacle_images.append(image)

        # assign a random image
        self.image = random.choice(self.obstacle_images)

        # position the obstacle just off the right side of the screen
        self.x = game_width
        self.y = game_height - self.image.get_height()

        # set the initial rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

    def draw(self):
        game.blit(self.image, (self.x, self.y))

    def update(self):
        ''' move obstacle to the left '''

        # move left
        self.x -= speed

        # update the rect
        self.rect = self.image.get_rect()
        self.rect.x = self.x
        self.rect.y = self.y

        # update the mask for collision detection
        self.mask = pygame.mask.from_surface(self.image)

    def reset(self):
        ''' assign a new image and reset back to original position '''

        self.image = random.choice(self.obstacle_images)
        self.x = game_width
        self.y = game_height - self.image.get_height()


def show_start_screen():
    start = True

    while start:
        # Fill the background with a color or an image
        game.fill((0, 150, 150))  # Example: Fill with a teal color

        # Display the title
        title_font = pygame.font.Font(pygame.font.get_default_font(), 48)
        title_text = title_font.render('Dash', True, (255, 255, 255))
        title_rect = title_text.get_rect(center=(game_width / 2, game_height / 2 - 50))
        game.blit(title_text, title_rect)

        # Display the instructions
        instructions_font = pygame.font.Font(pygame.font.get_default_font(), 24)
        instructions_text = instructions_font.render('Press SPACE to Start', True, (255, 255, 255))
        instructions_rect = instructions_text.get_rect(center=(game_width / 2, game_height / 2 + 50))
        game.blit(instructions_text, instructions_rect)

        pygame.display.update()

        for event in pygame.event.get():
            if event.type == QUIT:
                pygame.quit()
                exit()
            if event.type == KEYDOWN and event.key == K_SPACE:
                start = False


# game loop
clock = pygame.time.Clock()
fps = 90

# Show the start screen
show_start_screen()

quit = False

while not quit:
    # set the image for the sky
    sky = pygame.image.load('images/bg/sky.png').convert_alpha()
    num_bg_tiles = math.ceil(game_width / sky.get_width()) + 1

    # set the images for the parallax background
    bgs = []
    bgs.append(pygame.image.load('images/bg/mountains.png').convert_alpha())
    bgs.append(pygame.image.load('images/bg/trees.png').convert_alpha())
    bgs.append(pygame.image.load('images/bg/bushes.png').convert_alpha())

    # for the parallax effect, determine how much each layer will scroll
    parallax = []
    for x in range(len(bgs)):
        parallax.append(0)

    # create the player
    player = Player()

    # create the obstacle
    obstacles_group = pygame.sprite.Group()
    obstacle = Obstacle()
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

        # check if player collides with the obstacle
        if pygame.sprite.spritecollide(player, obstacles_group, True, pygame.sprite.collide_mask):
            player.health -= 1
            player.invincibility_frame = 30

            # remove obstacle and replace with a new one
            obstacles_group.remove(obstacle)
            obstacle = Obstacle()
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
        font = pygame.font.Font(pygame.font.get_default_font(), 16)
        text = font.render(f'Score: {score}', True, black)
        text_rect = text.get_rect()
        text_rect.center = (game_width - 50, 20)
        game.blit(text, text_rect)

        pygame.display.update()

        # gameover
        gameover = player.health == 0
        while gameover and not quit:

            # display game over message
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
                        # reset the game
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
