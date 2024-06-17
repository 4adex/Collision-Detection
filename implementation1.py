import pygame
import math
import numpy as np
from GJK import GJK
from aabbtree import AABB
from aabbtree import AABBTree


#setting up colors
red = (235, 64, 52)
white = (255, 255, 255)
green = (18,204,25)
blue = (66,135,245)
radius = 5

#initializing pygame
pygame.init()
W,H = 600,600
WIN = pygame.display.set_mode((W,H))
pygame.display.set_caption('Simulation')


class Button:
    def __init__(self, color, x, y, width, height, text=''):
        self.color = color
        self.x = x
        self.y = y
        self.width = width
        self.height = height
        self.text = text

    def draw(self, win, outline=None):
        if outline:
            pygame.draw.rect(win, outline, (self.x-2, self.y-2, self.width+4, self.height+4), 0)
            
        pygame.draw.rect(win, self.color, (self.x, self.y, self.width, self.height), 0)
        
        if self.text != '':
            font = pygame.font.SysFont('comicsans', 20)
            text = font.render(self.text, 1, (0, 0, 0))
            win.blit(text, (self.x + (self.width/2 - text.get_width()/2), self.y + (self.height/2 - text.get_height()/2)))

    def isOver(self, pos):
        if pos[0] > self.x and pos[0] < self.x + self.width:
            if pos[1] > self.y and pos[1] < self.y + self.height:
                return True
            
        return False

class polygon:
    color = red
    def __init__(self,vertices):
        self.vertices = vertices
    def furthest(self,d):
        furthestP = self.vertices[0]
        for point in self.vertices:
            if point.dot(d)>furthestP.dot(d):
                furthestP = point
        return furthestP
    def centroid(self):
        return sum(self.vertices)/3
    
    def draw(self):
        pygame.draw.polygon(WIN,self.color,[(point[0],point[1]) for point in self.vertices], width = 0)
    def aabb(self):
        xmin = self.furthest([-1,0,0])[0]
        xmax = self.furthest([1,0,0])[0]
        ymin = self.furthest([0,-1,0])[1]
        ymax = self.furthest([0,1,0])[1]
        return AABB([(xmin, xmax), (ymin, ymax)])
    def update(self, axis, val):
        if axis == 'x':
            for i in range(len(self.vertices)):
                self.vertices[i] = np.array([self.vertices[i][0] + val, self.vertices[i][1], self.vertices[i][2]])
        if axis == 'y':
            for i in range(len(self.vertices)):
                self.vertices[i] = np.array([self.vertices[i][0], self.vertices[i][1] + val, self.vertices[i][2]])


class particle:
    accx = 0
    accy = 98
    color = (235, 64, 52)
    def __init__(self,x,y,radius):
        self.x = x
        self.y = y
        self.radius = radius
    def draw(self,win):
        pygame.draw.circle(win,self.color,(self.x,self.y),self.radius)
    
    def update_position(self):
        self.vely = self.vely+self.accy*(1/60)
        self.y = self.y+self.vely*(1/60)
        self.x = self.x+self.velx*(1/60)
        if self.y+self.radius>200:
            self.vely = -self.vely*0.8
        
        if self.x+self.radius>200:
            self.velx = -self.velx
        
        if self.x-self.radius<-200:
            self.velx = -self.velx
        
        if self.y-self.radius<-200:
            self.vely = -self.vely
    

def main():
    player = polygon([np.array([310,300,0]),np.array([300,310,0]),np.array([290,290,0])])
    player.color = blue
    run = True
    state = 'draw'
    treeshow = True
    drawbutton = Button(green,10,10,120,50,'Draw Mode')
    playbutton = Button(red, 140,10,120,50,'Play Mode')
    showtree = Button(red, 270,10,150,50,'Show BVH tree')
    clock = pygame.time.Clock()
    shapes = []
    vertices = []
    points = []
    font = pygame.font.SysFont('comicsans', 15)
    text1 = font.render('Switch between draw and play using above buttons', 1, (255,255,255))
    text2 = font.render('While in play, control using UP-DOWN-RIGHT-LEFT', 1, (255,255,255))
    text3 = font.render('While in draw, click to place vertices, click on initial vertex to close the polygon', 1, (255,255,255))
    while run:

        #
        drawbutton.color = green if state=='draw' else red
        playbutton.color = green if state=='play' else red
        showtree.color = green if treeshow else red
        clock.tick(60)
        WIN.fill((0, 0, 0))
        x,y = 0,0
        for event in pygame.event.get():
            if event.type ==pygame.QUIT:
                run = False
                
            if event.type == pygame.MOUSEBUTTONUP:
                x,y = pygame.mouse.get_pos()
                

        drawbutton.draw(WIN)
        playbutton.draw(WIN)
        showtree.draw(WIN)
        WIN.blit(text1, (235,525))
        WIN.blit(text2, (220,545))
        WIN.blit(text3, (32,565))

        if drawbutton.isOver((x,y)):
            state = 'draw'
        
        if playbutton.isOver((x,y)):
            state = 'play'
        if showtree.isOver((x,y)):
            treeshow = not treeshow

        if x and y and (state == 'draw') and (drawbutton.isOver((x,y))==False) and (playbutton.isOver((x,y))==False) and (showtree.isOver((x,y))==False):
            flag = False
            if vertices:
                if (x<(vertices[0][0]+radius)) and (x>(vertices[0][0]-radius)) and (y<(vertices[0][1]+radius)) and (y>(vertices[0][1]-radius)):
                    flag = True
                    shapes.append(polygon(vertices))
                    vertices = []
            if flag==False:
                vertices.append(np.array([x,y,0]))
                points.append(particle(x,y,2))
        
        for point in points:
            point.draw(WIN)
        for shape in shapes:
            shape.draw()

        player.draw()

        #Getting input from the user
        pressed = pygame.key.get_pressed()

        #construction of BVH tree
        tree = AABBTree()
        for i in range(len(shapes)):
            tree.add(shapes[i].aabb(),i)

        
        # Checking for possible collision with player by traversing the tree and then checking GJK on them
        poscol = tree.overlap_values(player.aabb())
        if len(poscol):
            for other in poscol:
                if GJK(shapes[other],player):
                    player.color = white
                else:
                    player.color = blue
        else:
            player.color = blue

        
                
        #player controls
        vel = 5
        if state == 'play':
            if pressed[pygame.K_UP]: player.update('y',-vel)
            if pressed[pygame.K_DOWN]: player.update('y',vel)
            if pressed[pygame.K_LEFT]: player.update('x',-vel)
            if pressed[pygame.K_RIGHT]: player.update('x',vel)

        #visualizing the modified tree requires making another tree and appending player as leaf in it
        if treeshow:
            tree2 = tree
            tree2.add(player.aabb())
            tree2.draw(WIN,white)
        
        pygame.display.update()

    pygame.quit()

main()