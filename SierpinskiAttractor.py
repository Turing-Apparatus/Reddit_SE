from random import random, randint
from pygame.locals import *
import pygame as PG

orange  = (255,150,50)
blue    = (0,80,120)
yellow  = (255,255,80)
purple  = (75,10,140)
green   = (0,140,70)
red     = (255,0,0)

def pix((x,y)): return (int(dim[0]*x), int(dim[1]*(1-y)))
def avg(p1,p2): return ((p1[0]+p2[0])/2, (p1[1]+p2[1])/2)

P = [(0,0),(.35,0),(1,0),(1,1),(.25,1),(0,1),(0,.4),(.675,.5)]
T = [   (P[0],P[1],P[6]), (P[1],P[2],P[7]), (P[2],P[3],P[7]),
        (P[3],P[4],P[6]), (P[4],P[5],P[6]), (P[1],P[3],P[6])]
C = [yellow, purple, red, blue, orange, green]
X = [(.5,.5)]*len(T)

PG.init()
dim = (600,600)
canvas = PG.display.set_mode(dim)

while True:
    if PG.QUIT in [e.type for e in PG.event.get()]: break
    for i in xrange(len(X)):
        for j in xrange(100):
            PG.draw.circle(canvas, C[i], pix(X[i]), 0)
            X[i] = avg(X[i],T[i][randint(0,2)])
    PG.display.flip()