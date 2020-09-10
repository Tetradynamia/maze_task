import sys
import queue
import re


def maze_setup(maze):
    '''
    Muuttaa tekstitedostosta luetun sokkelon 2-ulotteiseksi listaksi. Mikäli
    alkupiste löytyy, sijoittaa tähän luvun 1. Muihin vapaisiin tiloihin
    sijoittaa luvun 0. Poimii loppupisteiden koordinaatit listaan. Mikäli alku-
    tai loppupistettä ei löydy, ohjelma tulostaa tästä kertovan viestin ja
    ohjelman suoritus päättyy.

    Palauttaa sokkelon 2-ulotteisena listana, alkupisteen koordinaatit (tuple)
    ja listan loppupisteiden koordinaateista.
    '''
    maze_map = []
    exits = []

    for i in range(len(maze)):
        maze_map.append([])
        for j in range(len(maze[i])):
            if maze[i][j] == '#':
                maze_map[i].append('#')
            elif maze[i][j] == '^':
                maze_map[i].append(1)
                start = (i, j)
            elif maze[i][j] == 'E':
                exits.append((i, j))
                maze_map[i].append(0)
            else:
                maze_map[i].append(0)
    try:
        start
    except NameError:
        print("Aloituspistettä ('^') ei voitu määrittää.")
        sys.exit(1)

    if len(exits) < 1:
        print("Sokkelon uloskäyntiä ('E') ei löytynyt. Ei ratkaisua.")
        sys.exit(0)

    return [maze_map, start, exits]


def solve_maze(maze_map, start, exits):
    '''
    Argumentit: Sokkelo 2-ulotteisena listana, alkupisteen koordinaatit (tuple)
                lista loppupisteiden koordinaateista.

    Ratkaisee sokkelon aloittaen alkupisteestä ja tarkastamalla kaikki ne
    pisteet, joihin siitä voi siirtyä. Jos pisteeseen voi siirtyä, se
    merkitään käydyksi sijoittamalla siihen numero, joka vastaa lähdöstä
    pisteeseen tarvittavien askelten lukumäärää. Piste lisätään jonoon ja
    prosessi toistetaan jokaiselle jonossa olevalle pisteelle, kunnes jonossa
    on jokin loppupiste.

    Mikäli jonossa ei ole pisteitä, ei sokkelolle ole ratkaisua. (Kaikki
    pisteet joihin voidaan päästä on käyty läpi)

    Palauttaa: Sokkelo 2-ulotteisena listana, käytetyn loppupisteen
               koordinaatit.
               False (mikäli ratkaisua ei ole)
    '''
    q = queue.Queue()
    i = start[0]
    j = start[1]

    q.put((i, j))

    while not q.empty():

        for item in list(q.queue):
            if item in exits:
                return [maze_map, item]

        next_step = q.get()
        i, j = next_step[0], next_step[1]

        if i > 0 and maze_map[i-1][j] == 0:
            maze_map[i-1][j] = maze_map[i][j] + 1
            q.put((i-1, j))

        if i < len(maze_map) - 1 and maze_map[i+1][j] == 0:
            maze_map[i+1][j] = maze_map[i][j] + 1
            q.put((i+1, j))

        if j > 0 and maze_map[i][j-1] == 0:
            maze_map[i][j-1] = maze_map[i][j] + 1
            q.put((i, j-1))

        if j < len(maze_map[i]) - 1 and maze_map[i][j+1] == 0:
            maze_map[i][j+1] = maze_map[i][j] + 1
            q.put((i, j+1))

    return False


def find_path(maze_map, end):
    '''
    Löytää polun sokkelon läpi aloittaen loppupisteestä ja siirtyen siitä
    pisteeseen, jossa arvo on yhtä pienempi kunnes päädytään pisteeseen, jossa
    arvo 1 (alkupiste). Palauttaa listan käytyjen pisteiden koordinaateista.
    '''
    i = end[0]
    j = end[1]
    step_count = maze_map[i][j]
    path = [(i, j)]
    while step_count > 1:
        if i > 0 and maze_map[i - 1][j] == step_count - 1:
            i, j = i - 1, j
            path.append((i, j))
            step_count -= 1
        elif i < len(maze_map) - 1 and maze_map[i + 1][j] == step_count - 1:
            i, j = i + 1, j
            path.append((i, j))
            step_count -= 1
        elif j > 0 and maze_map[i][j - 1] == step_count - 1:
            i, j = i, j - 1
            path.append((i, j))
            step_count -= 1
        elif j < len(maze_map[i]) - 1 and maze_map[i][j + 1] == step_count - 1:
            i, j = i, j + 1
            path.append((i, j))
            step_count -= 1
    return path


def show_solution(maze, path):
    '''
    Tulostaa alkuperäisen sokkelon johon lisäksi merkitty sen läpi löydetty
    polku.
    '''
    solution = []

    for i in range(len(maze)):
        solution.append('')
        for j in range(len(maze[i])):
            if (i, j) in path[1:-1]:
                solution[i] += '+'
            else:
                solution[i] += maze[i][j]

    for i, row in enumerate(solution):
        print(row)


def validate(input):
    '''
    Tarkistetaan että:
    1. Käyttäjä antaa ratkaistavan sokkelon sisältävän tiedoston.
    2. Tiedostopääte on .txt
    '''

    pattern = re.compile(r"^.*\.(txt)$")

    if len(input) < 2:
        print(f'Käyttö: python {sys.argv[0]} sokkelo.txt')
        sys.exit(1)

    if not pattern.fullmatch(input[1]):
        print(f'Käyttö: python {sys.argv[0]} sokkelo.txt')
        sys.exit(1)


# VARSINAINEN OHJELMA ALKAA TÄSTÄ

inputs = sys.argv

validate(inputs)


try:
    with open(inputs[1], mode='r') as file:
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
exits = maze_after_setup[2]

solved_maze = solve_maze(maze_map_initial, start, exits)

if solved_maze:
    maze_map = solved_maze[0]
    exit_point = solved_maze[1]
    path = find_path(maze_map, exit_point)
    print(f'Ratkaisu! ({len(path)} askelta.)')
    show_solution(maze, path)


else:
    print('Ei ratkaisua!')
