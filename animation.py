import pygame


class Animation:
    def __init__(self, path, num_frames, scale=1, speed=100, loop=True,
                flip=False, feet=0, crop=(0, 0, 0, 0)):
        sheet = pygame.image.load(path).convert_alpha()
        sheet_w, sheet_h = sheet.get_size()
        frame_w = sheet_w // num_frames
        frame_h = sheet_h
        left, top, right, bottom = crop


        left, top, right, bottom = crop
        self.frames = []
        for i in range(num_frames):
            frame = sheet.subsurface((i * frame_w + left, top,
                                    frame_w - left - right,
                                    frame_h - top - bottom))
        
            if scale != 1:
                w, h = frame.get_size()
                frame = pygame.transform.scale(frame, (round(w * scale), round(h * scale)))

            if flip:
                frame = pygame.transform.flip(frame, True, False)
            self.frames.append(frame)


        self.speed = speed            # ms per frame
        self.loop = loop
        self.feet = feet
        self.index = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()

    @property
    def image(self):
        return self.frames[self.index]

    @property
    def rect(self):
        return self.image.get_rect()

    def reset(self):
        self.index = 0
        self.finished = False
        self.last_update = pygame.time.get_ticks()

    def update(self):
        now = pygame.time.get_ticks()
        if now - self.last_update < self.speed:
            return
        self.last_update = now

        if self.index < len(self.frames) - 1:
            self.index += 1
        elif self.loop:
            self.index = 0
        else:
            self.finished = True