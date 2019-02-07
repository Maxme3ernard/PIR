import math
import random
import matplotlib.pyplot as plt

def cercles2(p1,p2):
    o=[(p1[0]+p2[0])/2,(p1[1]+p2[1])/2]
    r=math.sqrt((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)/2
    return o,r

def estDansCercle(p,c):
    if ((p[0]-c[0][0])**2)+((p[1]-c[0][1])**2)<=c[1]**2:
        return True
    else:
        return False

def contientPoints(cercle,points):
    for i in range(len(points)):
        if not estDansCercle(points[i],cercle):
            return False
    return True

def selectionnerCercle(cercles,points):
    c=[0,2**16]
    for i in range(len(cercles)):
        if cercles[i][1]<c[1] and contientPoints(cercles[i],points):
            c=cercles[i]
    return c

def afficher(x,y,cercle):
    circle = plt.Circle(cercle[0], cercle[1], fill=False)
    ax = plt.gca()
    ax.add_patch(circle)
    plt.axis('scaled')
    plt.scatter(x, y)
    plt.show()

if __name__ == '__main__':
    n=20
    points=[]
    cercles=[]
    x=[]
    y=[]

    for i in range(n):
        points.append([20*random.random()-10,20*random.random()-10])

    for i in range(len(points)):
        x.append(points[i][0])
        y.append(points[i][1])
        for j in range (i+1,len(points)):
            cercles.append(cercles2(points[i],points[j]))

    ppetitCercle=selectionnerCercle(cercles,points)
    print(ppetitCercle)
    afficher(x,y,ppetitCercle)
