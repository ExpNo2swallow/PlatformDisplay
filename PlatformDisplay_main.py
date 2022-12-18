import pygame
import sys
from pygame.locals import *
 
def sys_close():
    pygame.quit()
    sys.exit()

# define a main function
def main():
    pygame.init()
    window = pygame.display.set_mode((800,480))

    clock = pygame.time.Clock()
    
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                sys_close()
            elif event.type==KEYDOWN:
                if event.key==K_ESCAPE:
                    sys_close()
        

        clock.tick(50)
     
     
# run the main function only if this module is executed as the main script
# (if you import this as a module then nothing is executed)
if __name__=="__main__":
    # call the main function
    main()