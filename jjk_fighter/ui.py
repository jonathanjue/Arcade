import pygame
import math
import random

WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
RED = (255, 50, 50)
BLUE = (50, 100, 255)
YELLOW = (255, 200, 50)
GRAY = (100, 100, 100)
DARK_GRAY = (40, 40, 40)

CHAR_COLORS = {
    'yuji': (255, 150, 30), 'gojo': (30, 100, 255), 'sukuna': (255, 50, 50),
    'megumi': (180, 50, 255), 'nobara': (255, 100, 150), 'nanami': (200, 180, 100),
    'inumaki': (100, 200, 150), 'todo': (180, 180, 180), 'mahito': (150, 150, 200),
    'jogo': (255, 80, 20), 'hanami': (80, 160, 80), 'choso': (180, 30, 30),
}
CHAR_NAMES = {
    'yuji': 'Yuji Itadori', 'gojo': 'Satoru Gojo', 'sukuna': 'Ryomen Sukuna',
    'megumi': 'Megumi F.', 'nobara': 'Nobara K.', 'nanami': 'Kento Nanami',
    'inumaki': 'Toge Inumaki', 'todo': 'Aoi Todo', 'mahito': 'Mahito',
    'jogo': 'Jogo', 'hanami': 'Hanami', 'choso': 'Choso',
}


def draw_char_preview(surface, char_id, cx, cy, scale=1.0):
    """Draw a unique character preview silhouette at cx,cy"""
    c = CHAR_COLORS.get(char_id, (150, 150, 150))
    s = scale
    # Body
    body_rect = pygame.Rect(cx - int(20*s), cy - int(10*s), int(40*s), int(55*s))
    pygame.draw.rect(surface, c, body_rect, border_radius=int(5*s))
    # Head
    head_r = int(13*s)
    head_y = cy - int(25*s)
    pygame.draw.circle(surface, c, (cx, head_y), head_r)
    # Outline
    pygame.draw.rect(surface, (255,255,255), body_rect, 1, border_radius=int(5*s))
    pygame.draw.circle(surface, (255,255,255), (cx, head_y), head_r, 1)
    # Legs
    pygame.draw.line(surface, c, (cx - int(8*s), cy + int(45*s)), (cx - int(12*s), cy + int(65*s)), int(4*s))
    pygame.draw.line(surface, c, (cx + int(8*s), cy + int(45*s)), (cx + int(12*s), cy + int(65*s)), int(4*s))
    # Arms
    pygame.draw.line(surface, c, (cx - int(20*s), cy), (cx - int(28*s), cy + int(20*s)), int(3*s))
    pygame.draw.line(surface, c, (cx + int(20*s), cy), (cx + int(28*s), cy + int(20*s)), int(3*s))

    # Eyes
    eye_y = head_y - int(2*s)
    pygame.draw.circle(surface, WHITE, (cx - int(5*s), eye_y), int(3*s))
    pygame.draw.circle(surface, WHITE, (cx + int(5*s), eye_y), int(3*s))

    # Unique details
    if char_id == 'nanami':
        # Tie
        pygame.draw.line(surface, (140,120,60), (cx, cy - int(8*s)), (cx, cy + int(15*s)), int(2*s))
        # Cleaver on back
        bx = cx - int(24*s)
        pygame.draw.line(surface, (200,200,210), (bx, cy - int(30*s)), (bx, cy + int(10*s)), int(2*s))
        pygame.draw.polygon(surface, (180,180,190), [(bx, cy-int(35*s)), (bx-int(5*s), cy-int(25*s)), (bx+int(5*s), cy-int(25*s))])
    elif char_id == 'gojo':
        # Blindfold
        pygame.draw.rect(surface, (20,20,20), (cx - int(15*s), head_y - int(5*s), int(30*s), int(7*s)))
        # White hair
        for i in range(-2, 3):
            hx = cx + int(i * 5 * s)
            pygame.draw.line(surface, (230,230,240), (hx, head_y - head_r), (hx + int(i*2*s), head_y - head_r - int(8*s)), int(2*s))
    elif char_id == 'sukuna':
        # Extra eyes
        pygame.draw.circle(surface, (255,220,50), (cx - int(5*s), eye_y - int(5*s)), int(2*s))
        pygame.draw.circle(surface, (255,220,50), (cx + int(5*s), eye_y - int(5*s)), int(2*s))
        pygame.draw.circle(surface, (255,220,50), (cx + int(8*s), eye_y), int(2*s))
        # Marks
        pygame.draw.line(surface, (200,30,30), (cx-int(8*s), head_y+int(3*s)), (cx-int(15*s), head_y+int(8*s)), int(2*s))
        pygame.draw.line(surface, (200,30,30), (cx+int(8*s), head_y+int(3*s)), (cx+int(15*s), head_y+int(8*s)), int(2*s))
    elif char_id == 'megumi':
        # Shadow aura
        aura = pygame.Surface((int(45*s), int(60*s)), pygame.SRCALPHA)
        pygame.draw.rect(aura, (80,30,150,25), aura.get_rect(), border_radius=int(8*s))
        surface.blit(aura, (cx - int(22*s), cy - int(35*s)))
    elif char_id == 'nobara':
        # Hammer
        hx = cx + int(22*s)
        pygame.draw.line(surface, (160,120,80), (hx, cy - int(5*s)), (hx + int(12*s), cy - int(15*s)), int(2*s))
        pygame.draw.rect(surface, (100,100,100), (hx + int(8*s), cy - int(22*s), int(8*s), int(10*s)))
    elif char_id == 'todo':
        # Bigger body
        pygame.draw.rect(surface, c, (cx - int(24*s), cy - int(10*s), int(48*s), int(58*s)), border_radius=int(5*s))
        pygame.draw.rect(surface, (255,255,255), (cx - int(24*s), cy - int(10*s), int(48*s), int(58*s)), 1, border_radius=int(5*s))
    elif char_id == 'inumaki':
        # Mouth covering
        pygame.draw.rect(surface, (40,40,40), (cx - int(8*s), eye_y + int(3*s), int(16*s), int(7*s)))
        # Collar
        pygame.draw.line(surface, (60,60,60), (cx - int(14*s), cy - int(8*s)), (cx - int(18*s), head_y + int(8*s)), int(2*s))
        pygame.draw.line(surface, (60,60,60), (cx + int(14*s), cy - int(8*s)), (cx + int(18*s), head_y + int(8*s)), int(2*s))
    elif char_id == 'mahito':
        # Stitching
        pygame.draw.line(surface, (100,100,120), (cx - int(8*s), cy - int(5*s)), (cx + int(8*s), cy + int(20*s)), 1)
        # Heterochromatic
        pygame.draw.circle(surface, (100,100,200), (cx - int(5*s), eye_y), int(3*s))
        pygame.draw.circle(surface, (200,100,100), (cx + int(5*s), eye_y), int(3*s))
    elif char_id == 'jogo':
        # Volcano head
        pygame.draw.polygon(surface, (200,60,20), [(cx-int(10*s), head_y-head_r+int(2*s)), (cx, head_y-head_r-int(12*s)), (cx+int(10*s), head_y-head_r+int(2*s))])
        # Fire
        pygame.draw.circle(surface, (255,150,30), (cx, head_y - head_r - int(14*s)), int(3*s))
        # Red eyes
        pygame.draw.circle(surface, (255,50,0), (cx - int(5*s), eye_y), int(3*s))
        pygame.draw.circle(surface, (255,50,0), (cx + int(5*s), eye_y), int(3*s))
    elif char_id == 'hanami':
        # Antlers
        pygame.draw.line(surface, (60,120,40), (cx - int(10*s), head_y - int(8*s)), (cx - int(20*s), head_y - int(25*s)), int(2*s))
        pygame.draw.line(surface, (60,120,40), (cx + int(10*s), head_y - int(8*s)), (cx + int(20*s), head_y - int(25*s)), int(2*s))
        # Flower eye
        pygame.draw.circle(surface, (200,200,50), (cx + int(5*s), eye_y), int(4*s))
        pygame.draw.circle(surface, (80,40,20), (cx + int(5*s), eye_y), int(2*s))
    elif char_id == 'choso':
        # Blood vial
        pygame.draw.circle(surface, (180,20,20), (cx + int(16*s), head_y + int(3*s)), int(3*s))
    elif char_id == 'yuji':
        # Hoodie outline
        pygame.draw.arc(surface, (200,120,20), (cx - int(16*s), head_y - int(3*s), int(32*s), int(18*s)), 0, 3.14, 2)


# ===== HEALTH BAR =====
class HealthBar:
    def __init__(self, x, y, w, h, is_left=True):
        self.x, self.y, self.w, self.h = x, y, w, h
        self.is_left = is_left
        self.display_hp = 100

    def draw(self, surface, fighter):
        self.display_hp += (fighter.health - self.display_hp) * 0.12
        pygame.draw.rect(surface, DARK_GRAY, (self.x, self.y, self.w, self.h), border_radius=5)
        hp_w = max(0, int(self.w * (self.display_hp / 100)))
        if self.is_left:
            r = pygame.Rect(self.x, self.y, hp_w, self.h)
        else:
            r = pygame.Rect(self.x + self.w - hp_w, self.y, hp_w, self.h)
        pct = self.display_hp / 100
        color = (int(255*(1-pct)*2), 200, 50) if pct > 0.5 else (255, int(200*pct*2), 50)
        pygame.draw.rect(surface, color, r, border_radius=5)
        pygame.draw.rect(surface, WHITE, (self.x, self.y, self.w, self.h), 2, border_radius=5)
        f = pygame.font.SysFont('arial', 14, bold=True)
        name = getattr(fighter, 'name', '???')
        t = f.render(name.upper(), True, CHAR_COLORS.get(name, WHITE))
        if self.is_left:
            surface.blit(t, (self.x + 4, self.y + 2))
        else:
            surface.blit(t, (self.x + self.w - t.get_width() - 4, self.y + 2))


# ===== CE BAR =====
class CursedEnergyBar:
    def __init__(self, x, y, w, h, is_left=True):
        self.x, self.y, self.w, self.h, self.is_left = x, y, w, h, is_left

    def draw(self, surface, fighter):
        pygame.draw.rect(surface, DARK_GRAY, (self.x, self.y, self.w, self.h), border_radius=3)
        ew = max(0, int(self.w * (fighter.cursed_energy / fighter.max_cursed_energy)))
        if self.is_left:
            r = pygame.Rect(self.x, self.y, ew, self.h)
        else:
            r = pygame.Rect(self.x + self.w - ew, self.y, ew, self.h)
        pygame.draw.rect(surface, CHAR_COLORS.get(fighter.name, BLUE), r, border_radius=3)
        f = pygame.font.SysFont('arial', 9)
        surface.blit(f.render("CE", True, WHITE), (self.x + 2 if self.is_left else self.x + self.w - 16, self.y))


# ===== COMBO =====
class ComboCounter:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def draw(self, surface, fighter):
        if fighter.combo_count > 1:
            f = pygame.font.SysFont('arial', 32, bold=True)
            t = f.render(f"{fighter.combo_count} HIT!", True, YELLOW)
            surface.blit(t, (self.x + random.randint(-1,1), self.y + random.randint(-1,1)))


# ===== ROUND INDICATOR =====
class RoundIndicator:
    def __init__(self, x, y):
        self.x, self.y = x, y
    def draw(self, surface, p1w, p2w):
        for i in range(3):
            pygame.draw.circle(surface, YELLOW if i < p1w else DARK_GRAY, (self.x - 50 + i*22, self.y + 15), 7)
            pygame.draw.circle(surface, YELLOW if i < p2w else DARK_GRAY, (self.x + 50 - i*22, self.y + 15), 7)


# ===== TITLE SCREEN =====
class TitleScreen:
    def __init__(self, sw, sh):
        self.sw, self.sh = sw, sh
        self.sel = 0
        self.options = ["VS AI MODE", "2 PLAYER LOCAL", "STORY MODE", "QUIT"]
        self.frame = 0

    def draw(self, surface):
        self.frame += 1
        surface.fill((12, 8, 22))
        # Title
        tf = pygame.font.SysFont('arial', 68, bold=True)
        surface.blit(tf.render("JUJUTSU KAISEN", True, (255, 50, 50)), (self.sw//2 - tf.render("JUJUTSU KAISEN", True, (255,50,50)).get_width()//2, 70))
        sf = pygame.font.SysFont('arial', 60, bold=True)
        st = sf.render("CURSE CLASH", True, (30, 100, 255))
        surface.blit(st, (self.sw//2 - st.get_width()//2, 150))
        # Particles
        for i in range(6):
            px = self.sw//2 + math.sin(self.frame*0.02 + i)*200
            py = 230 + math.cos(self.frame*0.015 + i*1.3)*20
            pygame.draw.circle(surface, (255, 100+i*20, 30), (int(px), int(py)), 3)
        # Menu
        mf = pygame.font.SysFont('arial', 34)
        for i, opt in enumerate(self.options):
            y = 300 + i * 55
            if i == self.sel:
                hl = pygame.Surface((300, 44), pygame.SRCALPHA)
                pygame.draw.rect(hl, (255, 200, 50, 30), hl.get_rect(), border_radius=6)
                surface.blit(hl, (self.sw//2 - 150, y - 4))
                arr = pygame.font.SysFont('arial', 26, bold=True).render(">", True, YELLOW)
                surface.blit(arr, (self.sw//2 - 170, y + 4))
            t = mf.render(opt, True, YELLOW if i == self.sel else (180,180,190))
            surface.blit(t, (self.sw//2 - t.get_width()//2, y))
        # Controls
        hf = pygame.font.SysFont('arial', 14)
        for i, h in enumerate(["P1: WASD Move | 1/2/3 Attacks | Q Ultimate | S Block | ESC Back",
                                "P2: IJKL Move | 8/9/0 Attacks | U Ultimate | K Block",
                                "ENTER to select | E = lock P1 | O = lock P2"]):
            surface.blit(hf.render(h, True, (100,100,110)), (self.sw//2 - hf.render(h, True, (100,100,110)).get_width()//2, self.sh - 50 + i*18))

    def handle_input(self, keys, jp):
        if jp.get(pygame.K_w) or jp.get(pygame.K_UP): self.sel = (self.sel - 1) % len(self.options)
        if jp.get(pygame.K_s) or jp.get(pygame.K_DOWN): self.sel = (self.sel + 1) % len(self.options)
        if jp.get(pygame.K_RETURN) or jp.get(pygame.K_SPACE): return self.sel
        return -1


# ===== CHARACTER SELECT =====
class CharacterSelect:
    def __init__(self, sw, sh):
        self.sw, self.sh = sw, sh
        self.chars = ['yuji','gojo','sukuna','megumi','nobara','nanami','inumaki','todo','mahito','jogo','hanami','choso']
        self.p1, self.p2 = 0, 1
        self.p1_lock, self.p2_lock = False, False
        self.two_player = False
        self.story_mode = False
        self.story_chapter = None
        self.frame = 0
        self.lock_wait = 0

    def reset(self):
        self.p1, self.p2 = 0, 1
        self.p1_lock, self.p2_lock = False, False
        self.lock_wait = 0
        self.story_mode = False
        self.story_chapter = None

    def draw(self, surface):
        self.frame += 1
        surface.fill((12, 8, 22))

        # Title
        tf = pygame.font.SysFont('arial', 36, bold=True)
        if self.story_mode and self.story_chapter:
            title_text = f"STORY: {self.story_chapter.get('title','Chapter')}"
            tt = tf.render(title_text, True, (255, 200, 50))
        else:
            tt = tf.render("SELECT YOUR SORCERER", True, WHITE)
        surface.blit(tt, (self.sw//2 - tt.get_width()//2, 10))

        # P1/P2 labels
        lf = pygame.font.SysFont('arial', 20, bold=True)
        surface.blit(lf.render("PLAYER 1", True, BLUE), (40, 50))
        if self.story_mode:
            opp_name = CHAR_NAMES.get(self.story_chapter.get('opponent_char','???') if self.story_chapter else '???', '???')
            surface.blit(lf.render(f"VS {opp_name}", True, RED), (self.sw - 200, 50))
        elif self.two_player:
            surface.blit(lf.render("PLAYER 2", True, RED), (self.sw - 150, 50))
        else:
            surface.blit(lf.render("CPU", True, RED), (self.sw - 80, 50))

        # Grid
        cols, rows = 4, 3
        cw, ch = 130, 170
        gap = 12
        gw = cols * (cw + gap) - gap
        sx = (self.sw - gw) // 2
        sy = 75

        for i, cid in enumerate(self.chars):
            col, row = i % cols, i // cols
            x = sx + col * (cw + gap)
            y = sy + row * (ch + gap)
            cc = CHAR_COLORS.get(cid, (150,150,150))
            cr = pygame.Rect(x, y, cw, ch)

            # Card
            pygame.draw.rect(surface, (22, 18, 35), cr, border_radius=8)
            pygame.draw.rect(surface, cc, (x, y, cw, 5), border_radius=3)

            # P1 highlight
            if i == self.p1:
                pygame.draw.rect(surface, BLUE, cr, 3 if not self.p1_lock else 4, border_radius=8)
                ov = pygame.Surface((cw, ch), pygame.SRCALPHA)
                pygame.draw.rect(ov, (50, 100, 255, 22), ov.get_rect(), border_radius=8)
                surface.blit(ov, (x, y))
            # P2 highlight
            if i == self.p2:
                pygame.draw.rect(surface, RED, cr, 3 if not self.p2_lock else 4, border_radius=8)
                ov = pygame.Surface((cw, ch), pygame.SRCALPHA)
                pygame.draw.rect(ov, (255, 50, 50, 22), ov.get_rect(), border_radius=8)
                surface.blit(ov, (x, y))

            # Character preview
            draw_char_preview(surface, cid, x + cw//2, y + 75, scale=0.7)

            # Name
            nf = pygame.font.SysFont('arial', 11, bold=True)
            nt = nf.render(CHAR_NAMES.get(cid, cid), True, cc)
            surface.blit(nt, (x + cw//2 - nt.get_width()//2, y + ch - 28))

            # Lock text
            if i == self.p1 and self.p1_lock:
                lf2 = pygame.font.SysFont('arial', 10, bold=True)
                surface.blit(lf2.render("P1 READY", True, BLUE), (x + cw//2 - 25, y + ch - 14))
            if i == self.p2 and self.p2_lock:
                lf2 = pygame.font.SysFont('arial', 10, bold=True)
                surface.blit(lf2.render("P2 READY", True, RED), (x + cw//2 - 25, y + ch - 14))

        # Move list for selected P1 character
        self._draw_move_list(surface, self.chars[self.p1])

        # Instructions
        hf = pygame.font.SysFont('arial', 14)
        if self.two_player:
            surface.blit(hf.render("P1: A/D/W/S browse, E lock", True, BLUE), (20, self.sh - 30))
            surface.blit(hf.render("P2: J/L/I/K browse, O lock", True, RED), (self.sw - 250, self.sh - 30))
        else:
            ht = hf.render("A/D/W/S to browse, E to lock, ESC to go back", True, (140,140,150))
            surface.blit(ht, (self.sw//2 - ht.get_width()//2, self.sh - 30))

        # Ready message
        if self.p1_lock and (self.p2_lock or not self.two_player):
            rf = pygame.font.SysFont('arial', 28, bold=True)
            rt = rf.render("FIGHT STARTING...", True, YELLOW)
            surface.blit(rt, (self.sw//2 - rt.get_width()//2, self.sh - 55))

    def _draw_move_list(self, surface, char_id):
        """Draw move list panel on the right side"""
        from characters import CHARACTERS
        char = CHARACTERS.get(char_id, {})
        moves = char.get('moves', {})
        supers = char.get('supers', {})

        panel_x = self.sw - 280
        panel_y = 50
        panel_w = 265
        panel_h = 500

        # Panel background
        panel = pygame.Surface((panel_w, panel_h), pygame.SRCALPHA)
        pygame.draw.rect(panel, (0, 0, 0, 160), panel.get_rect(), border_radius=8)
        surface.blit(panel, (panel_x, panel_y))

        # Title
        tf = pygame.font.SysFont('arial', 16, bold=True)
        cc = CHAR_COLORS.get(char_id, WHITE)
        surface.blit(tf.render(f"{CHAR_NAMES.get(char_id, '')} - MOVES", True, cc), (panel_x + 10, panel_y + 8))

        # Moves
        mf = pygame.font.SysFont('arial', 12)
        sf = pygame.font.SysFont('arial', 11)
        y = panel_y + 32
        shown = 0
        for mname, mdata in moves.items():
            if shown >= 14:
                break
            inp = mdata.get('input', '?')
            dmg = mdata.get('damage', 0)
            cost = mdata.get('ce_cost', 0)
            mtype = mdata.get('type', '')
            color = YELLOW if mtype == 'special' else (255,150,150) if mtype in ('ultimate','super') else WHITE

            # Input + name
            display_name = mname.replace('_', ' ').title()
            line = f"{inp:>6}  {display_name}"
            surface.blit(mf.render(line, True, color), (panel_x + 10, y))
            # Damage + cost
            info = f"{dmg} dmg"
            if cost > 0:
                info += f" | {cost} CE"
            surface.blit(sf.render(info, True, (150,150,160)), (panel_x + 10, y + 15))
            y += 32
            shown += 1

        for sname, sdata in supers.items():
            if shown >= 15:
                break
            inp = sdata.get('input', '?')
            dmg = sdata.get('damage', 0)
            cost = sdata.get('ce_cost', 100)
            display_name = sname.replace('_', ' ').title()
            line = f"{inp:>6}  {display_name}"
            surface.blit(mf.render(line, True, (255,100,100)), (panel_x + 10, y))
            info = f"{dmg} dmg | {cost} CE [SUPER]"
            surface.blit(sf.render(info, True, (200,120,120)), (panel_x + 10, y + 15))
            y += 32

    def handle_input(self, keys, jp):
        if not self.p1_lock:
            if jp.get(pygame.K_a): self.p1 = (self.p1 - 1) % len(self.chars)
            if jp.get(pygame.K_d): self.p1 = (self.p1 + 1) % len(self.chars)
            if jp.get(pygame.K_w): self.p1 = max(0, self.p1 - 4)
            if jp.get(pygame.K_s): self.p1 = min(len(self.chars)-1, self.p1 + 4)
            if jp.get(pygame.K_e): self.p1_lock = True  # E to lock P1

        if self.two_player and not self.p2_lock:
            if jp.get(pygame.K_j): self.p2 = (self.p2 - 1) % len(self.chars)
            if jp.get(pygame.K_l): self.p2 = (self.p2 + 1) % len(self.chars)
            if jp.get(pygame.K_i): self.p2 = max(0, self.p2 - 4)
            if jp.get(pygame.K_k): self.p2 = min(len(self.chars)-1, self.p2 + 4)
            if jp.get(pygame.K_o): self.p2_lock = True  # O to lock P2

        if not self.two_player and self.p1_lock and not self.p2_lock:
            avail = [i for i in range(len(self.chars)) if i != self.p1]
            self.p2 = random.choice(avail)
            self.p2_lock = True

        if self.p1_lock and self.p2_lock:
            self.lock_wait += 1
            if self.lock_wait > 40:
                return (self.chars[self.p1], self.chars[self.p2])
        return None


# ===== STORY SELECT =====
class StorySelect:
    def __init__(self, sw, sh):
        self.sw, self.sh = sw, sh
        self.sel = 0
        self.frame = 0

    def draw(self, surface, chapters):
        self.frame += 1
        surface.fill((12, 8, 22))

        tf = pygame.font.SysFont('arial', 36, bold=True)
        tt = tf.render("STORY MODE", True, (255, 200, 50))
        surface.blit(tt, (self.sw//2 - tt.get_width()//2, 15))

        y = 65
        cf = pygame.font.SysFont('arial', 18)
        sf = pygame.font.SysFont('arial', 14)

        for i, (cid, ch) in enumerate(chapters.items()):
            is_sel = (i == self.sel)
            color = YELLOW if is_sel else (150, 150, 160)

            # Background
            if is_sel:
                hl = pygame.Surface((self.sw - 80, 42), pygame.SRCALPHA)
                pygame.draw.rect(hl, (255, 200, 50, 25), hl.get_rect(), border_radius=5)
                surface.blit(hl, (40, y - 2))

            # Chapter info
            title = f"Ch.{cid}: {ch['title']}"
            arc = ch.get('arc', '')
            opp = ch.get('opponent_name', '???')
            info = f"{arc} | vs {opp} | {ch.get('difficulty', 'normal').upper()}"

            surface.blit(cf.render(title, True, color), (55, y))
            surface.blit(sf.render(info, True, (120,120,130) if not is_sel else (180,180,190)), (55, y + 20))
            y += 48

        # Instructions
        hf = pygame.font.SysFont('arial', 14)
        ht = hf.render("W/S to browse, ENTER to start, ESC to go back", True, (140,140,150))
        surface.blit(ht, (self.sw//2 - ht.get_width()//2, self.sh - 30))

    def handle_input(self, keys, jp, max_chapters):
        if jp.get(pygame.K_w) or jp.get(pygame.K_UP): self.sel = max(0, self.sel - 1)
        if jp.get(pygame.K_s) or jp.get(pygame.K_DOWN): self.sel = min(max_chapters - 1, self.sel + 1)
        if jp.get(pygame.K_RETURN) or jp.get(pygame.K_SPACE): return self.sel + 1
        return -1


# ===== KO SCREEN =====
class KO_Screen:
    def __init__(self, sw, sh):
        self.sw, self.sh = sw, sh
        self.frame = 0
        self.alive = True

    def draw(self, surface, winner_name):
        self.frame += 1
        sz = min(110, 25 + self.frame * 4)
        f = pygame.font.SysFont('arial', int(sz), bold=True)
        t = f.render("K.O.!", True, (255, 50, 50))
        shake = max(0, 8 - self.frame) * (1 if self.frame % 2 == 0 else -1)
        surface.blit(t, (self.sw//2 - t.get_width()//2 + shake, self.sh//3 - t.get_height()//2))
        if self.frame > 25:
            wf = pygame.font.SysFont('arial', 32)
            wt = wf.render(f"{winner_name.upper()} WINS!", True, (255, 200, 50))
            surface.blit(wt, (self.sw//2 - wt.get_width()//2, self.sh//2))
        if self.frame > 90:
            hf = pygame.font.SysFont('arial', 18)
            ht = hf.render("Press ENTER to continue", True, (150,150,160))
            surface.blit(ht, (self.sw//2 - ht.get_width()//2, self.sh//2 + 50))
        if self.frame > 90:
            self.alive = False
