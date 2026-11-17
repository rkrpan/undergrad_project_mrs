import sys
import yaml

orig_stdout = sys.stdout

m = 500
n = 400

start_initial = (0, 0)
goal_initial = (n-1, m-1)


def buildMap(goal=goal_initial, start=start_initial):
    print("Building the map...")

    with open('map_big.txt', "w") as map_file:
        for i in range(n):
            row = []
            for j in range(m):
                if ((i, j) == start):
                    row.append('S')
                elif ((i, j) == goal):
                    row.append('G')
                else:
                    row.append('0')
            map_file.write("".join(row) + '\n')
    print("Map built succesfully!")

if __name__ == "__main__":
    buildMap()