from ete2 import Tree
import unittest
from CotreeGenerator import CotreeGenerator
from nodebox.graphics.physics import Graph
from nodebox.graphics import Color, Text

class CographGenerator:
    def generate_cograph_from_cotree(self, cotree):
        cograph = Graph()
        if len(cotree) == 1:
            cograph.add_node(cotree.get_leaves()[0].name)
            return cograph
        
        for leaf in cotree:
            for another_leaf in cotree:
                if leaf.name != another_leaf.name:
                    ancestor = cotree.get_common_ancestor(leaf.name, another_leaf.name)
                    if ancestor.name == '1':
                        cograph.add_edge(leaf.name, another_leaf.name)
                    else:
                        cograph.add_node(leaf.name, strokewidth=1)
                        cograph.add_node(another_leaf.name, strokewidth=1)

        return cograph
        
class CographGeneratorTest(unittest.TestCase):
    generator = CographGenerator()
        
    def testSingleNode(self):
        
        cotree = Tree("(A);")
        
        cograph = self.generator.generate_cograph_from_cotree(cotree)
        
        
        self.assertEqual(1, len(cograph))
        self.assertTrue('A' in cograph)

     
    def testTwoNodesNoEgde(self):
        cotree = Tree("((A,B)0);",format=8)
         
        cograph = self.generator.generate_cograph_from_cotree(cotree)
         
        self.assertEqual(2, len(cograph))
        self.assertTrue(cograph.node('B') not in cograph.node('A').links)
 
    def testTwoNodesWithEgde(self):
        cotree = Tree("((A,B)1);",format=8)
          
        cograph = self.generator.generate_cograph_from_cotree(cotree)
          
        self.assertEqual(2, len(cograph))
        self.assertTrue(cograph.node('B') in cograph.node('A').links)
  
    def testExampleFromWikipedia(self):
        cotree = Tree("(((A,(B,C)1,(D,E)1)0,(F,G)0)1);",format=8)
          
        cograph = self.generator.generate_cograph_from_cotree(cotree)
                  
        self.assertEqual(7, len(cograph))
        self.assertTrue('F' not in cograph.node('G').links)
          
    def testWithCotreeGenerator(self):
        cotree_generator = CotreeGenerator()
        cotree = cotree_generator.generate_cotree(100)
                    
        cograph = self.generator.generate_cograph_from_cotree(cotree)

        if cotree.name == '0':
            self.assertNotEqual(1, len(cograph.split()))
