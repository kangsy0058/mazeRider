class Tree:
    def __init__(self, parent = None, y = 0, x = 0, bfdir= None):
        self.parent = parent
        self.Y = y
        self.X = x
        self.Fleft = False
        self.Ffront = False
        self.Fright = False
        self.dist = 0
        self.dir = None
        self.bfDir = bfdir
        self.cornerlist = list()

    def isblock(self):
        if self.Fleft == False and self.Ffront == False and self.Fright == False:
            return True
        else:
            return False



class Maze:
    def __init__(self, mazearray = list()):
        self.maze = mazearray

        self.playerYX = [0,0]
        self.goalYX = [len(self.maze)-1, len(self.maze[0])-1]
        self.maze[self.goalYX[0]][self.goalYX[1]] = 4
        self.playerDirection = 0
        self.playerCursor = '>'

        self.printMaze()


    def setCursor(self):

        cursors = {0:'>', 1:'v', 2:'<', 3:'^'}

        self.playerCursor = cursors[self.playerDirection]


    def movePlayer(self, move):
        key = move
        score = 0
        state = False
        y,x = self.playerYX

        if key == 'w':
            if self.maze[y-1][x] == 0 or self.maze[y-1][x] == 3 :
                self.playerYX[0] -=1
                score = -0.1 / (len(self.maze) * len(self.maze[y]))
                state = False
                self.playerDirection = 3
            elif self.maze[y-1][x] == 4:
                self.playerYX[0] -= 1
                score = 10
                state = True

        elif key == 's':
            if self.maze[y+1][x] == 0 or self.maze[y+1][x] == 3 :
                self.playerYX[0] +=1
                score = -0.1 / (len(self.maze) * len(self.maze[y]))
                state = False
                self.playerDirection = 1
            elif self.maze[y+1][x] == 4:
                self.playerYX[0] += 1
                score = 10
                state = True

        elif key == 'a':
            if self.maze[y][x-1] == 0 or self.maze[y][x-1] == 3 :
                self.playerYX[1] -=1
                score = -0.1 / (len(self.maze) * len(self.maze[y]))
                state = False
                self.playerDirection = 2
            elif self.maze[y][x-1] == 4:
                self.playerYX[1] -= 1
                score = 10
                state = True

        elif key == 'd':
            if self.maze[y][x+1] == 0 or self.maze[y][x+1] == 3 :
                self.playerYX[1] +=1
                score =  -0.1 / (len(self.maze) * len(self.maze[y]))
                state = False
                self.playerDirection = 0

            elif self.maze[y][x+1] == 4:
                self.playerYX[1] += 1
                score = 10
                state = True 

        self.setCursor()
        return state

    def printMaze(self):
        for y in range(len(self.maze)):
            for x in range(len(self.maze[y])):
                if y == self.playerYX[0] and x == self.playerYX[1]:
                    print(self.playerCursor, end='')
                else:
                    print(self.maze[y][x], end='')
            print()

    def playerhand(self):
        Y, X =self.playerYX
        if self.playerDirection == 0:
            return [Y-1,X], [Y,X+1], [Y+1,X]
        elif self.playerDirection == 1:
            return [Y,X+1], [Y+1,X], [Y,X-1]
        elif self.playerDirection == 2:
            return [Y+1,X], [Y,X-1], [Y-1,X]
        else:
            return [Y, X -1], [Y - 1, X], [Y, X + 1]

    def man(self, y, x):
        ydist = self.goalYX[0] - y
        xdist = self.goalYX[1] - x

        return xdist+ydist

    def pathMaker(self,node = Tree()):
        pa = list()
        count = 1

        while not(node == None):
            node.cornerlist.reverse()
            if len(node.cornerlist) > 0:
                for i in node.cornerlist:
                    pa.append(i)

            pa.append(node.dir)

            self.maze[node.Y][node.X] = count
            node = node.parent
            count +=1

        pa.pop()
        pa.reverse()
        #self.printMaze()
        go = list()
        maind = {'left': 'l', 'front': 'f', 'right': 'r'}
        for i in pa:
            go.append(maind[i])
        return go

    def findpath(self):
        sw = False
        dir = {0: 'd', 1: 's', 2: 'a', 3: 'w'}
        root = Tree(y=self.playerYX[0], x=self.playerYX[1])
        root.Ffront = 10
        node = Pnode = root
        dist = 0

        while True:
            # print(f'y:{self.playerYX[0]} x:{self.playerYX[1]}')
            # print(f'node X :{node.X} node.Y :{node.Y} node dir {node.dir} node bfdir :{node.bfDir}')

            # go = False
            # print('direction = ', self.playerDirection)
            left, front, right = self.playerhand()
            if front[0] >= len(self.maze):
                left_stat, right_stat = self.maze[left[0]][left[1]], self.maze[right[0]][right[1]]
                front_stat = 1
            elif front[1] >= len(self.maze[0]):
                left_stat = self.maze[left[0]][left[1]]
                front_stat = 1
                right_stat = 1
            elif right[0] >= len(self.maze):
                left_stat, front_stat = self.maze[left[0]][left[1]], self.maze[front[0]][front[1]]
                right_stat = 1
            else:
                left_stat, front_stat, right_stat = self.maze[left[0]][left[1]], self.maze[front[0]][front[1]], self.maze[right[0]][right[1]]

            if self.playerYX[0] == 0:
                left_stat = 1

            if front_stat == 4:
                front_stat = 0

            # print(f'leftS = {left_stat} frontS = {front_stat} rightS = {right_stat}')
            if sw:
                return self.pathMaker(node)

            elif node.isblock():
                Pnode = node = node.parent
                if node.dir == 'left':
                    node.Fleft = False

                elif node.dir == 'front':
                    node.Ffront = False

                elif node.dir == 'right':
                    node.Fright = False
                dist = node.dist

            elif left_stat == 1 and right_stat == 1 and front_stat == 0:
                # print(1)
                sw = self.movePlayer(dir[self.playerDirection])
                dist+=1
                # print('go')
                go = False

            elif front_stat == 1 and right_stat == 0 and left_stat == 1:
                # print(2)
                self.playerDirection = (self.playerDirection + 1) % 4
                sw = self.movePlayer(dir[self.playerDirection])
                dist +=1
                node.cornerlist.append('right')

            elif front_stat == 1 and right_stat == 1 and left_stat == 0:
                # print(3)
                self.playerDirection = (self.playerDirection - 1) % 4
                sw = self.movePlayer(dir[self.playerDirection])
                dist+=1
                node.cornerlist.append('left')

            elif front_stat == 1 and right_stat == 1 and left_stat == 1:
                # print(4)

                if sw:
                    return self.pathMaker(node)

                if node.dir == 'left':
                    node.Fleft = False

                elif node.dir == 'front':
                    node.Ffront = False

                elif node.dir == 'right':
                    node.Fright = False

                self.playerYX = [node.Y, node.X]
                self.playerDirection = node.bfDir
                node.cornerlist = list()

                if node.Fleft > node.Ffront:
                    #print('left > front')
                    if node.Fleft > node.Fright:
                        #print('left > right')
                        self.playerDirection = (self.playerDirection - 1) % 4
                        sw = self.movePlayer(dir[self.playerDirection])
                        dist += 1
                        node.dir = 'left'


                    else:
                        self.playerDirection = (self.playerDirection + 1) % 4
                        sw = self.movePlayer(dir[self.playerDirection])
                        dist += 1
                        node.dir = 'right'


                elif node.Ffront > node.Fright:
                    #print('front > *')
                    #print(dir[self.playerDirection])
                    sw = self.movePlayer(move=dir[self.playerDirection])
                    dist += 1
                    node.dir = 'front'


                else:
                    #print('right > *')
                    self.playerDirection = (self.playerDirection + 1) % 4
                    sw = self.movePlayer(dir[self.playerDirection])
                    dist += 1
                    node.dir = 'right'




            else:
                #print(5,self.playerDirection)
                node = Tree(parent=Pnode, y = self.playerYX[0], x = self.playerYX[1], bfdir= self.playerDirection)
                Pnode = node
                node.dist = dist
                #print(f'else leftS = {left_stat} frontS = {front_stat} rightS = {right_stat}')
                if left_stat == 0:
                    #print('left')
                    node.Fleft = node.dist + self.man(left[0],left[1])

                if front_stat == 0:
                    #print('front')
                    node.Ffront = node.dist + self.man(front[0],front[1])

                if right_stat == 0:
                    #print('right')
                    node.Fright = node.dist + self.man(right[0],right[1])

                if node.Fleft > node.Ffront:
                    #print('left > front')
                    if node.Fleft > node.Fright:
                        #print('left > right')
                        self.playerDirection = (self.playerDirection - 1) % 4
                        sw = self.movePlayer(dir[self.playerDirection])
                        dist += 1
                        node.dir = 'left'

                    else:
                        self.playerDirection = (self.playerDirection + 1) % 4
                        sw = self.movePlayer(dir[self.playerDirection])
                        dist += 1
                        node.dir = 'right'

                elif node.Ffront > node.Fright:
                    #print('front > *')
                    #print(dir[self.playerDirection])
                    sw = self.movePlayer(move=dir[self.playerDirection])
                    dist += 1
                    node.dir = 'front'

                else:
                    #print('right > *')
                    self.playerDirection = (self.playerDirection + 1) % 4
                    sw = self.movePlayer(dir[self.playerDirection])
                    dist += 1
                    node.dir = 'right'

           # if go:
           #     self.printMaze()

