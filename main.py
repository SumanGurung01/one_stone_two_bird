"""
    Date : Fri Jan 20 2023 14:59:15 GMT+0530 (India Standard Time)
    Author : Suman Gurung
    Description : My version of OneStoneTwoBird game by PolyMars.  
"""

import pygame
import random

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 600,600

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("One Stone Two Bird")

SCORE_FONT = pygame.font.SysFont("comicsans",25)
MSG_FONT = pygame.font.SysFont("comicsans" , 30)

# CLASSES
class Slingblade():
    def __init__(self , x , y , shot):
        self.x = x
        self.y = y
        self.width = 80
        self.height = 100
        self.shot = shot
    def move(self , direction ):
        if direction == "left":
            self.x -= 5 
        if direction == "right":
            self.x += 5 

class Stone():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 20
        self.height = 20
        self.image = pygame.image.load("assets/stone.png")  
        self.release = 0
        self.dir = "up"
    def move(self):
        if self.dir == "up":
            self.y -= 5 
        if self.dir == "down":
            self.y += 5 

class Bird():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.dirX = random.choice([-1,1])
        self.dirY = 1  
        
        number = [[pygame.image.load("assets/bird4.png"),pygame.image.load("assets/bird1.png")] , [pygame.image.load("assets/bird3.png"),pygame.image.load("assets/bird2.png")] , [pygame.image.load("assets/bird5.png") , pygame.image.load("assets/bird6.png")]]
        
        self.random_bird = random.choice(number)
        
        if self.dirX < 0 : 
            self.image = self.random_bird[0]
        else:
            self.image = self.random_bird[1]  
        self.limit = y 
    
    def move(self):
        self.y += self.dirY * 1
        if self.y >= self.limit + 5:
            self.dirY *= -1 
        if self.y <= self.limit - 5:
            self.dirY *= -1 

        self.x+= self.dirX*2
        if self.x+50 >= WIN_WIDTH:
            self.dirX *= -1
            self.image = self.random_bird[0]
        if self.x <= 0:
            self.dirX *= -1
            self.image = self.random_bird[1]

class Block():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 100
        self.height = 100
        self.image = pygame.image.load("assets/block.png")  


# FUNCTIONS
def handle_slingblade_stone_movement(keys , slingblade , stone):
    if keys[pygame.K_a] and slingblade.x - 5 >= 0:
        slingblade.move(direction = "left")
        if not stone.release: 
            stone.x = slingblade.x+30
    if keys[pygame.K_d] and slingblade.x + slingblade.width + 5<= WIN_WIDTH:
        slingblade.move(direction = "right")
        if not stone.release: 
            stone.x = slingblade.x+30
    if stone.y<=0 and slingblade.shot>0:
        stone.release=0
        slingblade.shot-=1
        stone.x = slingblade.x+30
        stone.y = slingblade.y+50
    if stone.y>=WIN_HEIGHT-100 and stone.x+10 >= slingblade.x and stone.x+10 <= slingblade.x+80 and stone.dir == "down":
        stone.release=0
        stone.x = slingblade.x+30
        stone.y = slingblade.y+50
        stone.dir = "up"
    if stone.y>=WIN_HEIGHT and stone.dir == "down":
        stone.release=0
        slingblade.shot-=1
        stone.x = slingblade.x+30
        stone.y = slingblade.y+50
        stone.dir = "up"

    if keys[pygame.K_SPACE] and slingblade.shot>0:
        stone.release=1
    if stone.release:
        stone.move()
    
def handle_collision(birds , stone , blocks = []):
    for i , bird in enumerate(birds , start=0):
        if stone.x+10 >= bird.x and stone.x+10 <= bird.x+50:
            if stone.y <= bird.y+50 and stone.y+20 >= bird.y:
                birds.pop(i)
    for block in blocks:
        if stone.x+10 >= block.x and stone.x+10 <= block.x+100:
            if stone.y<= block.y+100 : 
                stone.dir="down"


# SCREENS
def welcome_screen(win):
    background = pygame.transform.scale( pygame.image.load("assets/bg.jpg"), (600,600))
    win.blit(background , (0 , 0))
    
    title = pygame.transform.scale( pygame.image.load("assets/title.png"), (300,150))
    win.blit(title , (WIN_WIDTH//2-150, WIN_HEIGHT//2-90))

    text = MSG_FONT.render(f"Press Enter to Start", 1 , (0,0,0))
    win.blit(text,(WIN_WIDTH//2 - 90, WIN_HEIGHT//2 + 100))
    
    pygame.display.update()

def retry_screen(win):
    background = pygame.transform.scale( pygame.image.load("assets/bg.jpg"), (600,600))
    win.blit(background , (0 , 0))
    
    text1 = MSG_FONT.render(f"GAMEOVER", 1 , (0,0,0))
    win.blit(text1,(WIN_WIDTH//2 - 50, WIN_HEIGHT//2))

    text2 = MSG_FONT.render(f"Press Enter to Retry", 1 , (0,0,0))
    win.blit(text2,(WIN_WIDTH//2 - 90 , WIN_HEIGHT//2 + 40))
    
    pygame.display.update()

def win_screen(win):
    background = pygame.transform.scale( pygame.image.load("assets/bg.jpg"), (600,600))
    win.blit(background , (0 , 0))
    
    text1 = MSG_FONT.render(f"YOU WON", 1 , (0,0,0))
    win.blit(text1,(WIN_WIDTH//2 - 50, WIN_HEIGHT//2))

    text2 = MSG_FONT.render(f"Created by Suman Gurung", 1 , (0,0,0))
    win.blit(text2,(WIN_WIDTH//2 - 120 , WIN_HEIGHT//2 + 40))
    
    pygame.display.update()


# DRAW ON WINDOW FUNCTION
def draw(win , slingblade , birds , stone , level , blocks=[]):

    background = pygame.transform.scale( pygame.image.load("assets/bg.jpg"), (600,600))
    win.blit(background , (0 , 0))
    
    board = pygame.transform.scale( pygame.image.load("assets/board.png"), (200,40))
    win.blit(board , (400 , 0))

    board_text = SCORE_FONT.render(f"Stone x {slingblade.shot} - Level x {level}", 1 , (0,0,0))
    win.blit(board_text,(420, 12))

    slingblade_sprite = pygame.transform.scale( pygame.image.load("assets/slingblade.png"), (80,100))
    win.blit(slingblade_sprite , (slingblade.x , slingblade.y))

    for bird in birds:
        bird_sprite = pygame.transform.scale( bird.image, (bird.width,bird.height))
        win.blit(bird_sprite , (bird.x, bird.y))
        bird.move()

    for block in blocks:
        block_sprite = pygame.transform.scale( block.image, (block.width,block.height))
        win.blit(block_sprite , (block.x, block.y))

    stone_sprite = pygame.transform.scale(stone.image, (stone.width,stone.height))
    win.blit(stone_sprite , (stone.x,stone.y))
    
    pygame.display.update()


# MAIN FUNCTION
def main():
    level=1
    run = True 
    gameover = 0
    won = False
    clock = pygame.time.Clock()

    while run:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        welcome_screen(WIN)
        keys = pygame.key.get_pressed() 
        if keys[pygame.K_RETURN]:
            run = False    
    
    run = True

    while run:
        gameover = 0

        if level==1:
            print("level 1")
            birds = []
            blocks = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100, 1)
            birds.append(Bird(random.randrange(50,550),200))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 

        if level==2:
            print("level 2")
            birds = []
            blocks = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 2)
            for i in range(1,3):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 
        
        if level==3:
            print("level 3")
            blocks = []
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 3)
            for i in range(1,4):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)
        
        if level==4:
            print("level 4")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 2)
            for i in range(1,7):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 400))
                birds.append(bird)
            blocks = []
            blocks.append(Block(100,50))
            blocks.append(Block(400,50))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 

        if level==5:
            print("level 5")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 1)
            for i in range(1,9):
                bird = Bird(random.randrange(50,550),random.randrange(160 , 400))
                birds.append(bird)
            blocks = []
            blocks.append(Block(300,50))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 
        
        if level==6:
            print("level 6")
            birds = []
            blocks = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 3)
            for i in range(1,5):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)  
        
        if level==7:
            print("level 7")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 1)
            for i in range(1,6):
                bird = Bird(random.randrange(50,550),random.randrange(210 , 400))
                birds.append(bird)
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            blocks = []
            blocks.append(Block(300,100))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)
        
        if level==8:
            print("level 8")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 1)
            for i in range(1,6):
                bird = Bird(random.randrange(50,550),random.randrange(210 , 400))
                birds.append(bird)
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            blocks = []
            blocks.append(Block(300,100))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)

        if level==9:
            print("level 9")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 4)
            for i in range(1,6):
                bird = Bird(random.randrange(50,550),random.randrange(210 , 400))
                birds.append(bird)
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            birds.append(Bird(random.randrange(50,550),random.randrange(10 , 50)))
            blocks = []
            blocks.append(Block(50,100))
            blocks.append(Block(250,100))
            blocks.append(Block(450,100))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 

        if level==10:
            print("level 10")
            birds = []
            blocks = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 3)
            for i in range(1,7):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)   
                  
        isrunning = True

        while isrunning:
            clock.tick(60) 
            draw(WIN,slingblade,birds,stone,level,blocks)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if len(birds) == 0:
                level+=1
                isrunning = False
            keys = pygame.key.get_pressed() 
            handle_slingblade_stone_movement(keys , slingblade , stone)
            handle_collision(birds , stone , blocks) 

            if len(birds)>0 and slingblade.shot == 0:
                gameover = 1
                isrunning = False
            
            if level > 10 : 
                won = True
                isrunning = False

        if gameover==1:
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                retry_screen(WIN)
                keys = pygame.key.get_pressed() 
                if keys[pygame.K_RETURN]:
                    break
        if won :
            while True:
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        pygame.quit()
                win_screen(WIN)
            run = False    

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
    
if __name__ == "__main__":
    main()