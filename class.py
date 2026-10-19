import random 
import sys
import pygame

class Nums:
    def __init__(self, low,high,count):
        self.low = low 
        self.high = high 
        self.count = count 
    def rand_return(self):
        return [random.randint(self.low,self.high) for _ in range(self.count)]
    def low_return(self):
        return [self.low for _ in range(self.count)]
    def high_return(self):
        return [self.high for _ in range(self.count)]
    def change_count(self,num):
        self.count = num 
    def avg_return(self):
        return [(self.high+self.low)/2 for _ in range(self.count)]
                   
n = Nums(1,10,10)
print(n.rand_return())
print(n.low_return())
n.change_count(20)
print(n.high_return())
n.change_count(5)
print(n.avg_return())   

def create_list_nums(count):
    return [((random.randint(0,10),random.randint(0,25), random.randint(0,25))) for _ in range(count)]

c = create_list_nums(10)
for x in c:
    print(x)
    n = Nums(*x)
    print(n.low_return())
    print(n.high_return())





player_coords = []

# 1. Initialize Pygame
pygame.init()

# 2. Setup constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BLOCK_SIZE = 40  # Size of each grid square in pixels

# Colors (RGB)
WHITE = pygame.Color("white")  # Dark Gray
BLACK = pygame.Color('black')

# 3. Create the display window
screen = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))
pygame.display.set_caption("Pygame Grid Example")
clock = pygame.time.Clock()

def draw_player():
    if player_coords == []:
        # Fixed: standard order is X (width) then Y (height)
        coords = [WINDOW_WIDTH // 2, WINDOW_HEIGHT // 2]
        player_coords.append(coords)
    else:
        coords = player_coords[0]    
    
    # Draw a solid black square (removed the '1' parameter so it fills completely)
    rect = pygame.Rect(coords[0], coords[1], BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, BLACK, rect)

def move_player():
    if not player_coords:  # Wait until coordinates are initialized
        return
        
    speed = 5
    coords = player_coords[0]
    
    # Get the state of all keyboard buttons
    keys = pygame.key.get_pressed()
    
    # Check states independently (allows holding buttons simultaneously)
    if keys[pygame.K_LEFT]:
        coords[0] -= speed 
    if keys[pygame.K_RIGHT]:
        coords[0] += speed 
    if keys[pygame.K_UP]:    # Fixed typo
        coords[1] -= speed 
    if keys[pygame.K_DOWN]:
        coords[1] += speed 

running = True
while running:
    # 1. Handle events (Only for window closing/one-time menus)
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    # 2. Handle continuous input & updates
    move_player()

    # 3. Draw everything
    screen.fill(WHITE)
    draw_player()

    # 4. Refresh display
    pygame.display.flip()
    clock.tick(60)

# Clean up and close
pygame.quit()
sys.exit()