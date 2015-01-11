import unittest
from nodebox.graphics.physics import Graph
from ete2 import Tree
from LexBFS import get_sigmas_and_slices
from helper_functions import get_graph_like_in_the_article
from GraphDrawer import draw_graph
class CotreeGeneratorFromCograph:
    def __init__(self):
        self.slices = {}
        self.slices_minus = {}
    
    def generate_tree_that_one_slice_is_null(self, v, v_i, root_name):
        cotree = Tree()
        
        cotree.name = root_name
        cotree.add_child(name=v.id)
        cotree.add_child(self.generate_cotree_of_v(v_i))
        return cotree

    def get_first_of_each_slice(self, slices):
        first_of_each = list()
        for a_slice in slices:
            first_of_each.append(a_slice[0])
            
        return first_of_each    
    
    def create_cotree_with_slice(self, first_in_slice, internal_node, cotree):
        new_cotree = Tree()
        new_cotree.name = internal_node
        new_cotree.add_child(cotree)
        new_cotree.add_child(self.generate_cotree_of_v(first_in_slice))
        
        return new_cotree
        
    def create_cotree_with_slices(self, v, first_of_each_slice_1, first_of_each_slice_2, internal_node_of_1):
        cotree = Tree()
        cotree.name = v.id
        internal_node_of_2 = str(1 - int(internal_node_of_1))
        
        slices_max_len = max(len(first_of_each_slice_1), len(first_of_each_slice_2))
        for i in range(slices_max_len):
            if i < len(first_of_each_slice_1):            
                cotree = self.create_cotree_with_slice(first_of_each_slice_1[i], internal_node_of_1, cotree)
            if i < len(first_of_each_slice_2):            
                cotree = self.create_cotree_with_slice(first_of_each_slice_2[i], internal_node_of_2, cotree)
            
        return cotree
    def handle_both_slices_are_not_empty(self, v):
        slices_of_v = self.slices[v.id]
        slices_minus_of_v = self.slices_minus[v.id]
        
        v_i = slices_of_v[1][0]
        v_i_minus = slices_minus_of_v[1][0]
        first_of_each_slice = self.get_first_of_each_slice(slices_of_v[1:])
        first_of_each_slice_minus = self.get_first_of_each_slice(slices_minus_of_v[1:])
        
        if v_i in v_i_minus.links:
            cotree = self.create_cotree_with_slices(v, first_of_each_slice, first_of_each_slice_minus, '0')
        else:
            cotree = self.create_cotree_with_slices(v, first_of_each_slice_minus, first_of_each_slice, '1')

        return cotree

    def generate_cotree_of_v(self, v):
        slices_of_v = self.slices[v.id]
        slices_minus_of_v = self.slices_minus[v.id]

        if not slices_of_v[1] and not slices_minus_of_v[1]:    
            cotree = Tree()
            cotree.name = v.id
            return cotree
        
        if not slices_of_v[1]:
            v_i_minus = slices_minus_of_v[1][0]
            return self.generate_tree_that_one_slice_is_null(v, v_i_minus, '1')

        if not slices_minus_of_v[1]:
            v_i = slices_of_v[1][0]
            return self.generate_tree_that_one_slice_is_null(v, v_i, '0')
        
        cotree = self.handle_both_slices_are_not_empty(v)
                      
        return cotree
    
    def generate_cotree(self, v, slices, slices_minus):
        self.slices = slices
        self.slices_minus = slices_minus
        
        return self.generate_cotree_of_v(v)
class CotreeGeneratorFromCographTest(unittest.TestCase):
    generator = CotreeGeneratorFromCograph()
    def test_first_case(self):
        cograph = Graph()
        
        cograph.add_node('a')
        
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)

        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)

        self.assertEqual('a', cotree.name)
        
    def test_second_case(self):
        cograph = Graph()
        
        cograph.add_edge('a', 'b')
        
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
                        
        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)
        
        self.assertEqual('1', cotree.name)
        self.assertEqual(['a', 'b'], cotree.get_leaf_names())
        
    def test_third_case(self):
        cograph = Graph()
        
        cograph.add_node('a')
        cograph.add_node('b')
        
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
        
        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)
        
        self.assertEqual('0', cotree.name)
        self.assertEqual(['a', 'b'], cotree.get_leaf_names())
    
    def test_fourth_case(self):
        cograph = Graph()
        
        cograph.add_edge('a', 'b')
        cograph.add_edge('b', 'c')
        cograph.add_node('d')

        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
                
        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)  
        
        self.assertEqual('0', cotree.name)
        self.assertEqual(['1', 'd'], [i.name for i in cotree.children])
        self.assertEqual(['0', 'b'], [i.name for i in cotree.children[0].children])
        self.assertEqual(['a', 'c'], [i.name for i in cotree.children[0].children[0]])

    def test_fifth_case(self):
        cograph = Graph()
        
        cograph.add_edge('a', 'b')
        cograph.add_node('b')
        cograph.add_node('c')
        cograph.add_node('d')

        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
        
        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)  

        self.assertEqual('0', cotree.name)
        self.assertEqual(['1', '0'], [i.name for i in cotree.children])
        self.assertEqual(['a', 'b'], [i.name for i in cotree.children[0].children])
        self.assertEqual(['c', 'd'], [i.name for i in cotree.children[1].children])
                
    def test_article_case(self):
        cograph = get_graph_like_in_the_article()
         
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
 
        cotree = self.generator.generate_cotree(cograph.node('x'), slices, slices_minus)
    def test_c4_graph(self):
        cograph = Graph()
        
        cograph.add_edge('a', 'b')
        cograph.add_edge('b', 'c')
        cograph.add_edge('c', 'd')
        cograph.add_edge('a', 'd')

        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
 
        cotree = self.generator.generate_cotree(cograph.node('a'), slices, slices_minus)
        
        print cotree.write(format=8) + cotree.name
        
        draw_graph(cograph)
        