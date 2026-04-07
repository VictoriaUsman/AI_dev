"""
╔══════════════════════════════════════════════════════════════╗
║           SERPENT'S PATH — A Text Adventure Game             ║
║                                                              ║
║  You are Naga, a mystical python who must slither through    ║
║  dangerous lands, eat prey to grow stronger, and reach       ║
║  the Sacred Nest before the Eagle King hunts you down.       ║
╚══════════════════════════════════════════════════════════════╝
"""

import random
import time
import os
import sys

# ── CONSTANTS ──────────────────────────────────────────────────
BOARD_WIDTH  = 20
BOARD_HEIGHT = 10
DIRECTIONS   = {"w": (0, -1), "s": (0, 1), "a": (-1, 0), "d": (1, 0)}
DIR_NAMES    = {"w": "North", "s": "South", "a": "West", "d": "East"}

PREY_TYPES = [
    {"name": "Mouse",   "emoji": "🐭", "points": 1, "rarity": 50},
    {"name": "Frog",    "emoji": "🐸", "points": 2, "rarity": 30},
    {"name": "Rabbit",  "emoji": "🐇", "points": 3, "rarity": 15},
    {"name": "Peacock", "emoji": "🦚", "points": 5, "rarity":  5},
]

HAZARDS = [
    {"name": "Mongoose",    "emoji": "🦡", "damage": 2},
    {"name": "Thorn Bush",  "emoji": "🌵", "damage": 1},
    {"name": "Eagle Scout", "emoji": "🦅", "damage": 3},
]

LORE = [
    "Ancient serpent lore says: 'He who grows longest, rules the jungle.'",
    "A faint hiss echoes... the Eagle King draws nearer.",
    "The wind carries the scent of prey to your forked tongue.",
    "Your scales shimmer in the dappled light of the canopy.",
    "Local legend speaks of a Golden Egg hidden in the Sacred Nest.",
]

# ── UTILS ──────────────────────────────────────────────────────
def clear():
    os.system("cls" if os.name == "nt" else "clear")

def slow_print(text, delay=0.03):
    for ch in text:
        sys.stdout.write(ch)
        sys.stdout.flush()
        time.sleep(delay)
    print()

def pause(msg="Press Enter to continue..."):
    input(f"\n  {msg}")

def bar(current, maximum, width=20, fill="█", empty="░"):
    filled = int(width * current / max(maximum, 1))
    return fill * filled + empty * (width - filled)

# ── GAME STATE ─────────────────────────────────────────────────
class Snake:
    def __init__(self):
        cx, cy = BOARD_WIDTH // 2, BOARD_HEIGHT // 2
        self.body   = [(cx, cy), (cx - 1, cy), (cx - 2, cy)]  # head first
        self.hp     = 10
        self.max_hp = 10
        self.score  = 0
        self.length = len(self.body)
        self.turns  = 0
        self.eaten  = []
        self.poison = 0     # poison ticks remaining
        self.shield = False # one-turn shield

    @property
    def head(self):
        return self.body[0]

    def move(self, dx, dy):
        hx, hy = self.head
        new_head = (hx + dx, hy + dy)
        self.body.insert(0, new_head)
        # Grow only when we just ate (controlled externally)
        self.body.pop()

    def grow(self):
        self.body.append(self.body[-1])
        self.length = len(self.body)

    def self_collision(self):
        return self.head in self.body[1:]

    def wall_collision(self):
        x, y = self.head
        return not (0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT)


class World:
    def __init__(self):
        self.prey    = {}   # (x,y) -> prey dict
        self.hazards = {}   # (x,y) -> hazard dict
        self.nest    = self._place_nest()
        self._spawn_items(prey_count=5, hazard_count=3)
        self.eagle_pos  = self._random_edge()
        self.eagle_hp   = 8
        self.eagle_turn = 0  # moves every N turns

    def _random_pos(self, margin=2):
        return (
            random.randint(margin, BOARD_WIDTH  - margin - 1),
            random.randint(margin, BOARD_HEIGHT - margin - 1),
        )

    def _random_edge(self):
        side = random.choice(["top","bottom","left","right"])
        if side == "top":    return (random.randint(0, BOARD_WIDTH-1), 0)
        if side == "bottom": return (random.randint(0, BOARD_WIDTH-1), BOARD_HEIGHT-1)
        if side == "left":   return (0, random.randint(0, BOARD_HEIGHT-1))
        return (BOARD_WIDTH-1, random.randint(0, BOARD_HEIGHT-1))

    def _place_nest(self):
        return (BOARD_WIDTH - 3, BOARD_HEIGHT - 3)

    def _spawn_items(self, prey_count, hazard_count):
        occupied = {self.nest}
        for _ in range(prey_count):
            pos = self._random_pos()
            while pos in occupied:
                pos = self._random_pos()
            occupied.add(pos)
            roll = random.randint(1, 100)
            cumulative = 0
            chosen = PREY_TYPES[0]
            for pt in PREY_TYPES:
                cumulative += pt["rarity"]
                if roll <= cumulative:
                    chosen = pt
                    break
            self.prey[pos] = chosen

        for _ in range(hazard_count):
            pos = self._random_pos()
            while pos in occupied:
                pos = self._random_pos()
            occupied.add(pos)
            self.hazards[pos] = random.choice(HAZARDS)

    def move_eagle(self, snake_head):
        """Eagle moves one step toward the snake's head."""
        ex, ey = self.eagle_pos
        hx, hy = snake_head
        dx = 0 if ex == hx else (1 if hx > ex else -1)
        dy = 0 if ey == hy else (1 if hy > ey else -1)
        # Move diagonally (pick one axis if both differ)
        if dx != 0 and dy != 0:
            if random.random() < 0.5:
                dy = 0
            else:
                dx = 0
        self.eagle_pos = (ex + dx, ey + dy)

    def replenish(self):
        """Keep at least 3 prey items on the board."""
        while len(self.prey) < 3:
            pos = self._random_pos()
            if pos not in self.prey and pos not in self.hazards:
                roll = random.randint(1, 100)
                cumulative = 0
                chosen = PREY_TYPES[0]
                for pt in PREY_TYPES:
                    cumulative += pt["rarity"]
                    if roll <= cumulative:
                        chosen = pt
                        break
                self.prey[pos] = chosen


# ── RENDERING ──────────────────────────────────────────────────
def render(snake: Snake, world: World, message: str = ""):
    clear()
    # Build grid
    grid = [["·"] * BOARD_WIDTH for _ in range(BOARD_HEIGHT)]

    # Nest
    nx, ny = world.nest
    if 0 <= nx < BOARD_WIDTH and 0 <= ny < BOARD_HEIGHT:
        grid[ny][nx] = "N"

    # Hazards
    for (x, y), h in world.hazards.items():
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            grid[y][x] = h["emoji"]

    # Prey
    for (x, y), p in world.prey.items():
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            grid[y][x] = p["emoji"]

    # Eagle King
    ex, ey = world.eagle_pos
    if 0 <= ex < BOARD_WIDTH and 0 <= ey < BOARD_HEIGHT:
        grid[ey][ex] = "🦅"

    # Snake body
    for i, (x, y) in enumerate(snake.body):
        if 0 <= x < BOARD_WIDTH and 0 <= y < BOARD_HEIGHT:
            grid[y][x] = "●" if i == 0 else "○"

    # Draw border + grid
    border_top    = "  ┌" + "─" * (BOARD_WIDTH * 2) + "┐"
    border_bottom = "  └" + "─" * (BOARD_WIDTH * 2) + "┘"
    print(border_top)
    for row in grid:
        cells = " ".join(c if len(c) > 1 else c + " " for c in row)
        # fix width for emoji (2 chars wide)
        line = ""
        for c in row:
            if len(c.encode("utf-8")) > 1:  # emoji
                line += c
            else:
                line += c + " "
        print("  │" + line + "│")
    print(border_bottom)

    # HUD
    hp_bar  = bar(snake.hp, snake.max_hp, width=15)
    eagle_bar = bar(world.eagle_hp, 8, width=10)
    poison_str = f"  ☠  Poison: {snake.poison} turns" if snake.poison > 0 else ""
    shield_str = "  🛡 Shielded!" if snake.shield else ""

    print(f"\n  🐍 Naga  HP [{hp_bar}] {snake.hp}/{snake.max_hp}{poison_str}{shield_str}")
    print(f"  🦅 Eagle HP [{eagle_bar}] {world.eagle_hp}/8   |   Length: {snake.length}   Score: {snake.score}   Turn: {snake.turns}")

    if message:
        print(f"\n  ► {message}")

    print("\n  Move: [W]North [S]South [A]West [D]East  |  [I]nventory  [Q]uit")


# ── INVENTORY / STATUS ─────────────────────────────────────────
def show_inventory(snake: Snake):
    clear()
    print("\n  ═══════════════ NAGA'S JOURNAL ═══════════════")
    print(f"  Score  : {snake.score}")
    print(f"  Length : {snake.length} segments")
    print(f"  HP     : {snake.hp}/{snake.max_hp}")
    print(f"  Turns  : {snake.turns}")
    print(f"\n  Prey eaten:")
    if not snake.eaten:
        print("    (none yet)")
    from collections import Counter
    for name, count in Counter(snake.eaten).items():
        print(f"    {name} × {count}")
    print(f"\n  Lore: {random.choice(LORE)}")
    print("  ══════════════════════════════════════════════")
    pause()


# ── INTRO ──────────────────────────────────────────────────────
def intro():
    clear()
    slow_print("""
  ╔══════════════════════════════════════════════════════════════╗
  ║              S E R P E N T ' S   P A T H                    ║
  ╚══════════════════════════════════════════════════════════════╝
""", delay=0.01)
    slow_print("  You are NAGA — an ancient mystical python awakened in the jungle.")
    slow_print("  Slither through the wilds, devour prey to grow powerful,")
    slow_print("  and reach the Sacred Nest (N) before the Eagle King catches you.")
    slow_print("\n  ── CONTROLS ──────────────────────────────────────────────────")
    slow_print("  W / S / A / D  →  Move North / South / West / East")
    slow_print("  I              →  Open inventory / journal")
    slow_print("  Q              →  Quit game")
    slow_print("\n  ── HOW TO WIN ────────────────────────────────────────────────")
    slow_print("  • Reach the Sacred Nest (N) with length ≥ 8 to win.")
    slow_print("  • Eat rare prey (🦚 Peacock) to gain 5 points & grow fast.")
    slow_print("  • Avoid hazards and the Eagle King (🦅) — he hunts you!")
    slow_print("\n  ── HOW TO LOSE ───────────────────────────────────────────────")
    slow_print("  • HP reaches 0   • You hit a wall   • You bite yourself")
    pause("Press Enter to begin your journey...")


# ── GAME OVER / WIN ────────────────────────────────────────────
def game_over(snake: Snake, reason: str):
    clear()
    slow_print(f"""
  ╔══════════════════════════════════════════╗
  ║            ☠  GAME OVER  ☠              ║
  ╚══════════════════════════════════════════╝

  {reason}

  Final Score  : {snake.score}
  Length       : {snake.length} segments
  Turns taken  : {snake.turns}
""", delay=0.02)
    pause("Press Enter to exit.")


def victory(snake: Snake):
    clear()
    slow_print("""
  ╔══════════════════════════════════════════╗
  ║          🥚  VICTORY!  YOU WIN  🥚       ║
  ╚══════════════════════════════════════════╝

  You reached the Sacred Nest and claimed the Golden Egg!
  The Eagle King retreats into the clouds, defeated.
  Naga coils triumphantly — the jungle is yours.
""", delay=0.02)
    slow_print(f"  Final Score  : {snake.score}")
    slow_print(f"  Length       : {snake.length} segments")
    slow_print(f"  Turns taken  : {snake.turns}")
    pause("Press Enter to exit.")


# ── MAIN GAME LOOP ─────────────────────────────────────────────
def play():
    intro()

    snake = Snake()
    world = World()
    message = "Your journey begins. Slither wisely, Naga."

    while True:
        render(snake, world, message)
        message = ""

        # ── Input ──
        raw = input("\n  Your move: ").strip().lower()

        if raw == "q":
            slow_print("\n  You retreat into the undergrowth. Farewell, Naga.")
            break

        if raw == "i":
            show_inventory(snake)
            continue

        if raw not in DIRECTIONS:
            message = "Invalid key! Use W/A/S/D to move."
            continue

        dx, dy = DIRECTIONS[raw]
        dir_name = DIR_NAMES[raw]

        # ── Move snake ──
        snake.move(dx, dy)
        snake.turns += 1
        grew = False

        # ── Wall collision ──
        if snake.wall_collision():
            game_over(snake, f"You crashed into the jungle wall heading {dir_name}.")
            return

        # ── Self collision ──
        if snake.self_collision():
            game_over(snake, "You bit your own tail! A fatal mistake.")
            return

        hx, hy = snake.head

        # ── Check nest ──
        if (hx, hy) == world.nest:
            if snake.length >= 8:
                victory(snake)
                return
            else:
                message = f"The Sacred Nest! But you need length 8 to claim it. (Current: {snake.length})"

        # ── Check prey ──
        if (hx, hy) in world.prey:
            prey = world.prey.pop((hx, hy))
            pts = prey["points"]
            snake.score += pts
            snake.eaten.append(prey["name"])
            for _ in range(pts):
                snake.grow()
                grew = True
            # Special: Rabbit heals 1 HP
            if prey["name"] == "Rabbit" and snake.hp < snake.max_hp:
                snake.hp = min(snake.max_hp, snake.hp + 1)
                message = f"You devoured a {prey['emoji']} {prey['name']}! +{pts} pts, grew {pts} segment(s), +1 HP restored!"
            else:
                message = f"You devoured a {prey['emoji']} {prey['name']}! +{pts} pts, grew {pts} segment(s)."
            world.replenish()

        # ── Check hazards ──
        elif (hx, hy) in world.hazards:
            hazard = world.hazards.pop((hx, hy))
            if snake.shield:
                snake.shield = False
                message = f"A {hazard['emoji']} {hazard['name']} struck — but your shield absorbed it!"
            else:
                dmg = hazard["damage"]
                # Mongoose poisons
                if hazard["name"] == "Mongoose":
                    snake.poison = 3
                    message = f"A {hazard['emoji']} {hazard['name']} bit you! -{dmg} HP + POISONED for 3 turns!"
                else:
                    message = f"You hit a {hazard['emoji']} {hazard['name']}! -{dmg} HP."
                snake.hp -= dmg
            if snake.hp <= 0:
                game_over(snake, f"You were slain by a {hazard['name']}.")
                return

        # ── Eagle King ──
        if (hx, hy) == world.eagle_pos:
            if snake.shield:
                snake.shield = False
                world.eagle_hp -= 2
                message += " The Eagle King struck — your shield deflected it and dealt 2 damage back!"
            else:
                snake.hp -= 3
                message += " 🦅 The Eagle King swooped and attacked! -3 HP!"
                if snake.hp <= 0:
                    game_over(snake, "The Eagle King caught you and carried you off!")
                    return

        # ── Poison tick ──
        if snake.poison > 0:
            snake.hp -= 1
            snake.poison -= 1
            message += f" ☠ Poison dealt 1 damage. ({snake.poison} turns remaining)"
            if snake.hp <= 0:
                game_over(snake, "The poison consumed you. Your scales grew still.")
                return

        # ── Eagle movement (every 3 turns) ──
        if snake.turns % 3 == 0:
            world.move_eagle(snake.head)
            if world.eagle_pos == snake.head:
                if snake.shield:
                    snake.shield = False
                    world.eagle_hp -= 2
                    message += " Eagle moved onto you — shield blocked it!"
                else:
                    snake.hp -= 3
                    message += " 🦅 Eagle King pounced! -3 HP!"
                    if snake.hp <= 0:
                        game_over(snake, "The Eagle King caught you off guard!")
                        return

        # ── Eagle defeated ──
        if world.eagle_hp <= 0:
            world.eagle_pos = (-99, -99)  # Remove from board
            snake.score += 10
            message += " 🎉 You defeated the Eagle King! +10 bonus score!"

        # ── Random events (every 10 turns) ──
        if snake.turns % 10 == 0:
            event = random.randint(1, 4)
            if event == 1 and snake.hp < snake.max_hp:
                snake.hp = min(snake.max_hp, snake.hp + 2)
                message += " ✨ A healing spring! +2 HP."
            elif event == 2:
                snake.shield = True
                message += " 🛡 A mystic rune grants you a shield for the next hit!"
            elif event == 3:
                world._spawn_items(prey_count=2, hazard_count=1)
                message += " 🌿 The jungle stirs... new creatures appear."
            elif event == 4:
                lore = random.choice(LORE)
                message += f" 📜 {lore}"

        if not message:
            message = f"You slither {dir_name}..."


# ── ENTRY POINT ────────────────────────────────────────────────
if __name__ == "__main__":
    try:
        play()
    except KeyboardInterrupt:
        print("\n\n  Game interrupted. Farewell, Naga.\n")
