from pydraw import *
from queue import PriorityQueue


def narediLabirint(dat):
    return [[int(i) for i in vrstica.strip().split(',')] for vrstica in open(dat)]


def najdiZacetek(lab):
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == -2:
                return x, y


def najdiKonec(lab):
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == -4:
                return x, y


def prestejZaklade(lab):
    koor = []
    st = 0
    for x in range(len(lab)):
        for y in range(len(lab[x])):
            if lab[x][y] == -3:
                st += 1
                koor.append((x, y))
    return st, koor


def najdiZaklad(zacetek, najdeniZakladi, algorithm, maze, obdelana):
    frontier = [zacetek]
    explored = [zacetek]
    naselKonec = False
    bfsPot = {}
    konec = None
    while not naselKonec:
        if algorithm == "BFS":
            currCell = frontier.pop(0)
        elif algorithm == "DFS":
            currCell = frontier.pop(len(frontier) - 1)
        else:
            break
        left = currCell[0], currCell[1]-1
        right = currCell[0], currCell[1]+1
        up = currCell[0]-1, currCell[1]
        down = currCell[0]+1, currCell[1]
        directions = [right, down, left, up]
        for direction in directions:
            if direction not in explored and maze[direction[0]][direction[1]] >= 0:
                frontier.append(direction)
                explored.append(direction)
                bfsPot[direction] = currCell
            elif maze[direction[0]][direction[1]] == -3 and direction not in explored and direction not in najdeniZakladi:
                explored.append(direction)
                najdeniZakladi.append(direction)
                bfsPot[direction] = currCell
                konec = direction
                naselKonec = True
                break
    obdelana.extend(explored)
    return bfsPot, konec


def najdiCilj(zacetek, algorithm, maze, obdelana):
    frontier = [zacetek]
    explored = [zacetek]
    naselKonec = False
    bfsPot = {}
    konec = None
    while not naselKonec:
        if algorithm == "BFS":
            currCell = frontier.pop(0)
        elif algorithm == "DFS":
            currCell = frontier.pop(len(frontier)-1)
        else:
            break
        left = currCell[0], currCell[1]-1
        right = currCell[0], currCell[1]+1
        up = currCell[0]-1, currCell[1]
        down = currCell[0]+1, currCell[1]
        directions = [right, down, left, up]
        for direction in directions:
            if direction not in explored and maze[direction[0]][direction[1]] >= 0:
                frontier.append(direction)
                explored.append(direction)
                bfsPot[direction] = currCell
            elif maze[direction[0]][direction[1]] == -4 and direction not in explored:
                explored.append(direction)
                bfsPot[direction] = currCell
                konec = direction
                naselKonec = True
                break
    obdelana.extend(explored)
    return bfsPot, konec


def najdiPot(celaPot, start, zakladi, najdeniZakladi, algorithm, maze, obdelana):
    zacetek = start
    najdeni = 0
    while najdeni < zakladi:
        tre = najdiZaklad(zacetek, najdeniZakladi, algorithm, maze, obdelana)
        bfsPot = tre[0]
        konec = tre[1]
        pot = [konec]
        potka = bfsPot[konec]
        while potka != zacetek:
            pot.append(potka)
            potka = bfsPot[potka]
        pot.append(potka)
        pot.reverse()
        celaPot.append(pot)
        zacetek = konec
        najdeni += 1
    tre = najdiCilj(zacetek, algorithm, maze, obdelana)
    bfsPot = tre[0]
    konec = tre[1]
    pot = [konec]
    potka = bfsPot[konec]
    while potka != zacetek:
        pot.append(potka)
        potka = bfsPot[potka]
    pot.append(potka)
    pot.reverse()
    celaPot.append(pot)
    najdeni += 1


def calcHCost(start, end):
    return abs(start[0] - end[0]) + abs(start[1] - end[1])


def hevristicnaOcena(zakladi, izhodisce):
    najSt = math.inf
    najKoor = None
    for zaklad in zakladi:
        if calcHCost(izhodisce, zaklad) < najSt:
            najSt = calcHCost(izhodisce, zaklad)
            najKoor = zaklad
    return najKoor


def starAlgorithm(start, end, treasures, maze, poti, zacKonci, obdelana):
    treasureCoords = treasures
    while len(treasureCoords) != 0:
        zac = start
        potDict = {}
        trenutna = []
        gcost = {}
        hcost = {}
        fscore = {}
        for x in range(len(maze)):
            for y in range(len(maze[x])):
                if (x, y) == start:
                    gcost[(x, y)] = 0
                    hcost[(x, y)] = calcHCost((x, y), hevristicnaOcena(treasureCoords, start))
                    fscore[(x, y)] = gcost[(x, y)] + hcost[(x, y)]
                else:
                    gcost[(x, y)] = math.inf
                    hcost[(x, y)] = calcHCost((x, y), hevristicnaOcena(treasureCoords, start))
                    fscore[(x, y)] = math.inf
        vrsta = PriorityQueue()
        vrsta.put((fscore[start], hcost[start], start))
        found = False
        currCell = vrsta.get()[2]
        steps = 1
        explored = [start]
        while not found:
            right = currCell[0], currCell[1]+1
            down = currCell[0]+1, currCell[1]
            left = currCell[0], currCell[1]-1
            up = currCell[0]-1, currCell[1]
            for cell in [right, down, left, up]:
                if maze[cell[0]][cell[1]] != -1 and maze[cell[0]][cell[1]] != -3 and cell not in explored:
                    potDict[cell] = currCell
                    gcost[cell] = steps
                    fscore[cell] = gcost[cell] + hcost[cell]
                    explored.append(cell)
                    vrsta.put((fscore[cell], hcost[cell], cell))
                    trenutna.append(cell)
                elif maze[cell[0]][cell[1]] == -3 and cell in treasureCoords:
                    explored.append(cell)
                    zacKonci.append((zac, cell))
                    potDict[cell] = currCell
                    found = True
                    start = cell
                    treasureCoords.remove(cell)
                    obdelana.extend(explored)
                    break
            nov = vrsta.get()
            steps = nov[0] - nov[1] + 1
            currCell = nov[2]
        poti.append(potDict)
        potDict = {}
    potDict = {}
    trenutna = []
    gcost = {}
    hcost = {}
    fscore = {}
    for x in range(len(maze)):
        for y in range(len(maze[x])):
            if (x, y) == start:
                gcost[(x, y)] = 0
                hcost[(x, y)] = calcHCost((x, y), end)
                fscore[(x, y)] = gcost[(x, y)] + hcost[(x, y)]
            else:
                gcost[(x, y)] = math.inf
                hcost[(x, y)] = calcHCost((x, y), end)
                fscore[(x, y)] = math.inf
    vrsta = PriorityQueue()
    vrsta.put((fscore[start], hcost[start], start))
    found = False
    currCell = vrsta.get()[2]
    steps = 1
    explored = [start]
    zacKonci.append((start, end))
    while not found:
        right = currCell[0], currCell[1] + 1
        down = currCell[0] + 1, currCell[1]
        left = currCell[0], currCell[1] - 1
        up = currCell[0] - 1, currCell[1]
        for cell in [right, down, left, up]:
            if maze[cell[0]][cell[1]] != -1 and maze[cell[0]][cell[1]] != -4 and cell not in explored:
                potDict[cell] = currCell
                gcost[cell] = steps
                fscore[cell] = gcost[cell] + hcost[cell]
                explored.append(cell)
                vrsta.put((fscore[cell], hcost[cell], cell))
                trenutna.append(cell)
            elif maze[cell[0]][cell[1]] == -4:
                explored.append(cell)
                potDict[cell] = currCell
                found = True
                obdelana.extend(explored)
                break
        nov = vrsta.get()
        steps = nov[0] - nov[1] + 1
        currCell = nov[2]
    poti.append(potDict)


def calculatePrice(maze, roadArray) -> int:
    price = 0
    specialNumbers = [-2, -3, -4]
    for road in roadArray:
        for coord in road:
            if maze[coord[0]][coord[1]] not in specialNumbers:
                price += maze[coord[0]][coord[1]]
    return price


def backtrackStar(vozlisca, startEnd, roadArray):
    for j in range(len(vozlisca)):
        dic = vozlisca[j]
        konec = startEnd[j][1]
        zac = startEnd[j][0]
        pot = [konec]
        potka = dic[konec]
        while potka != zac:
            pot.append(potka)
            potka = dic[potka]
        pot.append(potka)
        pot.reverse()
        roadArray.append(pot)


def izpisPodatkov(dat):
    lab1 = narediLabirint(dat)
    zacetek = najdiZacetek(lab1)
    konec = najdiKonec(lab1)
    stZakladov = prestejZaklade(lab1)[0]
    koorZakladov1 = prestejZaklade(lab1)[1]
    koorZakladov = prestejZaklade(lab1)[1]

    # BREADTH FIRST SEARCH ALGORITHM

    najdeniZakladiBFS = []
    celaPotBFS = []
    preverjenaVozliscaBFS = []
    dolzinaBFS = 0
    najdiPot(celaPotBFS, zacetek, stZakladov, najdeniZakladiBFS, "BFS", lab1, preverjenaVozliscaBFS)
    priceBFS = calculatePrice(lab1, celaPotBFS)
    for i in celaPotBFS:
        dolzinaBFS += len(i)

    # DEPTH FIRST SEARCH ALGORITHM

    najdeniZakladiDFS = []
    celaPotDFS = []
    preverjenaVozliscaDFS = []
    dolzinaDFS = 0
    najdiPot(celaPotDFS, zacetek, stZakladov, najdeniZakladiDFS, "DFS", lab1, preverjenaVozliscaDFS)
    priceDFS = calculatePrice(lab1, celaPotDFS)
    for i in celaPotDFS:
        dolzinaDFS += len(i)

    # A* ALGORITHM

    voz = []
    zacKonci = []
    preverjenaVozliscaStar = []
    celaPotStar = []
    dolzinaStar = 0
    starAlgorithm(zacetek, konec, koorZakladov1, lab1, voz, zacKonci, preverjenaVozliscaStar)
    backtrackStar(voz, zacKonci, celaPotStar)
    priceStar = calculatePrice(lab1, celaPotStar)
    for i in celaPotStar:
        dolzinaStar += len(i)

    print("Izpis podatkov za labirint številka " + str(dat[-5]) + ":")
    print("Breadth first search Algorithm: ")
    print("Najdena pot: ")
    print(celaPotBFS)
    print("Preverjenih vozlišč: " + str(len(preverjenaVozliscaBFS)) + "   cena: " + str(priceBFS) + "   dolžina poti: " + str(dolzinaBFS))
    print("Depth first search Algorithm: ")
    print(celaPotDFS)
    print("Preverjenih vozlišč: " + str(len(preverjenaVozliscaDFS)) + "   cena: " + str(priceDFS) + "   dolžina poti: " + str(dolzinaDFS))
    print("A* search Algorithm: ")
    print(celaPotStar)
    print("Preverjenih vozlišč: " + str(len(preverjenaVozliscaStar)) + "   cena: " + str(priceStar) + "   dolžina poti: " + str(dolzinaStar))
    print()


labirinti = [
    'labyrinth_1.txt',
    'labyrinth_2.txt',
    'labyrinth_3.txt',
    'labyrinth_4.txt',
    'labyrinth_5.txt',
    'labyrinth_6.txt',
    'labyrinth_7.txt',
    'labyrinth_8.txt',
    'labyrinth_9.txt'
]

for labirint in labirinti:
    izpisPodatkov(labirint)

# PRIPRAVA PODATKOV ZA IZRISOVANJE

velikost = 10
ime = 'labyrinth_8.txt'
lab1 = narediLabirint(ime)
zacetek = najdiZacetek(lab1)
konec = najdiKonec(lab1)
stZakladov = prestejZaklade(lab1)[0]
koorZakladov1 = prestejZaklade(lab1)[1]
koorZakladov = prestejZaklade(lab1)[1]

# BREADTH FIRST SEARCH ALGORITHM

najdeniZakladiBFS = []
celaPotBFS = []
preverjenaVozliscaBFS = []
najdiPot(celaPotBFS, zacetek, stZakladov, najdeniZakladiBFS, "BFS", lab1, preverjenaVozliscaBFS)

# DEPTH FIRST SEARCH ALGORITHM

najdeniZakladiDFS = []
celaPotDFS = []
preverjenaVozliscaDFS = []
najdiPot(celaPotDFS, zacetek, stZakladov, najdeniZakladiDFS, "DFS", lab1, preverjenaVozliscaDFS)

# A* ALGORITHM

voz = []
zacKonci = []
preverjenaVozliscaStar = []
celaPotStar = []
starAlgorithm(zacetek, konec, koorZakladov1, lab1, voz, zacKonci, preverjenaVozliscaStar)
backtrackStar(voz, zacKonci, celaPotStar)


screen = Screen(len(lab1[0])*velikost, len(lab1)*velikost, str(ime))
for x in range(len(lab1)):
    for y in range(len(lab1[x])):
        st = lab1[x][y]
        barva = None
        if st == -1:
            barva = 'black'
        elif st >= 0:
            barva = 'white'
        elif st == -2:
            barva = 'red'
        elif st == -3:
            barva = 'yellow'
        elif st == -4:
            barva = 'green'
        Rectangle(screen, velikost*y, velikost*x, velikost, velikost, Color(barva))


tipiBarv = ['black', 'cyan', 'blue', 'red', 'gray', 'brown', 'orange']
barve = {}
for i in range(stZakladov + 1):
    barve[i] = tipiBarv[i]
i = 0
risiPot = True
risiPregledana = True
fps = 60
running = True
while running:
    # if risiPot:
    #     for road in celaPotStar:
    #         for tocka in range(len(road) - 1):
    #             col = tipiBarv[i]
    #             screen.update()
    #             screen.sleep(1 / 144)
    #             line = Line(screen, int(road[tocka][1] * velikost + (velikost / 2)),
    #                         int(road[tocka][0] * velikost + (velikost / 2)),
    #                         int(road[tocka + 1][1] * velikost + (velikost / 2)),
    #                         int(road[tocka + 1][0] * velikost + (velikost / 2)), Color(col))
    #             line.thickness(5)
    #         i += 1
    #     risiPot = False
    if risiPregledana:
        i = 1
        najdeni = []
        for coor in preverjenaVozliscaStar:
            col = tipiBarv[i]
            if lab1[coor[0]][coor[1]] == -3:
                if coor not in najdeni:
                    i += 1
                    if i == len(tipiBarv):
                        i = 1
                    najdeni.append(coor)
            else:
                Rectangle(screen, velikost * coor[1], velikost * coor[0], velikost, velikost, Color(col))
            screen.update()
            screen.sleep(1 / 144)
        risiPregledana = False
        i = 0
    screen.update()
    screen.sleep(1 / fps)
screen.exit()
