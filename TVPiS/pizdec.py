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