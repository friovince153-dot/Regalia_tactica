import pygame 
from characters import Bandit, MageHealer 
from combat import Battle

pygame.init()

clock = pygame.time.Clock()
fps = 60

#game window
bottom_panel = 150
screen_width = 800
screen_height =  450 + bottom_panel     
screen = pygame.display.set_mode((screen_width, screen_height))
pygame.display.set_caption("Fantasy")

#font
font = pygame.font.SysFont('Times New Roman', 26)

#font color
rust_red = (183, 65, 14)
green = (0, 255, 0)
red = (255, 0, 0)


#load images
#background image
background = pygame.image.load('image/background/forest.png').convert_alpha()
#panel image
panel_img = pygame.image.load('image/ui/panel.png').convert_alpha()

def draw_text(text, font, text_col, x, y):
    img = font.render(text, True, text_col)
    screen.blit(img, (x, y))

def draw_bg():
    screen.blit(background, (0, 0))

class HealthBar():
    def __init__(self, x, y, hp, max_hp):
        self.x = x
        self.y = y
        self.hp = hp
        self.max_hp = max_hp

    def draw(self, hp):
        #update with new health
        self.hp = hp
        #calculate health ratio
        ratio = self.hp / self.max_hp
        pygame.draw.rect(screen, red, (self.x, self.y, 150, 20))
        pygame.draw.rect(screen, green, (self.x, self.y, 150 * ratio, 20))
        

mage = MageHealer(200, 446, "Sage", max_hp=30, strength=5,
                magic=8, speed=10, resistance=8)

bandit1 = Bandit(542, 442, "Bandit", max_hp=20, strength=10,
                 magic=0, speed=12, resistance=5)

bandit2 = Bandit(692, 442, "Bandit", max_hp=20, strength=10,
                 magic=0, speed=12, resistance=5)

top = screen_height - bottom_panel
Sage_health_bar = HealthBar(100, top + 45, mage.hp, mage.max_hp)
Bandit1_health_bar = HealthBar(550, top + 45, bandit1.hp, bandit1.max_hp)
Bandit2_health_bar = HealthBar(550, top + 110, bandit2.hp, bandit2.max_hp)

battle = Battle(players=[mage], enemies=[bandit1, bandit2])

def draw_panel():
    screen.blit(panel_img, (0, screen_height - bottom_panel))
    draw_text(f'{mage.name} HP: {mage.hp}', font, green, 100, screen_height - bottom_panel + 15)
    for count, i in enumerate([bandit1, bandit2]):
        draw_text(f'{i.name} HP: {i.hp}', font, rust_red, 550, screen_height - bottom_panel + 15 + count * 60)
    Sage_health_bar.draw(mage.hp)
    Bandit1_health_bar.draw(bandit1.hp)
    Bandit2_health_bar.draw(bandit2.hp)

run = True
while run:
    clock.tick(fps)

    clicked = False
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            run = False
        if event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
            clicked = True

    battle.update(pygame.mouse.get_pos(), clicked)   # updates every fighter, so no f.update() calls

    draw_bg()
    for f in (mage, bandit1, bandit2):
        f.draw(screen)
    draw_panel()
    battle.draw(screen)

    pygame.display.update()


pygame.quit()