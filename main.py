import pygame
import random

# slingblade width : 80
# slingblade height : 100

# stone.width : 20
# stone.height : 20

# bird.width : 50 
# bird.height :  50

pygame.init()

# CONSTANTS
WIN_HEIGHT,WIN_WIDTH = 600,600

WIN = pygame.display.set_mode((WIN_WIDTH , WIN_HEIGHT))
pygame.display.set_caption("One Stone Two Bird")

SCORE_FONT = pygame.font.SysFont("comicsans",25)

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
    def move(self):
        self.y -= 5 

class Bird():
    def __init__(self , x , y ):
        self.x = x
        self.y = y
        self.width = 50
        self.height = 50
        self.dirX = random.choice([-1,1])
        self.dirY = 1  
        if self.dirX < 0 : 
            self.image = pygame.image.load("assets/bird4.png")
        else:
            self.image = pygame.image.load("assets/bird1.png")  
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
            self.image = pygame.image.load("assets/bird4.png")
        if self.x <= 0:
            self.dirX *= -1
            self.image = pygame.image.load("assets/bird1.png")

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
    if keys[pygame.K_SPACE] and slingblade.shot>0:
        stone.release=1
    if stone.release:
        stone.move()
    

def handle_collision(birds , stone):
    for i , bird in enumerate(birds , start=0):
        if stone.x+10 >= bird.x and stone.x+10 <= bird.x+50:
            if stone.y <= bird.y+50 and stone.y+20 >= bird.y:
                birds.pop(i)

def draw(win , slingblade , birds , stone , level):

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

    stone_sprite = pygame.transform.scale(stone.image, (stone.width,stone.height))
    win.blit(stone_sprite , (stone.x,stone.y))
    
    pygame.display.update()

def main():
    level=1
    run = True 
    clock = pygame.time.Clock()
    while run:
        if level==1:
            print("level 1")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100, 1)
            birds.append(Bird(random.randrange(50,550),100))
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)  
        if level==2:
            print("level 2")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 2)
            for i in range(1,3):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50) 
        if level==3:
            print("level 3")
            birds = []
            slingblade = Slingblade(WIN_WIDTH//2 - 40 , WIN_HEIGHT - 100 , 3)
            for i in range(1,4):
                bird = Bird(random.randrange(50,550),random.randrange(200 , 300))
                birds.append(bird)
            stone = Stone(slingblade.x + 30 , slingblade.y + 50)     
        
        isrunning = True

        while isrunning:
            clock.tick(60) 
            draw(WIN,slingblade,birds,stone,level)
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
            if len(birds) == 0:
                level+=1
                isrunning = False
            keys = pygame.key.get_pressed() 
            handle_slingblade_stone_movement(keys , slingblade , stone)
            handle_collision(birds , stone) 
        
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
        
       

if __name__ == "__main__":
    main()