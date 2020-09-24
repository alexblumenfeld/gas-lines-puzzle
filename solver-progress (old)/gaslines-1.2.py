import time
import tkinter as tk

class Node():
    def __init__(self):
        self.row = None
        self.col = None
        self.path_up = 0
        self.path_down = 0
        self.path_right = 0
        self.path_left = 0
        self.house = False
        self.house_num = 0
        self.house_stack = []
        self.dir_changes = 1
        self.utility = False

    def connected(self):
        if self.path_up or self.path_down or self.path_left or self.path_right:
            return True
        else:
            return False

class Board():
    def __init__(self, height, width):
        self.board = [[0] * width for i in range(height)]
        self.house_list = []
        self.utility_list = []
        self.height = height
        self.width = width
        
    def __repr__(self):
        node_rows = ['' for i in range(self.height)]
        for row in range(self.height):
            for col in range(self.width):
                if self.board[row][col].house:
                    node_rows[row] += str(self.board[row][col].house_num)
                elif self.board[row][col].utility:
                    node_rows[row] += '•'
                else:
                    node_rows[row] += 'o'
                if col != (self.width - 1):
                    if self.board[row][col].path_right == 1:
                        node_rows[row] += '-'
                    else:
                        node_rows[row] += ' '
        verts = ['' for i in range(self.height - 1)]
        for row in range(self.height - 1):
            for col in range(self.width):
                if col == (self.width - 1):
                    if self.board[row][col].path_down == 1:
                        verts[row] += '|'
                    else:
                        verts[row] += ' '
                elif self.board[row][col].path_down == 1:
                    verts[row] += '| '
                else:
                    verts[row] += '  '
        output = ''
        for i in range(self.height - 1):
            output += node_rows[i]
            output += '\n'
            output += verts[i]
            output += '\n'
        output += node_rows[self.height - 1]
        return output

    def create_nodes(self):
        for row in range(self.height):
            for col in range(self.width):
                self.board[row][col] = Node()
                self.board[row][col].row = row
                self.board[row][col].col = col
    
    # In progress: new input method where you type into a graphical template of the board
    # def prepare_game(self, desired_board):
    #     init_rows = desired_board.split('\n')
    #     proper_rows = []
    #     for row in init_rows:
    #         if '-' in row:
    #             proper_rows.append(row)
    #     for i in range(len(proper_rows)):
    #         for char in proper_rows[i]:
    #             if 

    def prepare_game(self, houses, utilities):
        for coord in houses:
            self.board[coord[0]][coord[1]].house = True
            self.board[coord[0]][coord[1]].house_num = houses[coord]
            self.house_list.append(self.board[coord[0]][coord[1]])
        for coord in utilities:
            self.board[coord[0]][coord[1]].utility = True
            self.utility_list.append(self.board[coord[0]][coord[1]])

        # OLD prepare_game() method
        # for row in range(self.height):
        #     for col in range(self.width):
        #         if self.board[row][col].house:
        #             # Normal order
        #             self.house_list.append(self.board[row][col])
        #             # Reverse order
        #             # self.house_list.insert(0,self.board[row][col])
        #         elif self.board[row][col].utility:
        #             self.utility_list.append(self.board[row][col])

    def fill(self, row, col, direction):
        if direction == 'l':
            self.board[row][col].path_left = 1
            self.board[row][col-1].path_right = 1
        elif direction == 'r':
            self.board[row][col].path_right = 1
            self.board[row][col+1].path_left = 1
        elif direction == 'd':
            self.board[row][col].path_down = 1
            self.board[row+1][col].path_up = 1
        elif direction == 'u':
            self.board[row][col].path_up = 1
            self.board[row-1][col].path_down = 1
        else:
            raise Exception("Invalid direction specified.")

    def unfill(self,row,col,direction):
        if direction == 'l':
            self.board[row][col].path_left = 0
            self.board[row][col-1].path_right = 0
        elif direction == 'r':
            self.board[row][col].path_right = 0
            self.board[row][col+1].path_left = 0
        elif direction == 'u':
            self.board[row-1][col].path_down = 0
            self.board[row][col].path_up = 0
        elif direction == 'd':
            self.board[row+1][col].path_up = 0
            self.board[row][col].path_down = 0
        else:
            raise Exception("Invalid direction specified.")
    
    def solve(self, speed='fast'):
        if self.house_list == []:
            print('No houses specified. No solution exists.')
            return False
        elif self.utility_list == []:
            print('No utilities specified. No solution exists.')
        else:
            result = self.solve_house(0, self.house_list[0], self.house_list[0],speed)
            if result == False:
                print('No solution found.')
            else:
                print('Solution found.')
            return result
    
    def solve_house(self, house_list_index, house, location, speed='fast'):
        # Base case: if the most recent move was valid AND we just reached a utility, return True
        if speed == 'slow':
            print(self)
            print('------------')
        if location.utility:
            if house_list_index == (len(self.house_list) - 1):
                return True
            else:
                if speed == 'slow':
                    time.sleep(0.1)
                return self.solve_house(house_list_index + 1, self.house_list[house_list_index + 1], \
                    self.house_list[house_list_index + 1], speed)
        else:
            for direction in ['u','r','d','l']:
                if self.valid_move(house, location, direction):
                    # Designate the node which we'll be connecting to in this move
                    next_location = self.next_node(location, direction)
                    # Fill in the move currently under consideration
                    self.fill(location.row,location.col,direction)
                    if house.house_stack != [] and house.house_stack[-1][2] != direction:
                        house.dir_changes += 1
                    house.house_stack.append((location.row, location.col, direction))
                    # Recursive case outcome 1: if the move under consideration led to an eventual failure, undo it
                    if speed == 'slow':
                        time.sleep(0.1)
                    if self.solve_house(house_list_index, house, next_location,speed) == False:
                        self.unfill(location.row, location.col, direction)
                        if len(house.house_stack) >= 2 and (house.house_stack[-2][2] != house.house_stack[-1][2]):
                            house.dir_changes -= 1
                        house.house_stack.pop()
                    #Recursive case outcome 2: if the move under consideration led to an eventual success, return True
                    else:
                        return True
        return False

    def valid_move(self, house, location, direction):
        # Can't go off the edge of the board
        if direction == 'u' and location.row == 0:
            return False
        elif direction == 'r' and location.col == self.width - 1:
            return False
        elif direction == 'd' and location.row == self.height - 1:
            return False
        elif direction == 'l' and location.col == 0:
            return False
        # Can't go in the same direction as the last path component (if this isn't the first component)
        elif house.house_stack != [] and house.house_stack[-1][2] == 'u' and direction == 'd':
            return False
        elif house.house_stack != [] and house.house_stack[-1][2] == 'r' and direction == 'l':
            return False
        elif house.house_stack != [] and house.house_stack[-1][2] == 'd' and direction == 'u':
            return False
        elif house.house_stack != [] and house.house_stack[-1][2] == 'l' and direction == 'r':
            return False
        # Can't make a direction change that would go over the house's house_num value
        elif house.house_stack != [] and (house.house_stack[-1][2] != direction and house.dir_changes == house.house_num):
            return False
        # Can't go to a node which already has a connection
        elif self.next_node(location,direction).connected() and (self.next_node(location, direction).utility == False):
            return False
        # Can't go right to a utility if we have too few direction changes
        elif (self.next_node(location,direction).utility and house.house_stack != []) and (house.house_stack[-1][2] == direction \
            and house.house_num > house.dir_changes):
            return False
        elif (self.next_node(location,direction).utility and house.house_stack != []) and (house.house_stack[-1][2] != direction \
            and house.house_num > house.dir_changes + 1):
            return False
        elif (self.next_node(location,direction).utility and house.house_stack == []) and (house.house_num > house.dir_changes):
            return False
        # Can't go to a house
        elif self.next_node(location, direction).house:
            return False
        else:
            return True

    # Define the node to which the current location will be connected
    def next_node(self, location, direction):
        upcoming = None
        if direction == 'u':
            upcoming = self.board[location.row-1][location.col]
        elif direction == 'r':
            upcoming = self.board[location.row][location.col+1]
        elif direction == 'd':
            upcoming = self.board[location.row+1][location.col]
        elif direction == 'l':
            upcoming = self.board[location.row][location.col-1]
        return upcoming

def setup(height, width, houses, utilities):
    new_board = Board(height, width)
    new_board.create_nodes()
    new_board.prepare_game(houses, utilities)
    return new_board

# DATA
real_height = 7
real_width = 7
real_houses = {(1,0):2, (2,0):2, (2,5):1, (3,0): 3, (3,3): 4, (3,6): 2, (4,2): 2, \
    (4,4): 2, (4,5): 2, (5,1): 2, (5,6): 3, (6,1): 2, (6,2): 2}
real_utilities = [(0,1), (1,3), (3,5), (4,0), (5,3)]

example_height = 7
example_width = 7
example_houses = {(0,0):6, (1,2):5, (1,3):2, (2,1): 2, (4,5): 5, (5,2): 3, (5,5): 2}
example_utilities = [(1,0), (2,4), (4,2), (4,3)]

test1_height = 8
test1_width = 7
test1_houses = {(1,5):2, (2,1): 2, (5,1): 3, (6,3): 1, (7,0): 3}
test1_utilities = [(1,3),(3,2),(4,4),(4,5),(6,2)]

test2_height = 8
test2_width = 7
test2_houses = {(1,1):5, (1,2): 1, (1,4): 1, (2,3): 5}
test2_utilities = [(1,3),(3,2),(6,3)]

test3_height = 8
test3_width = 7
test3_houses = {(1,1):11, (1,3):1, (2,3): 6}
test3_utilities = [(1,5),(5,4),(6,1)]

test4_height = 7
test4_width = 7
test4_houses = {(3,3):12}
test4_utilities = [(6,0)]

test5_height = 7
test5_width = 7
test5_houses = {(0,0):1, (0,5): 3, (1,5): 1, (2,3): 5, (5,3): 4, (6,0): 1, (6,4): 1}
test5_utilities = [(0,4),(1,0),(5,1),(5,5),(6,5)]

real2_height = 7
real2_width = 7
real2_houses = {(0,2):2, (0,5): 2, (1,1): 1, (2,0): 2, (2,3): 3, (3,0): 5, (3,2): 3, (4,0): 2, (4,1): 1, \
    (5,2): 2, (5,4): 2, (6,2): 2}
real2_utilities = [(0,1), (1,3), (1,6), (4,2), (6,1)]

# Run the program
game_board = setup(real2_height, real2_width, real2_houses, real2_utilities)
game_board.solve(speed='fast')
print(game_board)