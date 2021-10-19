import itertools
import random

class Minesweeper():
    """
    Minesweeper game representation
    """

    def __init__(self, height=8, width=8, mines=8):

        # Set initial width, height, and number of mines
        self.height = height
        self.width = width
        self.mines = set()

        # Initialize an empty field with no mines
        self.board = []
        for i in range(self.height):
            row = []
            for j in range(self.width):
                row.append(False)
            self.board.append(row)

        # Add mines randomly
        while len(self.mines) != mines:
            i = random.randrange(height)
            j = random.randrange(width)
            if not self.board[i][j]:
                self.mines.add((i, j))
                self.board[i][j] = True

        # At first, player has found no mines
        self.mines_found = set()

    def print(self):
        """
        Prints a text-based representation
        of where mines are located.
        """
        for i in range(self.height):
            print("--" * self.width + "-")
            for j in range(self.width):
                if self.board[i][j]:
                    print("|X", end="")
                else:
                    print("| ", end="")
            print("|")
        print("--" * self.width + "-")

    def is_mine(self, cell):
        i, j = cell
        return self.board[i][j]

    def nearby_mines(self, cell):
        """
        Returns the number of mines that are
        within one row and column of a given cell,
        not including the cell itself.
        """

        # Keep count of nearby mines
        count = 0

        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Update count if cell in bounds and is mine
                if 0 <= i < self.height and 0 <= j < self.width:
                    if self.board[i][j]:
                        count += 1

        return count

    def won(self):
        """
        Checks if all mines have been flagged.
        """
        return self.mines_found == self.mines


class Sentence():
    """
    Logical statement about a Minesweeper game
    A sentence consists of a set of board cells,
    and a count of the number of those cells which are mines.
    """

    def __init__(self, cells, count):
        self.cells = set(cells)
        self.count = count

    def __eq__(self, other):
        return self.cells == other.cells and self.count == other.count

    def __str__(self):
        return f"{self.cells} = {self.count}"

    def known_mines(self):
        """
        Returns the set of all cells in self.cells known to be mines.
        """
        # If the count is equal to the number of cells in the set, that means that every cell in the set is a mine
        if len(self.cells) == self.count:
            return self.cells
        else:
            return None

    def known_safes(self):
        """
        Returns the set of all cells in self.cells known to be safe.
        """
        # If the count is zero, that means that every cell in the set is safe
        if self.count == 0:
            return self.cells
        else:
            return None
        
    def mark_mine(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be a mine.
        """
        # Check if the cell is in the set
        if cell in self.cells:
            # Remove the cell from the set and remove 1 from the minecount to mantain the sentence logic true
            self.cells.remove(cell)
            self.count -= 1
            return
        else:
            return

    def mark_safe(self, cell):
        """
        Updates internal knowledge representation given the fact that
        a cell is known to be safe.
        """
        # Check if the cell is in the set        
        if cell in self.cells:
            # Remove the cell from the set (the logic is not compromised)
            self.cells.remove(cell)
            return
        else:
            return


class MinesweeperAI():
    """
    Minesweeper game player
    """

    def __init__(self, height=8, width=8):

        # Set initial height and width
        self.height = height
        self.width = width

        # Keep track of which cells have been clicked on
        self.moves_made = set()

        # Keep track of cells known to be safe or mines
        self.mines = set()
        self.safes = set()

        # List of sentences about the game known to be true
        self.knowledge = []

    def mark_mine(self, cell):
        """
        Marks a cell as a mine, and updates all knowledge
        to mark that cell as a mine as well.
        """
        self.mines.add(cell)
        for sentence in self.knowledge:
            sentence.mark_mine(cell)

    def mark_safe(self, cell):
        """
        Marks a cell as safe, and updates all knowledge
        to mark that cell as safe as well.
        """
        self.safes.add(cell)
        for sentence in self.knowledge:
            sentence.mark_safe(cell)
    
    def check_inference(self):
        """
        Iterate through the KB and elaborate any possible inference
        """
        # Set a counter
        update_count = 0
        
        mine_set = set()
        safe_set = set()

        # Iterate through every sentences in the KB
        for sentence in self.knowledge:
            # Check if is infered a new mine cell. If so, add 1 to the counter and save the mines cordinates into a new set
            if sentence.known_mines() != None:
                update_count += 1
                for mine in sentence.known_mines():
                    mine_set.add(mine)
           
            if sentence.known_safes() != None:
            # Check if is infered a new safe cell. If so, add 1 to the counter and save the safes cordinates into a new set
                update_count += 1
                for safe in sentence.known_safes():
                    safe_set.add(safe)

        # Iterate over the new discovered mine and safe set and update the knowledge accordingly
        for mine in mine_set:
            self.mark_mine(mine)

        for safe in safe_set:
            self.mark_safe(safe)

        # Clean the blank sentences
        for sentence in self.knowledge:
            if len(sentence.cells) == 0 and sentence.count == 0:
                self.knowledge.remove(sentence)

        # Check if we made some new inference. 
        # If so, re-run the check_inference function to see if some new inference is now possible. 
        # Otherwise, break the loop and return (we can't discover anything new for now).
        if update_count != 0:
            self.check_inference()
        else:
            return
        

    def add_knowledge(self, cell, count):
        """
        Called when the Minesweeper board tells us, for a given
        safe cell, how many neighboring cells have mines in them.

        This function should:
            1) mark the cell as a move that has been made
            2) mark the cell as safe
            3) add a new sentence to the AI's knowledge base
               based on the value of `cell` and `count`
            4) mark any additional cells as safe or as mines
               if it can be concluded based on the AI's knowledge base
            5) add any new sentences to the AI's knowledge base
               if they can be inferred from existing knowledge
        """
        # 1) Mark the cell as a move that has been made
        self.moves_made.add(cell)

        # 2) Mark the cell as safe
        if cell not in self.safes:
            self.mark_safe(cell)
        
        # 3) Add a new sentence to the AI's knowledge base based on the value of `cell` and `count`
        # Create blank sentence and set the count
        tmp = Sentence({}, count)
        # Loop over all cells within one row and column
        for i in range(cell[0] - 1, cell[0] + 2):
            for j in range(cell[1] - 1, cell[1] + 2):

                # Ignore the cell itself
                if (i, j) == cell:
                    continue

                # Add cell to the nearby list if cell in bounds and it is not undetermined
                if 0 <= i < self.height and 0 <= j < self.width:
                    # If we know the neighboard is a mine, there's no point into adding in sentence, 
                    # but we have to substract 1 from the minecount to mantain true the sentence
                    # This long comment commemorize the braveness of this bug, that resist through too many hours of my debugging <3
                    if (i, j) in self.mines:
                        tmp.count -= 1
                    elif (i, j) not in self.safes and (i, j) not in self.mines:
                        tmp.cells.add((i, j))
                        
        # Add the sentence to the knowledge
        self.knowledge.append(tmp)

        # 4) Mark any additional cells as safe or as mines if it can be concluded based on the AI's knowledge base
        # 5) add any new sentences to the AI's knowledge base if they can be inferred from existing knowledge 
        self.check_inference()

    def make_safe_move(self):
        """
        Returns a safe cell to choose on the Minesweeper board.
        The move must be known to be safe, and not already a move
        that has been made.

        This function may use the knowledge in self.mines, self.safes
        and self.moves_made, but should not modify any of those values.
        """

        # Loop for each cell in the board
        for i in range(self.height):
            for j in range(self.width):
                # Check if the cell is a viable move and if it is a known safe cell. If true, return the "move"
                if (i, j) not in self.moves_made and (i, j) in self.safes:
                    return (i, j)

        else:
            return None

    def make_random_move(self):
        """
        Returns a move to make on the Minesweeper board.
        Should choose randomly among cells that:
            1) have not already been chosen, and
            2) are not known to be mines
        """
        # Create a list element for possible moves
        possible_move = []
        # Loop for each cell in the board
        for i in range(self.height):
            for j in range(self.width):
                # Check if the cell is a viable move and if it is not a know mines. If true, add it to the list of possible_moves
                if (i, j) not in self.safes and (i, j) not in self.mines:
                    possible_move.append((i, j))
        
        # Check if there is at least one possible_move available
        if not possible_move:
            return None
        # Extract and return a random move from the possibles one
        else:
            sorted_move = random.choice(possible_move)
            return sorted_move
