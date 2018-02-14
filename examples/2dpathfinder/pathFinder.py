import random
import yaastar

class SimpleMap(yaastar.Map):
    def __init__(self, filename):
        self.fstrings = open(filename).read().split("\n")
        self.xmax = max([len(i) for i in self.fstrings])
        self.ymax = len(self.fstrings)
        self.emptyChars = " .SG"
    
    def aprint(self):
        print " |"+"".join([str(i%10) for i in range(self.xmax)])+"| "
        print "--"+"-"*self.xmax
        for i,j in enumerate(self.fstrings):
            print "%d|%s|%d"%(i%10, j, i%10)
        print "--"+"-"*self.xmax
        print " |"+"".join([str(i%10) for i in range(self.xmax)])+"| "
    
    def heuristic_estimate_of_distance(self, start, goal):
        return self.dist_between(start, goal)

    def neighbor_nodes(self, x):
        
        offsets = [ (i,j) for i in range(3) for j in range(3) ]
        offsets.remove((1,1))
        
        for oi,oj in offsets:
            i = x[0] -1 + oi
            j = x[1] -1 + oj
            if j < 0 or j >= len(self.fstrings):
                continue
            if i < 0 or i >= len(self.fstrings[j]):
                continue
            
            if self.fstrings[j][i] in self.emptyChars:
                yield (i,j)
            

    def dist_between(self, start, goal):
        assert len(start) == len(goal)
        l = len(goal)
        return ( sum([(start[i] - goal[i]) ** 2 for i in range(l)]) ) ** 0.5 

        
    def mark(self,(i,j), mark):
        try:
            line = [c for c in self.fstrings[j]]
            line[i] = mark
            self.fstrings[j] = "".join(line)
        except IndexError:
            pass



def createPathPicture(path,allpaths,updateset, name):
        from PIL import Image
        from PIL import ImageDraw
        im = Image.new('RGB',((a_map.xmax+1) * 20, (a_map.ymax+1) * 20) )
        draw = ImageDraw.Draw(im)

        totuple = lambda p: tuple([ip*20 +10 for ip in p])

        for t in allpaths:
            draw.line(totuple([i for p in [t,allpaths[t]] for i in p]), fill=(0,0,100))

        draw.line(totuple([i for p in path for i in p]), fill=(0,100,0))

        for t, f in updateset:
            draw.line(totuple([i for p in [t,f] for i in p]), fill=(100,0,0))

        im.save(name+".gif", "GIF")


if __name__ == "__main__":
    iteration = 0
    while True:
        filename = raw_input("mapfile: ")
        print
        
        a_map = SimpleMap(filename)
        a_map.aprint()
        
        si = int(raw_input("start x: "))
        sj = int(raw_input("start y: "))

        gi = int(raw_input("goal x: "))
        gj = int(raw_input("goal y: "))
        print

        start = (si,sj)
        goal = (gi,gj)
        
        print "-"* 60
        path, allpaths, updateset = yaastar.a_star(start,goal,a_map)

        for x in path:
            a_map.mark(x,'x')
        print "-"* 60

        createPathPicture(path,allpaths,updateset, "paths-%d"%iteration )
        
        a_map.mark(start, 'S')
        a_map.mark(goal, 'G')
        a_map.aprint()
        iteration += 1
