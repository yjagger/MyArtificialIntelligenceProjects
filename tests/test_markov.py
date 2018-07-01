import unittest

import markov as mk

class TestMarkov(unittest.TestCase):
    
    def test_get_table(self):
        res = mk.get_table('ab')
        self.assterEqual(res, {'a' : {'b' : 1}})
    
    def test_get_table(self):
        res = mk.get_table('abc', size=2)
        self.assertEqual(res, {'ab': {'c': 1}})

    def test_get_table_word(self):
        res = mk.get_table(['hello', 'world'], word=True)
        self.assertEqual(res, {'hello' : {'world':1}})

    def test_markov2(self):
        m = mk.Markov('abc', size=2)
        ref = m.predict('ab')
        self.assertEqual(ref, 'c')

    def test_word_markov(self):
        m = mk.WordMarkov(['hello','world'])
        import pdb;pdb.set_trace()
        res = m.predict('hello')
        self.assertEqual(res, 'world')
        
if __name__ == '__main__':
    unittest.main()
