import pygame
import random
import sys
import os
import tkinter as tk

def resource_path(relative_path):
    """ Get absolute path to resource, works for dev and for PyInstaller """
    try:
        # PyInstaller creates a temp folder and stores path in _MEIPASS
        base_path = sys._MEIPASS
    except Exception:
        base_path = os.path.abspath(".")
    return os.path.join(base_path, relative_path)

# Initialize Pygame and Mixer
pygame.init()
pygame.mixer.init()

# Setup Display
WIDTH, HEIGHT = 800, 600
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Рыба")

# Setup Fonts
try:
    font_large = pygame.font.SysFont("timesnewroman", 64, bold=True)
    font_ui = pygame.font.SysFont("timesnewroman", 48, bold=True)
except:
    font_large = pygame.font.Font(None, 64)
    font_ui = pygame.font.Font(None, 48)

# Load Assets
try:
    raw_bg = pygame.image.load(resource_path("background.png")).convert()
    background_img = pygame.transform.scale(raw_bg, (WIDTH, HEIGHT))

    raw_bucket = pygame.image.load(resource_path("bucket.png")).convert_alpha()
    bucket_w, bucket_h = raw_bucket.get_width(), raw_bucket.get_height()
    # Scale bucket to reasonable size if it's too big (e.g. max 120 width)
    target_bw = 120
    target_bh = int((target_bw / bucket_w) * bucket_h)
    bucket_img = pygame.transform.scale(raw_bucket, (target_bw, target_bh))

    raw_fish = pygame.image.load(resource_path("fish.png")).convert_alpha()
    fish_w, fish_h = raw_fish.get_width(), raw_fish.get_height()
    target_fw = 80
    target_fh = int((target_fw / fish_w) * fish_h)
    fish_img = pygame.transform.scale(raw_fish, (target_fw, target_fh))

    pygame.mixer.music.load(resource_path("music.mp3"))
    vocal_sound = pygame.mixer.Sound(resource_path("vocals.mp3"))
except Exception as e:
    print(f"Error loading assets: {e}")
    sys.exit(1)

# Try loading the error asset
try:
    raw_error = pygame.image.load(resource_path("error.png")).convert()
    error_img = pygame.transform.scale(raw_error, (WIDTH, HEIGHT))
except Exception:
    error_img = pygame.Surface((WIDTH, HEIGHT))
    error_img.fill((255, 0, 0))

# Game State
state = "START" # START, PLAYING
score = 0
start_time = 0
current_time_str = "00:00"

bucket_rect = bucket_img.get_rect()
bucket_rect.midbottom = (WIDTH // 2, HEIGHT - 10)
bucket_speed = 8

fishes = [] # List of dicts: {'rect': pygame.Rect, 'speed': float}
FISH_SPAWN_EVENT = pygame.USEREVENT + 1

hint_shown = False
hint_end_time = 0
error_start_time = 0

# Cheat System
cheat_window = None
cheat_ext_window = None
cheat_slow_fish = False
cheat_flying_bucket = False
cheat_giant_bucket = False
cheat_reverse_gravity = False
cheat_auto_catch = False
cheat_disco = False
cheat_black_hole = False
cheat_time_stop = False
cheat_screen_shake = False
shake_amount = 0

def open_ext_cheat_window():
    global cheat_ext_window
    if cheat_ext_window is not None:
        return
        
    cheat_ext_window = tk.Tk()
    cheat_ext_window.title("PRO Чит")
    cheat_ext_window.geometry("300x420")
    cheat_ext_window.attributes('-topmost', True)
    
    def btn_reverse_gravity():
        global cheat_reverse_gravity
        cheat_reverse_gravity = not cheat_reverse_gravity
        
    def btn_auto_catch():
        global cheat_auto_catch
        cheat_auto_catch = not cheat_auto_catch
        
    def btn_disco():
        global cheat_disco
        cheat_disco = not cheat_disco
        
    def btn_black_hole():
        global cheat_black_hole
        cheat_black_hole = not cheat_black_hole
        
    def btn_time_stop():
        global cheat_time_stop
        cheat_time_stop = not cheat_time_stop
        
    def btn_screen_shake():
        global cheat_screen_shake
        cheat_screen_shake = not cheat_screen_shake

    tk.Label(cheat_ext_window, text="ПРО Читы (6700+ очков):", font=("Arial", 14, "bold"), fg="gold", bg="black").pack(fill=tk.X, pady=10)
    tk.Button(cheat_ext_window, text="Инверсия гравитации", command=btn_reverse_gravity, width=25, height=2).pack(pady=5)
    tk.Button(cheat_ext_window, text="Авто-ловля", command=btn_auto_catch, width=25, height=2).pack(pady=5)
    tk.Button(cheat_ext_window, text="Диско-режим", command=btn_disco, width=25, height=2).pack(pady=5)
    tk.Button(cheat_ext_window, text="Черная дыра", command=btn_black_hole, width=25, height=2).pack(pady=5)
    tk.Button(cheat_ext_window, text="Остановка времени", command=btn_time_stop, width=25, height=2).pack(pady=5)
    tk.Button(cheat_ext_window, text="Землетрясение", command=btn_screen_shake, width=25, height=2).pack(pady=5)
    
    def on_ext_closing():
        global cheat_ext_window
        cheat_ext_window.destroy()
        cheat_ext_window = None
    cheat_ext_window.protocol("WM_DELETE_WINDOW", on_ext_closing)

def open_cheat_window():
    global cheat_window
    if cheat_window is not None:
        return
        
    cheat_window = tk.Tk()
    cheat_window.title("Чит")
    cheat_window.geometry("300x400")
    cheat_window.attributes('-topmost', True)
    
    def btn_fish_rain():
        for _ in range(50):
            spawn_x = random.randint(0, WIDTH - target_fw)
            fish_rect = fish_img.get_rect()
            fish_rect.topleft = (spawn_x, random.randint(-1500, -target_fh))
            fishes.append({'rect': fish_rect, 'speed': random.uniform(3.0, 6.0)})
            
    def btn_giant_bucket():
        global cheat_giant_bucket, bucket_img, bucket_rect
        cheat_giant_bucket = not cheat_giant_bucket
        if cheat_giant_bucket:
            new_w = target_bw * 3
        else:
            new_w = target_bw
        bucket_img = pygame.transform.scale(raw_bucket, (new_w, target_bh))
        current_x = bucket_rect.centerx
        current_y = bucket_rect.bottom
        bucket_rect = bucket_img.get_rect(midbottom=(current_x, current_y))
        
    def btn_money_rain():
        global score
        score += 1000
        
    def btn_slow_fish():
        global cheat_slow_fish
        cheat_slow_fish = not cheat_slow_fish
        
    def btn_flying_bucket():
        global cheat_flying_bucket
        cheat_flying_bucket = True
        
    def btn_do_not_press():
        global state, cheat_window, error_start_time
        state = "ERROR"
        error_start_time = pygame.time.get_ticks()
        if cheat_window:
            cheat_window.destroy()
            cheat_window = None
            
        import threading
        import time
        import ctypes
        def spam_windows():
            for _ in range(150):
                try:
                    t = tk.Tk()
                    t.title("ВНИМАНИЕ ВИРУС!")
                    sw = t.winfo_screenwidth()
                    sh = t.winfo_screenheight()
                    w = random.randint(300, 800)
                    h = random.randint(150, 400)
                    x = random.randint(-50, max(1, sw - 50))
                    y = random.randint(-50, max(1, sh - 50))
                    t.geometry(f"{w}x{h}+{x}+{y}")
                    t.config(bg="red")
                    tk.Label(t, text="СИСТЕМА УДАЛЕНА!!\nВАШ ПК ПОВРЕЖДЕН", font=("Arial", 20, "bold"), fg="yellow", bg="red").pack(expand=True)
                    t.attributes('-topmost', True)
                    t.update()
                    time.sleep(0.01)
                except:
                    pass
        threading.Thread(target=spam_windows, daemon=True).start()

    tk.Label(cheat_window, text="Чит меню:", font=("Arial", 16, "bold")).pack(pady=10)
    
    tk.Button(cheat_window, text="Рыбный дождь", command=btn_fish_rain, width=25, height=2).pack(pady=5)
    tk.Button(cheat_window, text="Огромное ведро", command=btn_giant_bucket, width=25, height=2).pack(pady=5)
    tk.Button(cheat_window, text="Денежный дождь (+1000)", command=btn_money_rain, width=25, height=2).pack(pady=5)
    tk.Button(cheat_window, text="Медленные рыбы", command=btn_slow_fish, width=25, height=2).pack(pady=5)
    tk.Button(cheat_window, text="Летающее ведро", command=btn_flying_bucket, width=25, height=2).pack(pady=5)
    tk.Button(cheat_window, text="Не нажимать!", command=btn_do_not_press, width=25, height=2, bg="#ff9999", fg="black", font=("Arial", 10, "bold")).pack(pady=10)

    if score >= 6700:
        tk.Button(cheat_window, text="🌟 Обнаружен PRO Чит 🌟", command=open_ext_cheat_window, width=25, height=2, bg="gold", fg="black", font=("Arial", 10, "bold")).pack(pady=5)

    def on_closing():
        global cheat_window
        cheat_window.destroy()
        cheat_window = None

    cheat_window.protocol("WM_DELETE_WINDOW", on_closing)

clock = pygame.time.Clock()

def draw_text_black(surface, text, font, pos):
    text_surface = font.render(text, True, (0, 0, 0))
    surface.blit(text_surface, pos)

running = True
while running:
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
            
        if event.type == pygame.KEYDOWN:
            mods = pygame.key.get_mods()
            # Check for Ctrl+Alt+C anywhere to open cheat window
            if event.key == pygame.K_c and (mods & pygame.KMOD_CTRL) and (mods & pygame.KMOD_ALT):
                open_cheat_window()
                
            # Check for Ctrl+Q anywhere to quit
            if event.key == pygame.K_q and (mods & pygame.KMOD_CTRL):
                running = False
                
            elif state == "START":
                # Any key starts the game
                state = "PLAYING"
                start_time = pygame.time.get_ticks()
                pygame.time.set_timer(FISH_SPAWN_EVENT, 1500) # Spawn every 1.5s
                pygame.mixer.music.play(-1) # Loop indefinitely
                
        elif event.type == pygame.MOUSEBUTTONDOWN:
            if state == "START":
                state = "PLAYING"
                start_time = pygame.time.get_ticks()
                pygame.time.set_timer(FISH_SPAWN_EVENT, 1500)
                pygame.mixer.music.play(-1)
                
        if event.type == FISH_SPAWN_EVENT and state == "PLAYING":
            spawn_x = random.randint(0, WIDTH - target_fw)
            fish_rect = fish_img.get_rect()
            if cheat_reverse_gravity:
                fish_rect.bottomleft = (spawn_x, HEIGHT + target_fh)
            else:
                fish_rect.topleft = (spawn_x, -target_fh)
            speed = random.uniform(3.0, 6.0)
            fishes.append({'rect': fish_rect, 'speed': speed})

    keys = pygame.key.get_pressed()

    # Screen Shake Logic
    ox, oy = 0, 0
    if cheat_screen_shake and shake_amount > 0:
        ox = random.randint(-shake_amount, shake_amount)
        oy = random.randint(-shake_amount, shake_amount)
        shake_amount = max(0, shake_amount - 1)

    # Draw Background
    if cheat_disco:
        color = pygame.Surface((WIDTH, HEIGHT))
        color.fill((random.randint(0,255), random.randint(0,255), random.randint(0,255)))
        color.set_alpha(100)
        screen.blit(background_img, (ox, oy))
        screen.blit(color, (ox, oy))
    else:
        screen.blit(background_img, (ox, oy))

    if state == "START":
        text_surface = font_large.render("Старт", True, (0, 0, 0))
        text_rect = text_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
        
        # Draw a white backing for better visibility
        pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(40, 40))
        pygame.draw.rect(screen, (0, 0, 0), text_rect.inflate(40, 40), 3) # border
        screen.blit(text_surface, text_rect)

    elif state == "PLAYING":
        current_ticks = pygame.time.get_ticks()
        is_frozen = hint_shown and (current_ticks < hint_end_time)

        if not is_frozen:
            # Movement
            if keys[pygame.K_LEFT]:
                bucket_rect.x -= bucket_speed
            if keys[pygame.K_RIGHT]:
                bucket_rect.x += bucket_speed
            if cheat_flying_bucket:
                if keys[pygame.K_UP]:
                    bucket_rect.y -= bucket_speed
                if keys[pygame.K_DOWN]:
                    bucket_rect.y += bucket_speed
                
            # Constrain to screen
            if bucket_rect.left < 0:
                bucket_rect.left = 0
            if bucket_rect.right > WIDTH:
                bucket_rect.right = WIDTH
                
            if cheat_flying_bucket:
                if bucket_rect.top < 0: bucket_rect.top = 0
                if bucket_rect.bottom > HEIGHT: bucket_rect.bottom = HEIGHT
            else:
                bucket_rect.bottom = HEIGHT - 10

            if cheat_auto_catch and fishes:
                nearest_fish = min(fishes, key=lambda f: f['rect'].y if not cheat_reverse_gravity else -f['rect'].y)
                bucket_rect.centerx = nearest_fish['rect'].centerx

            # Update Fishes
            fishes_to_keep = []
            for f in fishes:
                if not cheat_time_stop:
                    speed_mod = f['speed']
                    if cheat_slow_fish:
                        speed_mod = max(1, int(f['speed'] / 3))
                    
                    if cheat_reverse_gravity:
                        f['rect'].y -= speed_mod
                    else:
                        f['rect'].y += speed_mod
                
                if cheat_black_hole:
                    # Move towards bucket smoothly
                    dx = bucket_rect.centerx - f['rect'].centerx
                    dy = bucket_rect.centery - f['rect'].centery
                    dist = max(1, (dx**2 + dy**2)**0.5)
                    f['rect'].x += int((dx / dist) * 12)
                    f['rect'].y += int((dy / dist) * 12)
                
                # Collision
                if bucket_rect.colliderect(f['rect']):
                    score += 1
                    vocal_sound.play() # Automatically layers due to pygame mixer
                    if cheat_screen_shake:
                        shake_amount = 30 # Huge shake
                        
                    if score == 67 and not hint_shown:
                        hint_shown = True
                        hint_end_time = current_ticks + 3000
                        start_time += 3000
                    continue # Do not keep
                    
                # Missed bounds check
                if cheat_reverse_gravity:
                    if f['rect'].bottom > 0:
                        fishes_to_keep.append(f)
                else:
                    if f['rect'].top < HEIGHT:
                        fishes_to_keep.append(f)
                    
            fishes = fishes_to_keep
            
        for f in fishes:
            dr = f['rect'].copy()
            dr.x += ox
            dr.y += oy
            screen.blit(fish_img, dr)

        # Draw Bucket
        db = bucket_rect.copy()
        db.x += ox
        db.y += oy
        screen.blit(bucket_img, db)

        if not is_frozen:
            # Time Calculation
            elapsed_seconds = (current_ticks - start_time) // 1000
            mins = elapsed_seconds // 60
            secs = elapsed_seconds % 60
            current_time_str = f"{mins:02d}:{secs:02d}"

        # Draw UI
        score_text = f"Рибы: {score}"
        time_text = f"Время: {current_time_str}"
        draw_text_black(screen, score_text, font_ui, (20 + ox, 20 + oy))
        draw_text_black(screen, time_text, font_ui, (20 + ox, 70 + oy))
        
        if is_frozen:
            hint_surface = font_large.render("CTRL + ALT + C", True, (255, 0, 0))
            hint_rect = hint_surface.get_rect(center=(WIDTH // 2, HEIGHT // 2))
            pygame.draw.rect(screen, (255, 255, 255), hint_rect.inflate(40, 40))
            pygame.draw.rect(screen, (0, 0, 0), hint_rect.inflate(40, 40), 5)
            screen.blit(hint_surface, hint_rect)

    elif state == "ERROR":
        import time
        screen.blit(error_img, (0, 0))
        warnings = ["СИСТЕМА УДАЛЕНА", "КРИТИЧЕСКИЙ СБОЙ", "ОШИБКА 0xDEAD", "ФАЙЛЫ ПОВРЕЖДЕНЫ", "ВИРУС АКТИВЕН"]
        for _ in range(15):
            txt = font_large.render(random.choice(warnings), True, (random.randint(150, 255), random.randint(0, 50), random.randint(0, 50)))
            rx = random.randint(0, max(1, WIDTH - txt.get_width()))
            ry = random.randint(0, max(1, HEIGHT - txt.get_height()))
            screen.blit(txt, (rx, ry))
        
        # Audio glitch (spamming the sound every frame creates an atrocious noise)
        vocal_sound.play()
        
        # Mouse glitch (jerk it randomly to feel like lag)
        mx, my = pygame.mouse.get_pos()
        pygame.mouse.set_pos(mx + random.randint(-150, 150), my + random.randint(-150, 150))
        
        # CPU/UI block lag to stutter the screen
        time.sleep(random.uniform(0.1, 0.5))
        
        # Auto crash in 12 seconds instead of 5
        if pygame.time.get_ticks() - error_start_time > 12000:
            os._exit(1)

    if cheat_window is not None:
        try:
            cheat_window.update()
        except:
            cheat_window = None

    if cheat_ext_window is not None:
        try:
            cheat_ext_window.update()
        except:
            cheat_ext_window = None

    pygame.display.flip()
    clock.tick(60)

pygame.quit()
sys.exit()
