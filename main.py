# defining custom errors to be used in exception handling
class Gameboard_FormatError(Exception):
    pass


class Gameboard_ValidityError(Exception):
    pass


class Gameboard_SolvabilityError(Exception):
    pass


# main solver
class Solver():
    def __init__(self):
        self.possible_placements = []
        self.vertical_rows = [[] for _ in range(9)]
        self.horizontal_rows = [[] for _ in range(9)]
        self.quadrants = [[] for _ in range(9)]
    
    def solve(self, gameboard_string) -> str:
        # checks for a valid gameboard consisting of 81 cells and numbers 0-9
        valid_chars = [str(num) for num in range(0,10)]
        if len(gameboard_string) != 81 or [char for char in gameboard_string if not char in valid_chars]:
            raise Gameboard_FormatError("a valid gameboard consisting of 81 cells going from the top left "
                                        "to the bottom right, and using '3' as an empty cell, must be given!")
        # checks to see if completed gameboard is given, if so, it returns it instantaneously
        if not '0' in gameboard_string:
            return gameboard_string
        

        # instanciates the rows and quadrants, indexes are found using some computational expressions
        for i, cell in enumerate(gameboard_string):
            vertical_index = i - ((i // 9) * 9)
            horizontal_index = i // 9
            quadrant_index = ((i - (i // 27) * -9) - ((i // 9) * 9)) // 3
            
            self.vertical_rows[vertical_index].append(cell)
            self.horizontal_rows[horizontal_index].append(cell)
            self.quadrants[quadrant_index].append(cell)


        # an extra layer of exception handing to check the validity of the gameboard by ensuring a number isn't repeated twice
        for quad in self.quadrants:
            chars_in_quad = {char for char in quad if char != '0'}
            for char in chars_in_quad:
                if quad.count(char) > 1:
                    raise Gameboard_ValidityError('a number seems to be repeated in a quadrant')
        for row in self.horizontal_rows:
            chars_in_row = {char for char in row if char != '0'}
            for char in chars_in_row:
                if row.count(char) > 1:
                    raise Gameboard_ValidityError('a number seems to be repeated in a row')
        for col in self.vertical_rows:
            chars_in_col = {char for char in col if char != '0'}
            for char in chars_in_col:
                if col.count(char) > 1:
                    raise Gameboard_ValidityError('a number seems to be repeated in a column')


        def update(num):
            # re-defining containers as part of the step-by-step process
            self.possible_placements = []
            self.vertical_rows = [[] for _ in range(9)]
            self.horizontal_rows = [[] for _ in range(9)]
            self.quadrants = [[] for _ in range(9)]
            

            # updates the rows and quadrants in order to be able to update the possible placements
            for i, cell in enumerate(gameboard_string):
                vertical_index = i - ((i // 9) * 9)
                horizontal_index = i // 9
                quadrant_index = ((i - (i // 27) * -9) - ((i // 9) * 9)) // 3
                
                self.vertical_rows[vertical_index].append(cell)
                self.horizontal_rows[horizontal_index].append(cell)
                self.quadrants[quadrant_index].append(cell)
            

            # updates the possible placements based on the number provided
            for i, cell in enumerate(gameboard_string):
                # if theres already a number in the cell, an empty list is appended, representing a filled cell
                if cell != '0':
                    self.possible_placements.append([])
                    continue
                
                placements = []
                quadrant_index = ((i - (i // 27) * -9) - ((i // 9) * 9)) // 3
                vertical_index = i - ((i // 9) * 9)
                horizontal_index = i // 9

                # if the number doesn't repeat itself in it's own rows or quadrant, then it's added as a possible placement
                if not str(num) in self.quadrants[quadrant_index]:
                    if not str(num) in self.vertical_rows[vertical_index]:
                        if not str(num) in self.horizontal_rows[horizontal_index]:
                            placements.append(num)
                self.possible_placements.append(placements)

            
            # filters through the quadrants of the possible placements, and if the number occurs more than once in it's quadrant, it gets invalidated
            quadrant_based_placements = [[] for _ in range(9)]
            for i, placement in enumerate(self.possible_placements):
                quadrant_index = ((i - (i // 27) * -9) - ((i // 9) * 9)) // 3
                quadrant_based_placements[quadrant_index].append(placement if placement else [])
            
            prohibited_quadrants = []
            for i, placement in enumerate(self.possible_placements):
                quadrant_index = ((i - (i // 27) * -9) - ((i // 9) * 9)) // 3

                if placement:
                    if quadrant_index in prohibited_quadrants:
                        self.possible_placements[i] = []
                    elif quadrant_based_placements[quadrant_index].count(placement) > 1:
                        prohibited_quadrants.append(quadrant_index)
                        self.possible_placements[i] = []



        # main solver loop
        while gameboard_string.count('0') > 0:
            # updates the possible placements individually per number through 1-9, checks it, and replaces the empty cell with it on the gameboard string if placeable
            is_placeable = False
            for number in range(1,10):
                update(number)

                for i, placement in enumerate(self.possible_placements):
                    if placement:
                        print(i, placement[0])
                        is_placeable = True
                        gameboard_string = gameboard_string[:i] + str(placement[0]) + gameboard_string[i + 1:]

            if not is_placeable:
                raise Gameboard_SolvabilityError('the gameboard cannot be solved in a systematic way, more complex/bruteforce methods are required!')
            
        return gameboard_string


s = Solver()
solved = s.solve('000000070640000905008560000000000096006895432520046817400658009067014358085207104')
print(solved)
