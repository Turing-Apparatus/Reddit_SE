import  pygame          as PG
from    pygame.locals   import *


orange = (255, 150, 50)
lightblue = (102, 178, 255)
blue = (0, 80, 120)
yellow = (255, 255, 80)
pink = (255, 80, 160)
purple = (75, 10, 140)
magenta = (130, 10, 80)
green = (0, 140, 70)
black = (0, 0, 0)
white = (255, 255, 255)
gray = (150,150,150)

rainbow = [  (0,0,0),
        (204,0,0), (204,102,0), (204,204,0),
        (0,204,0), (0,204,204), (0,102,204),
        (0,0,204), (102,0,204), (204,0,204),
        (102,102,102), (255,153,153), (255,204,153),
        (153,255,153), (153,255,153), (153,255,255),
        (153,204,255), (153,153,255), (204,153,255),
        (192,192,192),
        (255,51,153), (153,255,51), (255,255,255) ]


def fill_isocright(surf, col, (x,y), r, dim):
    triangle = [(x-.5*r,y-.5*r), (x,y), (x+.5*r,y-.5*r)]
    triangle = [pix(x,y,dim) for (x,y) in triangle]
    pg.draw.polygon(surf,col,triangle,0)

def fill_arc(surf, col, (x,y), r, t1, t2, dim):
    fill_regpoly(surf,col,(x,y),r,1000,t1,t2,dim)

def fill_regpoly(surf, col, (x,y), r, n, t1, t2, dim):
    ang = [t1+(t2-t1)*i/(n-1) for i in xrange(n)]
    v = [(x+r*cos(i),y+r*sin(i)) for i in ang]
    v = [pix(x,y,dim) for (x,y) in v]
    pg.draw.polygon(surf,col,v,0)

def pix(x,y,(xdim,ydim)):
    return (int(xdim/2+x*xdim), int(ydim/2-y*ydim))



class Display:
    def __init__(self, w,h):
        PG.init()
        PG.font.init()
        self.myfont = PG.font.SysFont("monospace", 24, True)
        self.screen = PG.display.set_mode((w,h),HWSURFACE|DOUBLEBUF|RESIZABLE)
        self.screen.fill(white)

    def alive(self, event_function):
        event = PG.event.poll()
        if event.type == QUIT:
            return False
        elif event.type == PG.KEYDOWN and event.key == PG.K_ESCAPE:
            return False
        elif event.type == VIDEORESIZE:
            dim = min(event.dict['size'])/18
            self.screen = PG.display.set_mode((dim*18,dim*18),HWSURFACE|DOUBLEBUF|RESIZABLE)
            return True
        event_function(event)
        return True

    def show(self):
        self.screen.fill(white)
        label = self.myfont.render('Time: {:.2f} '.format(PG.time.get_ticks()/1000.0), 1, black)
        self.screen.blit(label,(5,5))
        PG.display.flip()




