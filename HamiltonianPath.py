# -*- coding: utf-8 -*-

from ete2 import Tree
import unittest
from nodebox.graphics.physics import Graph
from CotreeGenerator import CotreeGenerator

# based on:
# D. G. Corneil, H. Lerchs, and L. K. Stewart, "Complement reducible graphs," Discrete
# Applied Mathematics, Vol. 3, 1981, pp. 163-174.

class HamiltonianPathTester():
    def get_max_scattering_number(self, children_scattering_number_and_size):
        max_scattering_number = children_scattering_number_and_size[0][0]
        
        for child_scattering_number_and_size in children_scattering_number_and_size[1:]:
            if max_scattering_number < child_scattering_number_and_size[0]:
                max_scattering_number = child_scattering_number_and_size[0]
                
        return max_scattering_number
    
    def get_sum_of_children_size(self, children_scattering_number_and_size):
        sum_of_children_size = 0
        for child_scattering_number_and_size in children_scattering_number_and_size:
            sum_of_children_size += child_scattering_number_and_size[1]
            
        return sum_of_children_size
    
    def get_scattering_number_and_size(self, cotree):
# scattering number and number of leaves to reduce a second iteration over the tree
        if cotree.is_leaf():
            return (-1, 1)
        
        children_scattering_number_and_size = list()
        for child in cotree.get_children():
            children_scattering_number_and_size.append(self.get_scattering_number_and_size(child))
        
        graph_size = self.get_sum_of_children_size(children_scattering_number_and_size)
                
        if cotree.name == '1':
            max_scattering_number = self.get_max_scattering_number(children_scattering_number_and_size)
            return (max_scattering_number - graph_size, graph_size)
 
        else:
            scattering_number = 0
            for child_scattering_number_and_size in children_scattering_number_and_size:
                scattering_number += max(child_scattering_number_and_size[0], 1)
            
            return (scattering_number, graph_size)


    def test_for_hamiltonian_path(self, cotree):
        scattering_number = self.get_scattering_number_and_size(cotree)[0]

        if scattering_number <= 1:
            return (True, scattering_number)
        
        return (False, scattering_number)
        
class HamiltonianPathTesterTest(unittest.TestCase):
    tester = HamiltonianPathTester()
    def test_simple_hamiltonian_path(self):
        cotree = Tree("((a,c)1,(b,d)1);",format=8)
        cotree.name = '1'
        
        is_path = self.tester.test_for_hamiltonian_path(cotree)
        
        self.assertEqual(True, is_path[0])

    def test_not_hamiltonian_path(self):
        cotree = Tree("((a,c)1,(b,d)1);",format=8)
        cotree.name = '0'
        
        is_path = self.tester.test_for_hamiltonian_path(cotree)
        
        self.assertEqual(False, is_path[0])

    def test_another_hamiltonian_path(self):
        cotree = Tree("((a,c)0,(b,d)1);",format=8)
        cotree.name = '1'
        
        is_path = self.tester.test_for_hamiltonian_path(cotree)
        
        self.assertEqual(True, is_path[0])
    
    def test_example_from_article(self):
        cotree = Tree("(((v,u)1,(w,y)1)0,(((b,c)0,d)1,e,(z,(a,x)0)1)0);",format=8)
        cotree.name = '1'

        is_path = self.tester.test_for_hamiltonian_path(cotree)

        self.assertEqual(True, is_path[0])
    
    def test_on_random(self):
        generator = CotreeGenerator()
        cotree = generator.generate_cotree(100)
        
        print cotree.write(format=8, format_root_node=True)
 
        is_path = self.tester.test_for_hamiltonian_path(cotree)
        print is_path
        