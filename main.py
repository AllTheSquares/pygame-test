import pygame, sys, random, time
from pygame.locals import *

pygame.init()
 
# Colours
BACKGROUND =(255, 255, 255)
RED = (255, 30, 70)

# Game Setup   
FPS = 30
fpsClock = pygame.time.Clock()
WINDOW_WIDTH = 600
WINDOW_HEIGHT = 300
WINDOW = pygame.display.set_mode((WINDOW_WIDTH, WINDOW_HEIGHT))

bg = pygame.transform.scale(pygame.image.load('images/bg.jpg'), (600,300))

groundHeight = 40
ground = pygame.Rect(0, WINDOW_HEIGHT-groundHeight, WINDOW_WIDTH, groundHeight)

pygame.display.set_caption('Hack Club Workshop')

SPAWNMONSTER = USEREVENT + 1
CHECKPLAYERCOLLISION = USEREVENT + 2
CHECKBULLETCOLLISION = USEREVENT + 3
# The main function that controls the game
def main ():
	looping = True
	characterHealth = 100
	characterX = 0
	characterY = WINDOW_HEIGHT
	characterWidth = 50
	characterHeight = 70
	character =  pygame.transform.scale(pygame.image.load('images/protag.png'), (50,75)).convert_alpha()
	characterHitbox = character.get_rect()
	#the default direction is the one the image is in (right)
	characterDirection = character;
	#flip the player when you press the left key
	lookLeft = pygame.transform.flip(characterDirection, True, False)

	pygame.time.set_timer(SPAWNMONSTER, 1000)
	pygame.time.set_timer(CHECKPLAYERCOLLISION, 500)

	#loading our enemy
	enemy = pygame.transform.scale(pygame.image.load('images/enem.gif'), (75,75)).convert_alpha()
	enemyDirection = enemy
	enemyRight = pygame.transform.flip(enemyDirection, True, False)
	#dimensions of enemy sprite
	enemyWidth = 75 
	enemyHeight =75


	#taking care of our physics--we have to come back down after a jump after all
	jumpInitialVelocity = 20
	jumpVelocity = -21
	jumpAcceleration = -2
	isJumping=False;
	

	enemies = []
	bullets = []


	def spawn_monster():
		random.seed(time.perf_counter())
		# We wanna spawn our monsters at least a little bit away from the player
		#CHALLENGE: Can you figure out how to accomplish this? We'll go over the solution in our next meet!
		#HINT: Python has an absolute value function called abs(). You can use this to verify/check that the monster is spawning at least a little left or right of our player!

		#We're getting a random coordinate, between 0 (the screen's left end) and WINDOW_WIDTH-enemyWidth (the screen's right end with space for our enemy)

		xPosition = random.randrange(enemyWidth, WINDOW_WIDTH-enemyWidth)
		yPosition = WINDOW_HEIGHT-groundHeight-enemyHeight

		spawnedHitbox = enemy.get_rect()
		spawnedHitbox.x = xPosition
		spawnedHitbox.y = yPosition

		enemies.append(spawnedHitbox)



	def playerCrash(characterHitbox, characterX, enemies):
		if(characterHitbox.collidelist(enemies)!=-1):
			return True
		return False

	def bulletHit(bullet, enemies):
		index = bullet.collidelist(enemies)
		if(index!=-1):
			enemies.pop(index)

  # The main game loop
	while looping:
		characterHitbox.x = characterX
		characterHitbox.y = characterY


		for event in pygame.event.get() :
			if event.type == QUIT :
				pygame.quit()
				sys.exit()
			elif event.type == SPAWNMONSTER:
				if(len(enemies) < 3):
					spawn_monster()
			if event.type == CHECKPLAYERCOLLISION:
					if(playerCrash(characterHitbox, characterX, enemies)):
						characterHealth = characterHealth - 10
					print(characterHealth)


			#This helps us check which key is currently pressed
			pressed = pygame.key.get_pressed()

			#Here we check if a certain key is pressed, and decide what to do based on that
			if (pressed[K_RIGHT] or pressed[K_d]):
				characterX = characterX + 10
				characterDirection = character
			if (pressed[K_LEFT] or pressed[K_a]):
				characterX = characterX - 10
				characterDirection = lookLeft
			if (pressed[K_UP] or pressed[K_w]):
				if(not isJumping):
					jumpVelocity = jumpInitialVelocity
					isJumping=True;
			if (event.type==pygame.KEYUP and event.key == pygame.K_SPACE):
				#If we press space, shoot a bullet!
				bulletVelocity = 10
				if(characterDirection==lookLeft):
					bulletVelocity = bulletVelocity * -1
				
				#This is called a dictionary! Check out the tutorials folder if you're feeling a little confused
				bullets.append({
						"shape": pygame.Rect(characterX, characterY, 10, 4),
						"velocity": bulletVelocity
					})


			if (event.type == pygame.KEYDOWN and event.key == K_r):
				characterX = 0
				characterY = 0

		if jumpVelocity >= -jumpInitialVelocity :
			characterY = characterY - jumpVelocity
			jumpVelocity = jumpVelocity + jumpAcceleration
			if(jumpVelocity < -jumpInitialVelocity):
				isJumping=False
		
		if (characterX + characterWidth > WINDOW_WIDTH):
			characterX = WINDOW_WIDTH-characterWidth
		if (characterX  <= 0 ) :
			characterX = 0

		if (characterY + characterHeight >= WINDOW_HEIGHT-groundHeight) :
			characterY = WINDOW_HEIGHT - groundHeight - characterHeight
		if (characterY <= 0) :
			characterY = 0
		if(characterHealth==0):
			print("Game Over")
			sys.exit()
		WINDOW.blit(bg, (0, 0))
		WINDOW.blit(characterDirection, (characterX, characterY))
		for hitbox in enemies:
			WINDOW.blit(enemyDirection, hitbox)

		pygame.draw.rect(WINDOW, RED, ground)

		for bullet in bullets:
			pygame.draw.rect(WINDOW, BACKGROUND, bullet["shape"])
			#This may seem complex but what we're doing is that we're adding
			#velocity is equal to distance over time. Every second, we're adding a little bit of distance to our bullet's x coordinate, which is what makes it go farther and farther!
			bullet["shape"].x = bullet["shape"].x + bullet["velocity"]
			bulletHit(bullet["shape"], enemies)

		pygame.display.update()
		fpsClock.tick(FPS)
 
main()