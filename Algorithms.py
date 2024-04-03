from pyamaze import maze,agent,COLOR,textLabel
from queue import PriorityQueue
import time

def BFS(m,start,goal):
    v = []
    q = []

    v.append(start)
    q.append(start)

    bfsPath={}
    bSearch=[]

    while q:
        if q[0] is goal:
            break

        vertex= q.pop(0)
        if vertex not in v:
            v.append(vertex)

        for child in 'ESNW':
            if m.maze_map[vertex][child]==True:
                if child=='E':
                    childCell=(vertex[0],vertex[1]+1)
                elif child=='W':
                    childCell=(vertex[0],vertex[1]-1)
                elif child=='N':
                    childCell=(vertex[0]-1,vertex[1])
                elif child=='S':
                    childCell=(vertex[0]+1,vertex[1])
  
                if childCell not in v:
                    q.append(childCell)
                    v.append(childCell)
                    bfsPath[childCell]=vertex
                    bSearch.append(childCell)
    fwdPath={}
    cell=goal
    while cell!=start:
        fwdPath[bfsPath[cell]]=cell
        cell=bfsPath[cell]
    return bSearch,bfsPath,fwdPath

def DFS(m,start,goal):
    v = []
    s = []
    v.append(start)
    s.append(start)
    dfsPath={}
    dSeacrh=[]
    p=[]
    while s:
        vertex=s[-1]
        dSeacrh.append(vertex)
        if vertex==goal:
            break
        if vertex not in v:
            v.append(vertex)
        
        poss=0
        for child in 'ESNW':
            if m.maze_map[vertex][child]==True:
                if child=='E':
                    childCell=(vertex[0],vertex[1]+1)
                elif child=='W':
                    childCell=(vertex[0],vertex[1]-1)
                elif child=='S':
                    childCell=(vertex[0]+1,vertex[1])
                elif child=='N':
                    childCell=(vertex[0]-1,vertex[1])
                if childCell in v:
                    continue
                poss+=1
                v.append(childCell)
                s.append(childCell)
                dfsPath[childCell]=vertex

        if poss>1:
            m.markCells.append(vertex)   
            p.append(vertex)  

    fwdPath={}
    while goal!=start:
        fwdPath[dfsPath[goal]]=goal
        goal=dfsPath[goal]
    return dSeacrh,dfsPath,fwdPath,p


def h(cell1):
    x1,y1=cell1
    x2,y2=goal
    return abs(x1-x2) + abs(y1-y2)

def aStar(m,start, goal):
    cost={cell:float('inf') for cell in m.grid}
    cost[start]=0
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start)

    p_q=PriorityQueue()
    p_q.put((h(start),h(start),start))
    aPath={}
    searchPath=[start]

    while not p_q.empty():
        currCell=p_q.get()[2]
        searchPath.append(currCell)

        if currCell==goal:
            break
        for next_node in 'ESNW':
            if m.maze_map[currCell][next_node]==True:
                if next_node=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if next_node=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if next_node=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if next_node=='S':
                    childCell=(currCell[0]+1,currCell[1])

                current_cost=cost[currCell]+1
                temp_f_score=current_cost+h(childCell)

                if temp_f_score < f_score[childCell]:
                    cost[childCell]= current_cost
                    f_score[childCell]= temp_f_score
                    p_q.put((temp_f_score,h(childCell),childCell))
                    aPath[childCell]=currCell

    fwdPath={}
    cell=goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath,f_score,cost

def UCS(m,start,goal):
    cost={cell:float('inf') for cell in m.grid}
    cost[start]=0

    p_q=PriorityQueue()
    p_q.put((cost[start],cost[start],start))
    aPath={}
    searchPath=[start]

    while not p_q.empty():
        currCell=p_q.get()[2]
        searchPath.append(currCell)
        if currCell==goal:
            break
        for next_node in 'ESNW':
            if m.maze_map[currCell][next_node]==True:
                if next_node=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if next_node=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if next_node=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if next_node=='S':
                    childCell=(currCell[0]+1,currCell[1])

                current_cost=cost[currCell]+1
                temp_f_score=current_cost

                if temp_f_score < cost[childCell]:
                    cost[childCell]= current_cost
                    p_q.put((temp_f_score,cost[childCell],childCell))
                    aPath[childCell]=currCell

    fwdPath={}
    cell=goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath,cost


def Greedy(m,start,goal):
    f_score={cell:float('inf') for cell in m.grid}
    f_score[start]=h(start)

    p_q=PriorityQueue()
    p_q.put((h(start),h(start),start))
    aPath={}
    searchPath=[start]

    while not p_q.empty():
        currCell=p_q.get()[2]
        searchPath.append(currCell)
        if currCell==goal:
            break
        for next_node in 'ESNW':
            if m.maze_map[currCell][next_node]==True:
                if next_node=='E':
                    childCell=(currCell[0],currCell[1]+1)
                if next_node=='W':
                    childCell=(currCell[0],currCell[1]-1)
                if next_node=='N':
                    childCell=(currCell[0]-1,currCell[1])
                if next_node=='S':
                    childCell=(currCell[0]+1,currCell[1])

                temp_f_score=h(childCell)

                if temp_f_score < f_score[childCell]:
                    f_score[childCell]= temp_f_score
                    p_q.put((temp_f_score,h(childCell),childCell))
                    aPath[childCell]=currCell

    fwdPath={}
    cell=goal
    while cell!=start:
        fwdPath[aPath[cell]]=cell
        cell=aPath[cell]
    return searchPath,aPath,fwdPath,f_score


if __name__=='__main__':
    m=maze(10,10)
    ############### Small Maze ################ 
    m.CreateMaze(1,1,loopPercent=40,loadMaze='maze--2022-04-19--22-51-14.csv')

    ############### Medium Maze ################ 
    # m.CreateMaze(1,1,loopPercent=40,loadMaze='maze--2022-04-24--23-15-09.csv')

    ############### Large Maze ################ 
    # m.CreateMaze(1,1,loopPercent=40,loadMaze='maze--2022-04-24--23-20-31.csv')

    goal=(1,1)
    start=(m.rows,m.cols)
    s=[(m.rows,m.cols)]
    starttime = time.time()

    ############### Breadth-first search ################ 
    bSearch,bfsPath,fwdPath=BFS(m,start,goal)

    ############### Depth-first search ################
    # bSearch,bfsPath,fwdPath,p=DFS(m,start,goal)

    ############### A* search ################
    # bSearch,bfsPath,fwdPath,f_score,cost=aStar(m,start,goal)

    ############### Greedy search ################
    # bSearch,bfsPath,fwdPath,f_score=Greedy(m,start,goal)

    ############### Uniform Cost Search ################
    # bSearch,bfsPath,fwdPath,cost=UCS(m,start,goal)

    # print("f: ",f_score)
    # print("cost:  ",cost)
    
    st=agent(m,color='red',filled=True)
    a=agent(m,footprints=True,color=COLOR.yellow,shape='square',filled=True)
    b=agent(m,footprints=True,color=COLOR.red,shape='square',filled=False)
    c=agent(m,1,1,footprints=True,color=COLOR.cyan,shape='square',filled=True,goal=(m.rows,m.cols))
    m.tracePath({a:bSearch,st:s},delay=100)
    m.tracePath({c:bfsPath},delay=100)
    m.tracePath({b:fwdPath},delay=100)
    end = time.time()
    searchingtime=end-starttime
    l=textLabel(m,'Length of Shortest Path',len(fwdPath)+1)
    l2=textLabel(m,'Searching Time: ',searchingtime)

    m.run()
