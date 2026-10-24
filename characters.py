import random
from animation import Animation

class Fighter:
    # name -> dict(path, frames, speed, loop, feet)   (set by subclasses)
    SHEETS = {}
 
    def __init__(self, x, y, name, max_hp, strength, magic, speed, resistance,
                 scale=1, flip=False):
        self.name = name
        self.max_hp = max_hp
        self.hp = max_hp
        self.strength = strength
        self.magic = magic
        self.speed = speed
        self.resistance = resistance
        self.alive = True
        self.x, self.y = x, y            # where the feet stand
        self.pending_hit = None          # (dmg, crit) to apply on the next update

        self.anims = {}
        for key, s in self.SHEETS.items():
            self.anims[key] = Animation(s['path'], s['frames'], scale=scale,
                                        speed=s.get('speed', 100), loop=s.get('loop', True),
                                        flip=flip, feet=s.get('feet', 0),
                                        crop=s.get('crop', (0, 0, 0, 0)))

        self.state = 'idle'
        self.current = self.anims['idle']
        # desync identical characters
        self.current.index = random.randrange(len(self.current.frames))

    @property   
    def rect(self):
        return self.current.image.get_rect(midbottom=(self.x, self.y + self.current.feet))

    @property
    def settled(self):
        if self.alive:
            return self.state == 'idle'
        return self.current.finished


    def play(self, state):
        if state == self.state and self.current.loop:
            return
        self.state = state
        self.current = self.anims[state]
        self.current.reset()

    def start_attack(self, crit, on_hit):
        self.pending_hit = on_hit
        self.play('crit' if crit and 'crit' in self.anims else 'attack')

    def take_damage(self, dmg):
        self.hp = max(0, self.hp - dmg)
        if self.hp == 0:
            self.alive = False
            self.play('die' if 'die' in self.anims else 'hurt')
        else:
            self.play('hurt')

    def _fire_hit(self):
        cb, self.pending_hit = self.pending_hit, None
        if cb:
            cb()

    def update(self):
        self.current.update()

        if self.pending_hit and self.state in ('attack', 'crit'):
            hit = self.SHEETS[self.state].get('hit', len(self.current.frames) - 1)
            if self.current.index >= hit:
                self._fire_hit()


        if self.current.finished and self.alive:
            self._fire_hit()
            self.play('idle')

    def draw(self, surface):
        surface.blit(self.current.image, self.rect)

class MageHealer(Fighter):
    SHEETS = {
        # your original idle sheet (needs its old crop)
        'idle':   dict(path='image/healer/idle.png', frames=8, speed=180, feet=32),
        'attack': dict(path='image/healer/attack.png', frames=10, speed=140, loop=False, feet=32, hit=8),
        'crit':   dict(path='image/healer/crit.png',   frames=11, speed=250, loop=False, feet=32, hit=7),
        'hurt':   dict(path='image/healer/hurt.png',   frames=4,  speed=140, loop=False, feet=32),
    }
    

class Bandit(Fighter):
    SHEETS = {
        'idle':   dict(path='image/bandit/idle.png',   frames=9, speed=180, feet=2),
        'attack': dict(path='image/bandit/attack.png', frames=8, speed=100, loop=False, feet=2, hit=4),
        'hurt':   dict(path='image/bandit/hurt.png',   frames=4, speed=110, loop=False, feet=2),
        'die':    dict(path='image/bandit/die.png',    frames=6, speed=120, loop=False, feet=2),
    }


    