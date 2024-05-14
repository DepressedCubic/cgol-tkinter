def conway(cell_value, neighbor_sum):
    """
    Using the standard rules of Conway's Game of Life, determines the state
    of a cell in the next timestep, as a function of the current state
    'cell_value' (0 = 'dead', 1 = 'alive'), and an integer number of alive
    neighbors 'neighbor_sum'.

    Returns a Boolean as an output (False = 'dead', True = 'alive').
    """
    if (cell_value == 1) and (neighbor_sum < 2):
        return False
    elif (cell_value == 1) and (2 <= neighbor_sum <= 3):
        return True
    elif (cell_value == 1) and (neighbor_sum > 3):
        return False
    elif (cell_value == 0) and (neighbor_sum == 3):
        return True
    else:
        return False

class WrongWorldType(Exception):
    """
    Exception designed to be thrown in case the wrong class method is used for
    the particular world type: for instance, if the method 'print_chunk' is
    called on a finite world where the notion of chunk is not defined.
    """
    def __init__(self, correct_world_type):
        pass

class Life:
    chunk_size = 32

    def __init__(self, world_type='infinite', size=None):
        """
        Initializes an object of the Life class, which represents the grid where
        the simulation takes place.
        """
        self.world_type = world_type
        self.size = size
        self.time = 0
        self.population = 0
        if self.world_type != 'infinite':
            self.world = [self.size * [False] for row in range(self.size)]
        else:
            self.chunk_dict = {}
            self.chunk_count = 1
            self.add_chunk(0,0)

    def get_neighbors(self, x_coord, y_coord):
        """
        Given the coordinates of the cell (in the form of two 'int' arguments: 
        'x_coord' and 'y_coord'), returns a list of ordered pairs containing 
        the coordinates of all of its neighbors.

        As is usual in Conway's Game of Life, a Moore neighborhood (with eight
        neighbors) is assumed.
        """
        neighbor_vec = [
                (-1, -1), (-1, 0), (-1, 1), (0, -1),
                (0, 1), (1, -1), (1, 0), (1, 1)
        ]
        neighbors = [(x_coord + x, y_coord + y) for x, y in neighbor_vec]
        if self.world_type == 'torus':
            neighbors = [(x % self.size, y % self.size) for x, y in neighbors]
        return neighbors

    def add_chunk(self, x_index, y_index):
        """
        Given 'int' chunk coordinates 'x_index' and 'y_index', and
        assuming the chosen world type is 'infinite', initializes a new
        chunk in the chunk dictionary with key ('x_index', 'y_index') --
        but only if a chunk with the same key hadn't been initialized before.

        The key represents the chunk coordinates of the chunk.
        """
        assert self.world_type == 'infinite'
        if (x_index, y_index) not in self.chunk_dict:
            self.chunk_dict[(x_index, y_index)] = [
                Life.chunk_size * [False] for row in range(Life.chunk_size)
            ]
            self.chunk_count += 1
    
    def get_cell(self, x_coord, y_coord):
        """
        Given the 'int' coordinates ('x_coord', 'y_coord') of a cell, returns:
        Either an ordered pair (v, c) in the case of an infinite world, or just
        v in the case of a finite world, where v = 1 if the given cell is alive,
        and v = 0 if the given cell is dead.

        In the infinite case, c represents an ordered pair containing the chunk
        coordinates of the given cell (i.e. an appropriate key for the chunk
        dictionary).
        """
        if self.world_type == 'infinite':
            chunk = (x_coord // Life.chunk_size, y_coord // Life.chunk_size)
            if chunk in self.chunk_dict:
                chunk_x = x_coord % Life.chunk_size
                chunk_y = y_coord % Life.chunk_size
                return (int(self.chunk_dict[chunk][chunk_x][chunk_y]), chunk)
            else:
                return (0, chunk)
        else:
            return int(self.world[x_coord][y_coord])

    def copy_world(self):
        """
        Returns a Life object that is an identical copy of the current Life  
        object, with the caveat that the 'time' and 'population' attributes
        are reset to 0.
        """
        new_world = Life(self.world_type, self.size)
        if self.world_type == 'infinite':
            for chunk in self.chunk_dict.keys():
                new_world.chunk_dict[chunk] = [
                    [cell for cell in row] for row in self.chunk_dict[chunk]
                ]
            new_world.chunk_count = self.chunk_count
        else:
            new_world.world = [[cell for cell in row] for row in self.world]
        return new_world

    def set_cell(self, x_coord, y_coord, mode='set'):
        """
        Given the 'int' coordinates of a cell ('x_coord', 'y_coord') and
        a 'mode', does one of two things:
        1. If mode = 'set', which is the default, sets the cell with the given
        coordinates.
        2. If mode = 'clear', clears the cell with the given coordinates.

        If 'mode' = 'set', the world is 'infinite', and either:
        1. The cell with the given coordinates is in an uninitialized chunk, or
        2. The cell is adjacent to a cell in an uninitialized chunk
        Then, the uninitialized chunk is initialized.
        """
        if self.world_type == 'infinite':
            chunk = (x_coord // Life.chunk_size, y_coord // Life.chunk_size)
            chunk_x = x_coord % Life.chunk_size
            chunk_y = y_coord % Life.chunk_size
            self.add_chunk(*chunk)
            neighbors = self.get_neighbors(x_coord, y_coord)
            if mode == 'set':
                for i in neighbors:
                    self.add_chunk(*(self.get_cell(*i)[1]))
                if not self.chunk_dict[chunk][chunk_x][chunk_y]:
                    self.population += 1
                self.chunk_dict[chunk][chunk_x][chunk_y] = True
            elif mode == 'clear':
                if self.chunk_dict[chunk][chunk_x][chunk_y]:
                    self.population -= 1
                self.chunk_dict[chunk][chunk_x][chunk_y] = False
        else:
            if mode == 'set':
                if not self.world[x_coord % self.size][y_coord % self.size]:
                    self.population += 1
                self.world[x_coord % self.size][y_coord % self.size] = True
            elif mode == 'clear':
                if self.world[x_coord % self.size][y_coord % self.size]:
                    self.population -= 1
                self.world[x_coord % self.size][y_coord % self.size] = False
        
    def step(self):
        """
        Updates the grid by a single time step, using the rules of Conway's
        Game of Life.

        Also increments the 'time' attribute and updates the 'population'
        attribute.
        """
        self.time += 1
        if self.world_type == 'infinite':
            current_world = self.copy_world()
            for chunk_index in current_world.chunk_dict.keys():
                for chunk_x in range(Life.chunk_size):
                    for chunk_y in range(Life.chunk_size):
                        x_coord = Life.chunk_size * chunk_index[0] + chunk_x
                        y_coord = Life.chunk_size * chunk_index[1] + chunk_y
                        neighbors = current_world.get_neighbors(x_coord, y_coord)
                        neighbor_values = [current_world.get_cell(*n) for n in neighbors]
                        cell = current_world.get_cell(x_coord, y_coord)
                        new_cell = conway(cell[0], sum([n[0] for n in neighbor_values]))
                        if new_cell:
                            self.set_cell(x_coord, y_coord, mode='set')
                        else:
                            self.set_cell(x_coord, y_coord, mode='clear')
        else:
            current_world = self.copy_world()
            self.world = [
                [conway(
                    int(current_world.world[x][y]), 
                    sum([current_world.get_cell(i,j) 
                         for i,j in current_world.get_neighbors(x,y)])
                ) 
                for y in range(self.size) ]
                for x in range(self.size)
            ]
            self.population = sum([sum(self.world[x]) 
                                   for x in range(self.size)])

    def print_chunk(self, x_index, y_index):
        """
        Assumes that the world type is infinite -- otherwise, raises a
        WrongWorldType exception.

        Given an ordered pair of 'int' chunk coordinates ('x_index', 'y_index'),
        prints the chunk with the given coordinates in the terminal, without
        having to run the GUI.
        """
        if self.world_type != 'infinite':
            raise WrongWorldType('infinite')
        else:
            start_x = Life.chunk_size * x_index
            start_y = Life.chunk_size * y_index
            print('+' + (Life.chunk_size * '-') + '+')
            for x in range(start_x, start_x + Life.chunk_size):
                s = ''.join([
                    ('#' if self.get_cell(x, y)[0] else ' ')
                    for y in range(start_y, start_y + Life.chunk_size)
                ])
                print('|' + s + '|')
            print('+' + (Life.chunk_size * '-') + '+')
