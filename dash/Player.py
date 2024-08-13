import pygame

pygame.init()

# create the game window
game_width = 1000
game_height = 550
size = (game_width, game_height)
game = pygame.display.set_mode(size)


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
        """ make the player go to jumping action when not already jumping or landing """
        if self.action not in ['jumping', 'landing']:
            self.action = 'jumping'
