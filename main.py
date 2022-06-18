import pygame
pygame.font.init() #adds fonts
pygame.mixer.init() #adds sounds

WIDTH, HEIGHT = 900, 500
WIN = pygame.display.set_mode((WIDTH, HEIGHT)) #sets up window
pygame.display.set_caption("Spaceship Game") #caption of top of screen
RED = (255, 0, 0)
YELLOW = (255, 255, 0)
BLACK = (0, 0, 0)
WHITE = (255, 255, 255)

BORDER = pygame.Rect((WIDTH // 2) - 5, 0, 10, HEIGHT)

BULLET_HIT_SOUND = pygame.mixer.Sound("Assets/Grenade+1.mp3")
BULLET_FIRE_SOUND = pygame.mixer.Sound("Assets/Gun+Silencer.mp3")

HEALTH_FONT = pygame.font.SysFont('comicsans', 40)
WINNER_FONT = pygame.font.SysFont('comicsans', 100)

FPS = 60
VEL = 4
BULLET_VEL = 10
MAX_BULLETS = 4
SPACESHIP_WIDTH, SPACESHIP_HEIGHT = 55, 40

YELLOW_HIT = pygame.USEREVENT + 1 #two separate user events
RED_HIT = pygame.USEREVENT + 2 #numbers used to diferentiate between events

YELLOW_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_yellow.png") #obtains image from assets
YELLOW_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    YELLOW_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 90) #rotates and scales image

RED_SPACESHIP_IMAGE = pygame.image.load("Assets/spaceship_red.png") #obtains image from assets
RED_SPACESHIP = pygame.transform.rotate(pygame.transform.scale(
    RED_SPACESHIP_IMAGE, (SPACESHIP_WIDTH, SPACESHIP_HEIGHT)), 270) #rotates and scales image

SPACE = pygame.transform.scale(pygame.image.load("Assets/space.png"), (WIDTH, HEIGHT))

def drawWindow(yellow, red, yellowBullets, redBullets, yellowHealth, redHealth):
    WIN.blit(SPACE, (0, 0)) #fills screen with white
    pygame.draw.rect(WIN, BLACK, BORDER) #draws the border

    yellowHealthText = HEALTH_FONT.render("Health: " + str(yellowHealth), 1, WHITE)
    redHealthText = HEALTH_FONT.render("Health: " + str(redHealth), 1, WHITE)
    WIN.blit(yellowHealthText, (10, 10))
    WIN.blit(redHealthText, (WIDTH - yellowHealthText.get_width() - 10, 10))

    WIN.blit(RED_SPACESHIP, (yellow.x, yellow.y)) #draws the yellow spaceship
    WIN.blit(YELLOW_SPACESHIP, (red.x, red.y)) #draws the red spaceship


    for bullet in yellowBullets:
        pygame.draw.rect(WIN, YELLOW, bullet)
    for bullet in redBullets:
        pygame.draw.rect(WIN, RED, bullet)

    pygame.display.update() # updates the screen

def yellowMovement(keysPressed, yellow):
    if keysPressed[pygame.K_a] and yellow.x - VEL > 0:  # LEFT
        yellow.x -= VEL
    if keysPressed[pygame.K_d] and yellow.x + VEL + SPACESHIP_HEIGHT < BORDER.x:  # RIGHT
        yellow.x += VEL
    if keysPressed[pygame.K_w] and yellow.y - VEL > 0:  # UP
        yellow.y -= VEL
    if keysPressed[pygame.K_s] and yellow.y + VEL + SPACESHIP_WIDTH < HEIGHT:  # DOWN
        yellow.y += VEL

def redMovement(keysPressed, red):
    if keysPressed[pygame.K_LEFT] and red.x - VEL > BORDER.x + BORDER.width:  # LEFT
        red.x -= VEL
    if keysPressed[pygame.K_RIGHT] and red.x + VEL + SPACESHIP_HEIGHT < WIDTH:  # RIGHT
        red.x += VEL
    if keysPressed[pygame.K_UP] and red.y - VEL > 0:  # UP
        red.y -= VEL
    if keysPressed[pygame.K_DOWN] and red.y + VEL + SPACESHIP_WIDTH < HEIGHT:  # DOWN
        red.y += VEL

def handleBullets(yellowBullets, redBullets, yellow, red):
    for bullet in yellowBullets:
        bullet.x += BULLET_VEL
        if red.colliderect(bullet): #checks if two rectangles collide
            pygame.event.post(pygame.event.Event(RED_HIT))
            yellowBullets.remove(bullet)
        elif bullet.x > WIDTH:
            yellowBullets.remove(bullet)

    for bullet in redBullets:
        bullet.x -= BULLET_VEL
        if yellow.colliderect(bullet): #checks if two rectangles collide
            pygame.event.post(pygame.event.Event(YELLOW_HIT))
            redBullets.remove(bullet)
        elif bullet.x < 0:
            redBullets.remove(bullet)

def drawWinner(text):
    drawText = WINNER_FONT.render(text, 1, WHITE)
    WIN.blit(drawText, (WIDTH // 2 - drawText.get_width() // 2, HEIGHT // 2 - drawText.get_height() // 2))
    pygame.display.update()
    pygame.time.delay(5000)

def main():
    # all variables in here should be game specific
    yellow = pygame.Rect(100, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT) # xPos, yPos, width, height
    red = pygame.Rect(750, 250, SPACESHIP_WIDTH, SPACESHIP_HEIGHT)

    redBullets = []
    yellowBullets = []

    redHealth = 10
    yellowHealth = 10

    running = True
    clock = pygame.time.Clock() #sets up clock
    while running:
        clock.tick(FPS) #makes game run at 60 fps
        for event in pygame.event.get():
            if event.type == pygame.QUIT: # red x quits the program
                running = False
                pygame.quit()
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_SPACE and len(yellowBullets) < MAX_BULLETS: #yellow bullet
                    bullet = pygame.Rect(yellow.x + yellow.height, yellow.y + yellow.height // 2 + 3, 10, 5) # x, y, width, height
                    yellowBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
                if event.key == pygame.K_l and len(redBullets) < MAX_BULLETS: #red bullet
                    bullet = pygame.Rect(red.x, red.y + red.height // 2 + 3, 10, 5)
                    redBullets.append(bullet)
                    BULLET_FIRE_SOUND.play()
            if event.type == RED_HIT:
                redHealth -= 1
                BULLET_HIT_SOUND.play()
            if event.type == YELLOW_HIT:
                yellowHealth -= 1
                BULLET_HIT_SOUND.play()
        winnerText = ""
        if redHealth <= 0:
            winnerText = "Yellow Wins"
        if yellowHealth <= 0:
            winnerText = "Red Wins"
        if winnerText != "":
            drawWinner(winnerText)
            break

        keysPressed = pygame.key.get_pressed()
        yellowMovement(keysPressed, yellow)
        redMovement(keysPressed, red)

        handleBullets(yellowBullets, redBullets, yellow, red)

        drawWindow(red, yellow, yellowBullets, redBullets, yellowHealth, redHealth)

    main()

if __name__ == "__main__":
    main()
