from math import inf, ceil, cos, acos, floor
from typing import List

# constants as stated in TSPlib doc
# https://www.iwr.uni-heidelberg.de/groups/comopt/software/TSPLIB95/tsp95.pdf
PI = 3.141592
RRR = 6378.388

class TSPData:
    """Reads instances from the Traveling Salesman Problem
    
    Right now only supports instances containing geographical coordinates 
    
    Attributes:
    
        n (int): number of cities
        d (List[List[int]]): distance matrix
    
    """
    def __init__(self, fileName : str):
        self.name = ''
        
        self.n = 0 
        
        self.d = None
        
        self.latitude : List[float] = []
        
        self.longitude : List[float] = []
        
        readingCoord = False
        
        self.x : List[float] = []
        self.y : List[float] = []
        
        f=open(fileName, 'r')
        for l in f:
            if ':' in l:
                vls = l.split(':')
                fn = vls[0].lower()
                fv = vls[1]
                if fn == 'name':
                    self.name = fv.strip()
                elif fn == 'dimension':
                    self.n = int(fv.strip())
                    self.d = [[inf for i in range(self.n)] for j in range(self.n)]
                    self.latitude = [0 for i in range(self.n)]
                    self.longitude = [0 for i in range(self.n)]
            elif 'NODE_COORD_SECTION' in l:
                readingCoord = True
            elif readingCoord:
                l = l.lstrip().rstrip().lower()
                if 'eof' in l:
                    break                
                vls = l.split(' ')
                i = int(vls[0])
                cx = float(vls[1])
                cy = float(vls[2])
                self.x.append( cx )
                self.y.append( cy )

        for i in range(self.n):
            deg = floor( self.x[i] )
            vmin = self.x[i] - deg
            self.latitude[i] = PI * (deg + 5.0 * vmin / 3.0 ) / 180.0
            deg = floor( self.y[i] )
            vmin = self.y[i] - deg
            self.longitude[i] = PI * (deg + 5.0 * vmin / 3.0 ) / 180.0

        for i in range(self.n):
            self.d[i][i] = 0
            for j in range(0, self.n):
                q1 = cos( self.longitude[i] - self.longitude[j] )
                q2 = cos( self.latitude[i] - self.latitude[j] )
                q3 = cos( self.latitude[i] + self.latitude[j] )
                self.d[i][j] = int(floor(RRR*acos(0.5*((1.0+q1)*q2-(1.0-q1)*q3))+1.0)) 
