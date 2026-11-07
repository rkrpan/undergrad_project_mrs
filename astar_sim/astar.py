from math import sqrt

next_field = [[1, 0],
              [1, 1],
              [0, 1],
              [-1, 1],
              [-1, 0],
              [-1, -1],
              [0, -1]
]

def heuristic(n, goal):
    '''Returns air distance between fields n and goal'''
    return sqrt( (n[0] - goal[0]) ** 2 + (n[1] - goal[1]) ** 2 )

def reconstruct_path(came_from, current):
    path = [list(current)]
    while current in came_from:
        current = came_from[current]
        path = [list(current)] + path
    return path

def astar(start, goal, map, heur):
    ''' s = start node, g = goal, map is n*m witn 1 = obstacle,
        S = start, G = goal and 0 = empty field. Heur is the
        heuristic function.
    '''
    n = len(map)
    m = len(map[0])

    start = tuple(start)
    goal = tuple(goal)

    node_set = {start}
    came_from = {}
    
    inf = n * m * 11
    g_value = [[ inf for j in range (m)] for i in range (n)]
    f_value = [[ inf for j in range (m)] for i in range (n)]

    g_value[start[0]][start[1]] = 0
    f_value[start[0]][start[1]] = heur(start, goal)

    while len(node_set) > 0:
        current = min(node_set, key=lambda x: \
            g_value[x[0]][x[1]] + heur(x, goal)
        )
        if current == goal:
            return reconstruct_path(came_from , current)
        
        node_set.discard(current)
        for inc in next_field:
            next = (current[0] + inc[0], current[1] + inc[1])
            
            if not (0 <= next[0] < n and 0 <= next[1] < m):
                continue
            if map[next[0]][next[1]] == '1':
                continue
            
            new_g_value = g_value[current[0]][current[1]] + 1

            if (new_g_value < g_value[next[0]][next[1]]):
                came_from[next] = current
                g_value[next[0]][next[1]] = new_g_value
                f_value[next[0]][next[1]] = new_g_value + heur(next, goal)

                if next not in node_set:
                    node_set.add(next)

    raise Exception("Goal not found!")

def main():
    inputFile = input()
    try:
        with open(inputFile, "r") as f:
            map = [line.strip() for line in f if line.strip()]
            print(map)
    except FileNotFoundError:
        map = ['S000', '0110', '0110', '000G']

    n = len(map)
    if n == 0:
        raise Exception("Map must not be empty.")
    m = len(map[0])
    for i in range (0, n, 1):
        if (len(map[i]) != m):
            raise Exception("Incorrect input file format: line " + str(i) + ".")

    start = None
    goal = None
    for i in range (n):
        for j in range (m):
            if map[i][j] == 'S':
                start = [i, j]
            if map[i][j] == 'G':
                goal = [i, j]
    
    if start is None or goal is None:
        raise Exception('Start or goal not found!')

    print(start, goal)

    # astar

    path = astar(start, goal, map, heuristic)

    for x in path:
        string = map[x[0]]
        i = x[0]
        j = x[1]
        if string[j] != 'S' and string[j] != 'G':
           map[i] = string[:j] + '.' + string[j+1:]

    print('\n'.join(map))

if __name__ == "__main__":
    main()