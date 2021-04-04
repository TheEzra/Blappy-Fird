import pygame, sys, random
from random import randint

# functions #
def draw_floor():
	screen.blit(floor_surface, (floor_xpos,450))
	screen.blit(floor_surface, (floor_xpos + 288,450))

def draw_bg():
	screen.blit(bg_surface, (bg_xpos,0))
	screen.blit(bg_surface, (bg_xpos + 288,0))

def create_pipe():
	random_pipe_pos = randint(200, 400)
	bottom_pipe = pipe_surface.get_rect(midtop = (320, random_pipe_pos))
	top_pipe = pipe_surface.get_rect(midbottom = (320, random_pipe_pos - 100))
	return bottom_pipe,top_pipe

def move_pipe(pipes):
	for pipe in pipes:
		pipe.centerx -= 5
	return pipes

def draw_pipes(pipes):
	for pipe in pipes:
		if pipe.bottom >= 512:
			screen.blit(pipe_surface,pipe)
		else:
			flip_pipe = pygame.transform.flip(pipe_surface, False, True)
			screen.blit(flip_pipe,pipe)

def check_collision(pipes):
	for pipe in pipes:
		if bird_rect.colliderect(pipe):
			return False


	if bird_rect.top <= -15 or bird_rect.bottom >= 450:
		return False

	return True


def rotate_bird(bird):
	new_bird = pygame.transform.rotozoom(bird, -bird_movement * 3, 1)
	return new_bird

def bird_animation():
	new_bird = bird_frames[bird_index]
	new_bird_rect = new_bird.get_rect(center = (100, bird_rect.centery))
	return new_bird, new_bird_rect

def score_display(game_state):
	if game_active:
		score_surface = game_font.render(str(int(score)), True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (288/2, 50))
		screen.blit(score_surface, score_rect)
	if game_active == False:
		score_surface = game_font.render(f'Score: {int(score)}', True, (255, 255, 255))
		score_rect = score_surface.get_rect(center = (288/2, 50))
		screen.blit(score_surface, score_rect)

		high_score_surface = game_font.render(f'High scr.: {int(high_score)}', True, (255, 255, 255))
		high_score_rect = high_score_surface.get_rect(center = (288/2, 512/5))
		screen.blit(high_score_surface, high_score_rect)

def update_score(score, high_score):
	if score > high_score:
		high_score = score
	return high_score

def PressButton_display(game_state):
	if game_active:
		gameover_surface = space_font.render('Press [Space] to restart!', True, (255, 255, 255))
		gameover_rect = gameover_surface.get_rect(center = (288/4, 420))

		screen.blit(gameover_surface, gameover_rect,)
		screen.blit(splash_surface, splash_rect)

def Start_screen(game_state):
	if game_active == False:
		screen.blit(splash_surface, splash_rect)



pygame.init()
pygame.display.set_caption('Blappy Fird')
screen = pygame.display.set_mode((288,512))
clock = pygame.time.Clock()
game_font = pygame.font.Font('assets/04B_19__.ttf' ,40)
space_font = pygame.font.Font('assets/04B_19__.ttf',21)

# game vars #
bird_initpos = 288/3,256
gravity = 0.50
bird_movement = 0
game_active = False
score = 0
high_score = 0

# bg stuff #
bg_surface = pygame.image.load('assets/background-night.png').convert()
bg_xpos = 0

# floor stuff #
floor_surface = pygame.image.load('assets/base.png').convert()
floor_xpos = 0

# bird stuff #
bird_downflap = pygame.image.load('assets/redbird-downflap.png').convert_alpha()
bird_midflap = pygame.image.load('assets/redbird-midflap.png').convert_alpha()
bird_upflap = pygame.image.load('assets/redbird-upflap.png').convert_alpha()
bird_frames = [bird_downflap, bird_midflap, bird_upflap]	
bird_index = 0

bird_surface = bird_frames[bird_index]
bird_rect = bird_surface.get_rect(center=(bird_initpos))

BIRDFLAP = pygame.USEREVENT + 1
pygame.time.set_timer(BIRDFLAP, 200)

favicon = pygame.image.load('favicon.ico').convert()
pygame.display.set_icon(favicon)

# pipe stuff #
pipe_surface = pygame.image.load('assets/pipe-red.png').convert()
pipe_list = []
SPAWNPIPE = pygame.USEREVENT
pygame.time.set_timer(SPAWNPIPE, 2000)

splash_surface = pygame.image.load('assets/message.png').convert_alpha()
splash_rect = splash_surface.get_rect(center=(288/2, 512/1.7))

# game loop #
while True:
	for event in pygame.event.get():
		if event.type == pygame.QUIT:
			pygame.quit()
			sys.exit()
		if event.type == pygame.KEYDOWN:
			if event.key == pygame.K_SPACE and game_active:
				bird_movement = 0
				bird_movement -= 6
			if event.key == pygame.K_SPACE and game_active == False:
				game_active = True
				pipe_list.clear()
				bird_rect.center = 288/3,256
				bird_movement = 0
				score = 0

		if event.type == BIRDFLAP:
			if bird_index < 2:
				bird_index += 1
			else:
				bird_index = 0

			bird_surface, bird_rect = bird_animation()

		if event.type == SPAWNPIPE:
			pipe_list.extend(create_pipe())	


	# bg animation #
	draw_bg()
	if bg_xpos <= -288:
		bg_xpos = 0


	if game_active :
		# move bird #
		bird_movement += gravity
		rotated_bird = rotate_bird(bird_surface)
		bird_rect.centery += bird_movement
		# draw bird #
		screen.blit(rotated_bird,bird_rect)
		game_active = check_collision(pipe_list)

		# Pipes
		pipe_list = move_pipe(pipe_list)
		draw_pipes(pipe_list)

		floor_xpos -= 5
		bg_xpos -= 0.4

		score += 0.05
		score_display('main_game')
	else:
		if game_active == False:
			high_score = update_score(score, high_score)
			score_display('game_over')
			PressButton_display('game_over')
			Start_screen(False)

	# floor animation #
	draw_floor()
	if floor_xpos <= -288:
		floor_xpos = 0

	pygame.display.update()
	clock.tick(30)