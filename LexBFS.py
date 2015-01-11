from nodebox.graphics.physics import Graph, Node
from nodebox.graphics import *
import unittest
from CographGenerator import CographGenerator
from ete2 import Tree
import copy
from helper_functions import *

# I figured it would be easier to clear the empty lists, since they are not used

def remove_empty_lists(L):
    empty_list = []
    while L.count(empty_list) != 0:
        L.remove([])

# def left_neighborhood(self, sigma, node):
#     index_of_node = sigma.index(node)
#     return lists_intersection(node.links, sigma[0:index_of_node])
# 
# def order_slices(self, sigma, slices):
#     for v in slices:
#         slices_of_v = slices[v]
#         for node_in_slice in slices_of_v[1]:
#             left_neighborhood(sigma, node_in_slice)
def split_slices(sigma, slices, split_nodes, last_node_in_sigma):
    for node in sigma[0:len(sigma)-1]:
        slices_of_node = slices[node.id]
        for a_slice in slices_of_node[1:]:
            split_nodes_in_slice = lists_intersection(a_slice, split_nodes)
            
            if last_node_in_sigma in slices_of_node[0] and split_nodes_in_slice and split_nodes_in_slice != a_slice:
                for node_neighbor in split_nodes_in_slice:
                    a_slice.remove(node_neighbor)
                
                slice_index = slices_of_node.index(a_slice)
                slices_of_node.insert(slice_index, split_nodes_in_slice)

def LexBFS(graph, slices = {}):
    L = list()
    sigma = list()
    L.append(copy.copy(graph.nodes))
    i = 1
    
    while L:
        node = L[0].pop(0)
        
        sigma.append(node)
        i += 1
        
        slices[node.id] = list()
        slice_A = lists_intersection(L[0], node.links)
        slices[node.id].append(slice_A)
        slice_N = subtract_list(L[0], node.links)
        slices[node.id].append(slice_N)

        for P in L:
            node_neighbors_in_P = lists_intersection(P, node.links)
            
            if node_neighbors_in_P and node_neighbors_in_P != P:
                for node_neighbor in node_neighbors_in_P:
                    P.remove(node_neighbor)
                
                P_index = L.index(P)
                L.insert(P_index, node_neighbors_in_P)
                
                split_slices(sigma, slices, node_neighbors_in_P, node)

        remove_empty_lists(L)
    
    return sigma

def pop_numbered_earliest(P, sigma):
    earliest_numbered_node = P[0]
    earliest_numbered_node_index = sigma.index(earliest_numbered_node)
         
    for node in P[1:]:
        if sigma.index(node) < earliest_numbered_node_index:
            earliest_numbered_node = node
            earliest_numbered_node_index = sigma.index(earliest_numbered_node)
            
    return P.pop(P.index(earliest_numbered_node))

def split_slices_minus(sigma_minus, slices, split_nodes, last_node_in_sigma):
    for node in sigma_minus[0:len(sigma_minus)-1]:
        slices_of_node = slices[node.id]
        for a_slice in slices_of_node[1:]:
            split_nodes_in_slice = lists_intersection(a_slice, split_nodes)
            
            if last_node_in_sigma in slices_of_node[0] and split_nodes_in_slice and split_nodes_in_slice != a_slice:
                for node_neighbor in split_nodes_in_slice:
                    a_slice.remove(node_neighbor)
                
                slice_index = slices_of_node.index(a_slice)
                slices_of_node.insert(slice_index+1, split_nodes_in_slice)

def LexBFS_minus(graph, sigma, slices = {}):
    L = list()
    sigma_minus = list()
    L.append(copy.copy(graph.nodes))

    i = 1
    
    while L:
        first_cell = L[0]
        node = pop_numbered_earliest(first_cell, sigma)

        sigma_minus.append(node)
        i += 1

        slices[node.id] = list()
        slice_A = subtract_list(L[0], node.links) 
        slices[node.id].append(slice_A)
        slice_N = lists_intersection(L[0], node.links)
        slices[node.id].append(slice_N)
        
        for P in L:            
            node_neighbors_in_P = lists_intersection(P, node.links)

            if node_neighbors_in_P and node_neighbors_in_P != P:
                for node_neighbor in node_neighbors_in_P:
                    P.remove(node_neighbor)
                
                P_index = L.index(P)
                L.insert(P_index+1, node_neighbors_in_P)
                
                split_slices_minus(sigma_minus, slices, node_neighbors_in_P, node)
        
        remove_empty_lists(L)

        
    for node in sigma_minus:
        slices_of_node = slices[node.id]
        ordered_slices_of_node = list()
        for a_slice in slices_of_node:
            a_slice = lists_intersection(sigma_minus, a_slice)
            ordered_slices_of_node.append(a_slice)
            slices[node.id] = ordered_slices_of_node
        
    return sigma_minus

def get_sigmas_and_slices(graph):
    slices = {}
    sigma = LexBFS(graph, slices)
        
    slices_minus = {}
    sigma_minus = LexBFS_minus(graph, sigma, slices_minus)
    
    return sigma, slices, sigma_minus, slices_minus

class LexBFSTest(unittest.TestCase):
    
        
    def test_remove_empty_lists(self):
        L = [[] for i in range(6)]

        remove_empty_lists(L)
                
        self.assertEqual(0, len(L))
    
    def test_lists_intersection(self):
        list1 = [1, 22, 12, 52, 11]
        list2 = [1, 22, 53, 52, 73, 1, 22]
        
        intersection = lists_intersection(list1, list2)
        
        self.assertEqual([1, 22, 52], intersection)

    def test_another_lists_intersection(self):
        list1 = [1, 282, 836, 376, 947, 648]
        list2 = [1, 247, 376, 273, 748, 899, 16]

        
        intersection = lists_intersection(list1, list2)
        
        self.assertEqual([1, 376], intersection)  
        
    def test_example_from_article(self):
        
        cograph = get_graph_like_in_the_article()
        
        sigma= LexBFS(cograph)
        
        sigma_str = ''
        for node in sigma:
            sigma_str += node.id
        self.assertEqual('xywzuvadcbe',sigma_str)

    def test_slices(self):
        cograph = get_graph_like_in_the_article()
        
        slices = {}
        
        sigma= LexBFS(cograph, slices)
        
        self.assertEqual([Node('y'), Node('u'), Node('v'), Node('w'), Node('z')], slices['x'][0])
        self.assertEqual([Node('w'), Node('z')], slices['y'][0])
        self.assertEqual([Node('z')], slices['w'][0])

        self.assertEqual([Node('a')], slices['x'][1])
        self.assertEqual([Node('d'), Node('e'), Node('c'), Node('b')], slices['x'][2])
        self.assertEqual([Node('u'), Node('v')], slices['y'][1])
        self.assertEqual([], slices['w'][1])
                
    def test_pop_numbered_earliest(self):
        P = ['x', 'y', 'z', 'w' , 'a', 'b']
        sigma=['w', 'y' , 'z', 'a' , 'b', 'x']
        
        earliest = pop_numbered_earliest(P, sigma)
        self.assertEqual('w', earliest)

        P = ['x', 'z', 'w', 'b']
        sigma=['a', 'y' , 'z', 'w' , 'b', 'x']
        earliest = pop_numbered_earliest(P, sigma)
        
        self.assertEqual('z', earliest)

    def test_LexBFS_minus_from_article(self):
        cograph = get_graph_like_in_the_article()
        
        sigma = LexBFS(cograph)
        
        sigma_minus = LexBFS_minus(cograph, sigma)
        
        sigma_str = ''
        for node in sigma_minus:
            sigma_str += node.id

        self.assertEqual('xadecbzyuvw',sigma_str)
        
    def test_on_LexBFS_minus(self):
        cograph = get_graph_like_in_the_article()
        
        slices = {}
        
        sigma= LexBFS(cograph)

        sigma_minus = LexBFS_minus(cograph, sigma, slices)
        
        self.assertEqual([cograph.node('a'), cograph.node('d'), cograph.node('e'), 
                              cograph.node('c'), cograph.node('b')], slices['x'][0])
        self.assertEqual([cograph.node('d'), cograph.node('e'), cograph.node('c'), cograph.node('b')], slices['a'][0])
        self.assertEqual([cograph.node('e')], slices['d'][0])

        self.assertEqual([cograph.node('z')], slices['x'][1])
        self.assertEqual([cograph.node('y'), cograph.node('u'), 
                          cograph.node('v'), cograph.node('w')], slices['x'][2])
        
        self.assertEqual([], slices['a'][1])
        self.assertEqual([cograph.node('c'), cograph.node('b')], slices['d'][1])
    
    def test_another_slices_of_LexBFS(self):
        cotree = Tree("(((a,b)0,((c,d)0,(e,f)1)1)0,((g,h)1,(i,j)0)1);",format=8)

        cograph_generator = CographGenerator()
        cograph = cograph_generator.generate_cograph_from_cotree(cotree)
        
        slices = {}
        
        sigma= LexBFS(cograph, slices)
        
        self.assertEqual([Node('d')], slices['c'][1])
        self.assertEqual([Node(id='g'), Node(id='h'), Node(id='i'), Node(id='j')], slices['c'][2])
    
    def test_slices_minus_of_P4(self):
        graph = Graph()
        
        graph.add_node('a')
        graph.add_node('b')
        graph.add_edge('c', 'd')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'f')

        
        sigma = LexBFS(graph)
        

        slices_minus = {}
        sigma_minus = LexBFS_minus(graph, sigma, slices_minus)
        
        self.assertEqual([Node('d')], slices_minus['c'][1])
        self.assertEqual([Node('e')], slices_minus['c'][2])
