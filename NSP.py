import copy
import random
import sys
import unittest

from ete2 import Tree
from nodebox.graphics.physics import Graph, Node

from CographGenerator import CographGenerator
from CotreeGenerator import CotreeGenerator
from LexBFS import LexBFS, LexBFS_minus, get_graph_like_in_the_article, get_sigmas_and_slices
from RandomGraphGenerator import RandomGraphGenerator
from helper_functions import *

# I don't know why, but the local neighborhood includes the current slice        
class NeighborhoodSubsetPropertyChecker:
    def sort_adjancency_list_with_respect_to_sigma(self, graph, sigma):
        new_adjacency_lists_dict = {}
        for node in sigma:
            new_adjacency_lists_dict[node.id] = []
        
        for node in sigma:
            for node_in_graph in graph.nodes:
                if node in node_in_graph.links:
                    new_adjacency_lists_dict[node_in_graph.id].append(node)
                    
        for node in graph.nodes:
            node.links = new_adjacency_lists_dict[node.id]
    
    def remove_adjacency_from_same_slice(self, slices):
        for one_slice in slices:
            for node in one_slice:
                node.links = subtract_list(node.links, one_slice)
                
                    
    def get_left_neighborhood(self, sigma, a_slice):
    # assumption: the order is with respect to sigma, 
    # therefore I can ask if the first one in node.links is first_node_in_slice. 
        left_N = list()
        first_index_of_slice_in_sigma = sigma.index(a_slice[0])

        for node in sigma[0:first_index_of_slice_in_sigma]:
            if a_slice[0] in node.links:
                left_N.append(node)
#             node.links = self.subtract_list(node.links, a_slice)
#                 
#         for node in a_slice:
#             node.links = self.subtract_list(node.links, left_N) 

        return left_N
    
    def lists_intersection(self, list1, list2):
        intersection = list()
        for obj in list1:
            if list2.count(obj) > 0:
                intersection.append(obj)

        return intersection

    def sort_slices_with_respect_to_sigma(self, sigma, slices):
        for node in sigma:
            slices_of_node = slices[node.id]
            new_slices_of_node = list()
            for a_slice in slices_of_node:
                new_slices_of_node.append(self.lists_intersection(sigma, a_slice))
            slices[node.id] = new_slices_of_node

    def check_NSP(self, sigma, slices, is_minus=False):
             
        if len(sigma) == 1:
            return True
        
        self.sort_slices_with_respect_to_sigma(sigma, slices)

        for v in sigma:
            slices_of_v = slices[v.id]
            if len(slices_of_v) < 3:
                continue
            print v.id + ': '
            print slices_of_v
                        
#             v1 = slices_of_v[1][0]
            
#             for node in slices_of_v[0]:
#                 node.links = self.subtract_list(node.links, [v]) 
# 
#             self.remove_adjacency_from_same_slice(slices_of_v)
            
#             left_N = self.get_left_neighborhood(sigma, [v1])
            A = calculate_local_neighborhood(v, [slices_of_v[0]], slices_of_v[1], is_minus)
            i = 1
            print A
            for i_slice in slices_of_v[2:]:
#                 v_i = i_slice[0]
#                 slice_index = slices_of_v.index(i_slice)
                
                B = calculate_local_neighborhood(v, slices_of_v[0:i+1], i_slice, is_minus)
                                
#                 slices_of_v_in_one_list = list()
#                 for a_slice in slices_of_v:
#                     slices_of_v_in_one_list += a_slice 
#                 slices_of_v_in_one_list += [v]
#                 B = self.lists_intersection(B, slices_of_v_in_one_list)
                
                print B
                
                if not set(B) <= set(A):
                    return False, v, i
                A = B
                i += 1
        
        return True, 0, 0
    
class NeighborhoodSubsetPropertyCheckerTest(unittest.TestCase):
    checker = NeighborhoodSubsetPropertyChecker()
    def test_sort_adjancency_list(self):
        graph = Graph()
        
        graph.add_edge('x', 'z')
        graph.add_edge('z', 'w')
        graph.add_edge('z', 'y')
        graph.add_edge('z', 'b')
        graph.add_edge('x', 'y')
        graph.add_edge('x', 'a')
        graph.add_edge('x', 'b')
        graph.add_edge('a', 'w')
        
        sigma = [Node(id='x'), Node(id='z'), Node(id='y'), Node(id='b'), Node(id='a'), Node(id='w')]
        
        self.checker.sort_adjancency_list_with_respect_to_sigma(graph, sigma)
                
        excpected_x_adjacency_list = [Node('z'), Node('y'), Node('b'), Node('a')]
        self.assertEqual(excpected_x_adjacency_list, graph.node('x').links)
        
        excpected_z_adjacency_list = [Node(id='x'), Node(id='y'), Node(id='b'), Node(id='w')]
        self.assertEqual(excpected_z_adjacency_list, graph.node('z').links)
        
        excpected_b_adjacency_list = [Node(id='x'), Node(id='z')]
        self.assertEqual(excpected_b_adjacency_list, graph.node('b').links)

    def test_remove_adjacency_from_same_slice(self):
        graph = Graph()
        
        graph.add_edge('x', 'z')
        graph.add_edge('z', 'w')
        graph.add_edge('z', 'y')
        graph.add_edge('z', 'b')
        graph.add_edge('x', 'y')
        graph.add_edge('x', 'a')
        graph.add_edge('x', 'b')
        graph.add_edge('a', 'w')
        
        x_slices = list()
        x_slice_A = [graph.node('z'), graph.node('y'), graph.node('b'), graph.node('a')]
        x_slice_1 = [graph.node('w')]
        
        x_slices.append(x_slice_A)
        x_slices.append(x_slice_1)
        
        self.checker.remove_adjacency_from_same_slice(x_slices)

        for node in x_slice_A:
            node.links = subtract_list(node.links, [Node('x')]) 

        self.assertEqual([Node('w')], graph.node('z').links)
        self.assertEqual([], graph.node('b').links)
    def test_get_left_neighborhood(self):
        graph = Graph()
        
        graph.add_edge('x', 'z')
        graph.add_edge('z', 'w')
        graph.add_edge('z', 'y')
        graph.add_edge('z', 'b')
        graph.add_edge('x', 'y')
        graph.add_edge('x', 'a')
        graph.add_edge('x', 'b')
        graph.add_edge('a', 'w')
        
        sigma = LexBFS(graph)
        self.checker.sort_adjancency_list_with_respect_to_sigma(graph, sigma)
        
        slice_s = [graph.node(id='z'), graph.node(id='y'), graph.node(id='b'), graph.node(id='a')]
        left_N = self.checker.get_left_neighborhood(sigma, slice_s)
        
        self.assertEqual([Node('x')], left_N)
                
        self.checker.remove_adjacency_from_same_slice([slice_s])
        
        slice_s = [Node(id='w')]
        left_N = self.checker.get_left_neighborhood(sigma, slice_s)
        
        self.assertEqual([Node('z'), Node('a')], left_N)

    def test_NSP_check_on_example_from_article(self):        
        cograph = get_graph_like_in_the_article()
        
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
        
        self.assertTrue(self.checker.check_NSP(sigma, slices))
        self.assertTrue(self.checker.check_NSP(sigma_minus, slices_minus, True))

    def test_another_NSP_check(self):
        for i in range(10): 
            cograph = create_cograph(100)
                     
            sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(cograph)
                 
            self.assertTrue(self.checker.check_NSP(sigma, slices))
            self.assertTrue(self.checker.check_NSP(sigma_minus, slices_minus, True))
    def test_sort_slices_with_respect_to_sigma(self):
        graph = Graph()
        
        graph.add_node('a')
        graph.add_node('b')
        graph.add_node('c')
        graph.add_edge('a', 'd')
        graph.add_edge('d', 'e')
        graph.add_edge('e', 'f')
        
        slices = {}
        sigma = LexBFS(graph, slices)
        
        slices_minus = {}
        sigma_minus = LexBFS_minus(graph, sigma, slices_minus)
        
        self.checker.sort_slices_with_respect_to_sigma(sigma, slices)
        
        self.assertEqual([Node('f'),Node('b'),Node('c')], slices['a'][2])
        
    def test_P4(self):
        for i in range(10):
            graph = create_p4_graph(100)
            sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
                         
            if (self.checker.check_NSP(sigma, slices)[0] and self.checker.check_NSP(sigma_minus, slices_minus, True)[0]):
                self.assertFalse(True)

    def test_on_random_graphs(self):
        for i in range(100):
            generator = RandomGraphGenerator()
            
            graph = generator.generate_random_graph(5)
            
            print graph.nodes
            print graph.edges
            
            sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)

            self.checker.check_NSP(sigma_minus, slices_minus, True)