import re
import MemAlloc
import Hash
from functools import reduce


def get_all(file_name):
    with open(file_name, 'r') as infile:
        return reduce(lambda a, x: a.extend(x), [inline.split() for inline in infile])


class IterationTokenizer:
    def __init__(self, file_name):
        self.file_name = file_name
        self.infile = open(file_name, 'r')

    def __del__(self):
        self.infile.close()

    def __iter__(self):
        return self

    def __next__(self):
        line = self.infile.readline()
        if not line:
            raise StopIteration
        return line.split()


class Lexem:

    def __init__(self, my_type, me):
        self.type = my_type
        self.me = me
        # self.ident_dic = {}

    def __str__(self):
        return f'({self.type} {self.me})'



def create_lexem(memAllock, h):
    rezerv = {'return': 'return',
              'print': 'print',
              'float': 'float',
              'while': 'while',
              'break': 'break',
              'scan': 'scan',
              'void': 'void',
              'else': 'else',
              'call': 'call',
              'int': 'int',
              'def': 'def',
              'let': 'let',
              'if': 'if',
              '&&': '&&',
              '||': '||',
              '==': '==',
              '!=': '!=',
              '>=': '>=',
              '<=': '<=',
              '/': '/',
              '=': '=',
              '<': '>',
              '>': '<',
              '+': '+',
              '-': '-',
              '*': '*',
              '(': '(',
              ')': ')',
              '{': '{',
              '}': '}',
              ';': ';'}

    it = IterationTokenizer('Code\\1.txt')
    lex = []

    import re
    identifier = r'^\w[\w\d]*$'
    number = r'^[\d]+$|^[\d]+\.[\d]+$'
    identifier_id = 1

    for line in it:
        for word in line:
            try:
                lex.append(Lexem(rezerv[word], word))
            except KeyError as e:
                if re.match(number, word) is not None:
                    lex.append(Lexem('num', word))
                elif re.match(identifier, word) is not None:
                    try:
                        word_id = "".join(map(chr, h.get(word)))
                    except Exception as e:
                        if word == 'main':
                            word_id = 'main'
                        else:
                            h.update(word,  bytes(str(identifier_id), 'utf8'))
                            word_id = str(identifier_id)
                            identifier_id = identifier_id + 1
                    lex.append(Lexem('var', word_id))
                else:
                    raise NameError(f"Error: unknown lexem '{word}'")
    return lex