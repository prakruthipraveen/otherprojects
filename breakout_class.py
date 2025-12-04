# Prakruthi Praveen
# **description of program**

import numpy as np
import traceback

class Breakout:
    def __init__(self, x = 3, y = 4, seed = None):
        np.random.seed(seed)
        self.field = np.random.randint(2, 99, size:=(x,y))
        self.broken = [0] * (x)

    # checks for divisible numbers, breaks them, and returns score
    def check_break(self, col, factor, depth):
        score = self.check_break_rec(0, col, factor, depth)
        multiplier = 2**(self.check_rows())
        return score * multiplier


    # recursively checks if numbers in each row are "broken"
    def check_break_rec(self, i, j, factor, depth):
        if not (0 <= i < self.field.shape[0] and 0 <= j < self.field.shape[1]):
            return 0
        else:
            value = self.field[i, j]
            if (i < 0 or i >= self.field.shape[0]) and (j < 0 or j >= self.field.shape[1]):
                return 0
            if factor < 2 or factor > 99:
                return 0
            # check if value is divisible by factor
            if value % factor != 0:
                return 0
            # check if broken using bitwise operation
            if self.broken[i] & (1 << j):
                return 0
            self.broken[i] |= (1 << j)
            # calculating score for this round
            score = factor * (i + 1)
            total_score = score
            for dj in (-1, 0, 1):
                total_score += self.check_break_rec(i + 1, j + dj, factor, depth + 1)
            return total_score


    # deletes row if entire row is found to be broken
    def check_rows(self):
        rows_removed = 0
        i=0
        while i < self.field.shape[0]:
            all_broken = True
            for j in range(self.field.shape[1]):
                if not self.broken[i] & (1 << j):
                    all_broken = False
            if all_broken:
                self.field = np.delete(self.field, i, axis=0)
                self.broken.pop(i)
                rows_removed += 1
                i -= 1
            i += 1
        return rows_removed

    # keeps the program running until all rows are broken
    def still_playing(self):
        return len(self.field) > 0

    # prints initial field and updates numbers as they "break"
    def print_field(self):
        if len(self.field) == 0:
            print("empty field")
            return
        for i in reversed(range(self.field.shape[0])):
            row_display = []
            for j in range(self.field.shape[1]):
                if self.broken[i] & (1 << j):
                    row_display.append("XX")
                else:
                    row_display.append(f"{self.field[i][j]:02d}")
            print(" ".join(row_display))

# --------- Main Program ---------
def main():
    my_field = Breakout(4, 5)
    score = 0
    while my_field.still_playing():
        my_field.print_field()
        col = input("Which column? ")
        factor = input("Which factor? ")
        new_score = my_field.check_break(int(col), int(factor), my_field.field.shape[0])
        score += new_score
        print("You got", new_score, "points this round for a total of", score, "points.")
    print("Thank you for playing!")

# --------- Sample Test ---------
def unit_test():
    errors = False
    my_field = Breakout(6, 5, 1)
    test = np.array([[39, 14, 74, 11, 77],
                 [7, 81, 66, 18, 3],
                 [78, 73, 8, 27, 52],
                 [22, 20, 86, 13, 30],
                 [31, 16, 52, 70, 89],
                 [89, 96, 98, 88, 15]])
    try:
        assert np.array_equal(my_field.field, test)
    except AssertionError:
        print("The board does not appear to be set up correctly")
        errors = True
    move_list = [(2, 2, 112), (0, 3, 18), (4, 1, 0), (0, 3, 0),
                 (1, 7, 21), (4, 11, 11), (5, 11, 0), (3, 11, 22), (4, 3, 18)]
    for i, move in enumerate(move_list):
        try:
            prev_broken = my_field.broken.copy()
            score = my_field.check_break(move[0], move[1], test.shape[0])
            new_broken = my_field.broken.copy()
            assert score == move[2]
        except AssertionError:
            print("Error in move", i, "column", move[0], "factor", move[1])
            my_field.broken = prev_broken
            print("Board looked like this before the move:")
            my_field.print_field()
            my_field.broken = new_broken
            print("And like this after")
            my_field.print_field()
            print("Reported score for the move was", score, " but should have been", move[2])
            errors = True
        except:
            print("Your program threw an error in move", i, "column", move[0], "factor", move[1])
            my_field.broken = prev_broken
            print("Board looked like this before the move:")
            my_field.print_field()
            errors = True

    if not errors:
        print("No errors were identified by the unit test.")
        print("You should still double check that your code meets spec.")
        print("You should also check that PyCharm does not identify any PEP-8 issues.")


if __name__ == "__main__":
    main()

if __name__ == "__main__":
    unit_test()
