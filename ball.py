#######################################################################
# Bouncing ball v1.0
#
#   This program is a first introduction to PyGame library, adapted
#   from the PyGame first tutorial.
#   It simply draw a ball on the screen and move it around.
#   If the ball bounce to the border, the background change color
#
# Author: Davide Valeriani
#         University of Essex
# 
#######################################################################

# Import libraries
import sys, pygame
# Init all PyGame modules statements
pygame.init()

# Size of the window
size = width, height = 640, 480
# Set linear speed (x, y)
speed = [1, 2]
# Background color list (RGB)
colors = [[0, 0, 0], [255, 0, 0], [255, 255, 0], [255, 0, 255], [0, 255, 0], [0, 255, 255], [0, 0, 255], [255, 255, 255]]
# Background color index
colorIndex = 0
# Create a graphical window
screen = pygame.display.set_mode(size)
# Load an image from file
ball = pygame.image.load("ball.gif")
# Get bounding box of the image
ballrect = ball.get_rect()
while 1:
    # Check if a key is pressed
    for event in pygame.event.get():
        if event.type == pygame.KEYDOWN: sys.exit()
    # Apply a speed to the bounding box of the image
    ballrect = ballrect.move(speed)
    # If the ball is out of the screen
    if ballrect.left < 0 or ballrect.right > width:
        # reverse the speed
        speed[0] = -speed[0]
        # change the background color
        colorIndex = (colorIndex + 1) % len(colors)
    if ballrect.top < 0 or ballrect.bottom > height:
        speed[1] = -speed[1]
        colorIndex = (colorIndex + 1) % len(colors)
    # Erase the screen to prepare printing the next frame
    screen.fill(colors[colorIndex])
    # Copy pixels from ball image to ballrect surface that will be drawn on the screen
    screen.blit(ball, ballrect)
    # Update the visible display
    pygame.display.flip()
    # Make it slower
    pygame.time.delay(10)
