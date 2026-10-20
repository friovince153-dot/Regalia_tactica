import pygame


class MageHealer:
    def __init__(self, x, y, name, max_hp, strength, magic, speed, resistance,
                 frame_w=64, frame_h=64, num_frames=4, anim_speed=120):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.magic = magic
        self.speed = speed
        self.resistance = resistance
        self.alive = True

        # Load the sheet once and slice it into frames
        sheet = pygame.image.load('image/healer/idle.png').convert_alpha()
        self.frames = [
            sheet.subsurface((i * frame_w, 0, frame_w, frame_h))
            for i in range(num_frames)
        ]

        self.frame_index = 0
        self.anim_speed = anim_speed          # ms per frame
        self.last_update = pygame.time.get_ticks()

        self.image = self.frames[0]
        self.rect = self.image.get_rect(topleft=(x, y))

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update >= self.anim_speed:
            self.frame_index = (self.frame_index + 1) % len(self.frames)
            self.image = self.frames[self.frame_index]
            self.last_update = now

    def draw(self, surface):
        surface.blit(self.image, self.rect)