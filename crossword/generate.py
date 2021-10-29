import sys

from crossword import *


class CrosswordCreator():

    def __init__(self, crossword):
        """
        Create new CSP crossword generate.
        """
        self.crossword = crossword
        self.domains = {
            var: self.crossword.words.copy()
            for var in self.crossword.variables
        }

    def letter_grid(self, assignment):
        """
        Return 2D array representing a given assignment.
        """
        letters = [
            [None for _ in range(self.crossword.width)]
            for _ in range(self.crossword.height)
        ]
        for variable, word in assignment.items():
            direction = variable.direction
            for k in range(len(word)):
                i = variable.i + (k if direction == Variable.DOWN else 0)
                j = variable.j + (k if direction == Variable.ACROSS else 0)
                letters[i][j] = word[k]
        return letters

    def print(self, assignment):
        """
        Print crossword assignment to the terminal.
        """
        letters = self.letter_grid(assignment)
        for i in range(self.crossword.height):
            for j in range(self.crossword.width):
                if self.crossword.structure[i][j]:
                    print(letters[i][j] or " ", end="")
                else:
                    print("█", end="")
            print()

    def save(self, assignment, filename):
        """
        Save crossword assignment to an image file.
        """
        from PIL import Image, ImageDraw, ImageFont
        cell_size = 100
        cell_border = 2
        interior_size = cell_size - 2 * cell_border
        letters = self.letter_grid(assignment)

        # Create a blank canvas
        img = Image.new(
            "RGBA",
            (self.crossword.width * cell_size,
             self.crossword.height * cell_size),
            "black"
        )
        font = ImageFont.truetype("assets/fonts/OpenSans-Regular.ttf", 80)
        draw = ImageDraw.Draw(img)

        for i in range(self.crossword.height):
            for j in range(self.crossword.width):

                rect = [
                    (j * cell_size + cell_border,
                     i * cell_size + cell_border),
                    ((j + 1) * cell_size - cell_border,
                     (i + 1) * cell_size - cell_border)
                ]
                if self.crossword.structure[i][j]:
                    draw.rectangle(rect, fill="white")
                    if letters[i][j]:
                        w, h = draw.textsize(letters[i][j], font=font)
                        draw.text(
                            (rect[0][0] + ((interior_size - w) / 2),
                             rect[0][1] + ((interior_size - h) / 2) - 10),
                            letters[i][j], fill="black", font=font
                        )

        img.save(filename)

    def solve(self):
        """
        Enforce node and arc consistency, and then solve the CSP.
        """
        self.enforce_node_consistency()
        self.ac3()
        return self.backtrack(dict())

    def enforce_node_consistency(self):
        """
        Update `self.domains` such that each variable is node-consistent.
        (Remove any values that are inconsistent with a variable's unary
         constraints; in this case, the length of the word.)
        """
        # Loop through every variable
        for var in self.crossword.variables:
            # Loop through every word in the dictionary
            for word in self.crossword.words:
                # Check if the word is longer than the variable.lenght and if true, remove the word from the variable domain
                if len(word) != var.length:
                    self.domains[var].remove(word)
        return

    def check_arc_consinstancy(self, x, y, word_x, word_y):
        """
        Check if the words assigned to two variable respect the existing binary requirements
        """
        # Check if there is some overlaps to consider
        overlap = self.crossword.overlaps[x, y]
        if not overlap:
            return True

        # Check that the word overlaps accordingly to the requirement
        i, j = overlap
        if word_x[i] == word_y[j]:
            return True
        else:
            return False

    def revise(self, x, y):
        """
        Make variable `x` arc consistent with variable `y`.
        To do so, remove values from `self.domains[x]` for which there is no
        possible corresponding value for `y` in `self.domains[y]`.

        Return True if a revision was made to the domain of `x`; return
        False if no revision was made.
        """
        # Declare some useful variables
        overlap = self.crossword.overlaps[x, y]
        revised = False
        word_to_remove = []

        # Chek if there is some overlaps between the variables. If not, simply return False
        if not overlap:
            return revised
        else:
            # Loop through every word in the variable domain
            i, j = overlap
            is_value_possible = False
            for word_x in self.domains[x]:
                # Check if consinsency is manteined for the variable y with that choice of x. If not, remove the word from the domain of X and turn revised to True
                for word_y in self.domains[y]:
                    if word_x[i] == word_y[j] and word_x != word_y:
                        is_value_possible = True
                        break
            if not is_value_possible:
                word_to_remove.append(word_x)
                revised = True

            # Remove the words from the domain
            # Note: I was trying to do that without a for loop, but I think there's a better solution. This seems a bit strange logically.  
            self.domains[x] = [w for w in self.domains[x] if w not in word_to_remove]

            # Exit the function and return True if some revision was made
            return revised


    def ac3(self, arcs=None):
        """
        Update `self.domains` such that each variable is arc consistent.
        If `arcs` is None, begin with initial list of all arcs in the problem.
        Otherwise, use `arcs` as the initial list of arcs to make consistent.

        Return True if arc consistency is enforced and no domains are empty;
        return False if one or more domains end up empty.
        """
        # Declare an empty queue
        queue = []
        # Check if some arcs value have been passed, otherwise create the queue based on all the overlaps
        if arcs == None:
            for arc in self.crossword.overlaps:
                queue.append(arc)
        else:
            queue = arcs
        
        # Loop while the queue have some arc to consider
        while len(queue) > 0:
            # Unqueue an arc
            xy = queue.pop(0)
            x = xy[0]
            y= xy[1]

            # Check arc consinstancy and add x neighbord to the queue if some revision was made
            if self.revise(x,y):
                if len(self.domains[x]) == 0:
                    return False
                else:
                    for z in self.crossword.neighbors(x):
                        if z != y:
                            queue.append((z,x))

        return True
        

    def assignment_complete(self, assignment):
        """
        Return True if `assignment` is complete (i.e., assigns a value to each
        crossword variable); return False otherwise.
        """
        # Loop through every variables in the crosswords
        for variable in self.crossword.variables:
            # Check if that variable exist in assignment
            if variable not in assignment:
                return False
            # Check if the word assigned to the variable is a word from the dictionary
            if assignment[variable] not in self.crossword.words:
                return False
        
        return True

    def consistent(self, assignment):
        """
        Return True if `assignment` is consistent (i.e., words fit in crossword
        puzzle without conflicting characters); return False otherwise.
        """
        # Declare a list to keep record of every word into the assignment
        assignment_words = []

        # Loop through every word in assignment
        for variable in assignment:
            word = assignment[variable]

            # Check if the word have been arleady used
            if word in assignment_words:
                return False
            else:
                assignment_words.append(word)
            
            # Check if lenght size is respected for every variables
            if len(word) != variable.length:
                return False

            # Check if consistancy with neighboard is respected
            for neighbor in self.crossword.neighbors(variable):
                if neighbor in assignment:
                    if not self.check_arc_consinstancy(variable, neighbor, word, assignment[neighbor]):
                        return False
        
        # If no inconsistancy are found, return True
        return True


    def order_domain_values(self, var, assignment):
        """
        Return a list of values in the domain of `var`, in order by
        the number of values they rule out for neighboring variables.
        The first value in the list, for example, should be the one
        that rules out the fewest values among the neighbors of `var`.
        """
        # Declare a dict to store the counters for each words
        counter = {}
        for word in self.domains[var]:
            counter[word] = 0

        # Loop through the possible values(words) into var domain
        for word in self.domains[var]:
            # Loop through every neighbors
            for neighbor in self.crossword.neighbors(var):
                #Loop through every possible values(words) into neighbor domain
                for n_word in self.domains[neighbor]:
                    # Check if the word is still viable (does not conflict with binary requirements)
                    # If the word is ruled out, update the counter for the "word" key
                    if not self.check_arc_consinstancy(var, neighbor, word, n_word):
                        counter[word] += 1

       # Create a list of ordered values(words), ordered by the counter(number of words removed by neighbors domains)
        ordered_values = sorted(counter.keys(), key = lambda v : v[1])

        return ordered_values

    def select_unassigned_variable(self, assignment):
        """
        Return an unassigned variable not already part of `assignment`.
        Choose the variable with the minimum number of remaining values
        in its domain. If there is a tie, choose the variable with the highest
        degree. If there is a tie, any of the tied variables are acceptable
        return values.
        """
        # Declare a list and populate it with every variable that is not yet assigned
        possible_var = []
        for variable in self.domains:
            if variable not in assignment:
                possible_var.append(variable)

        # Order the variable list by two key: the number of remaining values in its domain and the number of neighbors
        possible_var.sort(key = lambda v: (len(self.domains[v]), -(len(self.crossword.neighbors(v)))))
        var = possible_var[0]
        return var

    def backtrack(self, assignment):
        """
        Using Backtracking Search, take as input a partial assignment for the
        crossword and return a complete assignment if possible to do so.

        `assignment` is a mapping from variables (keys) to words (values).

        If no assignment is possible, return None.
        """
        # Check if the assignment is complete, and if True, return it
        if self.assignment_complete(assignment):
            return assignment

        # Select an unassigned var (sorted)
        var = self.select_unassigned_variable(assignment)
        # Try to assign word after word from the variable domains
        for word in self.order_domain_values(var, assignment):
            assignment[var] = word
            # Check if assignment is still consistent
            if self.consistent(assignment):
                # Recursively run backtrack to see if assignments are still possible
                # If yes, return the resulting completed assignment
                result = self.backtrack(assignment)
                if result != None:
                    return result

            # If the assignment is not consistend or recursive backtracking is not possible, remove the word from the assignment and try another one
            # Note: Just set to None the value is not ok, so I'll use del
            del assignment[var]

        # If no assignment is possible, return None
        return None


def main():

    # Check usage
    if len(sys.argv) not in [3, 4]:
        sys.exit("Usage: python generate.py structure words [output]")

    # Parse command-line arguments
    structure = sys.argv[1]
    words = sys.argv[2]
    output = sys.argv[3] if len(sys.argv) == 4 else None

    # Generate crossword
    crossword = Crossword(structure, words)
    creator = CrosswordCreator(crossword)
    assignment = creator.solve()

    # Print result
    if assignment is None:
        print("No solution.")
    else:
        creator.print(assignment)
        if output:
            creator.save(assignment, output)


if __name__ == "__main__":
    main()
