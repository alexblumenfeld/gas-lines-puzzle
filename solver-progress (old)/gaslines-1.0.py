class Node():
    def __init__(self):
        self.up = None
        self.down = None
        self.left = None
        self.right = None
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
                if col != 0:
                    self.board[row][col].left = self.board[row][col-1]
                if col != 6:
                    self.board[row][col].right = self.board[row][col+1]
                if row != 0:
                    self.board[row][col].up = self.board[row-1][col]
                if row != 6:
                    self.board[row][col].down = self.board[row+1][col]
    def prepare_game(self):
        # THE REAL PUZZLE
        self.board[0][1].utility = True
        self.board[1][0].house = True
        self.board[1][0].house_num = 2
        self.board[1][3].utility = True
        self.board[2][0].house = True
        self.board[2][0].house_num = 2
        self.board[2][5].house = True
        self.board[2][5].house_num = 1
        self.board[3][0].house = True
        self.board[3][0].house_num = 3
        self.board[3][3].house = True
        self.board[3][3].house_num = 4
        self.board[3][5].utility = True
        self.board[3][6].house = True
        self.board[3][6].house_num = 2
        self.board[4][0].utility = True
        self.board[4][2].house = True
        self.board[4][2].house_num = 2
        self.board[4][4].house = True
        self.board[4][4].house_num = 2
        self.board[4][5].house = True
        self.board[4][5].house_num = 2
        self.board[5][1].house = True
        self.board[5][1].house_num = 2
        self.board[5][3].utility = True
        self.board[5][6].house = True
        self.board[5][6].house_num = 3
        self.board[6][1].house = True
        self.board[6][1].house_num = 2
        self.board[6][2].house = True
        self.board[6][2].house_num = 2
        
        # THE EXAMPLE
        # self.board[0][0].house = True
        # self.board[0][0].house_num = 6
        # self.board[1][0].utility = True
        # self.board[1][2].house = True
        # self.board[1][2].house_num = 5
        # self.board[1][3].house = True
        # self.board[1][3].house_num = 2
        # self.board[2][1].house = True
        # self.board[2][1].house_num = 2
        # self.board[2][4].utility = True
        # self.board[4][2].utility = True
        # self.board[4][3].utility = True
        # self.board[4][5].house = True
        # self.board[4][5].house_num = 5
        # self.board[5][2].house = True
        # self.board[5][2].house_num = 3
        # self.board[5][5].house = True
        # self.board[5][5].house_num = 2

        for row in range(7):
            for col in range(7):
                if self.board[row][col].house:
                    self.house_list.append(self.board[row][col])

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
    
    def solve(self):
        # FIRST TEST: Solve for just the first house in the list
        result = self.solve_house(0, self.house_list[0], self.house_list[0])
        return result
    
    def solve_house(self, house_list_index, house, location):
        # Base case: if the most recent move was valid AND we just reached a utility, return True
        if location.utility:
            if house_list_index == (len(self.house_list) - 1):
                return True
            else:
                return self.solve_house(house_list_index + 1, self.house_list[house_list_index + 1], \
                    self.house_list[house_list_index + 1])
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
                    if self.solve_house(house_list_index, house, next_location) == False:
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
        if direction == 'u' and location.up == None:
            return False
        elif direction == 'r' and location.right == None:
            return False
        elif direction == 'd' and location.down == None:
            return False
        elif direction == 'l' and location.left == None:
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

def setup():
    new_board = Board(7,7)
    new_board.create_nodes()
    new_board.prepare_game()
    return new_board

game_board = setup()
game_board.solve()
print(game_board)