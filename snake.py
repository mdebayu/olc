import pygame
from random import randint

bit_size = 40
size = [bit_size * 20, bit_size*10]

# Define some colors
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
BLUE = (0, 0, 255)

class Snake:
    def __init__(self,scrn):
        self.head =[0,0]
        self.dir = [0,1];   
        self.length=1
        self.visited = [[0,0]]
        self.vis_no =len(self.visited);
        self.screen = scrn;
        self.next_move=[]

    def update(self):
        if self.next_move:
            tmp = self.next_move.pop(0);
            if (self.dir[0]!=0 and tmp[0]==0):
                self.dir = [tmp[0],tmp[1]]
            if (self.dir[1]!=0 and tmp[1]==0):
                self.dir = [tmp[0],tmp[1]]
        self.visited.append([self.head[0],self.head[1]])

        if self.vis_no > self.length:
            self.visited.pop(0)
            self.vis_no-=1
        
        self.head[0] += self.dir[0]*bit_size
        self.head[1] += self.dir[1]*bit_size
        self.vis_no +=1

    def draw(self):
        drawRects(self.screen,BLUE,self.visited[-1])
        for i in range(self.length-1):
            drawRects(self.screen,RED,self.visited[self.vis_no - 2  - i])

    def isCollision(self,loc):
        if self.head[0] == loc[0] and self.head[1] == loc[1]:
            return True
        else:
            return False
    def inbounds(self, size):
        if self.head[0] < 0 or self.head[0] > size[0] - bit_size or self.head[1] < 0 or self.head[1] > size[1] - bit_size:
            return True
        else:
            return False

class Food:
    def __init__(self,scrn):
        self.loc = [randint(0,size[0]),randint(0,size[1])]
        self.loc[0] = self.loc[0] - self.loc[0]%bit_size;
        self.loc[1] = self.loc[1] - self.loc[1]%bit_size 
        self.screen = scrn;
        self.eaten = False

    def update(self):
        if self.eaten:
            self.loc = [randint(0,size[0]),randint(0,size[1])]
            self.loc[0] = self.loc[0] - self.loc[0]%bit_size;
            self.loc[1] = self.loc[1] - self.loc[1]%bit_size 
            self.eaten = False

    def draw(self):
        drawRects(self.screen,GREEN,self.loc)

def drawRects(screen,col, rect):
    mgn = 2;        # margin width 
    pygame.draw.rect(screen, WHITE ,(rect[0],rect[1], bit_size, bit_size))
    pygame.draw.rect(screen, col ,(rect[0]+mgn,rect[1]+mgn, bit_size-mgn*2, bit_size-mgn*2))

def isCollision(rec1,rec2):
    if abs(rec1[0] - rec2[0]) < bit_size and abs(rec1[1] - rec2[1]) < bit_size:
        return True
    else:
        return False

def main():
    pygame.init()
 
    # Set the height and width of the screen
    
    screen = pygame.display.set_mode(size)
    pygame.display.set_caption("Snake")
 
    sn = Snake(screen);
    foo = Food(screen)
    tmp =None
    speed = 1

    # Bool to track when game finished
    done = False
     
    # Used to manage how fast the screen updates
    clock = pygame.time.Clock()
    
    delay = 0; 
    # -------- Main Program Loop -----------
    while not done:
        # ---Quit?
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                done = True
        
        if pygame.key.get_pressed()[pygame.K_UP]:
            tmp =[0,-1];
        if pygame.key.get_pressed()[pygame.K_DOWN]:
            tmp = [0,1];
        if pygame.key.get_pressed()[pygame.K_LEFT]:
            tmp =[-1,0];
        if pygame.key.get_pressed()[pygame.K_RIGHT]: 
            tmp = [1,0];

        if delay % bit_size == 0:
            if sn.next_move:
                if tmp != sn.next_move[-1]:
                    sn.next_move.append(tmp)
            else:
                if tmp: 
                    sn.next_move.append([tmp[0],tmp[1]])
            sn.update()
            foo.update()
            print(sn.visited)
            print(sn.vis_no)
            print(sn.next_move)
            print("\n\n")
            
            # Eat Food
            if sn.isCollision(foo.loc):
                sn.length+=1
                foo.eaten = True
                # Get Faster Over Time
                if sn.length % 2 == 0:
                    speed += 1
                    print("SPEED UP")
                print("EATEN")
            
            # Hit Edges
            if sn.inbounds(size):
                done = True
                print("EDGE HIT")
            
            # Hit self
            for i in range(sn.length):
                if sn.isCollision(sn.visited[sn.vis_no - 2 - i]):
                    done = True
                    print("SELF HIT")
            

        # --- Drawing
        # Set the screen background
        screen.fill(BLACK)
     
        # Draw to the screen
        sn.draw()
        foo.draw()
        
        # --- Wrap-up
        # Limit frames per second
        clock.tick(100)
     
        # Go ahead and update the screen with what we've drawn.
        pygame.display.flip()
        delay += 1
        #pygame.time.wait(10)
     
    # Close everything down
    pygame.quit()
if __name__ == "__main__":
    main()