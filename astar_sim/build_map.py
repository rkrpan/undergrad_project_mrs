import yaml

m = 500 # map size
n = 400 #
safety_perimiter = 0.1

# get max and min world coordinates and output map size and top left corner coordinates
def getSize(config):
    xs = []
    ys = []

    # obstacles
    for obs in config["obstacles"]:
        x, y, r = obs["x"], obs["y"], obs["radius"]
        xs.extend([x + r, x - r])
        ys.extend([y + r, y - r])

    # crazyflies
    for crazyfly in config["crazyflies"]:
        xs.append(crazyfly["pose"]["x"])
        ys.append(crazyfly["pose"]["y"])

    # ground_robots
    for ground_robot in config["ground_robots"]:
        xs.append(ground_robot["pose"]["x"])
        ys.append(ground_robot["pose"]["y"])

    # tether
    tether = config.get("tether", {})
    for point in ("winch", "object", "goal"):
        xs.append(tether[point]["x"])
        ys.append(tether[point]["y"])

    # find global bounds and return map size
    xplus, xminus = max(xs), min(xs)
    yplus, yminus = max(ys), min(ys)    
    return (xplus - xminus, yplus - yminus), (xminus, yminus)
    return xplus, xminus, yplus, yminus

###################################################################################

def world_to_cell(x, y, corner, map_size, rows, cols):
    """World (x, y) in metres -> map (row, col). row follows y, col follows x."""
    col = int((x - corner[0]) / map_size[0] * cols)
    row = int((y - corner[1]) / map_size[1] * rows)
    row = min(max(row, 0), rows - 1)
    col = min(max(col, 0), cols - 1)
    return row, col

def cell_to_world(cell, corner, map_size):
    """map (row, col) -> world (x, y) of the cell centre, in metres."""
    return (corner[0] + (cell[1] + 0.5) * map_size[0] / m,
            corner[1] + (cell[0] + 0.5) * map_size[1] / n)

def fill_obstacles(map, obstacles, corner, map_size, safety_perimiter):
    """Mark every cell covered by an obstacle as '1' (boundary AND interior).
 
    A cell is blocked when its centre lies inside the circle, i.e.
        (cx - ox)^2 + (cy - oy)^2 <= (radius + inflate)^2
    The circle is therefore a filled disc, not just an outline.
    `inflate` grows the disc so the planned path keeps a safety distance.
    Only the cells in the circle's bounding box are tested, so it stays fast.
    """
    rows, cols = len(map), len(map[0])

    for obs in obstacles:
        ox, oy = obs["x"], obs["y"]
        r = obs["radius"] + safety_perimiter
 
        # bounding box of the circle, in cells (clipped to the map)
        col_min = max(int((ox - r - corner[0]) / map_size[0] * cols), 0)
        col_max = min(int((ox + r - corner[0]) / map_size[0] * cols) + 1, cols - 1)
        row_min = max(int((oy - r - corner[1]) / map_size[1] * rows), 0)
        row_max = min(int((oy + r - corner[1]) / map_size[1] * rows) + 1, rows - 1)
 
        for row in range(row_min, row_max + 1):
            cy = corner[1] + (row + 0.5) * map_size[1] / rows 
            for col in range(col_min, col_max + 1):
                cx = corner[0] + (col + 0.5) * map_size[0] / cols
                if (cx - ox) ** 2 + (cy - oy) ** 2 <= r * r:
                    map[row][col] = '1'

###################################################################################

# if a coordinate is out of bounds...
def fix(coord, bound):
    if coord >= bound:
        coord = bound-1
    if coord < 0:
        coord = 0
    return coord

# adjust world coordinates to map coordinates
def adjust(point, map_size, corner):
    global n, m
    col = int ( (point[0] - corner[0]) / map_size[0] * m )
    row = int ( (point[1] - corner[1]) / map_size[1] * n )
    col = fix(col, m)
    row = fix(row, n)
    print(row, col)
    return (row, col)

# create the map_big.txt file with all necessary data
def buildMap(goal=None, start=None, yamlFileName = "../scenarios/my_world.yaml"):
    print("Building the map...")
    map = [['0'] * (m) for i in range(n)]

    # obstacle import from .yaml
    with open(yamlFileName, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    # get world size and top left corner coordinates
    map_size, corner = getSize(config)

    print("points: ", start, "->", goal, ", size: ", map_size, ", corner: ", corner)

    # put the obstacles into the map
    #todo
    fill_obstacles(map, config["obstacles"], corner, map_size, safety_perimiter=safety_perimiter)


    # put start an goal on the map
    if start is None:
        pos = config["tether"]["object"]
        start = (pos["x"], pos["y"])
        start = adjust(start,  map_size, corner)
    if goal is None:
        pos = config["tether"]["goal"]
        goal = (pos["x"], pos["y"])
        goal  = adjust(goal,   map_size, corner)
    print(start, goal)
    map[start[0]][start[1]] = 'S'
    map[goal[0]][goal[1]] = 'G'

    # write the map to 'map_big.txt'
    with open('map_big.txt', "w") as map_file:
        for i in range(n):
            map_file.write("".join(map[i]) + '\n')
    print("Map built succesfully!")

