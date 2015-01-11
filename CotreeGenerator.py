import unittest
import random
from ete2 import Tree

class CotreeGenerator(object):
    def generate_cotree(self, num_of_nodes):
        t = Tree()
        t.populate(num_of_nodes)
        
        for node in t.traverse():
            if not node.is_leaf():
                node.name=str(random.randint(0, 1))
        
        return t
class CotreeGeneratorTest(unittest.TestCase):
    generator = CotreeGenerator()
    
    def testCotreeGenerator(self):
        self.generator.generate_cotree(100)
#        n = 5;
#       cotree_graph = self.generator.generate_cotree_of_v(n)
#     nx.draw(cotree_graph)
#      plt.show()
