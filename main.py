#AW Space Invaders
import pygame
import random
import math
from pygame import mixer

# Initialize Pygame
pygame.init()

#set background
background = pygame.transform.scale(pygame.image.load('resources/background2.webp'), (800, 600))

#background music
mixer.music.load('resources\\background.wav')
mixer.music.play(-1)

#score text
score_font = pygame.font.Font('freesansbold.ttf', 32)

# Set up display
screen_width = 800
screen_height = 600
screen = pygame.display.set_mode((800, 600))
pygame.display.set_caption("Space Invaders")
pygame_icon = pygame.image.load('resources/icon.png')
#32x32 image
pygame.display.set_icon(pygame_icon)


class Button:
    def __init__(self, x,y, img, scale):
        self.x = x
        self.y = y
        self.img = pygame.image.load(img)
        self.img = pygame.transform.scale(self.img, (int(self.img.get_width()*scale), int(self.img.get_height()*scale)))
        self.rect = self.img.get_rect()
        self.surface = surface
        

    def draw(self):
        pos = pygame.mouse.get_position()
        print(pos)

        if self.rect.collidepoint(pos):
            print("Hover")
        screen.blit(self.img, (self.x, self.y))

    


#bullet class
class Bullet:
    def __init__(self, x = 0, y = 0):
        self.state = "ready"
        self.x = x
        self.y = y
        self.change = -1
        self.img = pygame.transform.scale(pygame.image.load('resources/bullet.png'), (32, 32))
        self.rotated = pygame.transform.rotate(self.img, 0)

    def shoot(self):
        self.change = -1
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.y += self.change
        if self.y <= 0:
            self.state = "ready"
    

#player class
class Player:
    def __init__(self, x, change = 0):
        self.img = pygame.transform.scale(pygame.image.load('resources/spaceship3.png'), (64, 64))
        self.x = x
        self.y = 600-69
        self.change = change
        self.score = 0

    def player_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.change
        if self.x <= 0:
            self.x = 0
        elif self.x >= (800-64):
            self.x = 736

#enemy class
class Enemy:
    def __init__(self, x, y):
        self.img = pygame.transform.scale(pygame.image.load('resources/alien.png'), (64, 64))
        self.x = x
        self.y = y
        self.x_change = 0.3
        self.y_change = 20

    def enemy_set(self):
        screen.blit(self.img, (self.x, self.y))

    def move(self):
        self.x += self.x_change
        if self.x <= 0:
            self.x_change = 0.3
            self.y += self.y_change
        elif self.x >= 800-64:
            self.x_change = -0.3
            self.y += self.y_change

    def is_hit(self, bullet):
        distance = math.sqrt((self.x-bullet.x)**2 + (self.y-bullet.y)**2)
        if distance < 48:
            return True
        return False
    
    def lose(self):
        if self.y >= 536:
            return True
        return False




player = Player(370)
bullet = Bullet()
enemies = []
for i in range(6):
    x = random.randint(0, 800-64)
    y = random.randint(0,300-64)
    enemies.append(Enemy(x, y))


game_over_font = pygame.font.Font('freesansbold.ttf', 64)
game_over_text = game_over_font.render("GAME OVER", True, (255, 0, 0))
game_over = True



running = True
while running:
    screen.fill((0,0,0))
    screen.blit(background, (0, 0))
    score_display = score_font.render(f"Score: {player.score}", True, (255,255,255))
    screen.blit(score_display, (10,10))
    #loop events
    for event in pygame.event.get():
        keys = pygame.key.get_pressed()
        if event.type == pygame.QUIT:
            running = False
        if event.type == pygame.KEYDOWN:
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_RIGHT]:
                player.change = 0.3
            if keys[pygame.K_LEFT]:
                player.change = -0.3
            if keys[pygame.K_SPACE]:
                if bullet.state == "ready":
                    bullet.x = player.x + 16
                    bullet.y = player.y + 10
                    bullet.state = "fire"
                    mixer.Sound.play('resources\\laser.wav').play() 
                
        if event.type == pygame.KEYUP:
            if event.key == pygame.K_LEFT or event.key == pygame.K_RIGHT:
                player.change = 0



    #Show items
    player.move()
    for enemy in enemies:
        enemy.move()
        if enemy.lose():
            enemies = []
            game_over = True
    if game_over == False:

            
        bullet.move()

        for i, enemy in enumerate(enemies):
            if enemy.is_hit(bullet):
                bullet.state = "ready"
                enemies.pop(i)
                bullet.x = player.x
                bullet.y = player.y
                bullet.change = 0
                player.score += 1
                mixer.Sound.play('resources\\explosion.wav').play()
            if enemies == []:
                for i in range(6):
                    x = random.randint(0, 800-64)
                    y = random.randint(0,300-64)
                    enemies.append(Enemy(x, y))

       
        

        #Show items
        player.player_set()
        enemy.enemy_set()
        if bullet.state == "fire":
            bullet.shoot()
    else:
        screen.blit(game_over_text, (200, 250))

        button = Button(400, 350, 'resources/button.png', 0.2)
        button.draw()
    
    player.player_set()

    pygame.display.flip()