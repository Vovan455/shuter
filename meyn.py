import pygame
import random

pygame.init()

WIDTH = 1200
HEIGHT = 700
SIZE = (WIDTH, HEIGHT)
FPS = 60

scor = 0
lost = 0
live = 5

window = pygame.display.set_mode(SIZE)
background = pygame.transform.scale(
    pygame.image.load("galaxy.jpg"),
    SIZE)
pygame.display.set_caption("шутер. Автор: ....")
clock = pygame.time.Clock()

pygame.mixer.init()
#pygame.mixer.music.load("space.ogg")
#pygame.mixer.music.play()

bullets = pygame.sprite.Group()

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
    def fire(self):
        new_bullet = bullet("bullet.png",(15,20), (self.rect.right,self.rect.centery), 11)
        bullets.add(new_bullet)
        


player = Player("rocket.png", (50,70), (HEIGHT-650, WIDTH/3), 10)
player.image = pygame.transform.rotate(player.image, 270)


class Enemy(GameSprite):
    def update (self):
        self.rect.x -= self.speed

        if self.rect.right < 0:
            self.rect.x = WIDTH
            self.rect.y = random.randint(self.rect.height,HEIGHT-self.rect.height)
            global lost
            lost += 1

class bullet(GameSprite):
    def __init__(self, filename, size, coords, speed):
        super().__init__(filename, size, coords, speed)
        self.image =  pygame.transform.rotate(self.image,270)
    def update(self):
        self.rect.x += self.speed

        if self.rect.left > WIDTH:
            self.kill()

pygame.font.init()
medium_font = pygame.font.SysFont("Arial",24)   
big_font = pygame.font.SysFont("Arial",50) 





enemies = pygame.sprite.Group()
enemies_nam = 5
for i in range(enemies_nam):
    n = random.randint(1,100)
    if n > 50:
        new_enemy = Enemy("ufo.png",
                        (70,50),
                        (WIDTH,random.randint( 50,HEIGHT-50)),
                        random.randint(4,14)
                            )
    else:
         new_enemy = Enemy("asteroid.png",
                        (70,50),
                        (WIDTH,random.randint( 50,HEIGHT-50)),
                        random.randint(4,14)
                            )

    enemies.add(new_enemy)





game = True
finish = False
while game:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            game = False
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_SPACE:
                player.fire()

    if not finish:
        window.blit(background, (0,0))
        lost_text = medium_font.render(str(lost), True, (255,255,255))
        scor_text = medium_font.render(str(scor), True, (255,255,255))
        window.blit(scor_text, (0,30))
         
        bullets.draw(window)
        bullets.update()
        window.blit(lost_text, (0,0))
        player.reset(window)
        player.update()
        enemies.draw(window)
        enemies.update()

        collided = pygame.sprite.groupcollide(enemies, bullets, True, True)
        for enemi in collided:
            scor += 1
            n = random.randint(1,100)
            if n > 50:
                new_enemy = Enemy("ufo.png",
                                (70,50),
                                (WIDTH,random.randint( 50,HEIGHT-50)),
                                random.randint(4,14)
                                    )
            else:
                new_enemy = Enemy("asteroid.png",
                                (70,50),
                                (WIDTH,random.randint( 50,HEIGHT-50)),
                                random.randint(4,14)
                                    )

            enemies.add(new_enemy)


    if scor >= 15:
        finish = True 
        win_text = big_font.render("WIN", True, (0,255,0)) 
        window.blit(win_text, (WIDTH//2-100, HEIGHT//2)) 
    if lost >= 10 or live <=0 :
        finish = True
        lus_text = big_font.render("LOSE", True, (255,0,0)) 
        window.blit(lus_text, (WIDTH//2-100, HEIGHT//2)) 


    collided = pygame.sprite.spritecollide(player, enemies, True)
    for enemi in collided:
        live -= 1
        n = random.randint(1,100)
        if n > 50:
            new_enemy = Enemy("ufo.png",
                            (70,50),
                            (WIDTH,random.randint( 50,HEIGHT-50)),
                            random.randint(4,14)
                                )
        else:
            new_enemy = Enemy("asteroid.png",
                            (70,50),
                            (WIDTH,random.randint( 50,HEIGHT-50)),
                            random.randint(4,14)
                                )

        enemies.add(new_enemy)



    pygame.display.update()
    clock.tick(FPS)