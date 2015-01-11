from nodebox.graphics.physics import Graph
import unittest
from ete2 import Tree
import operator
from GraphDrawer import draw_graph
from CotreeGenerator import CotreeGenerator
from CographGenerator import CographGenerator
import random
class MaxWeightedCliqueFinder:
    def find_max_weighted_clique(self, cotree):
        if cotree.is_leaf():
            return [[cotree.name], cotree.support]
        
        if len(cotree.get_children()) == 1:
            return self.find_max_weighted_clique(cotree.get_children()[0])
        
        if cotree.name == '0':
            first_son = self.find_max_weighted_clique(cotree.get_children()[0])
            
            max_clique = first_son[0]
            max_clique_weight = first_son[1]

            for sub_cotree in cotree.get_children()[1:]:
                sub_cotree_clique = self.find_max_weighted_clique(sub_cotree)
                
                if sub_cotree_clique[1] > max_clique_weight:
                    max_clique = sub_cotree_clique[0] 
                    max_clique_weight = sub_cotree_clique[1]

            return [max_clique, max_clique_weight]
        else:
            first_son = self.find_max_weighted_clique(cotree.get_children()[0])
            
            max_clique = list()
            max_clique_weight = 0
                
            for sub_cotree in cotree.get_children():
                sub_cotree_clique = self.find_max_weighted_clique(sub_cotree)
                
                max_clique += sub_cotree_clique[0] 
                max_clique_weight += sub_cotree_clique[1]

            return [max_clique, max_clique_weight]
            
class MaxWeightedCliqueFinderTest(unittest.TestCase):
    finder = MaxWeightedCliqueFinder()
    def add_weights_to_leaves(self, cotree, max_weight):
        for node in cotree.get_leaves():
            node.support = random.randint(0,max_weight)
    def test_simple_clique(self):
        cotree = Tree("(a,b);", format=8)
        cotree.name = '0'
        
        cotree.get_children()[0].support = 4
        cotree.get_children()[1].support = 3

        max_clique = self.finder.find_max_weighted_clique(cotree)
         
        self.assertEqual(4, max_clique[1])
        self.assertEqual('a', max_clique[0][0])
        
    def test_another_simple_clique(self):
        cotree = Tree("(a,b);", format=8)
        cotree.name = '1'

        cotree.get_children()[0].support = 4
        cotree.get_children()[1].support = 3
         
        max_clique = self.finder.find_max_weighted_clique(cotree)
         
        self.assertEqual(['a', 'b'], max_clique[0]);
        self.assertEqual(7, max_clique[1]);
         
    def test_clique_on_graph_from_article(self):
        cotree = Tree("(((v,u)1,(w,y)1)0,(((b,c)0,d)1,e,(z,(a,x)0)1)0);",format=8)
        cotree.name = '1'
        self.add_weights_to_leaves(cotree, 10)
        
        cotree.search_nodes(name='e')[0].support = 50
        cotree.search_nodes(name='w')[0].support = 10
        cotree.search_nodes(name='y')[0].support = 11
        
        max_clique = self.finder.find_max_weighted_clique(cotree)
        
        
        self.assertEqual(['w', 'y', 'e'], max_clique[0]);
        self.assertEqual(71, max_clique[1]);
         
#         draw_graph(get_graph_like_in_the_article())
    def test_random(self):
        tree_generator = CotreeGenerator()
        cograph_generator = CographGenerator()
        cotree = tree_generator.generate_cotree(10)
        print cotree.write(format=8)
          
        max_clique = self.finder.find_max_weighted_clique(cotree)
        print max_clique
        
        draw_graph(cograph_generator.generate_cograph_from_cotree(cotree))