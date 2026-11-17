import sys
import yaml

m = 500 # map size
n = 400 #

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
    newpointx = int ( (point[0] - corner[0]) / map_size[0] * (m-1) )
    newpointy = int ( (point[1] - corner[1]) / map_size[1] * (n-1) )
    newpointx = fix(newpointx, n)
    newpointy = fix(newpointy, m)
    print(newpointx, newpointy)
    return (newpointx, newpointy)

# create the map_big.txt file with all necessary data
def buildMap(goal=None, start=None, yamlFileName = "../scenarios/my_world.yaml"):
    print("Building the map...")
    map = [['0'] * (m) for i in range(n)]

    # obstacle import from .yaml
    with open(yamlFileName, "r") as yaml_file:
        config = yaml.safe_load(yaml_file)

    # get world size and top left corner coordinates
    map_size, corner = getSize(config)

    if start is None:
        pos = config["tether"]["object"]
        start = (pos["x"], pos["y"])
        start = adjust(start,  map_size, corner)
    if goal is None:
        pos = config["tether"]["goal"]
        goal = (pos["x"], pos["y"])
        goal  = adjust(goal,   map_size, corner)


    print("points: ", start, "->", goal, ", size: ", map_size, ", corner: ", corner)

    map[start[0]][start[1]] = 'S'
    map[goal[0]][goal[1]] = 'G'

    # put the obstacles into the map
    #todo
    for i in range(175):
        map[i + 100][250] = '1'

    # write the map to 'map_big.txt'
    with open('map_big.txt', "w") as map_file:
        for i in range(n):
            map_file.write("".join(map[i]) + '\n')
    print("Map built succesfully!")

if __name__ == "__main__":
    buildMap()