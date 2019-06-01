import matplotlib.pyplot as plt
import math as m
import random as rd
import time
import sys

def B_MINIDISK_FRONT(P,R):
    '''Renvoie le plus petit cercle contenant l'ensemble de points R avec
    l'ensemble de points R à son bord'''
    if len(P) == 0 or len(R) == 3:
        cercle = b_mdmax3(R)
    else:
        p = P[0]
        cercle = B_MINIDISK_FRONT(P[1:], R)
        if not est_dans(p,cercle):
            cercle = B_MINIDISK_FRONT(P[1:], [p]+R)
    return cercle

def b_mdmax3(R):
    '''Renvoie le plus petit cercle contenant l'ensemble de points R,
    R contenant au maximum 3 points'''
    if len(R) == 0:
        centre = "tous les points"
        rayon = 0
    elif len(R) == 1:
        centre = R[0]
        rayon = 0
    elif len(R) == 2:
        centre = ((R[0][0]+R[1][0])/2, (R[0][1]+R[1][1])/2)
        rayon = m.sqrt((R[0][0]-centre[0])**2+(R[0][1]-centre[1])**2)
    else:
        for i in range(len(R)):
            cercle = b_mdmax3(R[:i]+R[i+1:])
            if est_dans(R[i],cercle):
                return cercle
        centre, rayon = cercleCirconscrit(R[0],R[1],R[2])
    return (centre,rayon)

def cercleCirconscrit(pA,pB,pC):
    '''Renvoie les coordonnées du centre et le rayon du cercle passant par les trois points'''
    xa, ya = pA
    xb, yb = pB
    xc, yc = pC
    xm1 = (xb + xa)/2
    ym1 = (yb + ya)/2
    xm2 = (xc + xb)/2
    ym2 = (yc + yb)/2
    xVm1 = yb-ya
    yVm1 = xa-xb
    xVm2 = yc-yb
    yVm2 = xb-xc
    k2 = (yVm1*xm1-xVm1*ym1-xm2*yVm1+ym2*xVm1)/(xVm2*yVm1-xVm1*yVm2)
    xC = xm2 + k2*xVm2
    yC = ym2 + k2*yVm2
    R = ((xC-xa)**2 + (yC-ya)**2)**(1/2)
    return (((xC,yC),R))

def est_dans(p,cercle):
    '''Renvoie True si p est dans le cercle, False sinon'''
    centre, rayon = cercle
    if centre == "tous les points":
        return False
    if rayon == 0:
        return p == centre
    distance = m.sqrt((p[0]-centre[0])**2+(p[1]-centre[1])**2)
    return distance <= rayon

def est_sur(p,cercle):
    '''Renvoie True si p est dans le cercle, False sinon'''
    centre, rayon = cercle
    if centre == "tous les points":
        return False
    if rayon == 0:
        return p == centre
    distance = m.sqrt((p[0]-centre[0])**2+(p[1]-centre[1])**2)
    return distance == rayon

def aff_points(P):
    '''Permet l'affichage des points de P'''
    x, y = [], []
    for i in range(len(P)):
        x.append(P[i][0])
        y.append(P[i][1])
    plt.scatter(x,y)

def aff_convex_hull(convex_hull):
    '''Permet l'affichage de convex_hull'''
    x = []
    y = []
    for i in range(len(convex_hull)):
        x.append(convex_hull[i][0])
        y.append(convex_hull[i][1])
    x.append(convex_hull[0][0])
    y.append(convex_hull[0][1])
    plt.plot(x, y, linewidth=1)

def aff_circle(centre, rayon):
    '''Prépare l'affichage du cercle de centre centre et de rayon rayon'''
    if centre == "tous les points":
        return
    circ = plt.Circle(centre,radius = rayon, color='b', fill=False)
    ax=plt.gca()
    ax.add_patch(circ)
    plt.axis('scaled')

def produit_vectoriel(a,b,c):
    '''Produit vectoriel ac^ab
    > 0 si a,b,c sont dans le sens horaire
    '''
    return ((b[1]-a[1]) * (c[0]-a[0]) - (b[0]-a[0])*(c[1]-a[1]))

def sort_points(P):
    '''Fonction qui prend le point d'abscisse la plus faible et trie le reste du tableau en fonction de l'angle par rapport a ce dernier'''
    def angle(y):
        '''coefficient directeur de la droite entre deux points'''
        x = P[0]
        if ((y[0]-x[0])==0):
            if (y[1]>x[1]):
                return m.inf
            else:
                return -m.inf
        return((y[1]-x[1])/(y[0]-x[0]))
    P=sorted(P, key = lambda x:x[1])
    P=sorted(P, key = lambda x:x[0])
    P = P[:1] + sorted(P[1:], key = angle)
    return (P)

def graham_scan(P):
    '''Implementation de l'algorithme du parcours de Graham'''
    convex_hull =[]
    sorted_points = sort_points(P)
    for p in sorted_points:
        while len(convex_hull)> 1 and produit_vectoriel(convex_hull[-2],convex_hull[-1],p)>=0:
            convex_hull.pop()
        convex_hull.append(p)
    return convex_hull

def find_farthest(point, P):
    '''Détermine le point le plus éloigné parmi un ensemble de points pour un point donné'''
    dist_max = 0
    farthest = point
    for i in range(len(P)):
        distance = m.sqrt((point[0]-P[i][0])**2+(point[1]-P[i][1])**2)
        if distance > dist_max:
            dist_max= distance
            farthest = P[i]
    #aff_circle((0,0),dist_max)
    return farthest

def draw_circle(centre, rayon):
    #farthest = find_farthest((0,0),S)
    aff_circle((centre[0],centre[1]),rayon)

def distance_points(a,b):
    return m.sqrt((a[0]-b[0])**2+(a[1]-b[1])**2)

def optimal_core_set(P, epsilon):
    #Pick an arbitrary subset S ⊂ P of size ⌈1/ε⌉
    S = []
    P_copy = list(P)
    for i in range(int(1/epsilon)):
        S.append(P_copy.pop(rd.randint(0,len(P_copy)-1)))

    while (True):
        print("S = ",S)
        cercleS = B_MINIDISK_FRONT(S,[])
        #find the point a of P the farthest from cs
        a = find_farthest(cercleS[0], P)
        # let Sa := S ∪ {a}
        Sa = list(S)
        Sa.append(a)
        #some point b ∈ Sa
        b =Sa[rd.randint(0,len(Sa)-1)]
        #b=Sa[0]

        BSa = B_MINIDISK_FRONT(Sa,[])
        #if b is contained in the interior of B(Sa),
        SaWithoutb=list()
        if(not est_sur(b,BSa)):
            #let Sa\b := Sa\{b}
            SaWithoutb = list(Sa)
            SaWithoutb.remove(b)
        #otherwise, find the facet F of conv Sa with the largest circumscribed ball
        else:
            convex_hull = graham_scan(Sa)
            F = list()
            distance_max=0
            for j in range(len(convex_hull)-1):
                uneDistance = (distance_points(convex_hull[j],convex_hull[j+1]))
                if uneDistance > distance_max :
                    F=list()
                    F.append(convex_hull[j])
                    F.append(convex_hull[j+1])
                    distance_max = uneDistance
            # and let Sa\b denote the vertex set of F ;
            SaWithoutb = list(F)

        BSaWithoutb = B_MINIDISK_FRONT(SaWithoutb,[])
        #rSa\b 􏰋<= rS?
        if (BSaWithoutb[1]<=cercleS[1]):
            #return S as an ε-core-set
            print("fin avec S = ", S)
            break
        else :
            #otherwise set S:=Sa\b, and repeat these steps.
            S = list(SaWithoutb)

    solution = B_MINIDISK_FRONT(S,[])
    draw_circle(solution[0],solution[1])
    aff_points(P)
    aff_convex_hull(graham_scan(S))
    plt.show()

epsilon = 0.01
P = []
nb = 10000
# On cree une liste de points de manière aléatoire
for i in range(nb):
    P.append((round(rd.gauss(0,1),2),round(rd.gauss(0,1),2)))

t1 = time.time()
sys.setrecursionlimit(nb+10)
optimal_core_set(P, epsilon)
