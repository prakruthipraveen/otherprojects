# Prakruthi Praveen
# Converting a given "barcode" image to text and viceversa

import copy
from abc import ABC, abstractmethod
import numpy as np

class BarcodeABC(ABC):
    @abstractmethod
    def scan(self, bc):
        pass

    @abstractmethod
    def read_text(self, text):
        pass

    @abstractmethod
    def generate_image_from_text(self):
        pass

    @abstractmethod
    def translate_image_to_text(self):
        pass

    @abstractmethod
    def display_text_to_console(self):
        pass

    @abstractmethod
    def display_image_to_console(self):
        pass



class BarcodeImage:
    MAX_WIDTH = 65
    MAX_HEIGHT = 30

    def __init__(self, str_data=None):
        '''initialize starting array'''
        self.image_data = np.full((BarcodeImage.MAX_HEIGHT, BarcodeImage.MAX_WIDTH), 0)
        if str_data is None:
            return

        '''Calculate placement: lower-left corner'''
        height = len(str_data)
        width = max(len(row) for row in str_data)

        small_row = height - 1
        for row in range(BarcodeImage.MAX_HEIGHT - 1, -1, -1):
            for col in range(BarcodeImage.MAX_WIDTH):
                if col > width - 1:
                    break
                if str_data[small_row][col] == '*':
                    self.image_data[row][col] = True
                else:
                    self.image_data[row][col] = False
            small_row -= 1
            if small_row < 0:
                break


    # --------- Mutators ---------
    def set_pixel(self, row, col, value):
        if 0 <= row < BarcodeImage.MAX_HEIGHT and 0 <= col < BarcodeImage.MAX_WIDTH:
            # print(row, col, value)
            self.image_data[row][col] = value
            return True
        return False

    # --------- Accessors ---------
    def get_pixel(self, row, col):
        if 0 <= row < BarcodeImage.MAX_HEIGHT and 0 <= col < BarcodeImage.MAX_WIDTH:
            return self.image_data[row][col]
        return False

    # --------- Optional helpers ---------
    def check_size(self, data):
        if data is None:
            return False
        if len(data) > BarcodeImage.MAX_HEIGHT:
            return False
        for row in data:
            if len(row) > BarcodeImage.MAX_WIDTH:
                return False
        return True

    def display_to_console(self):
        for row in self.image_data:
            print("".join('*' if pixel else ' ' for pixel in row))



class InfoBox(BarcodeABC):
    black = '*'
    white = ' '
    image = None
    actual_height = 0
    actual_width = 0

    def __init__(self, image=None, text=None):
        self.image = image
        self.text = text
        if image is not None:
            self.scan(image)
        if text is not None:
            self.read_text(text)
            self.BI = BarcodeImage()


    # Scan & Store Image ------------------
    def scan(self, image):
        copied_image = copy.deepcopy(image.image_data)
        InfoBox.actual_height = len(copied_image)
        InfoBox.actual_width = len(copied_image[-1])
        return True


    # Store Text ------------------
    def read_text(self, text):
        '''store text only'''
        if not isinstance(text, str):
            return False
        self.text = text
        return True

    # --------- Accessors ---------
    def get_actual_width(self):
        return InfoBox.actual_width

    def get_actual_height(self):
        return InfoBox.actual_width


    # Compute array width and height
    def compute_signal_height(self):
        '''Count black pixels on left column.'''
        height = 0
        bottom = BarcodeImage.MAX_HEIGHT - 1
        for row in range(bottom, -1, -1):
            if self.image is None:
                if self.BI.get_pixel(row, 0):
                    height += 1
                else:
                    break
            else:
                if self.image.get_pixel(row, 0):
                    height += 1
                else:
                    break
        return height


    def compute_signal_width(self):
        '''Count black pixels on bottom row.'''
        bottom = BarcodeImage.MAX_HEIGHT - 1
        width = 0
        for col in range(BarcodeImage.MAX_WIDTH):
            if self.image is None:
                if not self.BI.get_pixel(bottom, 0):
                    return 0
                if self.BI.get_pixel(bottom, col):
                    width += 1
                else:
                    break
            else:
                if not self.image.get_pixel(bottom, 0):
                    return 0
                if self.image.get_pixel(bottom, col):
                    width += 1
                else:
                    break
        return width


    def write_char_to_col(self, col, char):
        """Write an 8-bit integer vertically into column col."""
        ascii_val = ord(char)
        for bit in range(10):
            if bit == 9:
                if col % 2 == 0:
                    bit_val = 1
                else:
                    bit_val = 0
            elif bit == 0:
                bit_val = 1
            else:
                bit_val = (ascii_val >> bit-1) & 1
            self.BI.set_pixel(BarcodeImage.MAX_HEIGHT - 1 - bit, col, bool(bit_val))


    def generate_image_from_text(self):
        if self.text is None:
            return False
        if len(self.text) > BarcodeImage.MAX_WIDTH:
            print("Text is larger than barcode. Keep text less than 64 characters.")
            return False


        col = 0
        self.write_char_to_col(col, chr(int("11111111", 2)))
        col +=1
        for char in self.text:
            self.write_char_to_col(col, char)
            col +=1

        InfoBox.actual_width = len(self.text) + 2
        InfoBox.actual_height = 10

        return True

    # ------------------------------------------
    # Convert image --> text
    # ------------------------------------------
    def translate_image_to_text(self):
        result = ""
        bottom = BarcodeImage.MAX_HEIGHT - 1

        # Iterate columns 1 through actual_width-2
        for col in range(1, self.actual_width - 1):
            value = 0
            for bit in range(8):
                if self.image.get_pixel(bottom - 1 - bit, col):
                    value |= (1 << bit)
            result += chr(value)

        self.text = result
        return True

    # ------------------------------------------
    def display_text_to_console(self):
        print(self.text)


    def display_image_to_console(self):
        h = self.compute_signal_height()
        w = self.compute_signal_width()

        print("-" * (w + 2))
        for r in range(BarcodeImage.MAX_HEIGHT - h, BarcodeImage.MAX_HEIGHT):
            print("|", end="")
            for c in range(w):
                if self.image is None:
                    ch = InfoBox.black if self.BI.get_pixel(r, c) else InfoBox.white
                else:
                    ch = InfoBox.black if self.image.get_pixel(r, c) else InfoBox.white
                print(ch, end="")

            print("|")




def main():
    sImageIn = np.array([
        "* * * * * * * * * * * * * * *",
        "*                           *",
        "**********  *** *** *******  ",
        "* ***************************",
        "**    * *   * *  *   * *     ",
        "* **     ** **          **  *",
        "****** ****  **   *  ** ***  ",
        "****  **     *   *   * **   *",
        "***  *  *   *** * * ******** ",
        "*****************************"])

    sImageIn_2 = np.array([
        "* * * * * * * * * * * * * * *",
        "*                           *",
        "*** ** ******** ** ***** *** ",
        "*  **** ***************** ***",
        "* *  *    *      *  *  *  *  ",
        "*       ** **** *          **",
        "*    * ****  **    * * * *** ",
        "***    ***       * **    * **",
        "*** *   **  *   ** * **   *  ",
        "*****************************"])

    bc1 = BarcodeImage(sImageIn)
    ib1 = InfoBox(bc1)

    # First secret message
    ib1.translate_image_to_text()
    ib1.display_text_to_console()
    ib1.display_image_to_console()

    # second secret message
    bc2 = BarcodeImage(sImageIn_2)
    ib2 = InfoBox(bc2)
    ib2.translate_image_to_text()
    ib2.display_text_to_console()
    ib2.display_image_to_console()

    # create your own message
    text = "What a great resume builder this is!"
    ib3 = InfoBox(None, text)
    ib3.generate_image_from_text()
    ib3.display_text_to_console()
    ib3.display_image_to_console()



if __name__ == '__main__':
    main()