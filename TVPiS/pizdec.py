try:
    word_id = "".join(map(chr, h.get(word)))
except Exception as e:
    if word == 'main':
        word_id = 'main'
    else:
        h.update(word, bytes(str(identifier_id), 'utf8'))
        word_id = str(identifier_id)
        Log.save(f'{word} is {identifier_id}')
        identifier_id = identifier_id + 1
lex.append(Lexem('var', word_id))





word = self.leafs[1].me
            global identifier_id
            try:
                h[deep].get(word)
                raise Exception(f"repeated declaration of identifier {self.leafs[1].me}")
            except KeyError as e:
                if word == 'main':
                    word_id = 'main'
                else:
                    h[deep].update(word, bytes(str(identifier_id), 'utf8'))
                    word_id = str(identifier_id)
                    Log.save(f'{word} is {identifier_id}')
                    identifier_id = identifier_id + 1
            self.leafs[1].me = word_id
            identifiers_desc.append((self.leafs[1].me, self.leafs[0], self.memAllock.alloc(1)))




identifiers_desc = []
h = [Hash.Hash(mem_alloc=MemAlloc.MemAlloc(1024))]
identifier_id = 0
deep = 0