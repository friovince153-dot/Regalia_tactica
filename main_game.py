import pygame 
from characters import MageHealer 

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height =  450 + bottom_panel     
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fantasy")


#load images
#background image
background = pygame.image.load('image/background/forest.png').convert_alpha()
#panel image
panel_img = pygame.image.load('image/ui/panel.png').convert_alpha()


def draw_bg():
    screen.blit(background, (0, 0))

def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))

mage = MageHealer(150, 250, "Mage", max_hp=30, strength=5,
                  magic=20, speed=10, resistance=8)

run = True
while run:
    #frames per second
    clock.tick(fps)

    #draw background
    draw_bg()

    #draw panel
    draw_panel()

    #draw mage
    mage.update()
    mage.draw(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False

    pygame.display.update()


pygame.quit()