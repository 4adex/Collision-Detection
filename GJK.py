import numpy as np
ORIGIN = np.array([0,0,0])

                
def normalize(x):
    return x/np.sqrt((x**2).sum())      

def triplep(a,b,c):
    return np.cross(np.cross(a,b),c)


def support(s1,s2,d):
    return s1.furthest(d)-s2.furthest(-d)


def handlesimplex(simplex,d):
    if len(simplex)==2:
        return LineCase(simplex,d)
    return TriangleCase(simplex,d)

def LineCase(simplex,d):
    B,A = simplex
    AB,AO = normalize(B-A),normalize(ORIGIN-A)
    ABperp = triplep(AB,AO,AB)
    d[:] = ABperp
    return False

def TriangleCase(simplex,d):
    C,B,A = simplex
    AB,AC,AO = normalize(B-A),normalize(C-A),normalize(ORIGIN-A)
    ABperp = triplep(AC,AB,AB)
    ACperp = triplep(AB,AC,AC)
    if np.dot(ABperp,AO)>0:
        simplex[:] = [s.tolist() for s in simplex]
        simplex.remove(C.tolist())
        simplex[:] = [np.array(s) for s in simplex]
        d[:] = ABperp
        return False
    elif np.dot(ACperp,AO)>0:
        simplex[:] = [s.tolist() for s in simplex]
        simplex.remove(B.tolist())
        simplex[:] = [np.array(s) for s in simplex]
        d[:] = ACperp
        return False
    return True

def GJK(s1,s2):
    d = s1.centroid()-s2.centroid()
    simplex = [normalize(support(s1,s2,d))]
    d = ORIGIN - simplex[0]
    while True:
        A = normalize(support(s1,s2,d))
        if A.dot(d)<0:
            return False
        simplex.append(A)
        if handlesimplex(simplex,d):
            return True
        