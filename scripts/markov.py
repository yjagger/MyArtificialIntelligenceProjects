"""

This is a module for creating markov chains


>>> m = Markov('ab')
>>> m.predict('a')
'b'
>>> get_table('ab')
{'a': {'b': 1}}
"""

import random
import sys
import urllib.request as req
import argparse
import sys

def fetch_url(url, ecncoding='utf8'):
    fin = req.urlopen(url)
    data = fin.read()
    return data.decode(encoding)

def write_file(filename, data, encoding='utf8'):
    with open(filename, 'w', encoding=encoding) as fout:
        fout.write(data)

def get_data(filename, enc):
    with open(filename, encoding=enc) as fin:
        data = fin.read()
    return data

class Markov:
    word = False
    def __init__(self, data,size=1):
        #This is the body of the constructor
        #self is the instance
        #self.table = get_table(data)
        #import pdb; pdb.set_trace()
        self.tables = []
        self.size = size
        for i in range(1, size+1):
            self.tables.append(get_table(data, size=i, word=self.__class__.word))

    def _get_table(self, data_in):
        table = self.tables[len(data_in)-1]
        return table
    
    def predict(self, data_in):
        #import pdb; pdb.set_trace()
        table = self._get_table(data_in)
        options = table.get(data_in, {})
        if not options:
            raise KeyError(f'{data_in} not found')
        possibles = []  # empty list literal
        for key, count in options.items():
            for i in range(count):
                possibles.append(key)
        return random.choice(possibles)


    def ipsum(self,length,seed):
        """
        >>> m = markov('find a city find yourself a city')
        >>> random.seed(42)
        >>> m.ipsum(10,'f')
        'find ind a'
        """
        #import pdb; pdb.set_trace()
        res = [seed]
        for i in range(length):
            last = res[-self.size:]
            joiner = ' ' if self.__class__.word else ''
            val = self.predict(joiner.join(last))
            res.append(val)
        return joiner.join(res)

class WordMarkov(Markov):
    word=True
    def __init__(self, data, size=1):
        if isinstance(data, str):
           data = data.split()
        super().__init__(data, size)
        
    def _get_table(self, data_in):
        for table in self.tables:
            if data_in in table:
                return table
        raise KeyError(f'{data_in} not in tables')

def get_table(data, size=1,word=False):
    results = {}
    #import pdb; pdb.set_trace()
    for i in range(len(data)):
        chars = data[i:i+size]
        try:
            out = data[i+size]
        except IndexError:
            break
        #print(f'chars: {chars}')
        if word:
            chars = ' '.join(chars)
        char_dict = results.get(chars, {})
        char_dict.setdefault(out, 0)
        char_dict[out] += 1
        results[chars] = char_dict
    return results

def repl(m):
    while True:
        try:
            txt = input('>')
        except (KeyboardInterrupt, EOFError):
            print("GoodBye!")
            break
        try:
            print(f'{m.predict(txt)}')
        except KeyError:
            print("try again")

def main(args):
    parser = argparse.ArgumentParser(description= "Markov chain generator")
    parser.add_argument('-f', '--file', help='specify file ')
    parser.add_argument('-e', '--encoding', help='specify encoding, default - utf8', default='utf8')
    parser.add_argument('-w', '--word-mode', help='run in word mode', action = 'store_true')
    parser.add_argument('-s', '--size', help='specify size', action='store', default=1, type=int)
    opt = parser.parse_args(args)
    if opt.file:
        data = get_data(opt.file, enc=opt.encoding)
        Klass = Markov
        if opt.word_mode:
            Klass = WordMarkov
        m = Klass(data, size=opt.size)
        repl(m)

if __name__ == '__main__':
    main(sys.argv[1:])
#    #I'm executing this file
#    import doctest
#    doctest.testmod()
    #m = load_from_file('frank.txt', size=4, word=True)
#else:
#    print("Using markov.py as a library")


txt = get_data('frank.txt', 'UTF-8')
m = WordMarkov(txt, size=4)

