import unittest
from test_path import PathTestCase

def start_test(file_name):
    file = open(file_name, 'r')
    lines = file.readlines()
    str_arr = []
    int_arr = []
    result = []
    for line in lines:
        if line[0] != '*':
            str_arr.append(line.split())
        else:
            int_arr = list(map(int, line[1:].split()))
            result.append({'str_arr' : str_arr.copy(), 'int_arr' : int_arr.copy()})
            int_arr.clear()
            str_arr.clear()
    file.close()
    return result

if __name__ == '__main__':
    suite = unittest.TestSuite()
    data = start_test('test.txt')
    for d in data:
        loadedtests = unittest.defaultTestLoader.loadTestsFromTestCase(PathTestCase)
        for t in loadedtests:
            t.str_arr = d['str_arr']
            t.int_arr = d['int_arr']
        suite.addTests(loadedtests)        

    print(unittest.TextTestRunner().run(suite))




