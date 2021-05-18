""" File: maze_solver.py
    Author: Jake Schuler
    CSC 120 Spring
    Purpose: The purpose of this program is to take a txt file which
        will be a maze and find the solution to the maze.
"""
class Tree:
    '''
    This class represents the Tree class which creates the tree
    which can be interated over for various tasks.

    The class defines several methods and fields:
        dump_tree(): prints the tree in a pre-order traversal
            based on depth
        solution_cords(): finds the coordniates of the correct solution
            of the maze
        print_solution_coords(): prints the path of the solution
            coordniates
    '''

    def __init__(self, val, x, y, depth, left=None, right=None, up=None, down=None):
        '''
        The constructor initializes the value, x-y coords, and the left, right,
        up, down nodes, and the cord_used variable is set to None.
        '''
        self.left = left
        self.right = right
        self.up = up
        self.down = down
        self.val = val
        self.x = x
        self.y = y
        self.depth = depth
        self.cord_used = None

    def dump_tree(self):
        '''
        This function takes the tree intialized and prints it in
        top, down, left, right order and based on the depth passed into
        the initalization. This is accomplished through recursive calls
        to the four directions.
        '''
        print('  ', end='')
        for i in range(self.depth):
            print('| ', end='')
        print((self.x, self.y))
        if self.up is not None:
            self.up.dump_tree()
        if self.down is not None:
            self.down.dump_tree()
        if self.left is not None:
            self.left.dump_tree()
        if self.right is not None:
            self.right.dump_tree()

    def solution_cords(self):
        '''
        This function traverses through the tree in all directions
        in search for the route which will end in 'E'. This is accomplished
        through concatenating lists and adding to the solution cords variable.
        '''
        self.cord_used = [(self.x, self.y)]
        solution_cords = []
        if self.val == 'E':
            return self.cord_used
        if self.up is not None:
            up = self.up.solution_cords()
            if len(up) > 0:
                return self.cord_used + up
        if self.down is not None:
            down = self.down.solution_cords()
            if len(down) > 0:
                return self.cord_used + down
        if self.left is not None:
            left = self.left.solution_cords()
            if len(left) > 0:
                return self.cord_used + left
        if self.right is not None:
            right = self.right.solution_cords()
            if len(right) > 0:
                return self.cord_used + right
        return solution_cords

    def print_solution_cords(self, solution):
        '''
        This functions prints out the path of the solution
        in the correct format.
        '''
        print('PATH OF THE SOLUTION:')
        for pair in solution:
            print('  ' + str(pair))


class Maze:
    '''
    This class represents the Maze which is created into a 2d grid
    based on the user txt file.

    The class defines several methods and fields:
        check_board(): Ensures board is of the highest standards
        file_read(): reads user input file and puts into 2d grid
        find_start_end(): finds 'S' and 'E' xy_cords in grid
        get_maze(): returns grid
        make_tree(): constructs tree through xy_cords in grid
        build_tree(): begins recursive calls to create tree
        find_xy(): loops through grid and sets xy_cords
        dump_cells(): Prints coords based on user input
        dump_size(): sets height and wid of maze
        print_size(): Prints height and wid of maze
        build_solution_grid(): updates grid and prints solution w/ '.'
    '''

    def __init__(self):
        '''
        The constructor initalizes the grid, start cord, end_cord, xy_cord variables
        that will be updated through different functions in the class
        '''
        self.grid = []
        self.start_cord = []
        self.end_cord = []
        self.xy_cord = []

    def check_board(self):
        '''
        This function checks the maze to ensure there is one start and end
        position. Also making sure only valid characters are in the grid through
        a for loop
        '''
        if len(self.start_cord) > 1:
            print('ERROR: The map has more than one START position')
            exit()
        elif len(self.start_cord) == 0 or len(self.end_cord) == 0:
            print('ERROR: Every map needs exactly one START and exactly one END position')
            exit()
        elif len(self.end_cord) > 1:
            print('ERROR: The map has more than one END position')
            exit()
        valid_chars = ['#', 'S', 'E', ' ']
        test = False
        for row in self.grid:
            for word in row:
                if word not in valid_chars:
                    test = True
        if test:
            print('ERROR: Invalid character in the map')
            exit()

    def file_read(self, txt_file):
        '''
        This function takes the user input file name and uses
        a for loop to read split and append the list to the self.
        grid variable.
        '''
        maze = []
        try:
            with open(txt_file) as f:
                for line in f.read().splitlines():
                    maze.append(list(line))
        except FileNotFoundError:
            print('ERROR: Could not open file: ' + txt_file)
            exit()
        while len(maze[0]) > len(maze[-1]):
            maze[-1].append(' ')
        self.grid = maze

    def find_start_end(self):
        '''
        Returns the start and end coordniates of the maze through
        looping through the 2d grid.
        '''
        start_cord = []
        end_cord = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] == 'S':
                    start_cord.append((j,i))
                if self.grid[i][j] == 'E':
                    end_cord.append((j,i))
        self.start_cord = start_cord
        self.end_cord = end_cord

    def get_maze(self):
        '''
        Returns 2d grid creating from txt file.
        '''
        return self.grid

    def get_xy(self):
        '''
        Returns the xy coordniates.
        '''
        return self.xy_cord

    def make_tree(self, x, y, grid, depth, used_vals):
        '''
        Creates the tree by recursively calling the different directions
        by checking the four directions of every point on the grid. The grid
        is then updated to ' ' in order to stop the grid from looping around
        to the same points. The cord_pair set is also used to keep the recursive
        calls from exceeding depth. Finally, the tree is returned and used in the
        Tree class.
        '''
        tree_val = grid[y][x]
        tree = Tree(tree_val, x, y, depth)
        grid[y][x] = ' '
        up = None
        left = None
        right = None
        down = None
        cord_pair = (x, y)
        if cord_pair in used_vals:
            return None
        if y > 0 and grid[y - 1][x] != ' ':
            new_used_vals = used_vals.copy()
            new_used_vals.add((x, y))
            up = self.make_tree(x, y - 1, grid, depth + 1, new_used_vals)
        if y < len(grid) - 1 and grid[y + 1][x] != ' ':
            new_used_vals = used_vals.copy()
            new_used_vals.add((x, y))
            down = self.make_tree(x, y + 1, grid, depth + 1, new_used_vals)
        if x > 0 and grid[y][x - 1] != ' ':
            new_used_vals = used_vals.copy()
            new_used_vals.add((x, y))
            left = self.make_tree(x - 1, y, grid, depth + 1, new_used_vals)
        if x < len(grid[0]) - 1 and grid[y][x + 1] != ' ':
            new_used_vals = used_vals.copy()
            new_used_vals.add((x, y))
            right = self.make_tree(x + 1, y, grid, depth + 1, new_used_vals)
        grid[y][x] = tree.val
        tree.up = up
        tree.down = down
        tree.left = left
        tree.right = right
        return tree

    def build_tree(self):
        '''
        Initalizes the tree creation at the starting coordniates along with the grid, depth,
        and coordniates used.
        '''
        return self.make_tree(self.start_cord[0][0], self.start_cord[0][1], self.grid, 0, set())

    def find_xy(self):
        '''
        Builds a list of tuple xy cordniates of the maze.
        '''
        xy_cord = []
        for i in range(len(self.grid)):
            for j in range(len(self.grid[i])):
                if self.grid[i][j] != ' ':
                    xy_cord.append((j,i))
        self.xy_cord = xy_cord

    def dump_cells(self):
        '''
        Prints all coordniates in sorted order of the maze
        '''
        print('DUMPING OUT ALL CELLS FROM THE MAZE:')
        for xy in sorted(self.xy_cord):
            if xy == self.start_cord[0]:
                print('  ' + str(xy) + '    START')
            elif xy == self.end_cord[0]:
                print('  ' + str(xy) + '    END')
            else:
                print('  ' + str(xy))

    def dump_size(self):
        '''
        Finds and returns the size of the maze based
        on x and y coordnates in maze.
        '''
        wid = 0
        hei = 0
        for cord in self.xy_cord:
            if cord[0] > wid:
                wid = cord[0]
            if cord[1] > hei:
                hei = cord[1]
        return wid + 1, hei + 1

    def print_size(self, wid, hei):
        '''
        Prints the map size based on wid and hei.
        '''
        print('MAP SIZE:')
        print('  wid: ' + str(wid))
        print('  hei: ' + str(hei))

    def build_solution_grid(self, solution_cords):
        '''
        Creates a copy of the self.grid variable and updates the
        new solution_grid created based on the solution_coordniates
        variblae found in the Tree class. Finally the updated grid
        is printed in the correct format.
        '''
        solution_grid = []
        for row in self.grid:
            new_list = []
            for col in row:
                new_list.append(col)
            solution_grid.append(new_list)
        while len(solution_grid[0]) > len(solution_grid[-1]):
             solution_grid[-1].append(' ')
        for cord in solution_cords:
            if solution_grid[cord[1]][cord[0]] != 'S' and solution_grid[cord[1]][cord[0]] != 'E':
                solution_grid[cord[1]][cord[0]] = '.'
        print('SOLUTION:')
        for row in solution_grid:
            for col in row:
                print(col, end='')
            print()

def main():
    file_name = input()
    maze = Maze()
    maze.file_read(file_name)
    maze.find_start_end()
    maze.find_xy()
    maze.check_board()
    tree = maze.build_tree()
    maze.dump_size()
    user_input = input()
    if user_input == 'dumpCells':
        maze.dump_cells()
    elif user_input == 'dumpTree':
        print('DUMPING OUT THE TREE THAT REPRESENTS THE MAZE:')
        tree.dump_tree()
    elif user_input == 'dumpSolution':
        solution = tree.solution_cords()
        tree.print_solution_cords(solution)
    elif user_input == 'dumpSize':
        wid, hei = maze.dump_size()
        maze.print_size(wid, hei)
    elif user_input == '':
        solution_cords = tree.solution_cords()
        maze.build_solution_grid(solution_cords)
    else:
        print('ERROR: Unrecognized command NOT_A_VALID_COMMAND')

if __name__ == '__main__':
    main()