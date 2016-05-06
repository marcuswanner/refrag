import sys, curses, time, random, enum
from curses import wrapper

inf = open(sys.argv[1], 'r')
log = open("fraglog", 'w')
dg = lambda s: [log.write(s+"\n"), log.flush()] #lolhaxx
tick = lambda t: time.sleep(0.02/d.gettexty()*t)

# change/override this method to accomodate different input formats
def readone():
    while 1:
        l = inf.readline()
        if not l:
            dg("finished reading file")
            return None
        info = l.strip().split()
        try:
            t = getattr(Access.Type, info[0])
            break
        except AttributeError as e:
            dg("not recognized: \"{}\" ({})".format(l.strip(), e))
    pos, size = map(int, [info[1], info[2]])
    return Access(pos, size, l, t)

class Access():
    class Type(enum.Enum):
        WRITE = 0
        READ = 1
        FREE = 2

    typechars = {
            Type.WRITE: "w",
            Type.READ: "r",
            Type.FREE: "#"}

    def __init__(self, *args):
        self.pos, self.length, self.raw, self.type = args
        self.c = None
        self.num = d.accesscounter()

    def tryaddstr(self, *args):
        try:
            d.win.addstr(*args)
        except curses.error:
            pass
            #dg("failed to draw " + str(args))

    def mkchar(self, loc):
        if not self.c:
            self.c = d.randomcolor()
        if loc in [self.pos, self.pos+1] and self.type != self.Type.FREE:
            char = "L"
            col = 1
        else:
            char = self.typechars[self.type]
            col = self.c
        return (char, curses.color_pair(col))

    def draw(self):
        d.map(self.pos+self.length-1) #make sure we don't draw over the string we're about to add
        self.tryaddstr(d.gettexty(), 0, str(self.num) + ": " + self.raw)
        dg("drawing block [{},{}] {}".format(self.pos, self.pos+self.length-1, self.type))
        for loc in range(self.pos, self.pos+self.length):
            self.tryaddstr(*d.map(loc), "#", curses.color_pair(1))
            d.win.refresh()
            tick(1)
            self.tryaddstr(*d.map(loc), *self.mkchar(loc))
            d.win.refresh()
        tick(20)
        try:
            d.win.move(d.gettexty(), 0)
            for i in range(len(self.raw.split("\n"))):
                d.win.deleteln()
        except curses.error:
            pass


class Display():
    def __init__(self):
        #self.win lazy init so it's after curses init
        self.win = None
        self.colors = 0
        self.maxy = 0
        self.width = 0
        self.acount = 0

    #map access location to (y,x) coords
    def map(self, a):
        if not self.width:
            width = 1
            while width*2 < d.win.getmaxyx()[1]:
                width *= 2
            self.width = width
            dg("set screen width to {} of {} chars".format(width, d.win.getmaxyx()[1]))
        y = int(a / self.width)
        x = (a % self.width)
        if y > self.maxy:
            self.maxy = y
        return (y, x)

    def randomcolor(self):
        if self.colors == 0:
            for a in dir(curses):
                if a.startswith("COLOR_") and not a in ["COLOR_PAIRS", "COLOR_BLACK"]:
                    self.colors += 1
                    curses.init_pair(self.colors, getattr(curses, a), curses.COLOR_BLACK)
        return random.randint(1, self.colors)

    def gettexty(self):
        return self.maxy + 1

    def accesscounter(self):
        self.acount += 1
        return self.acount


def main(stdscr):
    dg("-----------------")
    d.win = stdscr
    while 1:
        a = readone()
        if not a:
            break
        a.draw()
    while 1: pass

d = Display()
wrapper(main)
