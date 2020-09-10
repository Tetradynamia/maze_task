import sys
import timeit


def maze_setup(maze):
    maze_map = []

    for i in range(len(maze)):
        maze_map.append([])
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                maze_map[i].append('#')
            elif maze[i][j] == '^':
                maze_map[i].append(1)
                start = (i, j)
            else:
                maze_map[i].append(0)
    try:
        start
    except NameError:
        print("Aloituspistettä ('^') ei voitu määrittää.")
        sys.exit(1)
    return [maze_map, start]


def solve_maze(maze, maze_map, start):
    queue = []
    i = start[0]
    j = start[1]

    queue.append((i, j))
    while queue:
        i, j = queue[0][0], queue[0][1]

        for l in range(len(queue)):
            if maze[queue[l][0]][queue[l][1]] == 'E':
                return [maze_map, (queue[l][0], queue[l][1])]

            if i > 0 and maze_map[i-1][j] == 0:
                maze_map[i-1][j] = maze_map[i][j] + 1
                queue.append((i-1, j))

            if i < len(maze_map) - 1 and maze_map[i+1][j] == 0:
                maze_map[i+1][j] = maze_map[i][j] + 1
                queue.append((i+1, j))

            if j > 0 and maze_map[i][j-1] == 0:
                maze_map[i][j-1] = maze_map[i][j] + 1
                queue.append((i, j-1))

            if j < len(maze_map[i]) - 1 and maze_map[i][j+1] == 0:
                maze_map[i][j+1] = maze_map[i][j] + 1
                queue.append((i, j+1))

        queue.pop(0)

    return False


def find_path(maze_map, end):
    i = end[0]
    j = end[1]
    k = maze_map[i][j]
    path = [(i, j)]
    while k > 1:
        if i > 0 and maze_map[i - 1][j] == k - 1:
            i, j = i - 1, j
            path.append((i, j))
            k -= 1
        elif i < len(maze_map) - 1 and maze_map[i + 1][j] == k - 1:
            i, j = i + 1, j
            path.append((i, j))
            k -= 1
        elif j > 0 and maze_map[i][j - 1] == k - 1:
            i, j = i, j - 1
            path.append((i, j))
            k -= 1
        elif j < len(maze_map[i]) - 1 and maze_map[i][j + 1] == k - 1:
            i, j = i, j + 1
            path.append((i, j))
            k -= 1
    return path


def show_solution(maze, path):
    solution = []

    for i in range(len(maze)):
        solution.append('')
        for j in range(len(maze[i])):
            if (i, j) in path[1:-1]:
                solution[i] += '+'
            else:
                solution[i] += maze[i][j]

    for i in range(len(solution)):
        print(solution[i])

    return True


# Main function

inputs = sys.argv[1:]

if len(inputs) < 1:
    print('')
    sys.exit(1)

t1 = timeit.default_timer()
try:
    with open(inputs[0], mode='r') as file:
        maze = [x.rstrip('\n') for x in file.readlines()]
except FileNotFoundError:
    print('Tiedostoa ei löytynyt.')
    sys.exit(1)
except Exception:
    print('Jokin meni pieleen. :(')
    sys.exit(1)


maze_after_setup = maze_setup(maze)
maze_map_initial = maze_after_setup[0]
start = maze_after_setup[1]

solved_maze = solve_maze(maze, maze_map_initial, start)

if solved_maze:
    maze_map = solved_maze[0]
    exit_point = solved_maze[1]
    path = find_path(maze_map, exit_point)
    print(f'Ratkaisu! ({len(path)} askelta.)')
    show_solution(maze, path)
    print(timeit.default_timer() - t1)

else:
    print('Ei ratkaisua!')
