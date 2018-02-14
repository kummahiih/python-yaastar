import re
import yaastar
import copy


"""
class Map:
    def __init__(self):
        pass
    def heuristic_estimate_of_distance(self, start,goal):
        raise NotImplemented
    def neighbor_nodes(self, x):
        raise NotImplemented

    def dist_between(self, x, y):
        raise NotImplemented
"""

class PuzzleMap(yaastar.Map):
    def __init__(self, filename,holeNmbr):
        self.filename = filename
        self.holeNmbr = int(holeNmbr)
        self.fstring = open(filename).read()
        self.boxre = r"[ \d][\d]"
        self.linere = self.boxre*3+"\n"
        self.puzzleRe = self.linere*4
        if not re.match(self.puzzleRe, self.fstring):
            raise ValueError(
                "the file %s did not match %s"%(filename,self.puzzleRe))
        self.numbers = [int(i) for i in re.findall(self.boxre, self.fstring)]
        if set(self.numbers) != set( [ i for i in range(4*3)] ):
            raise ValueError("numbers not right")
        self.numbers = tuple([ tuple([self.numbers[i+j*3] for i in range(3)]) for j in range(4) ])
        self.goal = tuple([ tuple([i+j*3 for i in range(3)]) for j in range(4) ])

    def aprint(self,kk=None):
        if kk== None:
            kk = self.numbers
        print("  |"+ "|".join(["%02d"%i for i in range(3)])+"| ")
        print("--|"+"--|"*3)
        for i,j in enumerate(kk):
            print("%02d|%s|"%(i, "|".join(["%02d"%k for k in j])))
    
    def heuristic_estimate_of_distance(self, start, goal):
        posdict = dict([
                (start[j][i],(i,j)) for i in range(3) for j in range(4) 
                ])
                
        def dist(a, b):
            i1, j1 = a
            i2, j2 = b
            return ((i1-i2)**2 + (j1-j2)**2)**0.5
            
        distance = sum([
                dist(posdict[goal[j][i]], (i,j)) for i in range(3) for j in range(4)
                ])
        
        return distance

    def neighbor_nodes(self, x):
        
        offsets = [ [-1,0],[1,0],[0,-1],[0,1]]
        #TODO!!11!!!11
        
        
        def gethole():
            for i1 in range(3):
                for j1 in range(4):
                    if x[j1][i1] == self.holeNmbr:
                        #print x[j1][i1],i1,j1
                        return i1,j1
        i1,j1 = gethole()

        def swapncopy(xxx_todo_changeme,res):
            (i2,j2) = xxx_todo_changeme
            if i2 < 0 or j2 < 0:
                #print "raised"
                raise IndexError("noworries")
            #res = copy.deepcopy(s)
            #!"#!#"!"#11111
            res = list([list(j) for j in res])
            t = res[j1][i1]
            res[j1][i1] = res[j2][i2]
            res[j2][i2] = t
            #TODO!!111
            return tuple([tuple(j) for j in res])
        
        for oi,oj in offsets:
            try:
                kkkk = swapncopy((i1+oi,j1+oj),x)
                #print x,"||||", kkkk,i1+oi,j1+oj, i1,oi,j1,oj 
                yield kkkk 
            except IndexError:
                #print "indexerror",i1+oi,j1+oj, i1,oi,j1,oj 
                pass
        #print "--"
            
    def dist_between(self, start, goal):
        return 1

        

if __name__ == "__main__":
    while True:
        print("")
        filename = input("puzzlefile:")
        holenmbr = input("holenumber")
        print("")
        k = PuzzleMap(filename, holenmbr)
        k.aprint()
        situations = yaastar.a_star(k.numbers,k.goal,k)[0]
        if len(situations) == 0:
            situations = [k.numbers]
        for i,situation in enumerate(situations):
            if len(situation) == 0:
                break
            print("-"*60)
            print(i)
            #TODO ...
            k.numbers = situation
            k.aprint()
    
