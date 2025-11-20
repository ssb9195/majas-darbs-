import sys, math, os, pygame

WIDTH, HEIGHT = 900, 600
FPS = 120
DARK_RED = (140, 0, 26)
WHITE = (255, 255, 255)
BLACK = (0, 0, 0)
SOUND_FILENAME = 'fails.wav'
try:
    pygame.mixer.pre_init(44100, -16, 2, 512)
except:
    pass
pygame.init()
screen = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption('Latvijas karogs')
clock = pygame.time.Clock()
sound_bounce = None
if os.path.exists(SOUND_FILENAME):
    try:
        sound_bounce = pygame.mixer.Sound(SOUND_FILENAME)
    except:
        sound_bounce = None
header_font = pygame.font.SysFont(None, 26)
pulse_base = 48
pulse_amp = 14
pulse_speed = 1.6
circle_radius = 18
circle_x = 40
flag_top = 36
flag_height = HEIGHT - flag_top - 16
circle_y = flag_top + flag_height // 2
speed_x = 200
running = True

def draw_latvian_flag(surface, top_y, flag_h):
    unit = flag_h / 5.0
    h_top = int(round(unit * 2))
    h_mid = int(round(unit * 1))
    h_bot = flag_h - h_top - h_mid
    w = WIDTH
    x = 0
    pygame.draw.rect(surface, DARK_RED, (x, top_y, w, h_top))
    pygame.draw.rect(surface, WHITE, (x, top_y + h_top, w, h_mid))
    pygame.draw.rect(surface, DARK_RED, (x, top_y + h_top + h_mid, w, h_bot))

while running:
    dt = clock.tick(FPS) / 1000.0
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
        elif event.type == pygame.KEYDOWN and event.key == pygame.K_ESCAPE:
            running = False

    circle_x += speed_x * dt
    bounced = False
    if circle_x + circle_radius >= WIDTH:
        circle_x = WIDTH - circle_radius
        speed_x = -abs(speed_x)
        bounced = True
    if circle_x - circle_radius <= 0:
        circle_x = circle_radius
        speed_x = abs(speed_x)
        bounced = True
    if bounced and sound_bounce is not None:
        try:
            sound_bounce.play()
        except:
            pass

    screen.fill(BLACK)
    header_surf = header_font.render('Latvija 18. novembris', True, WHITE)
    header_rect = header_surf.get_rect(center=(WIDTH//2, 18))
    screen.blit(header_surf, header_rect)
    draw_latvian_flag(screen, flag_top, flag_height)
    pygame.draw.circle(screen, BLACK, (int(round(circle_x)), int(round(circle_y))), circle_radius)
    t = pygame.time.get_ticks() / 1000.0
    size = int(round(pulse_base + pulse_amp * math.sin(4 * math.pi * pulse_speed * t)))
    if size < 8:
        size = 80
    try:
        pulse_font = pygame.font.SysFont(None, size)
    except:
        pulse_font = pygame.font.Font(None, size)
    pulse_surf = pulse_font.render('Latvija', True, WHITE)
    pulse_rect = pulse_surf.get_rect(center=(WIDTH//2, flag_top + flag_height//2 + 140))
    screen.blit(pulse_surf, pulse_rect)
    pygame.display.flip()

pygame.quit()
sys.exit()