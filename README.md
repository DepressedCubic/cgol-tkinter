# Conway's Game of Life Simulator with Tkinter

A simulator of Conway's Game of Life using Tkinter, submitted
as a semester project for the Programming 1 class in Charles
University.

Conway's Game of Life is a mathematical game played on a 2D
grid of cells that can be either alive or dead, where only
the initial state of the game is specified and every step,
all the cells of the grid are updated simultaneously
according to the following rules:

- A cell's neighbors are defined as those cells
horizontally, vertically or diagonally adjacent to it
(this is called a Moore neighborhood, and has 8 cells).
- If a cell is alive and has less than 2 alive neighbors, 
it dies.
- If a cell is alive and has 2 or 3 alive neighbors,
it survives.
- If a cell is alive and has more than 3 alive neighbors,
it dies.
- If a cell is dead, it will turn alive exactly if it has 3
alive neighbors.

## User Instructions

- To run, make sure that the 'life.py' and 'view.py' files
are both in the same directory. Then, run 'view.py' using
Python 3.

- The grid that appears by default is infinite --
furthermore, the background color of the grid will be black
and the color of the (alive) cells white by default.

- To change the state of a particular cell (off -> on,
on -> off) it suffices to left-click on that particular
cell in the viewer.

- To move the viewer to a different part of the grid,
use the WASD keys (W = up, A = left, S = down, D = right).

- To zoom out, press the N key. To zoom in, press the M
key.

- To create a new world (with possibly different
parameters), click on the 'New World' button. The window
will allow you to choose the geometry of the new world
(which can either be infinite, or finite and toroidal),
and the size of the world (which must be a positive
integer N). If the chosen world type was finite, this will
create an NxN grid. If the chosen world type was infinite,
the chosen size will be ignored.

- To update the world by a single time step, click on the
'Take Step' button.

- To either run or stop the simulation, click on the
'Run/Stop' button.

- To set the speed of the simulation, click on the 'Set
speed' button. The window will allow you to choose the
simulation speed -- which must be a positive integer.
By default, the simulation speed is 100. Any value beyond
1000 will act indistinguishably from 1000 -- the computer
will simply run it as fast as it can.

- To change the color scheme of the viewer, click on the
'Color Scheme' button. The window will allow you to choose
the background color and (alive) cell color. The chosen
color must be written as RGB in Hexadecimal format,
prepended by a hash (#). For example, white would be
#FFFFFF.

- To view useful statistics about the simulation, click on
the 'Statistics' button, which will show four values:

    1. Population: the number of cells currently alive in
    the world.
    2. Time: the number of timesteps that have taken place
    since the beginning of the simulation.
    3. Upper left corner: contains the coordinates of the
    cell at the upper left corner of the viewer.
    4. Speed: speed of the simulation.

- To randomly populate a part of the world, click on the
'Randomize' button. The window will allow you to choose
the coordinates of the upper-left corner (in the form of
x_1 and y_1) and the lower-right corner (in the form of x_2
and y_2) of a rectangle that will be randomly populated by
alive cells. The 'density' is the probability that a given
cell inside this rectangle will be turned on. The density
must be written as a float between 0 and 1.

- As an interesting side note, the optimal density for a
randomized area in order to maximize the time it will take
to stabilize has been found to be around 0.375 (37.5%). So
this is a good value to try when using the 'Randomize
Rectangle' window.