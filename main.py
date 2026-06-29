import pgzrun
from pygame import Rect

WIDTH = 800
HEIGHT = 600

# Game States
game_state = 'MENU'
sound_enabled = True

class Button:
    def __init__(self, x, y, text):
        self.rect = Rect(x, y, 200, 50)
        self.text = text

    def draw(self):
        screen.draw.filled_rect(self.rect, (100, 100, 100))
        screen.draw.rect(self.rect, (255, 255, 255))
        screen.draw.text(self.text, center=self.rect.center, color="white", fontsize=30)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)

class AnimatedSprite(Actor):
    def __init__(self, idle_frames, run_frames, **kwargs):
        super().__init__(idle_frames[0], **kwargs)
        self.idle_frames = idle_frames
        self.run_frames = run_frames
        self.current_frame = 0
        self.anim_timer = 0
        self.is_running = False
        self.facing_right = True

    def update_animation(self):
        self.anim_timer += 1
        if self.anim_timer >= 15:  # Change frame every 15 ticks
            self.anim_timer = 0
            self.current_frame = (self.current_frame + 1) % 2
            
            frames = self.run_frames if self.is_running else self.idle_frames
            self.image = frames[self.current_frame]

class Hero(AnimatedSprite):
    def __init__(self, x, y):
        super().__init__(['hero_idle1', 'hero_idle2'], ['hero_run1', 'hero_run2'], center=(x, y))
        self.velocity_y = 0
        self.on_ground = False
        self.speed = 4

    def update_movement(self, platforms):
        self.is_running = False
        if keyboard.left:
            self.x -= self.speed
            self.is_running = True
            self.facing_right = False
        elif keyboard.right:
            self.x += self.speed
            self.is_running = True
            self.facing_right = True

        # Gravity
        self.velocity_y += 0.5
        self.y += self.velocity_y

        # Collision with platforms
        self.on_ground = False
        for platform in platforms:
            if self.colliderect(platform):
                if self.velocity_y > 0 and self.bottom <= platform.bottom:
                    self.bottom = platform.top
                    self.velocity_y = 0
                    self.on_ground = True
                elif self.velocity_y < 0:
                    self.top = platform.bottom
                    self.velocity_y = 0

        # Screen boundaries
        if self.left < 0: self.left = 0
        if self.right > WIDTH: self.right = WIDTH
        if self.bottom > HEIGHT:
            self.bottom = HEIGHT
            self.velocity_y = 0
            self.on_ground = True

        self.update_animation()

    def jump(self):
        if self.on_ground:
            self.velocity_y = -10
            if sound_enabled:
                sounds.jump.play()

class Enemy(AnimatedSprite):
    def __init__(self, x, y, min_x, max_x):
        super().__init__(['enemy_idle1', 'enemy_idle2'], ['enemy_run1', 'enemy_run2'], center=(x, y))
        self.min_x = min_x
        self.max_x = max_x
        self.direction = 1
        self.speed = 2
        self.is_running = True

    def update_movement(self):
        self.x += self.speed * self.direction
        if self.x > self.max_x:
            self.direction = -1
        elif self.x < self.min_x:
            self.direction = 1
            
        self.update_animation()

# Initialize objects
btn_play = Button(300, 200, "Play Game")
btn_sound = Button(300, 300, "Toggle Sound")
btn_exit = Button(300, 400, "Exit")

hero = Hero(50, 500)
platforms = [
    Actor('platform', center=(150, 400)),
    Actor('platform', center=(400, 300)),
    Actor('platform', center=(650, 450))
]

enemies = [
    Enemy(400, 268, 300, 500),
    Enemy(650, 418, 550, 750)
]

coins = [
    Actor('coin', center=(150, 350)),
    Actor('coin', center=(400, 230)),
    Actor('coin', center=(650, 380)),
    Actor('coin', center=(750, 500))
]

def reset_game():
    global hero, enemies, coins
    hero = Hero(50, 500)
    enemies = [
        Enemy(400, 268, 300, 500),
        Enemy(650, 418, 550, 750)
    ]
    coins = [
        Actor('coin', center=(150, 350)),
        Actor('coin', center=(400, 230)),
        Actor('coin', center=(650, 380)),
        Actor('coin', center=(750, 500))
    ]

def draw():
    screen.blit('bg', (0, 0))
    
    if game_state == 'MENU':
        screen.draw.text("Python Platformer", center=(WIDTH//2, 100), color="white", fontsize=50)
        btn_play.draw()
        btn_sound.draw()
        btn_exit.draw()
        status = "ON" if sound_enabled else "OFF"
        screen.draw.text(f"Sound: {status}", center=(WIDTH//2, 360), color="yellow", fontsize=20)
        
    elif game_state == 'PLAYING':
        for p in platforms:
            p.draw()
        for c in coins:
            c.draw()
        for e in enemies:
            e.draw()
        hero.draw()
        screen.draw.text(f"Coins: {4 - len(coins)}/4", topleft=(10, 10), color="white", fontsize=30)
        
    elif game_state == 'GAME_OVER':
        screen.draw.text("GAME OVER!", center=(WIDTH//2, HEIGHT//2), color="red", fontsize=80)
        screen.draw.text("Click to return to menu", center=(WIDTH//2, HEIGHT//2 + 50), color="white", fontsize=30)
        
    elif game_state == 'WIN':
        screen.draw.text("YOU WIN!", center=(WIDTH//2, HEIGHT//2), color="green", fontsize=80)
        screen.draw.text("Click to return to menu", center=(WIDTH//2, HEIGHT//2 + 50), color="white", fontsize=30)

def update():
    global game_state
    
    if game_state == 'PLAYING':
        hero.update_movement(platforms)
        
        for e in enemies:
            e.update_movement()
            if hero.colliderect(e):
                if sound_enabled:
                    sounds.hit.play()
                game_state = 'GAME_OVER'
                sounds.bgm.stop()
                
        # Coin collection
        for c in coins[:]:
            if hero.colliderect(c):
                if sound_enabled:
                    sounds.coin.play()
                coins.remove(c)
                
        if len(coins) == 0:
            game_state = 'WIN'
            sounds.bgm.stop()

def on_mouse_down(pos):
    global game_state, sound_enabled
    
    if game_state == 'MENU':
        if btn_play.is_clicked(pos):
            reset_game()
            game_state = 'PLAYING'
            if sound_enabled:
                sounds.bgm.play(loops=-1)
        elif btn_sound.is_clicked(pos):
            sound_enabled = not sound_enabled
        elif btn_exit.is_clicked(pos):
            exit()
            
    elif game_state in ['GAME_OVER', 'WIN']:
        game_state = 'MENU'

def on_key_down(key):
    if game_state == 'PLAYING' and key == keys.UP:
        hero.jump()

pgzrun.go()
