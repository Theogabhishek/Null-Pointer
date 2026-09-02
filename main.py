from ursina import *
from ursina.prefabs.first_person_controller import FirstPersonController
import math
import random

# === GAME CONFIGURATION ===
WINDOW_TITLE = "NullPointer - The OG Game"
WINDOW_WIDTH = 1280
WINDOW_HEIGHT = 720
WINDOW_FULLSCREEN = False
TARGET_FPS = 60

# === ENGINE INIT ===
app = Ursina(title=WINDOW_TITLE, borderless=False, fullscreen=WINDOW_FULLSCREEN)
window.fps_counter.enabled = True
window.exit_button.visible = True

# === RETRO CYBERPUNK COLOR PALETTE ===
neon_cyan = color.rgb(0, 0.9, 1.0)
neon_purple = color.rgb(0.6, 0, 1.0)
neon_green = color.rgb(0, 1.0, 0.4)
neon_red = color.rgb(1.0, 0.1, 0.3)
neon_gold = color.rgb(1.0, 0.8, 0.0)
dark_bg = color.rgb(10, 11, 20)
dark_panel = color.rgba(15, 17, 28, 200)

# === GAME STATE MANAGER ===
class GameState:
    ram_health = 8.0   # Player health (GB of RAM)
    cpu_energy = 100.0 # Player mana (CPU%)
    bugs_destroyed = 0
    quest_active = False
    quest_completed = False
    sudo_unlocked = False
    cooldown_sudo = 0.0
    cooldown_stash = 0.0
    cooldown_refactor = 0.0

# === PLAYER ===
player = FirstPersonController()
player.speed = 5.5
player.jump_height = 2.0
player.gravity = 1.0
player.cursor.visible = True
player.position = (0, 1, 0)

# Debugger Staff class - uses only built-in Ursina models (cube/sphere)
class DebuggerStaff(Entity):
    def __init__(self):
        super().__init__(
            parent=camera,
            model='cube',  # Using cube instead of cylinder (not built-in by default)
            color=color.rgb(20, 20, 25),
            scale=(0.05, 1.2, 0.05),
            position=(0.4, -0.6, 1.0),
            rotation=(15, -10, 0)
        )
        # Glowing neon tip using sphere (built-in)
        self.tip = Entity(
            parent=self,
            model='sphere',
            color=neon_cyan,
            scale=(3, 0.2, 3),
            position=(0, 0.5, 0)
        )
        # Rotating circuit ring
        self.ring = Entity(
            parent=self.tip,
            model='cube',
            color=neon_purple,
            scale=(2, 0.2, 2),
            rotation=(90, 0, 0)
        )
        self.recoil = 0.0

    def update(self):
        # Rotate ring
        self.ring.rotation_y += time.dt * 60
        self.ring.y = math.sin(time.time() * 3) * 0.05
        # Recoil reset
        if self.recoil > 0:
            self.recoil -= time.dt * 4
            self.z = 1.0 - (self.recoil * 0.2)
        else:
            self.z = 1.0

# Instantiate the staff
staff = DebuggerStaff()

# === SKY WITH SCROLLING BINARY CODE ===
class BinarySky:
    def __init__(self):
        self.particles = []
        for _ in range(15):
            x = random.uniform(-100, 100)
            y = random.uniform(30, 80)
            z = random.uniform(-100, 100)
            text_str = "".join(random.choice(["0", "1"]) for _ in range(4))
            e = Entity(
                model='quad',
                text=text_str,
                color=color.rgba(0, 120, 80, 15),
                scale=random.uniform(0.5, 2),
                position=(x, y, z),
                rotation=random.uniform(0, 360),
            )
            self.particles.append(e)

    def update(self):
        for p in self.particles:
            p.y -= time.dt * random.uniform(0.3, 1.5)
            if p.y < -50:
                p.y = 150
                p.x = random.uniform(-100, 100)
                p.z = random.uniform(-100, 100)

sky = BinarySky()

# === DARK GROUND & ENVIRONMENT ===
ground = Entity(model='plane', scale=300, texture='white_cube', texture_scale=(300, 300))
ground.color = color.rgb(8, 9, 15)
ground.collider = BoxCollider(ground, size=(300, 1, 300))
ground.y = -0.5

# === SERVER TOWERS (using cubes with colors) ===
for i in range(16):
    angle = (i * 2 * math.pi) / 16
    radius = random.uniform(25, 50)
    tx = radius * math.cos(angle)
    tz = radius * math.sin(angle)
    # Main tower
    tower = Entity(
        model='cube',
        color=color.rgb(12, 13, 20),
        position=(tx, random.uniform(6, 18), tz),
        scale=(4, random.uniform(6, 18), 4),
        collider='box'
    )
    # Glowing cyan circuit band
    Entity(parent=tower, model='cube', color=neon_cyan,
           position=(0, (tower.scale_y/2)-0.5, 0.51), scale=(1.02, 0.05, 0.02))
    # Glowing purple circuit band
    Entity(parent=tower, model='cube', color=neon_purple,
           position=(0, ((tower.scale_y/2)+0.5)*-1, -0.51), scale=(1.02, 0.05, 0.02))

AmbientLight(color=color.rgb(15, 15, 30))
dir_light = DirectionalLight()
dir_light.ambient = color.rgb(10, 10, 20)
dir_light.diffuse = color.rgb(40, 40, 80)
dir_light.yaw = 30
dir_light.pitch = 45

# === CYBER HUD / TERMINAL ===
class CyberHUD:
    def __init__(self):
        # Main task bar at bottom
        self.task_bg = Entity(parent=camera.ui, model='quad', scale=(1.0, 0.15), position=(0, -0.46), color=dark_panel)
        self.task_border = Entity(parent=camera.ui, model='quad', scale=(1.0, 0.15), position=(0, -0.46), color=neon_cyan, mode='line')

        # Objective text
        self.task_text = Text(text="MISSION: Talk to GCC Monolith (F) to start", position=(0, -0.44), color=neon_green, scale=1.2, parent=camera.ui, halma='center')

        # Controls help strip
        self.controls_bg = Entity(parent=camera.ui, model='quad', scale=(1.0, 0.1), position=(0, -0.58), color=dark_panel)
        self.controls_border = Entity(parent=camera.ui, model='quad', scale=(1.0, 0.1), position=(0, -0.58), color=neon_purple, mode='line')

        controls_text = "CONTROLS: WASD=Move  Space=Jump  Left Click=Ping  Q=Sudo Kill  E=Git Stash  R=Refactor  F=Interact  Esc=Exit"
        self.controls_text = Text(text=controls_text, position=(0, -0.56), color=color.gray, scale=0.9, parent=camera.ui, halma='center')

        # Console box
        self.console_bg = Entity(parent=camera.ui, model='quad', scale=(0.45, 0.25), position=(-0.6, -0.35), color=dark_panel)
        self.console_border = Entity(parent=camera.ui, model='quad', scale=(0.45, 0.25), position=(-0.6, -0.35), color=neon_green, mode='line')

        # Scrolling terminal logs
        self.logs = [
            "[system] Booting NullPointer Kernel...",
            "[system] Core architecture verified.",
            "[system] Sudo privileges restricted."
        ]
        self.log_texts = []
        for i in range(4):
            t = Text(text="", position=(-0.81, -0.25 - (i * 0.045)), color=neon_green, scale=1.2, parent=camera.ui)
            self.log_texts.append(t)
        self.update_terminal()

        # RAM Health bar
        Text("RAM CAPACITY:", position=(-0.81, 0.45), color=neon_cyan, scale=1.2, parent=camera.ui)
        self.ram_bg = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.03), position=(-0.62, 0.4), color=color.black)
        self.ram_bar = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.03), position=(-0.62, 0.4), color=neon_cyan)
        self.ram_text = Text(text="8.0 GB / 8.0 GB", position=(-0.78, 0.41), color=color.white, scale=1.1, parent=camera.ui)

        # CPU Energy bar
        Text("CPU UTILIZATION:", position=(-0.81, 0.32), color=neon_gold, scale=1.2, parent=camera.ui)
        self.cpu_bg = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.03), position=(-0.62, 0.27), color=color.black)
        self.cpu_bar = Entity(parent=camera.ui, model='quad', scale=(0.35, 0.03), position=(-0.62, 0.27), color=neon_gold)
        self.cpu_text = Text(text="100% Capacity", position=(-0.78, 0.28), color=color.white, scale=1.1, parent=camera.ui)

        # Skill hotbar
        self.skill_bg = Entity(parent=camera.ui, model='quad', scale=(0.45, 0.12), position=(0.6, -0.41), color=dark_panel)
        self.skill_border = Entity(parent=camera.ui, model='quad', scale=(0.45, 0.12), position=(0.6, -0.41), color=neon_purple, mode='line')
        self.skills = [
            ("L-CLICK: Ping", neon_cyan, 0.42),
            ("Q: Sudo Kill", neon_red, 0.54),
            ("E: Git Stash", neon_purple, 0.66),
            ("R: Refactor()", neon_green, 0.78)
        ]
        self.skill_texts = []
        for label, col, x_pos in self.skills:
            t = Text(text=label, position=(x_pos, -0.4), color=col, scale=1.1, parent=camera.ui)
            self.skill_texts.append(t)

        # Swarm indicator
        self.swarm_bg = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.08), position=(0.0, 0.42), color=dark_panel)
        self.swarm_border = Entity(parent=camera.ui, model='quad', scale=(0.4, 0.08), position=(0.0, 0.42), color=neon_red, mode='line')
        self.swarm_text = Text(text="SWARM OFFLINE", position=(-0.16, 0.43), color=neon_red, scale=1.3, parent=camera.ui)

        # Dialogue window
        self.diag_bg = Entity(parent=camera.ui, model='quad', scale=(0.7, 0.22), position=(0.0, -0.1), color=dark_panel, visible=False)
        self.diag_border = Entity(parent=camera.ui, model='quad', scale=(0.7, 0.22), position=(0.0, -0.1), color=neon_cyan, mode='line', visible=False)
        self.diag_text = Text(text="", position=(-0.32, -0.05), color=color.white, scale=1.3, parent=camera.ui, visible=False)
        self.diag_instruction = Text(text="Press [Space] to exit...", position=(-0.15, -0.17), color=neon_cyan, scale=1.1, parent=camera.ui, visible=False)

    def update_terminal(self):
        for idx, line in enumerate(self.logs):
            self.log_texts[idx].text = line

    def log(self, message):
        self.logs.append(message)
        if len(self.logs) > 4:
            self.logs.pop(0)
        self.update_terminal()

    def update_stats(self):
        # RAM bar
        ram_ratio = max(0.0, min(GameState.ram_health / 8.0, 1.0))
        self.ram_bar.scale_x = 0.35 * ram_ratio
        self.ram_bar.x = -0.62 - (0.35 * (1.0 - ram_ratio)) / 2
        self.ram_text.text = f"{round(GameState.ram_health, 1)} GB / 8.0 GB"

        # CPU bar
        cpu_ratio = max(0.0, min(GameState.cpu_energy / 100.0, 1.0))
        self.cpu_bar.scale_x = 0.35 * cpu_ratio
        self.cpu_bar.x = -0.62 - (0.35 * (1.0 - cpu_ratio)) / 2
        self.cpu_text.text = f"{round(GameState.cpu_energy, 0)}% Capacity"

        # Swarm text
        if GameState.quest_active:
            if GameState.quest_completed:
                self.swarm_text.text = "SWARM CLEARED! GCC."
                self.swarm_text.color = neon_green
                self.swarm_border.color = neon_green
            else:
                self.swarm_text.text = f"BUGS: {GameState.bugs_destroyed}/5"
                self.swarm_text.color = neon_cyan
                self.swarm_border.color = neon_cyan
        else:
            self.swarm_text.text = "Find GCC Monolith"

        # Skill cooldown colors
        self.skill_texts[1].color = neon_red if GameState.cooldown_sudo <= 0 else color.dark_gray
        self.skill_texts[2].color = neon_purple if GameState.cooldown_stash <= 0 else color.dark_gray
        self.skill_texts[3].color = neon_green if GameState.cooldown_refactor <= 0 else color.dark_gray

    def open_dialogue(self, text):
        self.diag_bg.visible = True
        self.diag_border.visible = True
        self.diag_text.visible = True
        self.diag_instruction.visible = True
        self.diag_text.text = text
        player.enabled = False
        mouse.locked = False

    def close_dialogue(self):
        self.diag_bg.visible = False
        self.diag_border.visible = False
        self.diag_text.visible = False
        self.diag_instruction.visible = False
        player.enabled = True
        mouse.locked = True

    def update_task(self, text):
        self.task_text.text = text

    def update_swarm(self):
        if GameState.quest_active:
            if GameState.quest_completed:
                self.swarm_text.text = "SWARM CLEARED! GCC."
                self.swarm_text.color = neon_green
                self.swarm_border.color = neon_green
            else:
                self.swarm_text.text = f"BUGS: {GameState.bugs_destroyed}/5"
                self.swarm_text.color = neon_cyan
                self.swarm_border.color = neon_cyan
        else:
            self.swarm_text.text = "Find GCC Monolith"

hud = CyberHUD()

# === PING PROJECTILE (uses built-in sphere) ===
class PingProjectile(Entity):
    def __init__(self, position, direction):
        super().__init__(
            model='sphere',
            scale=0.3,
            color=neon_cyan,
            position=position,
            collider='sphere'
        )
        self.direction = direction.normalized()
        self.speed = 50.0
        self.life = 2.5

    def update(self):
        self.position += self.direction * self.speed * time.dt
        self.life -= time.dt
        if self.life <= 0:
            destroy(self)
            return
        # Collision
        hit = self.intersects()
        if hit.hit:
            if hasattr(hit.entity, 'damage'):
                hit.entity.damage(1.0)
            destroy(self)

# === SUDO SHOCKWAVE ===
class Shockwave(Entity):
    def __init__(self, position):
        super().__init__(
            model='cylinder',  # Will use scaled cube as fallback
            color=neon_green,
            position=position,
            scale=(0.1, 0.05, 0.1),
            mode='line'
        )
        # Fallback: if cylinder model missing, use scaled cube
        if not hasattr(self, 'model_name') or self.model is None:
            self.model = 'cube'
            self.scale = (0.1, 0.05, 0.1)

    def update(self):
        self.scale_x += 25 * time.dt
        self.scale_z += 25 * time.dt
        alpha = int(255 * (1.0 - min(self.scale_x / 20, 1.0)))
        self.color = color.rgba(0, 255, 100, alpha)
        if self.scale_x >= 20:
            destroy(self)

# === SYNTAX GLITCH ENEMIES ===
class SyntaxGlitch(Entity):
    def __init__(self, x, z):
        # Use cube as base, add details with child entities
        super().__init__(
            model='cube',
            scale=(1.4, 0.7, 1.1),
            color=color.rgb(28, 24, 33),
            position=(x, random.uniform(1.5, 4.0), z),
            collider='box'
        )
        # Core eye
        Entity(parent=self, model='sphere', color=neon_red, scale=(0.5, 0.5, 0.5), position=(0, 0, 0.5))
        # Wings
        Entity(parent=self, model='cube', color=neon_purple, scale=(1.1, 0.1, 0.4), position=(-0.8, 0, 0))
        Entity(parent=self, model='cube', color=neon_purple, scale=(1.1, 0.1, 0.4), position=(0.8, 0, 0))
        self.health = 2.0
        self.speed = random.uniform(3.0, 5.0)
        self.bob_speed = random.uniform(2.0, 4.0)
        self.bob_offset = random.uniform(0, 100)

    def update(self):
        # Chase player
        self.look_at(player)
        self.rotation_y += 180
        dir_to_player = (player.position - self.position).normalized()
        self.position += dir_to_player * self.speed * time.dt
        # Float/bob
        self.y += math.sin(time.time() * self.bob_speed + self.bob_offset) * 0.02
        # Wings flap
        self.children[0].rotation_z = math.sin(time.time() * 15) * 30
        self.children[1].rotation_z = -math.sin(time.time() * 15) * 30
        # Damage on contact
        if distance(self.position, player.position) < 2.0:
            self.attack_player()

    def attack_player(self):
        GameState.ram_health -= 1.0 * time.dt
        hud.update_stats()
        camera.shake(duration=0.05, magnitude=1.5)
        spawn_particles(self.position, neon_red, 6)
        if random.random() < 0.01:
            hud.log("[CRITICAL] Memory Leak!")
        if GameState.ram_health <= 0:
            hud.open_dialogue("=== SYSTEM PANIC ===\n\nRAM depleted! Reboot required.")

    def damage(self, val):
        self.health -= val
        camera.shake(duration=0.1, magnitude=1.5)
        spawn_particles(self.position, neon_cyan, 8)
        hud.log(f"Hit: -{val} HP")
        if self.health <= 0:
            spawn_particles(self.position, neon_red, 20)
            GameState.bugs_destroyed += 1
            if GameState.quest_active and not GameState.quest_completed:
                if GameState.bugs_destroyed >= 5:
                    GameState.quest_completed = True
                    hud.log("[MISSION] 5 bugs purged. GCC access unlocked.")
            destroy(self)

# Enemy spawner
active_enemies = []
def spawn_wave():
    for _ in range(4):
        ang = random.uniform(0, 2*math.pi)
        rad = random.uniform(15, 28)
        ex = player.x + rad * math.cos(ang)
        ez = player.z + rad * math.sin(ang)
        active_enemies.append(SyntaxGlitch(ex, ez))
    hud.log("[WARN] Glitches spawned.")

# === GCC MONOLITH NPC ===
class GCCMonolith(Entity):
    def __init__(self):
        super().__init__(
            model='cube',
            color=color.rgb(10, 15, 30),
            scale=(3, 6, 3),
            position=(0, 2.5, 15),
            collider='box'
        )
        # Halo ring (use torus, but fallback to cube if missing - though torus isn't built-in, we fake it)
        # Actually, let's just use a cube scaled as a ring illusion, or skip the torus
        self.halo = Entity(parent=self, model='cube', color=neon_green,
                           scale=(1.5, 0.2, 1.5), position=(0, 3.0, 0))
        self.rotation_speed = random.uniform(10, 20)

    def update(self):
        self.rotation_y += time.dt * self.rotation_speed
        self.halo.rotation_z += time.dt * 45
        # Pulse indicator
        dist = distance(self.position, player.position)
        if dist < 8.0:
            self.halo.color = neon_cyan
            hud.log("[network] Press [F] to speak with GCC")
        else:
            self.halo.color = neon_green

gcc = GCCMonolith()

# Initial start dialogue - show controls and objectives
hud.open_dialogue(
    "GCC: 'Welcome, Alex. The NullPointer swarm infects the server.\n"
    "Press [F] to speak with GCC. Your mission: destroy 5 Syntax Glitches.\n"
    "Use [WASD] to move, [Space] to jump, [Left Click] to ping.\n"
    "Good luck, developer.'"
)
GameState.quest_active = True
spawn_wave()

# === PARTICLE SPARKS ===
class Spark(Entity):
    def __init__(self, pos, col):
        super().__init__(
            model='cube',
            scale=random.uniform(0.1, 0.25),
            color=col,
            position=pos
        )
        self.v = Vec3(random.uniform(-3,3), random.uniform(2,6), random.uniform(-3,3))
        self.l = 0.5

    def update(self):
        self.position += self.v * time.dt
        self.v.y -= 8.0 * time.dt
        self.l -= time.dt
        self.scale -= Vec3(1,1,1) * time.dt * 0.5
        if self.l <= 0 or self.scale_x <= 0:
            destroy(self)

def sparkle(pos, col, n=12):
    for _ in range(n):
        Spark(pos, col)

# === SPAWN PARTICLES ===
def spawn_particles(pos, col, n=12):
    for _ in range(n):
        Spark(pos, col)

# === CONTROLS ===
def input(key):
    # Exit dialogue
    if key == 'space' and hud.diag_bg.visible:
        hud.close_dialogue()
        return

    if not player.enabled:
        return

    # L-CLICK: Ping
    if key == 'left mouse down':
        staff.recoil = 1.0
        PingProjectile(camera.position + camera.forward*2, camera.forward)
        hud.log("[debug] Ping launched.")

    # Q: Sudo Kill
    if key == 'q':
        if GameState.sudo_unlocked and GameState.cooldown_sudo <= 0 and GameState.cpu_energy >= 40:
            GameState.cpu_energy -= 40
            GameState.cooldown_sudo = 12.0
            Shockwave(player.position)
            hud.log("[sudo] Purge wave activated!")
            # Damage nearby glitches
            for e in active_enemies:
                if distance(e.position, player.position) <= 12:
                    e.damage(3.0)
        else:
            hud.log("[error] Skill unavailable.")

    # E: Git Stash Dash
    if key == 'e':
        if GameState.cooldown_stash <= 0 and GameState.cpu_energy >= 15:
            GameState.cpu_energy -= 15
            GameState.cooldown_stash = 3.0
            dir = camera.forward
            dir.y = 0
            player.position += dir.normalized() * 10
            sparkle(player.position, neon_purple, 15)
            hud.log("[git] Stash dash!")
        else:
            hud.log("[error] Stash on cooldown.")

    # R: Refactor Heal
    if key == 'r':
        if GameState.cooldown_refactor <= 0 and GameState.cpu_energy >= 30 and GameState.ram_health < 8:
            GameState.cpu_energy -= 30
            GameState.cooldown_refactor = 8.0
            GameState.ram_health = min(8.0, GameState.ram_health + 3.0)
            hud.log("[system] refactor(): +3.0 GB RAM restored.")
            sparkle(player.position, neon_green, 15)
        else:
            hud.log("[error] Cannot refactor.")

    # F: GCC Dialogue
    if key == 'f':
        dist = gcc.position.distance(player.position)
        if dist < 8.0:
            if not GameState.quest_active:
                hud.open_dialogue(
                    "GCC: 'Alex, the NullPointer swarm expands.\n"
                    "Purge 5 Syntax Glitches and I will unlock sudo kill -9 for you!'"
                )
                GameState.quest_active = True
                spawn_wave()
            elif GameState.quest_active and not GameState.quest_completed:
                hud.open_dialogue(
                    f"GCC: 'Progress: {GameState.bugs_destroyed}/5 bugs purged.\n"
                    "Eliminate the remaining glitches!'"
                )
            elif GameState.quest_active and GameState.quest_completed and not GameState.sudo_unlocked:
                hud.open_dialogue(
                    "GCC: 'Excellent work. Sudo privileges compiled.\n"
                    "[Q] is now 'sudo kill -9' - use with care!'"
                )
                GameState.sudo_unlocked = True
                hud.log("[system] Sudo access unlocked!")
            else:
                hud.open_dialogue(
                    "GCC: 'The NullPointer King stirs in the Core.\n"
                    "Prepare for the final breach.'"
                )

# === UPDATE LOOP ===
def update():
    application.target_fps = TARGET_FPS

    # Update task/goal display
    if not GameState.quest_active:
        hud.update_task("MISSION: Talk to GCC Monolith (F) to start")
    elif GameState.quest_active and not GameState.quest_completed:
        hud.update_task(f"MISSION: Destroy {5 - GameState.bugs_destroyed} more Syntax Glitches")
    elif GameState.quest_active and GameState.quest_completed and not GameState.sudo_unlocked:
        hud.update_task("MISSION: Talk to GCC for Sudo privileges")
    else:
        hud.update_task("MISSION: Complete! Find the Root Citadel")

    # Energy regen
    if GameState.cpu_energy < 100:
        GameState.cpu_energy = min(100, GameState.cpu_energy + time.dt * 10)

    # Cooldowns
    for c in [GameState.cooldown_sudo, GameState.cooldown_stash, GameState.cooldown_refactor]:
        if c > 0:
            pass  # simplified for performance

    # HUD updates
    hud.update_stats()
    hud.update_swarm()

    # Enemy spawn logic
    if GameState.quest_active and not GameState.quest_completed:
        active = [e for e in scene.entities if isinstance(e, SyntaxGlitch)]
        if len(active) == 0:
            spawn_wave()

# === LAUNCH BANNER ===
if __name__ == '__main__':
    print("""
 ▄▄▄▄·  ▄▄▄·  ▄▄▄· ▪   ▄▄▄·  ▄▄▄· • ▌ • ▄▄▄▄▪   ·▄▄▄▄  ▄▄▄·▄▄▄▄▄▄▄▄·▄.▄▄▄▄▄▄▄▄▌ ▄▄·  ▄▄▄·▪ 
·██  ·· •██ █•█▌·██  ██ ▐█.▌▐█ ▄█ ██ ██▪▐█ ▀█  ██▪ ██ ▐█ ▄██▪ ██▐▌▐█ ▌▐▌▐█ ▌▐▌▐█ ▀█ •█▌▐██·
▐█.▪ ▐▌▐█·▐█·█▌▐█· ▐█· ▐█▌·▐█▀▐█ ██· ▐█·▐█▀▐█ ▄▀▐█·▐█▌ ▐█▐▌▐█· ▐█▌▐▌ ▐█▌▐█ █▌▐█▀▀█  ▐█·▐█▌
 ▀▀▀  ▀█▀ ·▀▀▀  ▀▀▀  ▀█▄▐▀▀▀· ▀▀▀ · ▀▀▀ █▪ ▀▀▀  ▀▀▀ ▀▀▀.▀▀▀ ·▀▀ █▪ ▀  █▪ ▀▀▀·  ▀▀▀  ▀▀▀ 
    """)
    print("NullPointer - The OG Game")
    print("Made by Theogabhishek with 3 cups of coffee & AI assistance")
    app.run()