import pygame
import random

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 600,600

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("One Stone Two Bird")

SCORE_FONT = pygame.font.SysFont("comicsans",25)

class Slingblade():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 100
    def move(self , direction ):
        if direction == "left":
            self.x -= 5 
        if direction == "right":
            self.x += 5 

class Bird():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.dirX = 1
        self.dirY = 1  
        self.image = pygame.image.load("assets/bird1.png")  
        self.limit = y 
    def move(self):
        self.x+= self.dirX*3
        
        if self.y >= self.limit + 5:
            self.dirY *= -1 
        if self.y <= self.limit - 5:
            self.dirY *= -1 
        
        self.y += self.dirY * 1

        if self.x+50 >= WIN_WIDTH:
            self.dirX *= -1
            self.image = pygame.image.load("assets/bird4.png")
        if self.x <= 0:
            self.dirX *= -1
            self.image = pygame.image.load("assets/bird1.png")
        
        

def draw(win , slingblade , bird):
    background = pygame.transform.scale( pygame.image.load("assets/bg.jpg"), (600,600))
    win.blit(background , (0 , 0))

    slingblade_sprite = pygame.transform.scale( pygame.image.load("assets/slingblade.png"), (80,100))
    win.blit(slingblade_sprite , (slingblade.x - 40, slingblade.y-100))

    bird_sprite = pygame.transform.scale( bird.image, (bird.width,bird.height))
    win.blit(bird_sprite , (bird.x, bird.y))

    bird.move()
    
    pygame.display.update()

def main():
    run = True 
    clock = pygame.time.Clock()

    # birds = []

    slingblade = Slingblade(WIN_WIDTH//2 , WIN_HEIGHT)

    bird = Bird(0,100)

    while run:
        clock.tick(60) 
        draw(WIN,slingblade,bird)       
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                 pygame.quit()

if __name__ == "__main__":
    main()