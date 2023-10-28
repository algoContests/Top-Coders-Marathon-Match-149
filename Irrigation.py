from collections import deque

import sys


def idebug(*args):
    return
    print(*map(lambda message: f'{Color.RED}{message}{Color.END}', args), file=sys.stderr, flush=True)


def debug(*args):
    # return
    print(*map(lambda message: f'{Color.DARKCYAN}{message}{Color.END}', args), file=sys.stderr, flush=True)


class Color:
    PURPLE = '\033[95m'
    CYAN = '\033[96m'
    DARKCYAN = '\033[36m'
    BLUE = '\033[94m'
    GREEN = '\033[92m'
    YELLOW = '\033[93m'
    RED = '\033[91m'
    BOLD = '\033[1m'
    UNDERLINE = '\033[4m'
    END = '\033[0m'


EMPTY = 0
WATER = 1
PLANT = 2
PIPE = 3

def irrigated_scores():
    sprinkler_scores = []
    for p in pipes:
        if p not in sprinklers:
            hit_plants = len([pl for pl, irrigated in plants.items() if dist2(p, pl) <= Z * Z and not irrigated])
            if hit_plants > 0:
                sprinkler_scores.append((p, hit_plants))
    return sprinkler_scores

def expand(r, c, d) -> tuple:
    global output, grid
    # if r0 is None or c0 is None:
    #     return -1, -1
    r2 = r + dx[d]
    c2 = c + dy[d]
    validr = validc = -1
    while 0 <= r2 < N and 0 <= c2 < N and grid[r2][c2] == EMPTY:
        validr = r2
        validc = c2
        r2 += dx[d]
        c2 += dy[d]
        grid[validr][validc] = PIPE
    if validr >= 0:
        output.append("P " + str(r) + " " + str(c) + " " + str(validr) + " " + str(validc))
        # output.append("S " + str(validr) + " " + str(validc))
    return validr, validc


N = int(input())
C = int(input())
P = int(input())
T = int(input())
Z = int(input())
idebug(N, C, P, T, Z)

dx = [1, 0, -1, 0]
dy = [0, 1, 0, -1]

# Read grid
grid = [[0 for x in range(N)] for y in range(N)]
for r in range(N):
    for c in range(N):
        grid[r][c] = int(input())
        idebug(grid[r][c])
# for r in range(N):
#     debug(grid[r])

dist2 = lambda t1, t2: (t2[1] - t1[1]) ** 2 + (t2[0] - t1[0]) ** 2
water_sources = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == WATER]
# plants = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == PLANT]
plants = {(r, c): False for r in range(N) for c in range(N) if grid[r][c] == PLANT}

output = []
water_sources.sort(key=lambda w: sum([dist2(w, p) for p in plants]), reverse=True)
while water_sources:
    ws = water_sources.pop(0)
    queue = deque([ws] * 4)
    while queue:
        r, c = queue.popleft()
        for d in range(4):
            new_pipe = expand(r, c, d)
            if new_pipe == (-1, -1):
                continue
            queue.append(new_pipe)

pipes = [(r, c) for r in range(N) for c in range(N) if grid[r][c] == PIPE]
sprinklers = set()
sprinkler_actions = irrigated_scores()
sprinkler_actions.sort(key=lambda x: x[1])

while sprinkler_actions:
    s, score = sprinkler_actions.pop()
    sprinklers.add(s)
    output.append("S " + str(s[0]) + " " + str(s[1]))
    for p in plants:
        if dist2(s, p) <= Z*Z:
            plants[p] = True
    # irrigated_plants = [p for p, i in plants.items() if i]
    # debug(f'{len(irrigated_plants)} irrigated plants: {irrigated_plants}')
    sprinkler_actions = irrigated_scores()
    sprinkler_actions.sort(key=lambda x: x[1])

# arrosage plantes non couvertes
dry_plants = [p for p, i in plants.items() if not i]

#while dry_plants:


debug(len(output))
print(len(output))
for o in output:
    # debug(o)
    print(o)

sys.stdout.flush()

# debug()
# for r in range(N):
#     debug(grid[r])

