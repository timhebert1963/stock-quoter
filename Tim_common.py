import os

def clear_screen():
    clear_screen = lambda: os.system('cls')
    clear_screen()
    print('\n')
    print('\n')

# **** End of function clear_screen() **** #


def assign_banner_attributes(debug, *args):

    # assign string(s) passed in as args to string_list
    string_list = []

    for arg in args:
        string_list.append(arg)

    # 1. create banner_obect and pass in debug, cards, string_list
    # 2. create first and last row in banner_object
    # 3. create blank space row in banner_object
    # 4. create string list row in banner_object
    banner_object = Banner(debug, string_list)
    banner_object.create_first_and_last_row()
    banner_object.create_blank_space_row()
    banner_object.create_string_list()


    return banner_object

    # **** End of function assign_banner_attributes() **** #


def display_banner(debug, banner):

    ####################################################
    #
    #           PRINT THE BANNER
    #
    ####################################################

    # print the 1st row and 2nd row of banner
    print(banner.get_first_and_last_row())
    print(banner.get_blank_space_row())

    # print the strings in distance_banner.get_string_list()
    for i in range(len(banner.get_string_list())):
        print(banner.get_string_list()[i])
        print(banner.get_blank_space_row())

    # print the next to last and last row of banner
    print(banner.get_blank_space_row())
    print(banner.get_first_and_last_row())
    print('\n')
    print('\n')

    # **** End of display_banner() **** #


class Banner():
    '''
    class Banner() is a template used for creating different banners to display during the blackjack game.
    '''

    def __init__(self, debug, string_list):

        self.debug = debug

        self.row_length         = 100              # length of all banner rows
        self.first_and_last_row = ''              # 1st and last row of banner
        self.blank_space_row    = ''              # rows in banner with blank spaces
        self.string_list        = string_list     # a list of strings for string display

    # **** End of Banner.__init__() **** #


    def create_first_and_last_row(self):

        # create_first_and_last_row will create a string of asterisks.
        # the number of asterisks == self.row_length
        for i in range(self.row_length):
            self.first_and_last_row = self.first_and_last_row + '*'

    # **** End of Banner.create_first_and_last_row() **** #


    def get_first_and_last_row(self):

        # return the self.first_and_last_row to display in banner
        return self.first_and_last_row

    # **** End of Banner.get_first_and_last_row() **** #


    def create_blank_space_row(self):

        # create_blank_space_row will create a string of with an asterisks as 1st character and last character.
        # characters between 1st and last asterisks will be a " "
        for i in range(self.row_length):
            if i == 0 or i == self.row_length -1:
                self.blank_space_row = self.blank_space_row + "*"
            else:
                self.blank_space_row = self.blank_space_row + " "


    # **** End of Banner.create_blank_space_row() **** #


    def get_blank_space_row(self):

        # return self.blank_space_row to display in banner
        return self.blank_space_row

    # **** End of Banner.get_blank_space_row() **** #


    def create_string_list(self):

        # create_string_row() will take the strings stored in self.string_list and pad with " " so the strings
        # passed in as *args are placed in the middle of the self.row_length 
        # 
        # the 1st and last character of each string will be an asterisks*

        asterisk = "*"

        for i in range(len(self.string_list)):

            # number of spaces and/or characters between the first and last asterisk in the new_string
            num_spaces = self.row_length -2

            # determine number of " "es before string and after string
            before = int((num_spaces - len(self.string_list[i])) / 2)   # number of spaces "before" self.string_list[i]
            after  = num_spaces - (before + len(self.string_list[i]))   # number of spaces "after"  self.string_list[i]

            before_string_spaces = ''
            after_string_spaces  = ''

            for x in range(before):
                before_string_spaces = before_string_spaces + " "
            for x in range(after):
                after_string_spaces = after_string_spaces + " "

            self.string_list[i] = asterisk + before_string_spaces + self.string_list[i] + after_string_spaces + asterisk


    # **** End of Banner.create_string_list() **** #

    def get_string_list(self):

        # returns self.string_list for display in banner
        return self.string_list

    # **** End of Banner.get_string_list() **** #


# **** End of class Banner() **** #