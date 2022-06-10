import re
import MemAlloc
import Hash
import Lexem
import GrammaticTree
import Log
from functools import reduce


memAlloc = MemAlloc.MemAlloc(1024)
h = Hash.Hash(memAlloc)

lex = Lexem.create_lexem('Code\\1.txt')
gp = GrammaticTree.GramParse(lex, memAllock=memAlloc)
find, tree = gp.find_gram('<module>')
Log.save(str(tree))

print(find, tree)

if gp.i_lex < len(gp.lex):
    raise Exception(f"Error: unknown syntax '{gp.lex[gp.max_i_lex].me}' line {gp.lex[gp.max_i_lex].line}, token {gp.lex[gp.max_i_lex].num} ")

print(tree.run('main', [7]))


