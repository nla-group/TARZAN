import unittest
import TARZAN
from string import ascii_lowercase
from random import choice
import numpy as np

class test_TARZAN(unittest.TestCase):

    # Suffix Trees
    def ztest_build_tree_McCreight(self):
        """
        Test McCreight algorithm implementation
        """
        string = 'banana'
        tree = TARZAN.SuffixTree(string, method='McCreight')
        self.assertEqual(tree.find('an'), [1, 3])
        self.assertEqual(tree.find('a'), [1, 3, 5])
        self.assertEqual(tree.find('ab'), [])
        self.assertEqual(tree.find('nan'), [2])

    def ztest_build_tree_BruteForce(self):
        """
        Test Brute Force algorithm implementation
        """
        string = 'banana'
        tree = TARZAN.SuffixTree(string, method='Brute')
        self.assertEqual(tree.find('an'), [1, 3])
        self.assertEqual(tree.find('a'), [1, 3, 5])
        self.assertEqual(tree.find('ab'), [])
        self.assertEqual(tree.find('nan'), [2])

    def ztest_tree_LargeExample(self):
        """
        Test suffix tree construction and find function on a very large example.
        """
        string = ''.join([choice(ascii_lowercase) for _ in range(1000000)])
        tree = TARZAN.SuffixTree(string, method='McCreight')
        l = tree.find(string[6783:6789])
        self.assertTrue(6783 in l)

    def ztest_tree_find(self):
        """
        Test all variants of SuffixTree find function
        """
        string = 'bananahanana'
        tree = TARZAN.SuffixTree(string, method='McCreight')

        # returns a list of indicies
        l = tree.find('an', list_all=True, index=True)
        self.assertEqual(l.sort(), [1, 3, 7, 9].sort())

        # returns a list of nodes
        l = tree.find('an', list_all=True, index=False)
        self.assertEqual(len(l), 4)
        self.assertTrue(isinstance(l[0], TARZAN._Node))

        # returns a bool
        l = tree.find('an', list_all=False, index=True)
        self.assertTrue(l)

        # returns a node
        l = tree.find('an', list_all=False, index=False)
        self.assertTrue(isinstance(l, TARZAN._Node))

    # _annotate_nodes
    def ztest_tree_annotate(self):
        """
        Check the annotate node function finds the frequency of each word correctly.
        """
        string = 'banana'
        tree = TARZAN.SuffixTree(string, method='McCreight')
        tree.root._annotate_nodes()

        node = tree.find('b', list_all=False, index=False)
        self.assertEqual(node.frequency, 1)
        node = tree.find('a', list_all=False, index=False)
        self.assertEqual(node.frequency, 3)
        node = tree.find('n', list_all=False, index=False)
        self.assertEqual(node.frequency, 2)
        node = tree.find('an', list_all=False, index=False)
        self.assertEqual(node.frequency, 2)
        node = tree.find('ana', list_all=False, index=False)
        self.assertEqual(node.frequency, 2)
        node = tree.find('ban', list_all=False, index=False)
        self.assertEqual(node.frequency, 1)

    # _symbol_prob
    def ztest_SymbolProbability(self):
        """
        If the substring does not exist and not all substrings of the substring
        exist then we compute product of the probabilities of each symbol
        """
        string = 'abababa' + 'c' + 'abababa' + 'd' + 'abababa'
        tree = TARZAN.SuffixTree(string, method='McCreight')
        tree.root._annotate_nodes()

        prob = TARZAN._symbol_prob(tree, string, 'cd')
        self.assertTrue(np.allclose(prob, 1/(len(string)**2)))

        prob = TARZAN._symbol_prob(tree, string, 'bc')
        self.assertTrue(np.allclose(prob, 9/(len(string)**2)))

        prob = TARZAN._symbol_prob(tree, string, 'ab')
        self.assertTrue(np.allclose(prob, 108/(len(string)**2)))

    # _lower_mod_prod
    def ztest_lower_mod_prod(self):
        """
        If a substring does not exist, check if substrings of that substring exist.
        A simple utility function to compute \prod_{j=jmin}^{jmax} f_tree(w[j:j+l])
        """
        string = 'aaaa' + 'bc' + 'aaaa' + 'cd' + 'aaaa' + 'de' + 'aaaa'
        tree = TARZAN.SuffixTree(string, method='McCreight')
        tree.root._annotate_nodes()

        prob = TARZAN._lower_mod_prod(tree, 'bcde', 0, 2, 2)
        self.assertEqual(prob, 1)

    # compute_expectation
    def test_compute_expectation(self):
        """
        Test simple Tarzan example by finding in predefined string using method==None
        """

        R = 'abcbabcbabcbabcba'
        X = 'abccba'

        Rtree = TARZAN.SuffixTree(R, method='McCreight')
        Rtree.root._annotate_nodes()
        E1 = TARZAN.compute_expectation('abc', R, X, Rtree)
        E2 = TARZAN.compute_expectation('bcc', R, X, Rtree)

        self.assertEqual(E1, (len(X)-3+1)/(len(R)-3+1)*4)
        self.assertEqual(E2, (len(X)-3+1)*((8*4*4)/(17**3)))


        print('abc', E1-1, 'bcc', E2-1)

        score = TARZAN.TARZAN(R, X, 3, method=None)


if __name__=="__main__":
    unittest.main()
