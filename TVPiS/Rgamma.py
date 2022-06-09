import re
import MemAlloc
import Hash
import Lexem
import GrammaticTree
import Log
from functools import reduce


memAlloc = MemAlloc.MemAlloc(1024)
h = Hash.Hash(memAlloc)

lex = Lexem.create_lexem(memAlloc)
gp = GrammaticTree.GramParse(lex, memAllock=memAlloc)
find, tree = gp.find_gram('<module>')
Log.save(str(tree))

print(find, tree)

if gp.i_lex < len(gp.lex):
    raise NameError(f"Error: unknown syntax '{gp.lex[gp.i_lex]}' line {gp.lex[gp.i_lex]}, token {gp.lex[gp.i_lex]} ")

print(tree.run('main', [7]))


