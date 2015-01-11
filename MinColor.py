from nodebox.graphics.physics import Graph
import unittest
from ete2 import Tree
import operator
from GraphDrawer import draw_graph
from CotreeGenerator import CotreeGenerator

class MinColorOnCotreeFinder:
    def find_min_color(self, cotree):
        if cotree.is_leaf():
            return { cotree.name : 1}
        
        if len(cotree.get_children()) == 1:
            return self.find_min_color(cotree.get_children()[0])
        
        if cotree.name == '0':
            coloring = {}
            for sub_cotree in cotree.get_children():
                sub_cotree_coloring = self.find_min_color(sub_cotree)
                coloring.update(sub_cotree_coloring)

            return coloring
        else:
            coloring = self.find_min_color(cotree.get_children()[0])
            for sub_cotree in cotree.get_children()[1:]:
                sub_cotree_coloring = self.find_min_color(sub_cotree)
                
                max_label = max(coloring.iteritems(), key=operator.itemgetter(1))[1]               
                for node in sub_cotree_coloring:
                    sub_cotree_coloring[node] += max_label
                
                coloring.update(sub_cotree_coloring)

            return coloring
            
class MinColorOnCotreeFinderTest(unittest.TestCase):
    finder = MinColorOnCotreeFinder()
    def test_simple_coloring(self):
        cotree = Tree("((a,b)1);", format=8)
        
        coloring = self.finder.find_min_color(cotree)
        
        self.assertEqual(1, coloring['a']);
        self.assertEqual(2, coloring['b']);
    def test_another_simple_coloring(self):
        cotree = Tree("((a,b)0);", format=8)
        
        coloring = self.finder.find_min_color(cotree)
        
        self.assertEqual(1, coloring['a']);
        self.assertEqual(1, coloring['b']);
        
    def test_coloring_on_graph_from_article(self):
        cotree = Tree("(((v,u)1,(w,y)1)0,(((b,c)0,d)1,e,(z,(a,x)0)1)0);",format=8)
        cotree.name = '1'
         
        coloring = self.finder.find_min_color(cotree)
        
        print coloring
        
#         draw_graph(get_graph_like_in_the_article())
    def test_random(self):
        tree_generator = CotreeGenerator()
        
        cotree = tree_generator.generate_cotree(100)
        
        print self.finder.find_min_color(cotree)