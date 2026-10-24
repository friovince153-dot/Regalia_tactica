import random
import pygame
 
# ---- tuning -------------------------------------------------------------
CRIT_BASE = 0.5          # 5% base chance
CRIT_PER_SPEED = 0.01     # +1% per point of speed
CRIT_CAP = 0.5
CRIT_MULT = 2.0
DAMAGE_SPREAD = 0         # +/- random swing on every hit
WAIT_MS = 700             # pause before each turn acts (stops clicks carrying over)
POPUP_MS = 900
 
 
def crit_chance(fighter):
    return min(CRIT_CAP, CRIT_BASE + fighter.speed * CRIT_PER_SPEED)
 
 
def roll_attack(attacker, target):
    """Returns (damage, crit). Only fighters with a 'crit' animation can crit."""
    power = max(attacker.strength, attacker.magic)
    dmg = max(1, power - target.resistance + random.randint(-DAMAGE_SPREAD, DAMAGE_SPREAD))
    crit = 'crit' in attacker.anims and random.random() < crit_chance(attacker)
    if crit:
        dmg = int(dmg * CRIT_MULT)
    return dmg, crit
 
 
class Popup:
    def __init__(self, surf, x, y):
        self.surf, self.x, self.y = surf, x, y
        self.born = pygame.time.get_ticks()
 
 
class Battle:
    def __init__(self, players, enemies, sort_by_speed=False):
        self.players = players
        self.enemies = enemies
        self.order = players + enemies
        if sort_by_speed:
            self.order.sort(key=lambda f: -f.speed)
        self.turn = 0
        self.phase = 'wait'               # 'wait' (ready to act) -> 'acting' (animations running)
        self.phase_start = pygame.time.get_ticks()
        self.actor = self.order[0]
        self.target = None
        self.hover = None                 # enemy under the mouse on the player's turn
        self.result = None                # None | 'victory' | 'defeat'
        self.popups = []
        self.font = pygame.font.SysFont(None, 32)
        self.crit_font = pygame.font.SysFont(None, 56)
        self.banner_font = pygame.font.SysFont(None, 96)
 
    # ---------------------------------------------------------------- helpers
    @staticmethod
    def _alive(group):
        return [f for f in group if f.alive]
 
    def _enemy_at(self, pos):
        for e in self.enemies:
            if e.alive and e.rect.collidepoint(pos):
                return e
        return None
 
    def _next_turn(self):
        self.turn = (self.turn + 1) % len(self.order)
        self.phase = 'wait'
        self.phase_start = pygame.time.get_ticks()
        self.target = None
 
    def _popup(self, target, dmg, crit):
        if crit:
            surf = self.crit_font.render(f'{dmg}!', True, (255, 215, 0))
        else:
            surf = self.font.render(str(dmg), True, (255, 255, 255))
        self.popups.append(Popup(surf, target.x, target.rect.top))
 
    def _resolve(self, attacker, target, dmg, crit):
        """Runs on the attack animation's hit frame."""
        target.take_damage(dmg)
        self._popup(target, dmg, crit)
 
    def _start_attack(self, attacker, target):
        dmg, crit = roll_attack(attacker, target)     # decided up front so the right animation plays
        self.actor, self.target = attacker, target
        self.phase = 'acting'
        attacker.start_attack(crit, lambda: self._resolve(attacker, target, dmg, crit))
 
    def _check_result(self):
        if not self._alive(self.enemies):
            self.result = 'victory'
        elif not self._alive(self.players):
            self.result = 'defeat'
 
    # ----------------------------------------------------------------- update
    def update(self, mouse_pos, clicked):
        for f in self.order:
            f.update()
 
        self.hover = None
        if self.result:
            return
 
        now = pygame.time.get_ticks()
 
        if self.phase == 'wait':
            actor = self.order[self.turn]
            if not actor.alive:
                self._next_turn()
                return
            self.actor = actor
            if now - self.phase_start < WAIT_MS:
                return
            if actor in self.players:                         # player: click an enemy
                self.hover = self._enemy_at(mouse_pos)
                if clicked and self.hover:
                    self._start_attack(actor, self.hover)
            else:                                             # enemy AI: hit a random living player
                self._start_attack(actor, random.choice(self._alive(self.players)))
 
        elif self.phase == 'acting':
            if self.actor.settled and self.target.settled:
                self._check_result()
                if not self.result:
                    self._next_turn()
 
    # ------------------------------------------------------------------- draw
    @staticmethod
    def _marker(surface, fighter, color):
        r = fighter.rect
        x, y = r.centerx, r.top - 6
        pygame.draw.polygon(surface, color, [(x - 9, y - 14), (x + 9, y - 14), (x, y)])
 
    def draw(self, surface):
        if not self.result and self.phase == 'wait':
            if self.actor.alive:
                self._marker(surface, self.actor, (80, 220, 80))        # whose turn
            if self.hover:
                self._marker(surface, self.hover, (255, 70, 70))        # who you'd hit
 
        now = pygame.time.get_ticks()
        for p in self.popups[:]:
            age = now - p.born
            if age > POPUP_MS:
                self.popups.remove(p)
                continue
            p.surf.set_alpha(255 - int(255 * age / POPUP_MS))
            surface.blit(p.surf, p.surf.get_rect(midbottom=(p.x, p.y - 10 - age // 18)))
 
        if self.result:
            text, col = ('VICTORY', (255, 215, 0)) if self.result == 'victory' else ('DEFEAT', (200, 40, 40))
            img = self.banner_font.render(text, True, col)
            surface.blit(img, img.get_rect(center=(surface.get_width() // 2, surface.get_height() // 3)))
