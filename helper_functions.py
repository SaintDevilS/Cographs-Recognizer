from ete2 import Tree
from CographGenerator import CographGenerator
from CotreeGenerator import CotreeGenerator
import unittest
import random
from nodebox.graphics.physics import Graph

def move_node_to_index(cograph, node_name, wanted_index):
    node_index = cograph.nodes.index(cograph.node(node_name))
    cograph.nodes.insert(wanted_index, cograph.nodes.pop(node_index))

def lists_intersection(list1, list2):
    intersection = list()
    for obj in list1:
        if list2.count(obj) > 0:
            intersection.append(obj)

    return intersection

def subtract_list(list1, list2):
    return [item for item in list1 if item not in list2]

def get_graph_like_in_the_article():
    cotree = Tree("((((v,u)1,(w,y)1)0,(((b,c)0,d)1,e,(z,(a,x)0)1)0)1);",format=8)
    cograph_generator = CographGenerator()
        
    cograph = cograph_generator.generate_cograph_from_cotree(cotree)
        
    move_node_to_index(cograph, 'x', 0)
    move_node_to_index(cograph, 'd', 1)
    move_node_to_index(cograph, 'y', 2)
    move_node_to_index(cograph, 'u', 3)
    move_node_to_index(cograph, 'e', 4)
    move_node_to_index(cograph, 'v', 5)
    move_node_to_index(cograph, 'w', 6)
    move_node_to_index(cograph, 'c', 7)
    move_node_to_index(cograph, 'a', 8)
    move_node_to_index(cograph, 'z', 9)
    
    return cograph

def lists_merge(list1, list2):
    merged = list()
    max_length = max(len(list1), len(list2))
    for i in range(max_length):
        if i < len(list1):
            merged.append(list1[i])
        if i < len(list2):
            merged.append(list2[i])
            
    return merged

def add_p4(graph, num_of_edges_not_including_p4):
    node = graph.nodes[random.randint(0,num_of_edges_not_including_p4-1)]
    
    print 'selected: ' + node.id
    if not node.links:
        graph.add_edge('e', 'f')
    graph.add_edge(node, 'd')
    graph.add_edge('d', 'e')

def create_p4_graph(num_of_edges_not_including_p4):
    generator = CotreeGenerator()
    cograph_generator = CographGenerator()               

    cotree = generator.generate_cotree(num_of_edges_not_including_p4)
    print cotree.write(format=8) + cotree.name
                       
    graph = cograph_generator.generate_cograph_from_cotree(cotree)
         
    add_p4(graph, num_of_edges_not_including_p4)     
    
    return graph             

def create_cograph(num_of_edges):
    generator = CotreeGenerator()
    cograph_generator = CographGenerator()               

    cotree = generator.generate_cotree(num_of_edges)
    print cotree.write(format=8) + cotree.name
                       
    graph = cograph_generator.generate_cograph_from_cotree(cotree)    
    return graph             
     
def calculate_local_neighborhood(v, slices_of_v, a_slice_of_v, is_minus=False):
    local_N = list()
    slices_of_v_in_one_list = list()
    
    for a_slice in slices_of_v:
        slices_of_v_in_one_list += a_slice 
    slices_of_v_in_one_list += [v];
    
    for node in slices_of_v_in_one_list:
        for node_in_slice in a_slice_of_v:
            if is_minus:
                if not node_in_slice in node.links and not node in local_N:
                    local_N.append(node)
            else:
                if node_in_slice in node.links and not node in local_N:
                    local_N.append(node)
    return local_N

def get_complement(graph):
    
    complement_graph = Graph()
    
    for node in graph.nodes:
        for not_an_edge_node in subtract_list(graph.nodes, node.links):
            if node != not_an_edge_node:
                complement_graph.add_edge(node.id, not_an_edge_node.id)
                
    return complement_graph


class HelperFunctionTester(unittest.TestCase):
    def test_lists_merge(self):
        list1 = [1, 3, 5]
        list2 = [2, 4] 
        
        self.assertEqual([1, 2, 3, 4, 5], lists_merge(list1, list2))           
        
        list1 = [1, 3]
        list2 = [2, 4, 5] 
        
        self.assertEqual([1, 2, 3, 4, 5], lists_merge(list1, list2))   
                
    def test_subtract_lists(self):
        list1=['a', 'b', 'c', 'd']
        list2=['b', 'c', 'e']
        
        self.assertEqual(['a', 'd'],subtract_list(list1, list2))

    