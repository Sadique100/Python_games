# program template for Spaceship
import simplegui
import math
import random

# globals for user interface
WIDTH = 800
HEIGHT = 600
score = 0
lives = 3
time = 0.5
start_game =  False
rock_group = set([])
missile_group = set([])
explosion_group = set([])
ship_plosion = set([])
class ImageInfo:
    def __init__(self, center, size, radius = 0, lifespan = None, animated = False):
        self.center = center
        self.size = size
        self.radius = radius
        if lifespan:
            self.lifespan = lifespan
        else:
            self.lifespan = float('inf')
        self.animated = animated

    def get_center(self):
        return self.center

    def get_size(self):
        return self.size

    def get_radius(self):
        return self.radius

    def get_lifespan(self):
        return self.lifespan

    def get_animated(self):
        return self.animated

    
# art assets created by Kim Lathrop, may be freely re-used in non-commercial projects, please credit Kim
    
# debris images - debris1_brown.png, debris2_brown.png, debris3_brown.png, debris4_brown.png
#                 debris1_blue.png, debris2_blue.png, debris3_blue.png, debris4_blue.png, debris_blend.png
debris_info = ImageInfo([320, 240], [640, 480])
debris_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/debris2_blue.png")

# nebula images - nebula_brown.png, nebula_blue.png
nebula_info = ImageInfo([400, 300], [800, 600])
nebula_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/nebula_blue.png")

# splash image
splash_info = ImageInfo([200, 150], [400, 300])
splash_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/splash.png")

# ship image
ship_info = ImageInfo([45, 45], [90, 90], 35)
ship_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/double_ship.png")

# missile image - shot1.png, shot2.png, shot3.png
missile_info = ImageInfo([5,5], [10, 10], 3, 50)
missile_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/shot2.png")

# asteroid images - asteroid_blue.png, asteroid_brown.png, asteroid_blend.png
asteroid_info = ImageInfo([45, 45], [90, 90], 40)
asteroid_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/asteroid_blue.png")

# animated explosion - explosion_orange.png, explosion_blue.png, explosion_blue2.png, explosion_alpha.png
explosion_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_alpha.png")
explosion2_info = ImageInfo([64, 64], [128, 128], 17, 24, True)
explosion2_image = simplegui.load_image("http://commondatastorage.googleapis.com/codeskulptor-assets/lathrop/explosion_blue.png")

# sound assets purchased from sounddogs.com, please do not redistribute
soundtrack = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/soundtrack.mp3")
missile_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/missile.mp3")
missile_sound.set_volume(.5)
ship_thrust_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/thrust.mp3")
explosion_sound = simplegui.load_sound("http://commondatastorage.googleapis.com/codeskulptor-assets/sounddogs/explosion.mp3")

# helper functions to handle transformations
def angle_to_vector(ang):
    return [math.cos(ang), math.sin(ang)]

def dist(p,q):
    return math.sqrt((p[0] - q[0]) ** 2+(p[1] - q[1]) ** 2)


# Ship class
class Ship:
    def __init__(self, pos, vel, angle, image, info):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.thrust = False
        self.angle = angle
        self.angle_vel = 0
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        
    def draw(self,canvas):
        canvas.draw_image(self.image, self.image_center,self.image_size,self.pos, self.image_size, self.angle)

    def update(self):
        self.angle += self.angle_vel
        
        forward = angle_to_vector(self.angle)
       
        if self.thrust == True:
            self.vel[0] += (1-0.3)*forward[0]*0.5
            self.vel[1] += (1-0.3)*forward[1]*0.5
        else:
            self.vel[0] *= 0.9
            self.vel[1] *= 0.9
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        
        if self.pos[0]  < 0 and self.vel[0] < 0:
            self.pos[0] = WIDTH
        elif self.pos[0]  > WIDTH and self.vel[0] > 1:
            self.pos[0] = 0
        if self.pos[1]  < 0 and self.vel[1] < 0:
            self.pos[1] = HEIGHT
        elif self.pos[1]  > HEIGHT and self.vel[1] > 1:
            self.pos[1] = 0
            
    def key_input(self,key):
        
        if key == simplegui.KEY_MAP["left"]:
            self.angle_vel = -0.1
        elif key == simplegui.KEY_MAP["right"]:
            self.angle_vel = 0.1
        
        if key == simplegui.KEY_MAP["up"]:
            self.thrust = True
            my_ship.thrust_pic()
 
        if key == simplegui.KEY_MAP["space"]:
            my_ship.shoot()
            
    def reset_vels(self, key):
        if key == simplegui.KEY_MAP["left"] or key == simplegui.KEY_MAP["right"]:
            self.angle_vel = 0
        if key == simplegui.KEY_MAP["up"]:
            self.image_center[0] /= 3
            self.thrust = False
            ship_thrust_sound.rewind()
           
    def shoot(self):
        global missile_group
        mis_pos = [0,0]
        mis_vel = [0,0]
        forward = angle_to_vector(self.angle)
        mis_pos[0] = self.pos[0] + forward[0]*self.radius
        mis_pos[1] = self.pos[1] + forward[1]*self.radius
        mis_vel[0] = self.vel[0] + forward[0]*2
        mis_vel[1] = self.vel[1] + forward[1]*2
        a_missile = Sprite([mis_pos[0], mis_pos[1]], [mis_vel[0],mis_vel[1]], 0, 0, missile_image, missile_info, missile_sound)
        missile_group.add(a_missile)
    def thrust_pic(self):
        if self.thrust == True:
            self.image_center[0] *= 3
            ship_thrust_sound.play()
            
    def get_position(self):
        return self.pos
    
    def get_radius(self):
        return self.radius   

    def ship_hit(self,rock_group):
        global lives, ship_plosion
        if len(group_collision(rock_group, my_ship)):
            lives -= 1
            explode = Sprite([self.pos[0],self.pos[1]], [self.vel[0]*0.1,self.vel[1]*0.1], 0, 0, explosion2_image, explosion2_info, explosion_sound)
            ship_plosion.add(explode)
            #print set(ship_plosion)
# Sprite class
class Sprite:
    def __init__(self, pos, vel, ang, ang_vel, image, info, sound = None):
        self.pos = [pos[0],pos[1]]
        self.vel = [vel[0],vel[1]]
        self.angle = ang
        self.angle_vel = ang_vel
        self.image = image
        self.image_center = info.get_center()
        self.image_size = info.get_size()
        self.radius = info.get_radius()
        self.lifespan = info.get_lifespan()
        self.animated = info.get_animated()
        self.age = 0
        if sound:
            sound.rewind()
            sound.play()
   
    def draw(self, canvas):
        shift = 0
        if self.animated == True:
            shift  = self.image_center[0]*self.age
            print self.image_center, shift,self.age
            canvas.draw_image(self.image, [self.image_center[0]+shift,self.image_center[1]], self.image_size, self.pos, self.image_size, self.angle)
        else:   
            canvas.draw_image(self.image, self.image_center,self.image_size,self.pos, self.image_size, self.angle)
    
    def update(self):
        self.angle += self.angle_vel
        self.pos[0] += self.vel[0]
        self.pos[1] += self.vel[1]
        self.age += 1
        if self.pos[0]  < 0: 
            self.pos[0] = WIDTH
        elif self.pos[0]  > WIDTH: 
            self.pos[0] = 0
        
        if self.pos[1]  < 0: 
            self.pos[1] = HEIGHT
        elif self.pos[1]  > HEIGHT: 
            self.pos[1] = 0       
        
        if self.age >= self.lifespan:
            return True
        else:
            return False
            
    def get_position(self):  
        return self.pos
    
    def get_radius(self):
        return self.radius
    
    def collision_detector(self, object1, object2):        
        collision = False
        if dist(object1.get_position(),object2.get_position()) <= object1.get_radius()+object2.get_radius():
            collision = True
        return collision

def group_collision(group, object_other):
    global rock_group
    collide = set([])
    for item in group:
        if item.collision_detector(item, object_other) == True:
            collide.add(item)
    rock_group.difference_update(collide)
   
    return collide

def group_group_collide(group1, group2):
    global rock_group, missile_group, score
    explode = set([]) 
    for item in group1:
        if len(group_collision(group2, item)):
            explode.add(item)
            explosion = Sprite([item.pos[0],item.pos[1]], [0,0], 0, 0, explosion_image, explosion_info, explosion_sound)
            explosion_group.add(explosion)
    missile_group.difference_update(explode)
    #print set(explosion_group)
    return(explode)

def process_sprite_group(group, canvas):
    #collision = group_collision(rock_group, my_ship)
    expired = set([])
    for item in group:
        item.draw(canvas)
    for item in group:
        item.update()
        if item.update() == True:
            expired.add(item)
    group.difference_update(expired)
            
   
            
def draw(canvas):
    global time, lives, rock_group, score, start_game
    
    # animiate background
    time += 1
    center = debris_info.get_center()
    size = debris_info.get_size()
    wtime = (time / 8) % center[0]
    canvas.draw_image(nebula_image, nebula_info.get_center(), nebula_info.get_size(), [WIDTH / 2, HEIGHT / 2], [WIDTH, HEIGHT])
    canvas.draw_image(debris_image, [center[0] - wtime, center[1]], [size[0] - 2 * wtime, size[1]], 
                                [WIDTH / 2 + 1.25 * wtime, HEIGHT / 2], [WIDTH - 2.5 * wtime, HEIGHT])
    canvas.draw_image(debris_image, [size[0] - wtime, center[1]], [2 * wtime, size[1]], 
                                [1.25 * wtime, HEIGHT / 2], [2.5 * wtime, HEIGHT])

    
    
    if start_game == True:
        
        # draw ship and sprites
        my_ship.draw(canvas)
        process_sprite_group(rock_group, canvas)
        process_sprite_group(missile_group, canvas)
        process_sprite_group(explosion_group, canvas)
        process_sprite_group(ship_plosion, canvas)
        # update ship
        my_ship.update()
        my_ship.ship_hit(rock_group)
        
        score += 10*len(group_group_collide(missile_group, rock_group))
        
        if lives <= 0:
            start_game = False
            
        
    else:
        rock_group = set([])
        canvas.draw_image(splash_image, splash_info.get_center(), splash_info.get_size(), [WIDTH/2, HEIGHT/2], [2*(WIDTH/3),2*(HEIGHT/3)])

    canvas.draw_text("Lives : " +str(lives), [WIDTH/12, HEIGHT/10], 30, "Orange")
    canvas.draw_text("Score : " +str(score), [9.5*(WIDTH/12),HEIGHT/10], 30, "Orange")        

    
# timer handler that spawns a rock    
def rock_spawner():
    global a_rock, rock_group
    if len(rock_group) <=10:
        a_rock = Sprite([random.randrange(0, WIDTH), random.randrange(0, HEIGHT)], [random.randrange(-20,20)/10, random.randrange(-20,20)/10], random.randrange(0,1), random.randrange(15,25)/100, asteroid_image, asteroid_info)
        if dist(a_rock.get_position(),my_ship.get_position()) > 2*my_ship.get_radius():
            rock_group.add(a_rock)
      
#keydown handler
def key_down_handler(key):
    my_ship.key_input(key)
    
#keyup handler    
def key_up_handler(key):
    my_ship.reset_vels(key)

#start game
def start(position):
    global start_game, lives, score
    if start_game == False:
        pos = position
        if pos[0] < (2*WIDTH/3) and pos[0] > (WIDTH/3) and pos[1] > (HEIGHT/3) and pos[1] < 2*(HEIGHT/3):
            start_game = True    
            lives = 3
            score = 0
        my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)
# initialize frame
frame = simplegui.create_frame("Asteroids", WIDTH, HEIGHT)

# initialize ship and two sprites
my_ship = Ship([WIDTH / 2, HEIGHT / 2], [0, 0], 0, ship_image, ship_info)

# register handlers
frame.set_draw_handler(draw)
frame.set_keydown_handler(key_down_handler)
frame.set_keyup_handler(key_up_handler)
frame.set_mouseclick_handler(start)
timer = simplegui.create_timer(1000.0, rock_spawner)

# get things rolling
timer.start()
frame.start()
