# Intro to GameDev - main game file
import pgzrun
import random

WIDTH = 1000
HEIGHT = 600

BLUE = (0, 0, 255)

level = 0
level_screen = 0
score = 0
junk_collect = 0
lvl2_LIMIT=10
lvl3_LIMIT=15
JUNK_SPEED = 5
SATELLITE_SPEED = 5
DEBRIS_SPEED = 3
LASER_SPEED = -5

START_IMG = "start_button"
INSTRUCTIONS_IMG = "instructions_button"
BACKGROUND_TITLE = "logo"
BACKGROUND_LEVEL1 = "level_1"
BACKGROUND_LEVEL2 = "level_2"
BACKGROUND_LEVEL3 = "level_3"
BACKGROUND_IMG = BACKGROUND_TITLE
PLAYER_IMG = 'player_spaceship'
JUNK_IMG = 'space_junk'
SATELLITE_IMG = "satellite_adv"
DEBRIS_IMG = "space_debris2"
LASER_IMG = "laser_red"

SCOREBOX_HEIGHT = 70

def init():
    global player, junks, satellite, debris, lasers
    player = Actor(PLAYER_IMG)
    player.midright = (WIDTH - 15, HEIGHT/2)
        
    junks = []

    lasers = []
    player.laserActive = 1

    music.play("spacelife")

    for i in range(5):
        junk = Actor(JUNK_IMG)
        x_pos = random.randint(-500, -50)
        y_pos = random.randint(SCOREBOX_HEIGHT,HEIGHT - junk.height)
        junk.topleft = (x_pos, y_pos)
        junks.append(junk)

    satellite=Actor(SATELLITE_IMG)
    x_sat = random.randint(-500, -50)
    y_sat = random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
    satellite.topright = (x_sat, y_sat)

    debris=Actor(DEBRIS_IMG)
    x_deb = random.randint(-500, -50)
    y_deb = random.randint(SCOREBOX_HEIGHT, HEIGHT - debris.height)
    debris.topright = (x_deb, y_deb)

start_button = Actor(START_IMG)
start_button.center = (WIDTH/2, 425)
instructions_button = Actor(INSTRUCTIONS_IMG)
instructions_button.center = (WIDTH/2, 500)

init()

def update():
    global level, level_screen, BACKGROUND_IMG, junk_collect, score
    if junk_collect == lvl2_LIMIT:
        level=2
    if junk_collect == lvl3_LIMIT:
        level=3
    if level == -1: 
        BACKGROUND_IMG = BACKGROUND_LEVEL1

    if score>=0 and level>=1:
        if level_screen == 1:
            BACKGROUND_IMG = BACKGROUND_LEVEL1
            if keyboard.RETURN == 1:
                level_screen = 2
        if level_screen == 2:
            updatePlayer()
            updateJunk()
        if level == 2 and level_screen <=3:
            BACKGROUND_IMG = BACKGROUND_LEVEL2
            level_screen=3
            if keyboard.RETURN == 1:
                level_screen= 4
                music.play("space_suspense")
        if level_screen==4:
            updatePlayer()
            updateJunk()
            updateSatellite()
        if level == 3 and level_screen <= 5:
            level_screen=5
            BACKGROUND_IMG = BACKGROUND_LEVEL3
            if keyboard.RETURN == 1:
                level_screen=6
                music.play("space_mysterious")
        if level_screen==6:
            updatePlayer()
            updateJunk()
            updateSatellite()
            updateDebris()
            updateLasers()
            music.stop
            music.play("spacelife")

    if score<0 or level ==-2:
        if keyboard.RETURN==1:
            BACKGROUND_IMG="logo"
            score=0
            junk_collect=0
            level=0
            init()

def updatePlayer():
    if (keyboard.up == 1):
        player.y += -5
    elif(keyboard.down == 1):
        player.y += 5
    if player.bottom > HEIGHT:
        player.bottom = HEIGHT
    if player.top<70:
        player.top=70

    if keyboard.space== 1 and level==3:
        laser = Actor(LASER_IMG)
        laser.midright = (player.midleft)
        fireLasers(laser)

def updateJunk():
    global score, junk_collect
    for junk in junks:
        junk.x += JUNK_SPEED
        collision = player.colliderect(junk)
        if junk.left > WIDTH or collision == 1:
            x_pos = -50
            y_pos = random.randint(SCOREBOX_HEIGHT, HEIGHT - junk.height)
            junk.topleft = (x_pos, y_pos)

            if (collision == 1):
                sounds.collect_pep.play()
                score += 1
                junk_collect += 1

def updateSatellite():
    global score
    satellite.x += SATELLITE_SPEED

    collision=player.colliderect(satellite)
    if satellite.left>WIDTH or collision==1:
        x_sat=random.randint(-500, -50)
        y_sat=random.randint(SCOREBOX_HEIGHT, HEIGHT-satellite.height)
        satellite.topright = (x_sat, y_sat)

    if collision==1:
        score+= -10

def updateDebris():
    global score
    debris.x += DEBRIS_SPEED

    collision=player.colliderect(debris)
    if debris.left>WIDTH or collision == 1:
        x_deb=random.randint(-500, -50)
        y_deb=random.randint(SCOREBOX_HEIGHT, HEIGHT-debris.height)
        debris.topright= (x_deb, y_deb)

    if collision==1:
        score+=-10

player.laserActive = 1  # add laserActive status to the player

def makeLaserActive():  # when called, this function will make lasers active again
    global player
    player.laserActive = 1

def fireLasers(laser):
    if player.laserActive == 1:  # active status is used to prevent continuous shoot when holding space key
        player.laserActive = 0
        clock.schedule(makeLaserActive, 0.2)  # schedule an event (function, time afterwhich event will occur)
        sounds.laserfire03.play()  # play sound effect
        lasers.append(laser)  # add laser to lasers list
        
def draw():
    screen.clear()
    screen.blit(BACKGROUND_IMG, (0,0))
    if level == 0:
        start_button.draw()
        instructions_button.draw()
    if level == -1:
        start_button.draw()
        show_instructions = "Use UP and DOWN arrow keys to move your player\n\npress SPACEBAR to shoot"
        screen.draw.text(show_instructions, midtop=(WIDTH/2, 70), fontsize=35, color="white")

    if level>=1:
        player.draw()
        for junk in junks:
            junk.draw()
        satellite.draw()
        debris.draw()
        for laser in lasers:
            laser.draw()
    if score<0:
        game_over="GAME OVER\nPress ENTER to play again"
        screen.draw.text(game_over, center=(WIDTH/2, HEIGHT/2), fontsize=60, color="white")

    show_score = "Score: " + str(score)
    screen.draw.text(show_score, topleft=(750 ,40), fontsize=35, color="white")

    show_collect_value="Junk: " + str(junk_collect)
    screen.draw.text(show_collect_value, topleft=(450, 40), fontsize=35, color="white")

    if level>=1:
        show_level="LEVEL" + str(level)
        screen.draw.text (show_level, topright=(160, 40), fontsize=35, color="white")

    if level_screen == 1 or level_screen == 3 or level_screen == 5:
        show_level_title = "LEVEL" + str(level) + "\nPress ENTER to continue..."
        screen.draw.text(show_level_title, center=(WIDTH/2,HEIGHT/2), fontsize=70, color="white")
        
def updateLasers():
    global score
    for laser in lasers:
        laser.x+= LASER_SPEED
        if laser.right<0:
            lasers.remove(laser)
        if satellite.colliderect(laser)==1:
            lasers.remove(laser)
            x_sat=random.randint(-500,-50)
            y_sat=random.randint(SCOREBOX_HEIGHT, HEIGHT - satellite.height)
            satellite.topright = (x_sat, y_sat)
            score+=-5
            sounds.explosion.play()
        if debris.colliderect(laser)== 1:
            lasers.remove(laser)
            x_deb=random.randint(-500, -50)
            y_deb=random.randint(SCOREBOX_HEIGHT, HEIGHT-debris.height)
            debris.topright=(x_deb, y_deb)
            score+=5
            sounds.explosion.play()

def on_mouse_down(pos):
    global level, level_screen
    if start_button.collidepoint(pos):
        level=1
        level_screen=1
        print("start button is pressed")

    if instructions_button.collidepoint(pos):
        level=-1
        print("instructions button is pressed")
        

pgzrun.go()
