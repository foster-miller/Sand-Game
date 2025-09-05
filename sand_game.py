"""
    This program draws and simulates a world in which the user can control certain elements that take place, such as building a floor,
    sprinkling sand, and making it rain. The user selects which element they would like to use by pressing the key associated with
    the element. 
    
    Filename: sand_game.py
    Author: foster miller
    Date: 02/22/2024
    Collaborators: None
    Internet Source: NA
"""
import dudraw
import random

def level_water(world_list: list, empty_space: tuple, current_water: tuple):
    """
    switches values of two list elements - empty to water (0 to 3), and water to empty (3 to 0)
    parameters: (list, tuple, tuple)
    return: None
    """  
    world_list[empty_space[0]][empty_space[1]] = 3
    world_list[current_water[0]][current_water[1]] = 0

def level_sand(world_list: list, empty_space: tuple, current_sand: tuple):
    """
    switches values of two list elements - empty to sand (0 to 1), and sand to empty (1 to 0)
    parameters: (list, tuple, tuple)
    return: None
    """  
    world_list[empty_space[0]][empty_space[1]] = 1
    world_list[current_sand[0]][current_sand[1]] = 0

def swap_particle(world_list: list, row_y: int, col_x: int, elem_num: int):  # swaps two particles (above and below)
    """
    switches values of two list elements above and below eachother on the 2D list
    parameters: (list, tuple, tuple)
    return: None
    """  
    swapped_particle = world_list[row_y - 1][col_x]
    world_list[row_y - 1][col_x] = elem_num
    world_list[row_y][col_x] = swapped_particle

def process_element(world_list: list, row_y: int, col_x: int, particle: int, width: int):
    """
    decides the path of the current particle, should it go down, diagonally down and to the left or right, left or right
    parameters: (list, int, int, int, int)
    return: None
    """  
    if particle == 1:   # if Sand
        if row_y > 0 and world_list[row_y - 1][col_x] != 2:     # if not at lowest row AND particle below is not Floor
            if world_list[row_y - 1][col_x] != 1:   # if particle below is not sand
                swap_particle(world_list, row_y, col_x, particle)   
            elif row_y > 1 and world_list[row_y - 1][col_x] == 1 and world_list[row_y -2][col_x] == 1:  # if current particle is above the bottom two rows, and both particles below are sand
                if col_x - 1 >= 0 and (world_list[row_y - 2][col_x - 1] == 0 or world_list[row_y - 2][col_x - 1] == 3):   # if 2 rows down and to the left is empty or water
                    empty_space = (row_y - 2, col_x - 1)
                    current_sand = (row_y, col_x)
                    level_sand(world_list, empty_space, current_sand)
                elif col_x + 1 < width and (world_list[row_y - 2][col_x + 1] == 0 or world_list[row_y - 2][col_x + 1] == 3):    # if col + 1 is within index range (prevent error),  
                    empty_space = (row_y - 2, col_x + 1)                                                                        # and if 2 rows down and to the right is empty or water
                    current_sand = (row_y, col_x)
                    level_sand(world_list, empty_space, current_sand)

    elif particle == 3:     # if Water
        if row_y > 0:   # if not at lowest row
            current_water = (row_y, col_x)
            if world_list[row_y - 1][col_x] == 0:  # if particle below is empty
                swap_particle(world_list, row_y, col_x, particle)
            elif col_x - 1 >= 0 and world_list[row_y - 1][col_x - 1] == 0:     # check diagonally down and left
                empty_space = (row_y - 1, col_x - 1)
                level_water(world_list, empty_space, current_water)
            elif col_x + 1 < width and world_list[row_y - 1][col_x + 1] == 0:   # check diagonally down and right
                empty_space = (row_y - 1, col_x + 1)
                level_water(world_list, empty_space, current_water)
            elif col_x - 1 >= 0 and world_list[row_y][col_x - 1] == 0:     # check left
                empty_space = (row_y, col_x - 1)
                level_water(world_list, empty_space, current_water)
            elif col_x + 1 < width and world_list[row_y][col_x + 1] == 0:   # check right
                empty_space = (row_y, col_x + 1)
                level_water(world_list, empty_space, current_water)

def process_world(world_list: list, particles_list: list, width: int):    
    """
    breaks down a list of particles and calls the process_element function to process each particle
    parameters: (list, list, int)
    return: None
    """ 
    row_y = ''
    col_x = ''
    element = ''
    for i in range(len(particles_list)):
        row_y = particles_list[i][0]
        col_x = particles_list[i][1]
        element = particles_list[i][2]
        process_element(world_list, row_y, col_x, element, width)


def update_world(list_of_particles: list):  # updating colors on canvas
    """
    breaks down a list of particles and inputs the x, y, and particle type of each particle into the place_element function
    parameters: (list)
    return: None
    """ 
    for particle in list_of_particles:
        place_element(particle[0], particle[1], particle[2])

def element_to_number_converter(element: str) -> int:
    """
    takes the particle name and converts it to a number
    parameters: (str)
    return: int
    """ 
    if element == 'Sand':
        return 1
    elif element == 'Floor':
        return 2
    elif element == 'Water':
        return 3
    else: 
        return 0

def place_element(row_y: int, col_x: int, element: int):
    """
    decides what the element is and calls place_ function 
    parameters: (int, int, int)
    return: None
    """ 
    if element == 1:    # SAND
        place_sand(row_y, col_x)
    elif element == 2:  # FLOOR
        place_floor(row_y, col_x)
    elif element == 3:  # WATER
        place_water(row_y, col_x)

def place_water(row_y: int, col_x: int):
    """
    takes the x, y coordinates and draws a filled blue square on the canvas
    parameters: (int, int)
    return: None
    """ 
    dudraw.set_pen_color(dudraw.BLUE)
    dudraw.filled_square(col_x, row_y, .5)

def place_floor(row_y: int, col_x: int):
    """
    takes the x, y coordinates and draws a filled black square on the canvas
    parameters: (int, int)
    return: None
    """ 
    dudraw.set_pen_color(dudraw.BLACK)
    dudraw.filled_square(col_x, row_y, 1)

def place_sand(row_y: int, col_x: int):
    """
    takes the x, y coordinates and draws a filled brown square on the canvas
    parameters: (int, int)
    return: None
    """ 
    dudraw.set_pen_color_rgb(187,139,89)    # sand color
    dudraw.filled_square(col_x, row_y, .5)

def main():
    """
    sets up canvas, creates 2D list, creates animation loop
    parameters: None
    return: None
    """ 
    width = 600
    height = 750

    dudraw.set_canvas_size(width, height)
    dudraw.set_x_scale(0, width//5)
    dudraw.set_y_scale(0, height//5)
    
    new_world = [[0 for j in range(width//5)] for i in range(height//5)]  # creates new nested list of 0's
    current_world = list(new_world) # creates copy of new world

    particle_selected = 'Sand'
    key = ''
    while key != 'q':
        dudraw.clear(dudraw.LIGHT_GRAY)

        key = dudraw.next_key() # constantly checks for next_key, if nothing is pressed key = ''

        if key == 's':
            particle_selected = 'Sand'
        elif key == 'f':
            particle_selected = 'Floor'
        elif key == 'w':
            particle_selected = 'Water'

        # allows for current element selected to be displayed for user
        dudraw.set_pen_color(dudraw.BLACK)
        dudraw.set_font_size(25)
        dudraw.text(0.11 * width//5, 0.95 * height//5, particle_selected)

        if dudraw.mouse_is_pressed():
            x = int(dudraw.mouse_x())
            y = int(dudraw.mouse_y())
            if x >= 0 and x < (width//5) - 3 and y >= 0 and y < (height//5) - 3 and current_world[y][x] != 2:    # prevents from placing sand directly on floor (erasing floor) (kinda works)
                place_element(y, x, particle_selected)
                elem_number = element_to_number_converter(particle_selected)
                if elem_number == 2:    # floor (creates bigger block)
                    for i in range(-1, 2):
                        current_world[y + i][x + i] = elem_number # assigns appropriate element number to world list

                elif elem_number == 1:  # sand (sprinkle effect)
                    for i in range(3):
                        random_x = random.randint(-3, 3)
                        random_y = random.randint(-3, 3)
                        current_world[y + random_y][x + random_x] = elem_number
                
                elif elem_number == 3:  # water (sprinkle from top of canvas)
                    for i in range(3):
                        random_x = random.randint(-3, 3)
                        random_y = random.randint(-5, -1)
                        rain_y = (height//5) + random_y
                        rain_x = x + random_x
                        current_world[rain_y][rain_x] = elem_number
        
        particles_list = []     # creates and appends particles to a list if particle is not empty
        for i in range(height//5):
            for j in range(width//5):
                if current_world[i][j] > 0:
                    particles_list.append((i, j, current_world[i][j]))
        
        update_world(particles_list)    # changes look of canvas

        process_world(current_world, particles_list, width//5)    # changes particle numbers in current_world 2D list

        dudraw.show(20)
    particles_list.sort()

if __name__ == '__main__':
    main()