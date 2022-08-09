import sys
"""
    File: battleship.py
    Author: Anna Rowena Waldron
    Purpose: to simulate the first part of the game battleship.
    Course/Sect/Semester: CSC120, 1G, spring18
"""

class Board:
    """Class that creates the grid of x,y points at the beginning of the game.
    Holds two attributes, a list of lists containing grid points and a
    dictionary of ships placed by player 1. """
    def __init__(self):
        self._grid = []
        self._ships = {}       
    def get_grid(self):
        return self._grid
    def get_ship(self):
        return self._ships
    def __str__(self):
        return "length: {}, ships: {}".format(len(self._grid), len(self._ships))
    
    def add(self, ship_obj, dic):
        """Add method that is called in other function that
        creates the dictionary on ships placed by player 1. Takes a ship
        object and the dictionary of all the possible battleship sizes."""
        for key, value in dic.items():
            if value[0] == ship_obj.get_type():
                self._ships[key] = ship_obj
                
    def grid(self):
        """Grid method that creates gripd position objects and forms lists
        based on x value and appends to the grid attribute."""
        for i in range(10):
            mini = []
            for j in range(10):
                pos = GridPos(i, j)
                mini.append(pos)
            self._grid.append(mini)
    
    def guesses(self):
        """Guesses method which takes user input for the guesses of ship
        locations by player 2, and prints out whether the guess was a hit
        or a miss. Checks for errors for legal guesses. Updates ship objects
        with the amount of times it was hit at different points and
        updates the grid position objects whether it was guessed or not.
        At the end, quits the program."""
        guess_file = input()
        try:
            file = open(guess_file)
        except FileNotFoundError:
            print("ERROR: Cannot read file: " + guess_file)
            sys.exit()
        file = file.readlines()
        checky = []
        hits = []
        sunk = []
        for line in file:
            line1 = line.split()
            x = int(line1[0])
            y = int(line1[1])
            if x > 9 or x < 0 or y > 9 or y < 0:
                print("illegal guess")
                continue
            for key, value in self._ships.items():
                v = value.get_pos()
                rat = False
                for j in range(len(v)):
                    if x == v[j].get_x() and y == v[j].get_y():
                        v[j].update_guess()
                        target = v[j].get_ship()
                        if line1 in hits:
                            print("hit (again)")
                            rat = True
                            break
                        elif line1 not in hits:
                            target.update_safe()
                            hits.append(line1)
                            v[j].update_guess()
                            if target.get_safe() == 0:
                                sunk.append(target)
                                print("{} sunk".format(key))
                                if len(sunk) == 5:
                                    print("all ships sunk: game over")
                                    sys.exit()
                                rat = True
                                break
                            else:
                                print("hit")
                                rat = True
                                break 
                if rat == True:
                    break
            if rat == True:
                continue
            else:
                if line1 not in checky:
                    print("miss")
                    checky.append(line1)
                    continue
                if line1 in checky:
                    print("miss (again)")
                    continue
        sys.exit()         

class GridPos:
    """Class which creates grid position objects for each point on the grid
    with attributes of x and y values, which ship occupies the point,
    and if the point has been guessed."""
    def __init__(self, x, y):
        self._x = int(x)
        self._y = int(y)
        self._ship = None
        self._guess = None
    def __str__(self):
        return "({}, {})".format(self._x, self._y)
    def get_x(self):
        return self._x
    def get_y(self):
        return self._y
    def edit_ship(self, ship_obj):
        self._ship = ship_obj
    def update_guess(self):
        self._guess = True
    def get_ship(self):
        return self._ship
    def get_guess(self):
        return self._guess
    def __eq__(self, other):
        return self._x == other.get_x() and self._y == other.get_y
    
class Ship:
    """Class which creates ship objects based on the input file of player 1.
    has attributes of type which holds the name of the ship, size with the
    number of points the ship object occupies, a list of these point objects,
    and the number of unguessed points."""
    def __init__(self, dic):
        self._type = dic[0]
        self._size = dic[1]
        self._grid_pos = []
        self._safe = dic[1]
    def add_pos(self, pos_obj):
        self._grid_pos.append(pos_obj)
    def get_type(self):
        return self._type
    def get_pos(self):
        return self._grid_pos
    def get_safe(self):
        return self._safe
    def update_safe(self):
        self._safe = self._safe - 1
    def __str__(self):
        q = len(self._grid_pos)
        p = "{},{},{},{}".format(self._type, self._size, q, self._safe)
        return p
        
def creation():
    """Function which takes user input by player 1 of a file with ships
    and their positions, determines if the ships location is valid,
    searches for errors, and creates ship objects. Appends to ship
    objects all the points that the size of the ship occupies.
    Parameters: N/A
    Returns: returns the board object with all updated information
        including all ship objects and corresponding grid point objects.
    Post-Conditions: board object's ship dictionary includes ship objects
        as values.
    Pre-Condition: board object has an empty dictionary. 
    """
    battleship = {'A':['Aircraft carrier', 5], 'B':['Battleship', 4], \
                  'S':['Submarine', 3], 'D':['Destroyer', 3], \
                  'P':['Patrol boat', 2]}
    placement = input()
    try:
        file = open(placement)
    except FileNotFoundError:
        print("ERROR: Could not open file: " + placement)
        sys.exit()
    file = file.readlines()
    if len(file) != 5:
        print("ERROR: fleet composition incorrect")
        sys.exit()
    c = Board()
    c.grid()
    griddy = c.get_grid()
    check = []
    check2 = []
    for line in file:
        line1 = line
        if line[0] not in battleship:
            print("ERROR: fleet composition incorrect")
        elif line[0] in battleship:
            line = line.split()
            if battleship[line[0]][0] in check:
                print("ERROR: fleet composition incorrect")
                sys.exit()
            else:
                check.append(battleship[line[0]][0])
            if line[1] == line[3]:
                b = max(int(line[2]), int(line[4]))
                v = min(int(line[2]), int(line[4]))
                if b > 9 or v < 0 or b < 0 or v > 9:
                    print("ERROR: ship out-of-bounds: " + line1)
                    sys.exit()
                size = b - v + 1
                spot = int(line[1])
                if size != battleship[line[0]][1]:
                    print("ERROR: incorrect ship size: " + line1)
                    sys.exit()
                shipy = Ship(battleship[line[0]])
                for i in range(v, b + 1):
                    shipy.add_pos(griddy[spot][i])
                    if griddy[spot][i] in check2:
                        print("ERROR: overlapping ship: " + line1)
                        sys.exit()
                    check2.append(griddy[spot][i])
                    griddy[spot][i].edit_ship(shipy)
            if line[2] == line[4]:
                b = max(int(line[1]), int(line[3]))
                v = min(int(line[1]), int(line[3]))
                if b > 9 or v < 0 or b < 0 or v > 9:
                    print("ERROR: ship out-of-bounds: " + line1)
                    sys.exit()
                size = b - v + 1
                spot = int(line[2])
                if size != battleship[line[0]][1]:
                    print("ERROR: incorrect ship size: " + line1)
                    sys.exit()
                shipy = Ship(battleship[line[0]])
                for i in range(v, b + 1):
                    shipy.add_pos(griddy[i][spot])
                    if griddy[i][spot] in check2:
                        print("ERROR: overlapping ship: " + line1)
                        sys.exit()
                    check2.append(griddy[i][spot])
                    griddy[i][spot].edit_ship(shipy)
            elif line[1] != line[3] and line[2] != line[4]:
                print("ERROR: ship not horizontal or vertical: " + line1)
                sys.exit()
            c.add(shipy, battleship)
    return c
               
def main():
    """Main function that calls the create function then uses the method
    of the board class guesses."""
    board = creation()
    board.guesses()
    
"""Calls the main function. """                
main()
    
