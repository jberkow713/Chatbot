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

# ---------------------------------------------------------------------------
# GAME WORK
player_coords = []
block_coords = []
remove_coords = []
border_size = None

# 1. Initialize Pygame
pygame.init()

# 2. Setup constants
WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
BLOCK_SIZE = 40  # Size of each grid square in pixels

# Colors (RGB)
WHITE = pygame.Color("white")  # Dark Gray
BLACK = pygame.Color('black')
RED = pygame.Color('red')
YELLOW = pygame.Color('yellow')

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

def draw_border(size):
    Rects = []
    hor_blocks = int(WINDOW_WIDTH/size)
    vert_blocks = int(WINDOW_HEIGHT/size)
    start_x =0
    start_y = 0
    end_x = WINDOW_WIDTH-size
    end_y = WINDOW_HEIGHT-size
    for _ in range(hor_blocks):
        Rects.append((start_x,start_y,size,size))
        start_x+=size
    start_x = 0 
    for _ in range(hor_blocks):
        Rects.append((start_x,end_y,size,size))
        start_x+=size
    start_x = 0    
    for _ in range(vert_blocks):
        Rects.append((start_x,start_y,size,size))
        start_y +=size
    start_y = 0    
    for _ in range(vert_blocks):
        Rects.append((end_x,start_y,size,size))
        start_y +=size
    for rect in Rects:
        pygame.draw.rect(screen,RED,rect)
    global border_size
    border_size=size     

def check_manual_collision(x1, y1, x2, y2, BLOCK_SIZE):
  # Check X-axis overlap and Y-axis overlap simultaneously
  x_overlap = (x1 < x2 + BLOCK_SIZE) and (x1 + BLOCK_SIZE > x2)
  y_overlap = (y1 < y2 + BLOCK_SIZE) and (y1 + BLOCK_SIZE > y2)

  return x_overlap and y_overlap
def draw_block_color(x, y, x_block, y_block, color):
  if color == BLACK:
    if (x, y, BLOCK_SIZE, BLOCK_SIZE) not in block_coords:
      block_coords.append((x, y, BLOCK_SIZE, BLOCK_SIZE))

  if color == WHITE:
    new_blocks = []
    # 1. Define the Eraser's real boundaries explicitly
    ex1, ey1 = x, y
    ex2, ey2 = x + BLOCK_SIZE, y + BLOCK_SIZE

    # Use a copy slice [:] so we can safely remove items while looping
    for coord in block_coords[:]:
      bx, by, bw, bh = coord
      bx2, by2 = bx + bw, by + bh

      # Only alter blocks that actually intersect
      if check_manual_collision(x, y, bx, by, BLOCK_SIZE):
        block_coords.remove(coord)

        # 2. Slice Left: If the block extends to the left of the eraser
        if bx < ex1:
          new_blocks.append((bx, by, ex1 - bx, bh))

        # 3. Slice Right: If the block extends to the right of the eraser
        if bx2 > ex2:
          new_blocks.append((ex2, by, bx2 - ex2, bh))

        # 4. Slice Top: Clip what is remaining vertically inside the eraser's X-span
        # We find the exact window of horizontal overlap to prevent double corners
        overlap_left = max(bx, ex1)
        overlap_right = min(bx2, ex2)

        if overlap_left < overlap_right:
          if by < ey1:
            new_blocks.append(
                (overlap_left, by, overlap_right - overlap_left, ey1 - by)
            )

          # 5. Slice Bottom: Clip what is remaining vertically beneath
          if by2 > ey2:
            new_blocks.append(
                (overlap_left, ey2, overlap_right - overlap_left, by2 - ey2)
            )

    # Clean up zero-width or zero-height slivers before appending to prevent stretching artifacts
    valid_remnants = [
        b for b in new_blocks if b[2] > 1 and b[3] > 1
    ]  # 1px threshold
    block_coords.extend(valid_remnants)
'''    
def draw_block_color(x,y,x_block,y_block,color):
    rect = pygame.Rect(x, y, BLOCK_SIZE, BLOCK_SIZE)
    pygame.draw.rect(screen, color, rect)
    if color==BLACK:
        if (x,y) not in block_coords:
            block_coords.append((x,y,BLOCK_SIZE,BLOCK_SIZE))
        # TODO
        # Insert collision function here to check if (x,y) is colliding with any values from the 
        # remove_block list, and then remove it from the remove block list
        
    if color ==WHITE:
        e = enumerate(block_coords)
        for idx,coord in e:
            if check_manual_collision(x,y,coord[0],coord[1],BLOCK_SIZE)==True:
                if coord[1]+BLOCK_SIZE>y:
                    print(y,coord[1])
                    diff = y-coord[1]
                    block_coords[idx]=((coord[0],coord[1],BLOCK_SIZE,diff))
                    return 
                    # print(coord[0],y)
                    # print(coord[0],coord[1]-BLOCK_SIZE)    
                
        # remove_coords.append((x,y))
    #TODO
    # white needs to be drawn initially, so remove_coords need to append the value, but because these values
    # need to remove the remove block from blocks that are being drawn, or from blocks that are touching 
    # the new blocks being drawn, need a collision function that tracks the coords of the draw_block_color(x,y)
    # value, versus all values in the remove list, and if so, remove that from the remove_block list
'''
def add_block():
    if not player_coords:  # Wait until coordinates are initialized
        return
    
    mouse_buttons = pygame.mouse.get_pressed()
    coords= player_coords[0]
        # Check if the left mouse button (index 0) is held down
    if mouse_buttons[2]:
        draw_block_color(*coords,BLOCK_SIZE,BLOCK_SIZE,WHITE)
        return 
    if mouse_buttons[0]:    
        draw_block_color(*coords,BLOCK_SIZE,BLOCK_SIZE,BLACK)

def draw_blocks():
  for b in block_coords:
    # Ensure we use the dynamic width b[2] and height b[3] generated by the eraser
    rect = pygame.Rect(b[0], b[1], b[2], b[3])
    pygame.draw.rect(screen, BLACK, rect)
'''
def draw_blocks():
    for b in block_coords:
        rect = pygame.Rect(b[0], b[1], b[2],b[3])
        pygame.draw.rect(screen, BLACK, rect)
'''    
            

def move_player():
    if not player_coords:  # Wait until coordinates are initialized
        return
        
    speed = 5
    coords = player_coords[0]
    # coords are top left of cube

    # Get the state of all keyboard buttons
    keys = pygame.key.get_pressed()
    
    # Check states independently (allows holding buttons simultaneously)
    if keys[pygame.K_LEFT]:
        
        new = coords[0]-speed
        coords[0] = max(new,border_size) 
    if keys[pygame.K_RIGHT]:
        new = coords[0]+speed
        coords[0] = min(new,WINDOW_WIDTH-BLOCK_SIZE-border_size) 
        
    if keys[pygame.K_UP]:    # Fixed typo
        new = coords[1]-speed
        coords[1] = max(new,border_size) 
    if keys[pygame.K_DOWN]:
        new = coords[1]+speed
        coords[1] = min(new,WINDOW_HEIGHT-BLOCK_SIZE-border_size) 

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
    
    add_block()
    draw_blocks()
    draw_player()
    
    draw_border(BLOCK_SIZE)

    # 4. Refresh display
    pygame.display.flip()
    clock.tick(60)

# Clean up and close
pygame.quit()
sys.exit()