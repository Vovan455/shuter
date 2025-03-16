import pygame
import random

pygame.init()

WIDTH = 1200
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
FPS = 60

window = pygame.display.set_mode(SIZE)
background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE)
pygame.display.set_caption("шутер. Автор: ....")
clock = pygame.time.Clock()

pygame.mixer.init()
#pygame.mixer.music.load("space.ogg")
#pygame.mixer.music.play()


class GameSprite(pygame.sprite.Sprite) :
    def __init__ (self, filename:str, size:tuple[int,int], coords: tuple[int,int], speed:int):
        super(). __init__ ()
        self.image = pygame.transform.scale(pygame.image.load(filename), size)
        self.rect = self. image. get_rect (center=coords )
        self.speed = speed
    def reset(self, window):
        window.blit(self. image, self. rect)

class Player (GameSprite):
    def update(self):
        keys = pygame.key.get_pressed()
        if keys[pygame.K_w] and self.rect.y > 0:
            self.rect.y -= self.speed

        if keys[pygame.K_s] and self.rect.y < HEIGHT :
            self.rect.y += self.speed

        if keys[pygame.K_d] and self.rect.x < WIDTH :
            self.rect.x += self.speed

        if keys[pygame.K_a] and self.rect.x > 0:
            self.rect.x -= self.speed

player = Player("rocket.png", (50,70), (HEIGHT-650, WIDTH/3), 10)
player.image = pygame.transform.rotate(player.image, 270)


class Enemy(GameSprite):
    def update (self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(self.rect.height,HEIGHT-self.rect.height)

test_enemy = Enemy("ufo.png", (70,50), (WIDTH-75, random.randint(0,HEIGHT)),8 )






game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
    if not finish:
        window.blit(background, (0,0))

        player.reset(window)
        player.update()
        test_enemy.reset(window)
        test_enemy.update()

    pygame.display.update()
    clock.tick(FPS)