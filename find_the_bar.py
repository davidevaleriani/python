#######################################################################
# Find the bar v1.0
#
#   This simple game consists in finding the red vertical bar in a set
#   of different green and red horizontal and vertical bars as quick as
#   possible by clicking on it.
#   Several sessions are performed and a mean score is computated
#
# Author: Davide Valeriani
#         University of Essex
# 
#######################################################################

# Import libraries
import sys, pygame, random
# Init all PyGame modules statements
pygame.init()

# This class represents a single rectangle        
# It derives from the "Sprite" class in Pygame
class Block(pygame.sprite.Sprite):     
    # Constructor. Pass in the color of the block, 
    # and its x and y position
    def __init__(self, color, size, position):
        # Call the parent class (Sprite) constructor
        pygame.sprite.Sprite.__init__(self) 
        
        # Create an image of the block, and fill it with a color.
        self.image = pygame.Surface(size)
        self.image.fill(color)
        
        # Fetch the rectangle object that has the dimensions of the image
        # image.
        # Update the position of this object by setting the values 
        # of rect.x and rect.y
        self.rect = self.image.get_rect()
        self.rect.x, self.rect.y = position

# Check if the user click on the target
def clickOnTarget(target, mouse):
    if (target.rect.x <= mouse[0] <= target.rect.x + target.rect.width) and (target.rect.y <= mouse[1] <= target.rect.y + target.rect.height):
        return True
    return False

# Erase the screen and write the instructions of the game at the top
def reset_screen():
    # Erase screen
    screen.fill(bgColor)
    # Add some text
    header = "Find the vertical red rectangle!"
    myfont = pygame.font.SysFont("Impact", 20)
    label = myfont.render(header, 1, (0, 0, 255))
    screen.blit(label, ((width-myfont.size(header)[0])/2, 0))
    # Update margins
    margin[0] = myfont.size(header)[1] + 10

# Re
def init_rectangles():
    # Init the list of rectangles
    rect_list = pygame.sprite.Group()
    # Add the target
    target = Block(barColors[0], types[0], [random.randint(0 + margin[3], width - types[0][0] - margin[1]), random.randint(0 + margin[0], height - types[0][1] - margin[2])])
    rect_list.add(target)
    # Add some other rectangles
    for i in range(number_of_nontargets):
        # Make sure there is no other targets
        color = barColors[random.randint(0,1)]
        if (color == barColors[0]):
            typ = types[1]
        else:
            typ = types[random.randint(0,1)]
        # Create a new sprite
        newSprite = Block(color, typ, [random.randint(0 + margin[3], width - typ[0] - margin[1]), random.randint(0 + margin[0], height - typ[1] - margin[2])])
        # Check if it collides with another one in the list
        collisions_list = pygame.sprite.spritecollide(newSprite, rect_list, False)
        while (collisions_list):
            # Create a new sprite
            newSprite = Block(color, typ, [random.randint(0 + margin[3], width - typ[0] - margin[1]), random.randint(0 + margin[0], height - typ[1] - margin[2])])
            collisions_list = pygame.sprite.spritecollide(newSprite, rect_list, False)
        # Add the sprite to the list
        rect_list.add(newSprite)
    return rect_list, target

######### INIT ############
# Number of rectangles to draw
number_of_nontargets = 99
# Size of the window
size = width, height = 800, 600
# Number of repetitions
sessions = 10
# Types of rectangles
types = [[10, 40],[40, 10]]
# Background color list (RGB)
bgColor = 255, 255, 255
barColors = [[255, 0, 0], [0, 255, 0]]
# Set margins top, right, bottom, left
margin = [0, 0, 0, 0]
# Background color index
colorIndex = 0
# Create a graphical window
screen = pygame.display.set_mode(size)
pygame.display.set_caption("Find vertical red rectangle!")
######## END INIT ##########
# Erase the screen
reset_screen()
rect_list, target = init_rectangles()
# Print the rects
rect_list.draw(screen)
# Update the visible display
pygame.display.flip()
end = False
clock = pygame.time.Clock()
clock.tick()
resp = []
s = 1
score = 0
f = open('times.txt', 'a')
while s <= sessions:
    # Check if a key is pressed
    for event in pygame.event.get():
        # Exit button
        if event.type == pygame.QUIT: sys.exit()
        # Mouse button - left=yes, right=no
        if event.type == pygame.MOUSEBUTTONDOWN:
            if clickOnTarget(target,pygame.mouse.get_pos()):
                clock.tick()
                #print "Time elapsed:",clock.get_time()/1000.0,"s"
                f.write(str(clock.get_time()/1000.0)+'\n')
                score += 1 / (clock.get_time()/1000.0) * 100
                s += 1
                if s <= sessions:
                    # Generate new game
                    reset_screen()
                    rect_list, target = init_rectangles()
                    rect_list.draw(screen)
                    pygame.display.flip()
                else:
                    break
            elif pygame.mouse.get_pressed()[0]:
                resp.append('yes')
            elif pygame.mouse.get_pressed()[2]:
                resp.append('no')
print '*'*20
print "  Your score: %.0f" % (score/sessions)
print '*'*20
f.close()
