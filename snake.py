import pygame
from random import randint

map_size = [50,30]
bit_size = 20;

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)
YELLOW = (255,255,153)

class Snake:
    def __init__(self):
        self.body = [[20,9],[20,9],[20,10]];
        self.dir = 0;   # 0-UP, 1-RIGHT, 2-DOWN, 3-LEFT 
        self.key_q = []

    def move(self,eat=False):
        if self.key_q:
            self.dir = self.key_q.pop(0)

        if self.dir ==0:
            self.body.insert(0,[self.body[0][0],self.body[0][1]-1])
        if self.dir ==1:
            self.body.insert(0,[self.body[0][0]+1,self.body[0][1]])
        
        if self.dir ==2:
            self.body.insert(0,[self.body[0][0],self.body[0][1]+1])
        
        if self.dir ==3:
            self.body.insert(0,[self.body[0][0]-1,self.body[0][1]])
        if not eat:
            self.body.pop()
    
    def isCollision(self,loc):
        if (loc[0] == self.body[0][0]) and (loc[1] == self.body[0][1]):
            return True
        else:
            return False
        
    def outOfBounds(self):
        if self.body[0][0] < 0 or self.body[0][0] > map_size[0] or self.body[0][1] < 0 or self.body[0][1] > map_size[1]:
            return True
        else:
            return False
class Food:
    def __init__(self):
        self.loc = [10,10]

    def newLoc(self):
        self.loc = [randint(0,map_size[0]),randint(0,map_size[1])]
        print("VALUES: %i %i" % (self.loc[0],self.loc[1]))

def draw(screen,col,map_pt):
    pygame.draw.rect(screen,col,[map_pt[0]*bit_size,map_pt[1]*bit_size,bit_size,bit_size]) 

def main():
    pygame.init()
    font = pygame.font.Font('freesansbold.ttf', 32)
    # Set the height and width of the screen
    screen_size = [(dim+1)*bit_size for dim in map_size]
    margin = 30
    screen_size[1] += margin
    screen = pygame.display.set_mode(screen_size)
    pygame.display.set_caption("Snake")
    
    # Bool to track when game finished
    done = False
    quit = False
     
     # Instantiate
    sn = Snake()
    food = Food()
    eat = False
    score = 0;
    game_speed = 10

    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    
    # Unlatch keys 
    up_pressed = False
    right_pressed = False
    down_pressed = False
    left_pressed = False


    # -------- Main Program Loop -----------
    while not quit:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                quit = True
            if event.type == pygame.KEYDOWN:
                if pygame.key.get_pressed()[pygame.K_SPACE]:
                    sn.__init__();
                    food.__init__();
                    score = 0;
                    game_speed = 10
                    eat = False
                    done = False

        while not done:
            scoreText= "Score: %i  Level: %i " % (score,len(sn.body)-2)
            # ---Quit?
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    done = True
                    quit = True
                if event.type == pygame.KEYDOWN:
                    if pygame.key.get_pressed()[pygame.K_UP] and sn.dir != 2 and not up_pressed:
                        sn.key_q.append(0);
                        up_pressed = True
                    if pygame.key.get_pressed()[pygame.K_RIGHT] and sn.dir != 3 and not right_pressed:
                        sn.key_q.append(1);
                        right_pressed = True
                    if pygame.key.get_pressed()[pygame.K_DOWN] and sn.dir != 0 and not down_pressed:
                        sn.key_q.append(2);
                        down_pressed = True
                    if pygame.key.get_pressed()[pygame.K_LEFT] and sn.dir != 1 and not left_pressed:
                        sn.key_q.append(3);
                        left_pressed = True;
                if event.type == pygame.KEYUP:
                    if not pygame.key.get_pressed()[pygame.K_UP] and up_pressed:
                        up_pressed = False
                    if not pygame.key.get_pressed()[pygame.K_RIGHT] and right_pressed:
                        right_pressed = False
                    if not pygame.key.get_pressed()[pygame.K_DOWN] and down_pressed:
                        down_pressed = False
                    if not pygame.key.get_pressed()[pygame.K_LEFT] and left_pressed:
                        left_pressed = False;
            
            sn.move(eat)    
            eat = False
            
            # Eat Food
            if sn.isCollision(food.loc):
                eat = True
                inSnake = True
                score+= len(sn.body) * game_speed
                while inSnake:
                    food.newLoc()
                    if food.loc not in sn.body:
                        inSnake = False
                    
            # Hit Edges
            if sn.outOfBounds():
                done = True
                    
            # Hit self
            for i,bit in enumerate(sn.body):
                if i == 0:
                    continue
                else:
                    if sn.isCollision(bit):
                        done = True
                
            # --- Drawing
            if not done:
                # Set the screen background
                screen.fill(BLACK)
                # Draw to the screen
                for i,bit in enumerate(sn.body):
                    if i==0:
                        draw(screen,YELLOW,bit)    
                    else:
                        draw(screen,RED,bit)
                draw(screen,GREEN,food.loc)
                pygame.draw.rect(screen,WHITE,[0,screen_size[1]- margin, screen_size[0],2]);

                text = font.render(scoreText,False,WHITE)
                screen.blit(text,[0,screen_size[1]-30])
                # --- Wrap-up
                # Limit frames per second
                game_speed = (len(sn.body) -3 ) + 10
                clock.tick(game_speed)
                
            else:
                replay = font.render("PRESS SPACE TO PLAY AGAIN",False,WHITE)
                screen.blit(replay,[(map_size[0]/2)*bit_size -200,(map_size[1]/2)*bit_size])    
            
            pygame.display.flip()
            

     
    # Close everything down
    pygame.quit()
if __name__ == "__main__":
    main()