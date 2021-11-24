import unittest
from path import find_path

class PathTestCase(unittest.TestCase):

    def __init__(self, str_arr=[], int_arr=[]):
        super().__init__()
        self.str_arr = str_arr
        self.int_arr = int_arr
    
    def runTest(self):
        result = find_path(self.str_arr)
        self.assertEqual(result, self.int_arr)
