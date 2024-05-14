import life, tkinter as tk, random

SCALE = 400
root = tk.Tk()
root.title("Conway's Game of Life")
class LifeWindow(tk.Canvas):
    """
    Subclass of the Tkinter Canvas class.
    Its objects represent windows in which to view a particular grid of a Life object.
    """
    def __init__(self, world):
        """
        Given a Life object 'world', initializes a LifeWindow
        object which lets the user view the grid of the 'world'
        object.

        The LifeWindow object lets the user click on it to set
        or clear cells, as well as using certain keys to move the
        view across the grid and zooming in and out.

        The default background color is black, the default cell color is white,
        the default speed is 100, and the default zoom level is 20.
        """
        self.world = world
        self.zoom = 20
        self.is_running = False
        self.speed = 100
        self.coords = (0,0)
        self.bg_color = "#000000"
        self.cell_color = "#FFFFFF"
        super().__init__(root, width = 2 * SCALE, height = 2 * SCALE, 
                         bg = "#000000")
        self.bind("<Button>", self.on_click)
        self.grid(column = 1, row = 1, columnspan=30, rowspan=30)
        self.draw()

    def cell(self, x,y):
        """
        Helper method that, given 'int' cell coordinates 'x' and 'y',
        returns the value (1 = alive, 0 = dead) of the cell with those
        coordinates.
        """
        if self.world.world_type == 'infinite':
            return self.world.get_cell(x,y)[0]
        else:
            return self.world.get_cell(x,y)

    def draw(self):
        """
        Draws (or redraws) the whole LifeWindow object.
        """
        self.delete('all')
        cell_size = 2 * SCALE // self.zoom
        for x in range(self.zoom):
            for y in range(self.zoom):
                world_x = self.coords[0] + x
                world_y = self.coords[1] + y
                if self.world.world_type != "infinite":
                    world_x = world_x % self.world.size
                    world_y = world_y % self.world.size
                if self.cell(world_x, world_y):
                    self.create_rectangle(
                    x * cell_size, 
                    y * cell_size, 
                    (x + 1) * cell_size,
                    (y + 1) * cell_size,
                    fill = self.cell_color,
                    outline = self.bg_color)

    def on_click(self, event):
        """
        Helper method that, upon being called with some 'event' argument,
        (which is usually clicking on the grid), will do one of two things in 
        the grid:
        1. Set the cell where the event took place, if the cell was
        previously turned off, or
        2. Clear the cell where the event took place, if the cell was
        previously turned on.
        Afterwards, it will redraw the LifeWindow object.
        """
        cell_size = 2 * SCALE // self.zoom
        cell_x = self.coords[0] + int(event.x / cell_size)
        cell_y = self.coords[1] + int(event.y / cell_size)
        if self.world.world_type != 'infinite':
            cell_x = cell_x % self.world.size
            cell_y = cell_y % self.world.size
        if self.cell(cell_x, cell_y):
            self.world.set_cell(cell_x, cell_y, mode='clear')
        else:
            self.world.set_cell(cell_x, cell_y)
        self.draw()
        
    def take_step(self):
        """
        Helper method that updates the grid by a single time step and
        then redraws the LifeWindow object.
        """
        self.world.step()
        self.draw()

    def run(self, start_stop=False):
        """
        Given a Boolean 'start_stop' argument, does one of three
        things:
        1. If start_stop = True and the simulation was previously not
        running, it starts running by switching the value of the 'is_running'
        attribute and recursively calling itself.
        2. If start_stop = True and the simulation was previously running,
        it stops running by switching the value of the 'is_running' attribute.
        3. If start_stop = False, runs the simulation by taking one time step
        and recursively calling itself -- but only if the 'is_running' attribute
        is True.
        """
        if start_stop:
            self.is_running = not self.is_running
            self.after(1000 // self.speed, self.run)
        elif self.is_running:
            self.take_step()
            self.after(1000 // self.speed, self.run)

    def change_view(self, event):
        """
        Helper method that, upon being called with some 'event' argument,
        (which is usually pressing a key), will either move the current
        view of the grid (if the key pressed was one of W, A, S, or D)
        or zoom in/out (if the key pressed was either N or M).
        """
        x, y = self.coords
        match event.keysym:
            case 'a':
                self.coords = (x - 1, y)
            case 'd':
                self.coords = (x + 1, y)
            case 'w':
                self.coords = (x, y - 1)
            case 's':
                self.coords = (x, y + 1)
            case 'n':
                self.zoom += 1
            case 'm':
                self.zoom -= 1
        self.draw()

    def change_color(self, bg, cell):
        """
        Helper method that, upon being called with arguments
        'bg' and 'cell' (which are strings representing colors
        in RGB), will update the color scheme of the LifeWindow
        object, such that:
        1. The background color will now be 'bg'.
        2. The cell color will now be 'cell'.
        """
        self.bg_color, self.cell_color = bg, cell
        self.configure(bg=self.bg_color)
        self.draw()


global l
l = life.Life()
global w 
w = LifeWindow(l)

def new_world_window():
    """
    Creates a new 'New World' helper window, which lets the user
    create a new grid with an specified world type and size.
    """
    def create_world():
        global l
        global w
        type_list = ["infinite", "torus"]
        w_size = int(e1.get()) if e1.get() else 32
        w_type = type_list[var.get()]
        l = life.Life(world_type=w_type,size=w_size)
        w = LifeWindow(l)
        world_window.destroy()
        draw_widgets(w)

    w.is_running = False
    world_window = tk.Toplevel(root)
    world_window.title("New World")
    
    l1 = tk.Label(world_window,text="World Type:")
    l1.grid(column=0, row=0)

    
    var = tk.IntVar()
    r1 = tk.Radiobutton(world_window,
                        text="Infinite",
                        variable=var,
                        value=0)
    r1.grid()
    r2 = tk.Radiobutton(world_window,
                        text="Torus (finite)",
                        variable=var,
                        value=1)
    r2.grid()    
    l2 = tk.Label(world_window,text="Size (default: 32):")
    l2.grid()
    e1 = tk.Entry(world_window)
    e1.grid()
    b1 = tk.Button(world_window,text="Create World",command=create_world)
    b1.grid()

def new_speed_window():
    """
    Creates a new 'Set Speed' helper window, which lets the user choose the 
    simulation speed.
    """
    def set_speed():
        w.speed = int(e1.get())
        speed_window.destroy()
    w.is_running = False
    speed_window = tk.Toplevel(root)
    speed_window.title("Set Speed")

    l1 = tk.Label(speed_window,text="Speed: ")
    l1.grid(column=0,row=0)
    e1 = tk.Entry(speed_window)
    e1.grid(column=1,row=0)
    b1 = tk.Button(speed_window, text="Change speed", command=set_speed)
    b1.grid(column=1,row=1)

def new_stats_window():
    """
    Creates a new 'Stats' helper window, with relevant information about the 
    world, including Population, Time, the coordinates of the Upper left corner
    of the view, and the Speed.
    """
    w.is_running = False
    stats_window = tk.Toplevel(root)
    stats_window.title("Stats")

    lb1 = tk.Listbox(stats_window)
    lb1.insert(1, "Population:")
    lb1.insert(2, str(w.world.population))
    lb1.insert(3, "Time:")
    lb1.insert(4, str(w.world.time))
    lb1.insert(5, "Upper left corner:")
    lb1.insert(6, f"x= {w.coords[0]}, y = {w.coords[1]}")
    lb1.insert(7, "Speed:")
    lb1.insert(8, str(w.speed))
    lb1.grid()

def new_color_window():
    """
    Creates a new 'Color Scheme' helper window, which lets the user choose
    the background color and cell color in the grid (using RGB in Hexadecimal
    format).
    """
    def set_colors():
        bg = e1.get() if len(e1.get()) > 0 else w.bg_color
        cell = e2.get() if len(e2.get()) > 0 else w.cell_color
        w.change_color(bg, cell)
        color_window.destroy()

    w.is_running = False
    color_window = tk.Toplevel(root)
    color_window.title("Color Scheme")

    l1 = tk.Label(color_window,text="Background color: ")
    l1.grid(column=0,row=0)
    l2 = tk.Label(color_window,text="Cell color: ")
    l2.grid(column=0,row=1)
    e1 = tk.Entry(color_window)
    e1.grid(column=1,row=0)
    e2 = tk.Entry(color_window)
    e2.grid(column=1,row=1)
    b1 = tk.Button(color_window, text="Change Colors", command=set_colors)
    b1.grid(column=1,row=2)
    
def new_rand_window():
    """
    Creates a new 'Randomize Rectangle' helper window, which lets the user
    specify the coordinates of the upper-left corner and lower-right corner of a
    rectangle that will be randomly populated by alive cells, with a particular
    density.
    """
    def set_random():
        x1, x2 = int(e1.get()), int(e2.get())
        y1, y2 = int(e3.get()), int(e4.get())
        density = float(e5.get())
        for x in range(x1, x2 + 1):
            for y in range(y1, y2 + 1):
                val = random.randint(1,100)
                if val <= int(100 * density):
                    w.world.set_cell(x,y)
        rand_window.destroy()
        w.draw()

    w.is_running = False
    rand_window = tk.Toplevel(root)
    rand_window.geometry('270x120')
    rand_window.title("Randomize Rectangle")

    l1 = tk.Label(rand_window,text="x_1: ")
    l1.grid(column=0, row=0)
    e1 = tk.Entry(rand_window,width=9)
    e1.grid(column=1, row=0)
    l2 = tk.Label(rand_window,text="x_2: ")
    l2.grid(column=0, row=1)
    e2 = tk.Entry(rand_window,width=9)
    e2.grid(column=1, row=1)
    l3 = tk.Label(rand_window,text="y_1: ")
    l3.grid(column=2, row=0)
    e3 = tk.Entry(rand_window,width=9)
    e3.grid(column=3, row=0)
    l4 = tk.Label(rand_window,text="y_2: ")
    l4.grid(column=2, row=1)
    e4 = tk.Entry(rand_window,width=9)
    e4.grid(column=3, row=1)
    
    l5 = tk.Label(rand_window,text="Density: ")
    l5.grid(column=0, row=2)
    e5 = tk.Entry(rand_window,width=9)
    e5.grid(column=1, row=2)
    
    b1 = tk.Button(rand_window, 
                   text="Generate rectangle",
                   command=set_random)
    b1.grid(column=0, row=4, columnspan=4)

def draw_widgets(w):
    """
    Given a LifeWindow object 'w', creates all of the Tkinter
    widgets that are to the left of the LifeWindow.
    """
    b1 = tk.Button(root, text="Take step", command=w.take_step)
    b1.grid(column=0, row=4)

    b2 = tk.Button(root, text="Run/Stop", command=lambda : w.run(start_stop=True))
    b2.grid(column=0, row=5)

    b3 = tk.Button(root, text="Set speed", command=new_speed_window)
    b3.grid(column=0, row=6)

    b4 = tk.Button(root, text="Color Scheme", command=new_color_window)
    b4.grid(column=0, row=8)

    b5 = tk.Button(root, text="New World", command=new_world_window)
    b5.grid(column=0, row=1)

    b6 = tk.Button(root, text="Statistics", command=new_stats_window)
    b6.grid(column=0, row=10)

    b7 = tk.Button(root, text="Randomize", command=new_rand_window)
    b7.grid(column=0, row=11)
    root.bind("<KeyPress>", w.change_view)



draw_widgets(w)
root.mainloop()
