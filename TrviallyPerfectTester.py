from ete2 import Tree
import unittest
from nodebox.graphics.physics import Graph
from CotreeGenerator import CotreeGenerator

# based partially on: 
# Pinar Heggernes, Dieter Kratsch, Linear-time certifying algorithms for recognizing trivially perfect graphs
# I found a counterexample to the article which is tested in the 3rd test, so the algorithm is a bit modified.

class TriviallyPerfectTester:

    def check_if_c4_found_in_sons(self, cotree):
        for node in cotree.get_children():
            c4_answer = self.get_c4_pairs(node)
            
            if len(c4_answer) == 4:
                return c4_answer
        return []
    
    def get_c4_pairs(self, cotree):
        if cotree.is_leaf():
            return []

        c4_list = self.check_if_c4_found_in_sons(cotree)
        
        if c4_list != []:
            return c4_list

        if cotree.name == '0':
            leaves = [leaf.name for leaf in cotree.get_leaves()]

            if len(leaves) > 1:
                return [leaves[0], leaves[-1]] # from different sons
            
            return []
        
        else:
            c4_nodes = list()
            
            for node in cotree.get_children():
                c4_answer = self.get_c4_pairs(node)

                if len(c4_answer) == 2:
                    c4_nodes += c4_answer
                
                if len(c4_nodes) == 4:
                    return c4_nodes
            
            if len(c4_nodes) == 2:
                return c4_nodes
            
        return []
    def test_and_get_c4(self, cotree):
        c4_pairs = self.get_c4_pairs(cotree)
        
        if len(c4_pairs) == 4:
            return [c4_pairs[0], c4_pairs[2], c4_pairs[1], c4_pairs[3]]
        
        return []
class TriviallyPerfectTesterTest(unittest.TestCase):
    tester = TriviallyPerfectTester()
    def test_simple_c4(self):
        cotree = Tree("((a,c)0,(b,d)0);",format=8)
        cotree.name = '1'
           
        c4 = self.tester.test_and_get_c4(cotree)
           
        self.assertEqual(['a', 'b', 'c', 'd'], c4)
  
    def test_another_simple_c4(self):
        cotree = Tree("((b,d)0,((e,a)1,c)0);",format=8)
        cotree.name = '1'
           
        c4 = self.tester.test_and_get_c4(cotree)
           
        self.assertEqual(['b', 'e', 'd', 'c'], c4)
          
    def test_c4_not_immediate_sons(self):
        cotree = Tree("(((a,b)0,(c,d)1)1,(e,f)0);",format=8)
        cotree.name = '1'
  
        c4 = self.tester.test_and_get_c4(cotree)
  
        self.assertEqual(['a', 'e', 'b', 'f'], c4)

    def test_no_c4(self):
        cotree = Tree("(((a,b)0,(c,d)1)1,(e,f)1);",format=8)
        cotree.name = '1'

        c4 = self.tester.test_and_get_c4(cotree)
  
        self.assertEqual([], c4)
        
    def test_c4_on_random(self):
        generator = CotreeGenerator()
        cotree = generator.generate_cotree(100)
        
        print cotree.write(format=8, format_root_node=True)
 
        c4 = self.tester.test_and_get_c4(cotree)
        print c4
