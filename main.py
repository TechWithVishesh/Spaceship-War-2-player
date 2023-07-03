import pygame
pygame.font.init()
pygame.mixer.init()

SCREEN_WIDTH, SCREEN_HEIGHT = 900, 500
SCREEN = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
pygame.display.set_caption("Spaceship War")

WHITE = (255, 255, 255)
FPS = 60
BULLET_VEL = 10
YELLOW_VEL = 5
RED_VEL = 5

BULLET_HIT_SOUND = pygame.mixer.Sound("Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Gun+Silencer.mp3")

YELLOW_HIT = pygame.USEREVENT + 1
RED_HIT = pygame.USEREVENT + 2

SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 60, 55
BULLET_WIDTH, BULLET_HEIGHT = 15, 7

BACKGROUND = pygame.transform.scale(pygame.image.load("space.png"), (SCREEN_WIDTH, SCREEN_HEIGHT))
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("spaceship_yellow.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90)
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(pygame.image.load("spaceship_red.png"), (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), -90)

BORDER_WIDTH, BORDER_HEIGHT = 10, 500

WINNER_FONT = pygame.font.SysFont("algerian", 100)
HEALTH_FONT = pygame.font.SysFont("timesnewroman", 40)

def yellow_spaceship_movement(keys, yellow, border):
    if keys[pygame.K_a] and yellow.x - YELLOW_VEL >= 0:
        yellow.x -= YELLOW_VEL
    if keys[pygame.K_d] and yellow.x + YELLOW_VEL + yellow.width <= border.x:
        yellow.x += YELLOW_VEL
    if keys[pygame.K_w] and yellow.y - YELLOW_VEL >= 0:
        yellow.y -= YELLOW_VEL
    if keys[pygame.K_s] and yellow.y + YELLOW_VEL + yellow.height <= SCREEN_HEIGHT:
        yellow.y += YELLOW_VEL

def red_spaceship_movement(keys, red, border):
    if keys[pygame.K_LEFT] and red.x - RED_VEL >= border.x + border.width + 5:
        red.x -= YELLOW_VEL
    if keys[pygame.K_RIGHT] and red.x + RED_VEL + red.width <= SCREEN_WIDTH:
        red.x += YELLOW_VEL
    if keys[pygame.K_UP] and red.y - RED_VEL >= 0:
        red.y -= YELLOW_VEL
    if keys[pygame.K_DOWN] and red.y + RED_VEL + red.height <= SCREEN_HEIGHT:
        red.y += YELLOW_VEL

def bullets_handle(yellow_bullets, red_bullets, yellow, red):
    for bullet in yellow_bullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet):
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellow_bullets.remove(bullet)
        elif bullet.x > SCREEN_WIDTH:
            yellow_bullets.remove(bullet)

    for bullet in red_bullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet):
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            red_bullets.remove(bullet)
        elif bullet.x < 0:
            red_bullets.remove(bullet)
    
def draw(yellow, red, border, red_bullets, yellow_bullets, red_health, yellow_health):
    SCREEN.fill(WHITE)
    SCREEN.blit(BACKGROUND, (0, 0))

    red_health_font = HEALTH_FONT.render("Health: " + str(red_health), 1, "white")
    yellow_health_font = HEALTH_FONT.render("Health: " + str(yellow_health), 1, "white")
    SCREEN.blit(red_health_font, (SCREEN_WIDTH - red_health_font.get_width() - 10, 10))
    SCREEN.blit(yellow_health_font, (10, 10))

    SCREEN.blit(YELLOW_SPACESHIP, (yellow.x, yellow.y))
    SCREEN.blit(RED_SPACESHIP, (red.x, red.y))

    pygame.draw.rect(SCREEN, "black", border)

    for bullet in red_bullets:
        pygame.draw.rect(SCREEN, "red", bullet)
    for bullet in yellow_bullets:
        pygame.draw.rect(SCREEN, "yellow", bullet)

    pygame.display.update()

def win(text):
    winner_text = WINNER_FONT.render(text, 1, "orange")
    SCREEN.blit(winner_text, (SCREEN_WIDTH/2 - winner_text.get_width()/2, SCREEN_HEIGHT/2 - winner_text.get_height()/2))
    pygame.display.update()
    pygame.time.delay(4000)

def main():
    clock = pygame.time.Clock()
    run = True

    yellow = pygame.Rect(20, SCREEN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    red = pygame.Rect(880 - SPACESHIP_WIDTH, SCREEN_HEIGHT/2 - SPACESHIP_HEIGHT/2, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)
    border = pygame.Rect(SCREEN_WIDTH/2 - BORDER_WIDTH/2, SCREEN_HEIGHT/2 - BORDER_HEIGHT/2, BORDER_WIDTH, BORDER_HEIGHT)

    red_bullets = []
    yellow_bullets = []
    MAX_BULLETS = 3

    yellow_health, red_health = 10, 10

    while run:
        clock.tick(FPS)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LCTRL and len(yellow_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(yellow.x + yellow.width, yellow.y + yellow.height//2, BULLET_WIDTH, BULLET_HEIGHT)
                    yellow_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                
                if event.key == pygame.K_RCTRL and len(red_bullets) < MAX_BULLETS:
                    bullet = pygame.Rect(red.x, red.y + red.height//2, BULLET_WIDTH, BULLET_HEIGHT)
                    red_bullets.append(bullet)
                    BULLET_FIRE_SOUND.play()

            if event.type == RED_HIT:
                red_health -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellow_health -= 1
                BULLET_HIT_SOUND.play()

        winner_t = ""
        if red_health <= 0:
            winner_t = "YELLOW WINS!!"
        if yellow_health <= 0:
            winner_t = "RED WINS!!"
        if winner_t != "":
            win(winner_t)
        
        keys = pygame.key.get_pressed()

        draw(yellow, red, border, red_bullets, yellow_bullets, red_health, yellow_health)
        yellow_spaceship_movement(keys, yellow, border)
        red_spaceship_movement(keys, red, border)
        bullets_handle(yellow_bullets, red_bullets, yellow, red)

    main()

if __name__ == "__main__":
    main()