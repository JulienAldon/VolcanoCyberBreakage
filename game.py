# KidsCanCode - Game Development with Pygame video series
# Tile-based game - Part 5
# Player Graphics
# Video link: https://youtu.be/FVLRUmkV27Q
import pygame as pg
import sys
from os import path
from settings import *
from sprites import *
from tilemap import *
from map_gen import write_map
class Game:
	def __init__(self, selection):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.spritesheet = {}
		write_map("map.txt")
		self.load_data()
		self.char_team = selection
		self.coins = []
		self.current_map = 0
		self.game_folder = ""
		self.firsts_walls = None
		self.done = False
		self.score = 0
		self.player_dead = False
		self.title_font = pg.font.SysFont("Arial", 30)
		self.particles_list = []
		self.last_time = 0

	def load_data(self):
		self.game_folder = path.dirname(__file__)
		img_folder = path.join(self.game_folder, 'sprites')
		self.map = [Map(path.join(self.game_folder, 'map.txt')),
					Map(path.join(self.game_folder, 'treasure.txt')),
					Map(path.join(self.game_folder, 'map.txt')),]
		# Load swordEffect
		self.spritesheet['playerRun'] = Spritesheet(path.join(img_folder, "Robots/NormalRun_64.png"))
		self.spritesheet['playerIdle'] = Spritesheet(path.join(img_folder, "Robots/NormalIdle_64.png"))
		self.spritesheet['playerJump'] = Spritesheet(path.join(img_folder, "Robots/NormalJump_64.png"))
		self.spritesheet['weapons'] = Spritesheet(path.join(img_folder, "Weapons.png"))
		self.spritesheet['impactJump'] = Spritesheet(path.join(img_folder, "impact_jmp.png"))
		self.bullet_img = pg.image.load(path.join(img_folder, "Bullet.png")).convert_alpha()
		self.terrain = pg.image.load(path.join(img_folder, "lavaTerrain.png")).convert_alpha()
		self.terrain2 = pg.image.load(path.join(img_folder, "lavaTerrain_variante.png")).convert_alpha()
		self.marked_wall = pg.image.load(path.join(img_folder, "lavaTerrain_marked.png")).convert_alpha()
	def new(self):
		# initialize all variables and do all the setup for a new game
		self.all_sprites = pg.sprite.RenderUpdates()
		self.walls = pg.sprite.Group()
		self.ennemies = pg.sprite.Group()
		self.bullets = pg.sprite.Group()
		try:
			current_char = self.player.current
		except:
			current_char = 0
		if self.current_map == 0:
			self.firsts_walls = self.walls
		self.players = pg.sprite.Group()

		if self.current_map == 0:
			for i, a in enumerate(self.map[2].data):
				if 'X' in a:
					self.map[2].data[i] = a.replace('X', 'P')
				if 'P' in a:
					self.map[2].data[i] = a.replace('P', 'X')
		for row, tiles in enumerate(self.map[self.current_map].data):
			for col, tile in enumerate(tiles):
				if tile == '1':
					Wall(self, col, row, self.terrain, hit=False)
				if tile == '3':
					Wall(self, col, row, self.terrain)
				if tile == '2':
					Wall(self, col, row, self.terrain, RED)
				if tile == 'X':
					self.end = End(self, col, row)
				if tile == 'P':
					to_start = vec(col, row)
					self.player = Player(self, col, row, self.char_team, current_char)					
				if tile == 'O':
					self.coins.append(Coin(self, col, row))
				if tile == 'M':
					Mob(self, col, row)
		if self.current_map == 2:
			self.lava = Lava(self, to_start)

		self.stats = InGameStats(self, 0, 0, self.player)
		self.camera = Camera(self.map[self.current_map].width, self.map[self.current_map].height)

	def run(self):
		# game loop - set self.playing = False to end the game
		self.playing = True
		while self.playing:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.draw()
			self.update()
		if self.current_map == 1:
			self.score = self.player.coins	
		if self.current_map == 2:
			self.done = True
			pass
			# for a in self.firsts_walls:
			# 	if a.color == RED:
			# 		tmp = list(self.map[0].data[a.y])
			# 		tmp[a.x] = '2'
			# 		self.map[0].data[a.y] = ''.join(tmp)
			# self.remap()
			# self.map[2].write('map3.txt', self.map[0].data)
			# self.map[2].read('map3.txt')
		# if self.current_map > len(self.map) - 1:
		# 	self.map[0].read('map.txt')
		# 	self.remap()
		# 	print("aze")
		# 	self.map[2].write('map3.txt', self.map[0].data)
		# 	self.done = True
		self.current_map += 1

	def remap(self):
		for y, a in enumerate(self.map[2].data):
			for x, b in enumerate(a):
				if b == 'P':
					t = list(self.map[0].data[y])
					t[x] = 'X'
					self.map[0].data[y] = ''.join(t)
				elif b == 'X':
					t = list(self.map[0].data[y])
					t[x] = 'P'
					self.map[0].data[y] = ''.join(t)
					# print(self.map[0].data[y])

	def quit(self):
		pg.quit()
		sys.exit()

	def update(self):
		# update portion of the game loop
		self.walls.update()
		self.all_sprites.update()
		# self.last_time = pg.time.get_ticks()
		self.screen.blit(self.stats.image, self.stats.rect)
		self.camera.update(self.player)			

	def draw_grid(self):
		for x in range(0, WIDTH, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (x, 0), (x, HEIGHT))
		for y in range(0, HEIGHT, TILESIZE):
			pg.draw.line(self.screen, LIGHTGREY, (0, y), (WIDTH, y))

	def draw(self):
		self.screen.fill(BGCOLOR)
		# self.draw_grid()
		# for sprite in self.walls:
		# 	self.screen.blit(sprite.image, self.camera.apply(sprite))
		for sprite in self.all_sprites:
			self.screen.blit(sprite.image, self.camera.apply(sprite))
		pg.display.update()

	def events(self):
		# catch all events here
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				if event.key == pg.K_z:
					self.player.switch()
				if event.key == pg.K_SPACE:
					self.player.jump()
				if event.key == pg.K_a:
					if self.player.stats['track'] > 0:
						self.player.mark()

	def draw_text(self, text, font_name, size, color, x, y, align="topleft"):
		# font = pg.font.Font(font_name, size)
		text_surface = self.title_font.render(text, True, color)
		text_rect = text_surface.get_rect(**{align: (x, y)})
		self.screen.blit(text_surface, text_rect)

	def show_start_screen(self):
		pass

	def show_go_screen(self):
		self.screen.fill(BLACK)
		self.draw_text("GAME OVER", self.title_font, 100, RED,
		WIDTH / 2, HEIGHT / 2, align="center")
		if self.player_dead:
			self.draw_text("Score : PLAYER IS DEAD", self.title_font, 100, RED, 
			WIDTH / 2, HEIGHT * 2 / 3, align="center")
		else:
			self.draw_text("Score : " + str(self.score), self.title_font, 100, RED, 
			WIDTH / 2, HEIGHT * 2 / 3, align="center")

		self.draw_text("Press a key to start", self.title_font, 75, WHITE,
		WIDTH / 2, HEIGHT * 3 / 4, align="center")
		pg.display.flip()
		self.wait_for_key()


	def show_score_screen(self):
		pass

	def wait_for_key(self):
		pg.event.wait()
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.quit()
				if event.type == pg.KEYUP:
					waiting = False

class Select:
	def __init__(self):
		pg.init()
		self.screen = pg.display.set_mode((WIDTH, HEIGHT))
		pg.display.set_caption(TITLE)
		self.clock = pg.time.Clock()
		self.no = 0
		self.team_list = []

	def quit(self):
		pg.quit()
		sys.exit()

	def new(self):
		# initialize all variables and do all the setup for a new game
		self.all_sprites = pg.sprite.Group()
		self.char = Character(self, GRIDWIDTH/2 - GRIDWIDTH / 8, GRIDHEIGHT/2 - GRIDHEIGHT / 8)
		self.team = Team(self, GRIDWIDTH/8, 0)

	def run(self):
		# game loop - set self.playing = False to end the game
		self.selecting = True
		while self.selecting:
			self.dt = self.clock.tick(FPS) / 1000
			self.events()
			self.update()
			self.draw()
			if len(self.team_list) == 4:
				self.selecting = False

	def draw(self):
		self.screen.fill(BGCOLOR)
		# self.draw_grid()
		self.font = pg.font.SysFont("Arial", 30)
		self.counter = self.font.render("Remaining : " + str(4 - self.no), 1, BLACK)
		self.rules = self.font.render("Select your rolster : right to accept, left to refuse", 1, BLACK)
		self.rules2 = self.font.render("You can not refuse more than 4 time after that choices are random", 1, BLACK)
		H = self.rules.get_height()
		W = self.rules.get_width()
		self.screen.blit(self.counter, [int(WIDTH / 2 - W), int(HEIGHT - 2 * H)])
		self.screen.blit(self.rules2, [int(WIDTH / 2 - W), int(HEIGHT - 3 * H)])
		self.screen.blit(self.rules, [int(WIDTH / 2 - W), int(HEIGHT - 4 * H)])
		self.all_sprites.draw(self.screen)
		if len(self.team_list) >= 4:
			self.font = pg.font.SysFont("Arial", 30)
			ready = self.font.render("READY ?!", 1, BLACK)
			press = self.font.render("press any key to continue", 1, BLACK)
			H = ready.get_height()
			W = ready.get_width()
			image = pg.Surface((WIDTH, int(HEIGHT/4)))
			image.fill(WHITE)
			self.screen.blit(image, [0, int(HEIGHT / 2 - HEIGHT / 6)])
			self.screen.blit(ready, [int(WIDTH / 2 - W), int(HEIGHT / 2 - 2 * H)])
			self.screen.blit(press, [int(WIDTH / 2 - 2 * W), int(HEIGHT / 2 - H)])
		pg.display.flip()

	def update(self):
		# update portion of the game loop
		self.all_sprites.update()

	def refuse(self):
		if self.no < 3:
			self.char = Character(self, GRIDWIDTH/2 - GRIDWIDTH / 8, GRIDHEIGHT/2 - GRIDHEIGHT / 8)
		else:
			while len(self.team_list) < 4:
				c = Character(self, GRIDWIDTH/2 - GRIDWIDTH / 8, GRIDHEIGHT/2 - GRIDHEIGHT / 8)
				self.team.add_member(c)
				self.team_list.append(c)
		self.no += 1

	def accept(self):
		self.team_list.append(self.char)
		self.team.add_member(self.char)

		self.char = Character(self, GRIDWIDTH/2 - GRIDWIDTH / 8, GRIDHEIGHT/2 - GRIDHEIGHT / 8)

	def events(self):
		# catch all events here
		for event in pg.event.get():
			if event.type == pg.QUIT:
				self.quit()
			if event.type == pg.KEYDOWN:
				if event.key == pg.K_ESCAPE:
					self.quit()
				if event.key == pg.K_LEFT:
					self.refuse()
				if event.key == pg.K_RIGHT:
					self.accept()
	
	def wait_for_key(self):
		pg.event.wait()
		waiting = True
		while waiting:
			self.clock.tick(FPS)
			for event in pg.event.get():
				if event.type == pg.QUIT:
					waiting = False
					self.quit()
				if event.type == pg.KEYUP:
					waiting = False

	def getSelection(self):
		return self.team_list
# create the game object
s = Select()
while len(s.team_list) < 4:
	s.new()
	s.run()

s.wait_for_key()
selection = s.getSelection()

g = Game(selection)
g.show_start_screen()

while g.done == False and g.player_dead == False:
	g.new()
	g.run()
	g.show_start_screen()

g.show_go_screen()
