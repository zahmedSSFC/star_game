import pygame,sys, time
from random import randint
pygame.init()

screen_width = 600
screen_height = 600

screen = pygame.display.set_mode((screen_width,screen_height))
pygame.display.set_caption('Star game')

clock = pygame.time.Clock()

def get_input():
	keys = pygame.key.get_pressed()
	if keys[pygame.K_LEFT]:
		player.x +=-5
	elif keys[pygame.K_RIGHT]:
		player.x +=5

def player_screen_check():
	if player.x >= 570:
		player.x = 570
	elif player.x <=0:
		player.x = 0

def star_update(star_list, speed=5):
	for star in star_list:
		star.y += speed
		if star.y >= screen_height:
			star_list.remove(star)


def draw_stars(star_list):
	for star in star_list:
		pygame.draw.rect(screen, 'white', star)


def collisions(star_list):
	for star in star_list:
		if star.colliderect(player):
			return False
	return True

def display_score(score):
	score_text = game_font.render(f'Score : {int(score)}', True, 'white')
	score_text_rect = score_text.get_rect(topleft = (10,10))
	screen.blit(score_text, score_text_rect)

def display_highscore(high_score):
	high_score_text = game_font.render(f'High Score: {int(high_score)}',True,'white')
	high_score_text_rect = high_score_text.get_rect(topleft = (400,10))
	screen.blit(high_score_text,high_score_text_rect)

def start_music():
	background_music.play(loops = -1)

#background
background = pygame.image.load('bg.jpeg')
background = pygame.transform.scale(background, (1000,800))
background_rect = background.get_rect(topleft =(0,0))

#music
background_music = pygame.mixer.Sound('sophie.mp3')

 
#font
game_font = pygame.font.SysFont("Tahoma",30)

#player
player = pygame.Rect(300,540, 30,60)
player_speed = 5

#stars
star_list = []


score = 0
high_score = 0

star_vel = 5
star_count = 0
star_timer = pygame.USEREVENT + 1
timer_duration = 2000
pygame.time.set_timer(star_timer, timer_duration)

game_active = True
start_music()

while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		
		if event.type == star_timer:
			for _ in range(3):
				xpos = randint(1,screen_width)
				ypos = randint(-100, -50)
				star_rect = pygame.Rect(xpos,ypos,10,20)
				star_list.append(star_rect)

			
		timer_duration = max(200, timer_duration - 50)
		pygame.time.set_timer(star_timer, timer_duration)

		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				star_list.clear()
				score = 0
				start_music()

	if game_active:

		get_input()
		player_screen_check()
		screen.blit(background, background_rect)
		pygame.draw.rect(screen,'red',player)
		star_update(star_list)
		draw_stars(star_list)
		game_active = collisions(star_list)
		display_score(score)
		score += 0.01
		display_highscore(high_score)

	else:
		if score > high_score:
			high_score = score

		screen.fill('black')
		game_over_text = game_font.render('Game over',False, 'white')
		game_over_text_rect = game_over_text.get_rect(topleft = (225,250))
		screen.blit(game_over_text, game_over_text_rect )
		display_highscore(high_score)
		background_music.stop()



	pygame.display.update()
	clock.tick(60)