import pygame as pg
from settings import *
import random
vec = pg.math.Vector2
from tilemap import collide_hit_rect
import math
from effects import *

class Spritesheet:
	def __init__(self, filename):
		self.spritesheet = pg.image.load(filename).convert_alpha()

	def get_image(self, x, y, width, height):
		# grab an image out of a larger spritesheet
		image = pg.Surface((width, height), pg.SRCALPHA)
		image.blit(self.spritesheet, (0, 0), (x, y, width, height))
		image = pg.transform.scale(image, (width, height))
		return image

def collide_with_walls_mob(sprite, group, dir):
	if dir == 'x':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
			sprite.vel.x = 0
			sprite.hit_rect.centerx = sprite.pos.x
	if dir == 'y':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centery > sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
			if hits[0].rect.centery < sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
			sprite.vel.y = 0
			sprite.hit_rect.centery = sprite.pos.y

def collide_with_walls(sprite, group, dir):
	if dir == 'x':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centerx > sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.left - sprite.hit_rect.width / 2
				if sprite.jumping is True:
					sprite.last_dir = 20
			if hits[0].rect.centerx < sprite.hit_rect.centerx:
				sprite.pos.x = hits[0].rect.right + sprite.hit_rect.width / 2
				if sprite.jumping is True:
					sprite.last_dir = -20
			sprite.wall_slide = True
			# sprite.vel.x = 0
			sprite.hit_rect.centerx = sprite.pos.x
		else:
			sprite.wall_slide = False
			sprite.jumping = False
	if dir == 'y':
		hits = pg.sprite.spritecollide(sprite, group, False, collide_hit_rect)
		if hits:
			if hits[0].rect.centery > sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.top - sprite.hit_rect.height / 2
				sprite.walk = True
			if hits[0].rect.centery < sprite.hit_rect.centery:
				sprite.pos.y = hits[0].rect.bottom + sprite.hit_rect.height / 2
			sprite.vel.y = 0
			sprite.hit_rect.centery = sprite.pos.y
		else:
			sprite.walk = False
			sprite.jumping = True

class Team(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		
		self.list = []
		self.image = pg.Surface((WIDTH - WIDTH/4, HEIGHT/4))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.pos = vec(x, y) * TILESIZE

	def update(self):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		for i, a in enumerate(self.list):
			img = pg.transform.scale(a.image, (int(self.rect.width / 4) - 60, self.rect.height - 20))
			self.image.blit(img, [ 10 + i* int(self.rect.width / 4) , 10])
	def add_member(self, char):
		self.list.append(char)

class Character(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.weapon = ""
		self.archetype = random.choice(ARCHETYPES)

		if ARCHETYPES.index(self.archetype) == 0: # Tracker
			self.track = random.randint(8, 20)
			self.speed = 3
			self.Hack = random.randint(1, 2)
			self.life = random.randint(1, 3)
		elif ARCHETYPES.index(self.archetype) == 1: # Hacker
			self.track = random.randint(1, 2)
			self.speed = 3
			self.Hack = random.randint(3, 5)
			self.life = random.randint(1, 3)
		elif ARCHETYPES.index(self.archetype) == 2: # Runner
			self.track = random.randint(1, 2)
			self.speed = 4
			self.Hack = random.randint(1, 2)
			self.life = random.randint(1, 2)
		elif ARCHETYPES.index(self.archetype) == 3: # Tank
			self.track = random.randint(1, 2)
			self.speed = 2
			self.Hack = random.randint(1, 2)
			self.life = random.randint(4, 8)

		self.font = pg.font.SysFont("Arial", 30)
		track = "Tracking : " + str(self.track)
		speed = "Speed : " + str(self.speed)
		Hack = "Hack : " + str(self.Hack)
		life = "Life : " + str(self.life)
		self.text_archetype = self.font.render(self.archetype, 1, BLACK)
		self.textSurf_track = self.font.render(track, 1, BLACK)
		self.textSurf_speed = self.font.render(speed, 1, BLACK)
		self.textSurf_Hack = self.font.render(Hack, 1, BLACK)
		self.textSurf_life = self.font.render(life, 1, BLACK)
		self.image = pg.Surface((WIDTH/4, HEIGHT/2))
		self.color = random.choice(COLORS)
		self.image.fill(self.color)
		self.rect = self.image.get_rect()
		H = self.textSurf_track.get_height()
		self.image.blit(self.text_archetype, [10, self.rect.height/2 - 3 * H])
		self.image.blit(self.textSurf_speed, [10, self.rect.height/2])
		self.image.blit(self.textSurf_track, [10, self.rect.height/2 - H])
		self.image.blit(self.textSurf_Hack, [10, self.rect.height/2 - H + 2 * H])
		self.image.blit(self.textSurf_life, [10, self.rect.height/2 - H + 3 * H])
		self.vel = vec(0, 0)
		self.pos = vec(x, y) * TILESIZE
	
	def update(self):
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

class Mob(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites, game.ennemies
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((32, 32))
		self.rect = self.image.get_rect()

		self.pos = vec(x, y) * TILESIZE

		self.hit_rect = pg.Rect(0, 0, self.rect.width - 15, self.rect.height - 15)
		self.hit_rect.center = self.rect.center

		self.vel = vec(0, 0)
		self.acc = vec(0, 0)
		self.rect.center = self.pos
		self.health = 3
		self.speed = 3
		self.dir = 0

	def update(self):
		self.acc = vec(self.dir, PLAYER_GRAV)
		# equations of motion
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		self.acc = vec(0, 0)
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
		self.hit_rect.centerx = self.pos.x
		collide_with_walls_mob(self, self.game.walls, 'x')
		self.hit_rect.centery = self.pos.y
		collide_with_walls_mob(self, self.game.walls, 'y')
		self.rect.center = self.hit_rect.center
		if self.health <= 0:
			a = random.randint(0, 1)
			if a == 1:
				Explosion(self.game, self.pos.x, self.pos.y)
			self.kill()
		# self.rect.center = self.pos

class Player(pg.sprite.Sprite):
	def __init__(self, game, x, y, team, current_char=0):
		self.groups = game.all_sprites, game.players
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.load_images()

		self.image = self.running_frames[0]
		self.rect = self.image.get_rect()

		# Color
		self.color = team[0].color
		# self.image.fill(self.color)
		self.rect.center = vec(x, y) * TILESIZE
		self.vel = vec(0, 0)
		self.pos = vec(x, y) * TILESIZE
		self.hit_rect = pg.Rect(0, 0, self.rect.width - 15, self.rect.height - 25)
		self.hit_rect.center = self.rect.center

		self.team = team
		self.current = current_char

		self.weapon = Weapon(game, self.pos.x, self.pos.y)
		self.stats = {
			"track": self.team[self.current].track,
			"speed": self.team[self.current].speed,
			"Hack": self.team[self.current].Hack,
			"life": self.team[self.current].life
		}

		self.wall_slide = False
		self.acc = vec(0, 0)
		self.last_dir = -20
		self.coins = 0
		self.walk = False
		self.idle = False
		self.jumping = False

		# Animation
		self.current_frame = 0
		self.last_update = 0
		self.angle = 0

		# Shoot
		self.last_shot = 0
		self.shoots = self.weapon.bullets
		self.reloading = False
		self.shooting = False

	def mark(self):
		hits = pg.sprite.spritecollide(self, self.game.walls, False)
		if hits:
			for hit in hits:
				hit.mark()
			self.team[self.current].track -= 1

	def get_keys(self):
		keys = pg.key.get_pressed()
		# print(self.shooting)
		if keys[pg.K_LEFT]:
			if self.shooting: # strafe (while shooting you don't change direction)
				self.acc.x = -self.stats['speed']
			else:
				self.last_dir = -self.stats['speed']
				if self.jumping:
					self.acc.x = -self.stats['speed'] / 1.5
				else:
					self.acc.x = -self.stats['speed']
		if keys[pg.K_RIGHT]:
			if self.shooting: # strafe
				self.acc.x = self.stats['speed']
			else:
				self.last_dir = self.stats['speed']
				if self.jumping:
					self.acc.x = self.stats['speed'] / 1.5
				else:
					self.acc.x = self.stats['speed']

		if keys[pg.K_e]:
			now = pg.time.get_ticks()
			if now - self.last_shot > self.weapon.bullet_rate and self.shoots > 0:
				self.last_shot = now
				self.shooting = True
				self.reloading = False
				if self.last_dir < 0:
					pos = vec(self.pos.x - self.weapon.barrel_offset.x, self.pos.y + self.weapon.barrel_offset.y)
					Bullet(self.game, pos, vec(-self.last_dir/self.last_dir, 0))
					self.vel += vec(self.weapon.kickback, 0)
				elif self.last_dir > 0:
					pos = vec(self.pos.x + self.weapon.barrel_offset.x, self.pos.y + self.weapon.barrel_offset.y)
					Bullet(self.game, pos, vec(self.last_dir/self.last_dir, 0))
					self.vel += vec(-self.weapon.kickback, 0)
				self.shoots -= 1
		else:
			self.shooting = False
			# self.vel = vec(-self.weapon.kickback, 0)

	def jump(self):
		self.jumping = True
		self.rect.x += 1
		hits = pg.sprite.spritecollide(self, self.game.walls, False)
		self.rect.x -= 1
		if hits:
			self.vel.y = -20
			if self.wall_slide and not self.walk:
				self.vel.x = -self.last_dir * self.stats['speed']
				if self.last_dir < 0:
					JumpFx(self.game, self.pos.x, self.pos.y, 3)
				else:
					JumpFx(self.game, self.pos.x, self.pos.y, 2)
			else:
				JumpFx(self.game, self.pos.x, self.pos.y, 1)
		self.walk = False
		self.idle = False

	def load_images(self):
		self.jumping_frames = [self.game.spritesheet['playerJump'].get_image(0, 0, 45, 83),
								self.game.spritesheet['playerJump'].get_image(47, 0, 49, 83),
								self.game.spritesheet['playerJump'].get_image(97, 0, 54, 83),
								self.game.spritesheet['playerJump'].get_image(152, 0, 48, 83),
		]
		self.standing_frames = [self.game.spritesheet['playerIdle'].get_image(0, 0, 42, 83),
								self.game.spritesheet['playerIdle'].get_image(45, 0, 43, 83),
								self.game.spritesheet['playerIdle'].get_image(90, 0, 43, 83),
								self.game.spritesheet['playerIdle'].get_image(132, 0, 43, 83),
							]
		self.running_frames = [self.game.spritesheet['playerRun'].get_image(0, 0, 40, 84),
								self.game.spritesheet['playerRun'].get_image(40, 0, 41, 84),
								self.game.spritesheet['playerRun'].get_image(82, 0, 49, 84),
								self.game.spritesheet['playerRun'].get_image(136, 0, 49, 84),
								self.game.spritesheet['playerRun'].get_image(187, 0, 49, 84),
								self.game.spritesheet['playerRun'].get_image(237, 0, 44, 84),
								self.game.spritesheet['playerRun'].get_image(282, 0, 47, 84),
								self.game.spritesheet['playerRun'].get_image(332, 0, 53, 84),
								self.game.spritesheet['playerRun'].get_image(388, 0, 53, 84),
								self.game.spritesheet['playerRun'].get_image(443, 0, 53, 84),
								]
		# for frame in self.running_frames:
		# 	frame.set_colorkey(BLACK)

	def animate(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 100:
			self.last_update = now
			if self.walk is True:
				self.current_frame = (self.current_frame + 1) % len(self.running_frames)
				bottom = self.rect.bottom
				self.image = self.running_frames[self.current_frame]
			elif self.idle is True:
				self.current_frame = (self.current_frame + 1) % len(self.standing_frames)
				bottom = self.rect.bottom
				self.image = self.standing_frames[self.current_frame]
			elif self.jumping is True:
				self.current_frame = (self.current_frame + 1) % len(self.jumping_frames)
				bottom = self.rect.bottom
				self.image = self.jumping_frames[self.current_frame]
			else:
				bottom = self.rect.bottom
			# self.image = pg.transform.rotate(self.running_frames[self.current_frame], 180)
			if self.last_dir < 0:
				self.image = pg.transform.flip(self.image, True, False)
			self.rect.bottom = bottom

	def update(self):
		# Animation
		if self.vel.x < 1 and self.vel.x > -1 and self.jumping is False:
			self.idle = True
			self.walk = False
		if self.current_frame >= len(self.running_frames) - 1:
			self.current_frame = 0

		# shoot
		now = pg.time.get_ticks()
		if self.shoots <= 0:
			self.reloading = True
		if now - self.last_shot > self.weapon.loading_time:
			self.shoots = self.weapon.bullets
		if self.reloading == True:
			pass
			# LoadingBar(self.game, self.pos.x, self.pos.y, self.weapon.loading_time)
		if self.shooting == True:
			self.game.camera.shaking = True
		else:
			self.game.camera.shaking = False

		self.animate()

		# Color
		self.color = self.team[self.current].color
		# colorImage = pg.Surface(self.image.get_size()).convert_alpha()
		# colorImage.fill(self.color, special_flags=pg.BLEND_RGBA_MULT)
		# self.image.blit(colorImage, (0,0), special_flags=pg.BLEND_RGBA_MULT)
		slow = 0
		if self.wall_slide:
			slow = 0.4
			# self.acc.y = 0
			self.vel.y = self.vel.y / 1.05
		# apply friction
		self.acc = vec(0, PLAYER_GRAV - slow)
		self.get_keys()
		# equations of motion
		self.acc.x += self.vel.x * PLAYER_FRICTION
		self.vel += self.acc
		self.pos += self.vel + 0.5 * self.acc
		self.acc = vec(0, 0)

		self.rect.x = self.pos.x
		self.rect.y = self.pos.y

		self.rect.center = self.pos
		self.hit_rect.centerx = self.pos.x
		if self.last_dir >= 0:
			self.pos.x -= 10
			collide_with_walls(self, self.game.walls, 'x')
			self.pos.x += 10
		elif self.last_dir < 0:
			self.pos.x += 10
			collide_with_walls(self, self.game.walls, 'x')
			self.pos.x -= 10
		self.hit_rect.centery = self.pos.y
		collide_with_walls(self, self.game.walls, 'y')
		self.rect.center = self.hit_rect.center

		self.stats = {
			'track': self.team[self.current].track,
			'speed': self.team[self.current].speed / 1.5,
			'Hack': self.team[self.current].Hack,
			'life': self.team[self.current].life
		}

	def switch(self):
		if self.current + 1 > 3:
			self.current = 0
		else:
			self.current += 1	

class Bullet(pg.sprite.Sprite):
	def __init__(self, game, pos, dir):
		self.groups = game.all_sprites, game.bullets
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = self.game.bullet_img
		self.image = pg.transform.scale(self.image, (64, 30))
		if dir.x == -1:
			self.image = pg.transform.flip(self.image, True, False)
		# self.image.fill(WHITE)
		self.rect = self.image.get_rect()
 
		self.hit_rect = self.rect
		self.pos = vec(pos.x, pos.y)
		self.rect.center = self.pos
		spread = random.uniform(-self.game.player.weapon.spread,self.game.player.weapon.spread)
		# print(dir.rotate(spread))
		self.vel = dir.rotate(spread) * self.game.player.weapon.speed
		self.spawn_time = pg.time.get_ticks()

	def update(self):
		self.pos.x += self.vel.x * self.game.dt
		self.pos.y += self.vel.y * self.game.dt
		self.rect.center = self.pos
		if pg.sprite.spritecollideany(self, self.game.walls):
			Explosion(self.game, self.pos.x, self.pos.y, 100)
			# if self.vel.x > 0:
			# 	create_particles(self.game, self.game.particles_list, self.pos, 2)
			# elif self.vel.x < 0:
			# 	create_particles(self.game, self.game.particles_list, self.pos, 4)
			# if self.vel.y > 0:
			# 	create_particles(self.game, self.game.particles_list, self.pos, 1)
			# if self.vel.y < 0:
			# 	create_particles(self.game, self.game.particles_list, self.pos, 3)
			self.kill()
		hits = pg.sprite.spritecollideany(self, self.game.ennemies)
		if hits:
			hits.health -= 1
		if pg.time.get_ticks() - self.spawn_time > self.game.player.weapon.bullet_lifetime:
			self.kill()

class Weapon(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.load_images()
		self.image = self.weapons[0]
		self.rect = self.image.get_rect()
		self.pos = vec(x, y)
		self.image = pg.transform.scale(self.image, (60, 20))
		self.mod = 0
		self.last_turn = 0
		
		# weapon Stats
		self.loading_time = 3000
		self.bullets = 150
		self.bullet_rate = 50
		self.kickback = 1
		self.spread = 5
		self.speed = 4000
		self.bullet_lifetime = 10000
		self.barrel_offset = vec(32, 10)

	def load_images(self):
		self.weapons = [self.game.spritesheet['weapons'].get_image(254, 111, 112, 43),]
		# for i in self.weapons:

	def update(self):
		self.pos = self.game.player.pos
		if self.game.player.last_dir < 0 and self.last_turn == 0:
			self.last_turn = 1
			self.image = pg.transform.flip(self.image, True, False)
			self.mod = self.game.player.rect.width
		elif self.game.player.last_dir > 0 and self.last_turn == 1: 
			self.mod = self.game.player.rect.width / 2
			self.image = pg.transform.flip(self.image, True, False)
			self.last_turn = 0
		# print(self.game.player.last_dir)
		self.rect.x = self.pos.x - self.mod
		self.rect.y = self.pos.y

class InGameStats(pg.sprite.Sprite):
	def __init__(self, game, x, y, player):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.player = player
		self.track = self.game.char_team[self.game.player.current].track
		self.speed = self.game.char_team[self.game.player.current].speed
		self.Hack = self.game.char_team[self.game.player.current].Hack
		self.life = self.game.char_team[self.game.player.current].life
		self.pox = vec(x, y)

		self.font = pg.font.SysFont("Arial", 30)
		track = "Tracking : " + str(self.track)
		speed = "Speed : " + str(self.speed)
		Hack = "Hack : " + str(self.Hack)
		life = "Life : " + str(self.life)
		self.textSurf_track = self.font.render(track, 1, BLACK)
		self.textSurf_speed = self.font.render(speed, 1, BLACK)
		self.textSurf_Hack = self.font.render(Hack, 1, BLACK)
		self.textSurf_life = self.font.render(life, 1, BLACK)
		self.image = pg.Surface((WIDTH/7, HEIGHT/2), pg.SRCALPHA)
		self.rect = self.image.get_rect()
		H = self.textSurf_track.get_height()
		self.image.blit(self.textSurf_track, [10, self.rect.height/2 - H])
		self.image.blit(self.textSurf_speed, [10, self.rect.height/2])
		self.image.blit(self.textSurf_Hack, [10, self.rect.height/2 - H + 2 * H])
		self.image.blit(self.textSurf_life, [10, self.rect.height/2 - H + 3 * H])
	
	def update(self):
		self.image.fill(pg.SRCALPHA)
		self.track = self.game.char_team[self.game.player.current].track
		self.speed = self.game.char_team[self.game.player.current].speed
		self.Hack = self.game.char_team[self.game.player.current].Hack
		self.life = self.game.char_team[self.game.player.current].life
		
		self.font = pg.font.SysFont("Arial", 30)
		track = "Tracking : " + str(self.track)
		speed = "Speed : " + str(self.speed)
		Hack = "Hack : " + str(self.Hack)
		life = "Life : " + str(self.life)
		self.textSurf_track = self.font.render(track, 1, BLACK)
		self.textSurf_speed = self.font.render(speed, 1, BLACK)
		self.textSurf_Hack = self.font.render(Hack, 1, BLACK)
		self.textSurf_life = self.font.render(life, 1, BLACK)
		H = self.textSurf_track.get_height()
		self.image.blit(self.textSurf_track, [10, self.rect.height/2 - H])
		self.image.blit(self.textSurf_speed, [10, self.rect.height/2])
		self.image.blit(self.textSurf_Hack, [10, self.rect.height/2 - H + 2 * H])
		self.image.blit(self.textSurf_life, [10, self.rect.height/2 - H + 3 * H])
		self.pos = vec(-self.game.camera.x + TILESIZE, -self.game.camera.y - TILESIZE * 2)
		self.rect.x = self.pos.x
		self.rect.y = self.pos.y
			
class End(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(BLACK)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

	def update(self):
		collide = pg.sprite.spritecollide(self, self.game.players, False)
		if collide:
			self.game.playing = False

class Wall(pg.sprite.Sprite):
	def __init__(self, game, x, y, image, color=None, hit=True):
		if hit:
			self.groups = game.walls, game.all_sprites
		else:
			self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = image
		self.color = color
		if self.color:
			self.image.fill(self.color)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE
		self.health = 10

	def mark(self):
		self.image = self.game.marked_wall

	def destroy(self):
		self.kill()
		
	def update(self):
		if self.health <= 0:
			self.destroy()
		# if self.color
		# self.image.fill(self.color)

class Coin(pg.sprite.Sprite):
	def __init__(self, game, x, y):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game
		self.image = pg.Surface((TILESIZE, TILESIZE))
		self.image.fill(YELLOW)
		self.rect = self.image.get_rect()
		self.x = x
		self.y = y
		self.rect.x = x * TILESIZE
		self.rect.y = y * TILESIZE

	def update(self):
		collide = pg.sprite.spritecollide(self, self.game.players, False)
		if collide:
			self.game.player.coins += 1
			self.kill()

class Lava(pg.sprite.Sprite):
	def __init__(self, game, start):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.image = pg.Surface((0, 0))
		self.image.fill(ORANGE)
		self.rect = self.image.get_rect()
		self.x = start.x
		self.y = start.y
		self.rect.x = start.x * TILESIZE
		self.rect.y = start.y * TILESIZE
		self.last_update = pg.time.get_ticks()
		self.lava_start = False
		self.w = 10
		self.h = 10
	
	def update(self):
		now = pg.time.get_ticks()
		if now - self.last_update > 5000:
			self.last_update = now
			self.lava_start	= True
		if self.lava_start and now - self.last_update > 100:
			self.last_update = now
			self.w += 50
			self.h += 50
			self.rect = self.image.get_rect()
			self.rect.x = self.x * TILESIZE
			self.rect.y = self.y * TILESIZE
			self.image.fill(ORANGE)
			self.rect.center = vec(self.x * TILESIZE, self.y * TILESIZE)
			# self.rect.y -= 6
			# self.y -= 10

		collide = pg.sprite.spritecollide(self, self.game.players, False)
		if collide:
			self.game.player_dead = True
			self.game.playing = False
			# self.game.player.kill()

class Particle(pg.sprite.Sprite):
	def __init__(self, game, x, y, dx, dy, size, orr):
		self.groups = game.all_sprites
		pg.sprite.Sprite.__init__(self, self.groups)
		self.game = game

		self.image = pg.Surface((size, size))
		self.color = self.game.player.color
		# self.image.fill(self.color)
		self.image.set_colorkey(BLACK)
		self.size = size
		pg.draw.ellipse(self.image, self.color, [0,0,size/2,size])
		self.rect = self.image.get_rect()
		try:
			self.vel = vec(dx, dy).normalize() * 5
		except:
			self.vel = vec(dx, dy)
		_amod = 0
		if orr.x == 1:
			_amod = 90
		_angle = angle((orr.x, orr.y), (self.vel.x, self.vel.y))
		self.image = pg.transform.rotate(self.image, math.degrees(_angle) + _amod)
		self.hit_rect = pg.Rect(0, 0, size, size)
		self.hit_rect.center = self.rect.center
		self.pos = vec(x, y)
		self.rect.x = x
		self.rect.y = y
		self.gravity = 0.25
		self.timedisplayed = random.randint(300, 400)
		self.time = pg.time.get_ticks()
 
	def update(self):
		#self.y_velocity += self.gravity
		self.rect.x += self.vel.x
		self.rect.y += self.vel.y		
		if pg.time.get_ticks() - self.time >= self.timedisplayed:
			self.kill()

	def display(self, main_surface):
		main_surface.blit(self.image, (self.rect.x, self.rect.y))

def dotproduct(v1, v2):
	return sum((a*b) for a, b in zip(v1, v2))

def length(v):
	return dotproduct(v, v)**0.5

def angle(v1, v2):
	try:
		return math.acos(dotproduct(v1, v2) / (length(v1) * length(v2)))
	except:
		return 0

def create_particles(game, p_list, position, _dir=1):
	"""
	_dir : 
	1 : up, 2 : right, 3 : down, 4 : left
	"""
	particle_count = 30
	if _dir == 1:
		numbersy = range(-100, 0)
		numbersx = range(-100, 100)
		orr = vec(1, 0)
	elif _dir == 2:
		numbersy = range(-100, 100)
		numbersx = range(-100, 0)
		orr = vec(0, 1)
	elif _dir == 3:
		numbersy = range(0, 100)
		numbersx = range(-100, 100)
		orr = vec(1, 0)
	elif _dir == 4:
		numbersy = range(-100, 100)
		numbersx = range(0, 100)
		orr = vec(0, 1)
	for i in range(0, particle_count):
		dx = random.choice(numbersx)
		dy = random.choice(numbersy)
		size = random.randint(1, 10)
		p = Particle(game, position.x, position.y + 32, dx, dy, size, orr)
		p_list.append(p)
	return p_list
