import unittest
from nodebox.graphics.physics import Graph
from ete2 import Tree
from LexBFS import get_sigmas_and_slices
from CographGenerator import CographGenerator
from NSP import NeighborhoodSubsetPropertyChecker
from helper_functions import *

class P4Reporter:

    def report_p4_of_minus(self, v, j, slices_of_v, y, w):
        if y in v.links:
            return [v.id, w.id, y.id, slices_of_v[j+1][0].id]
        elif w not in y.links:
            return [slices_of_v[j][0].id, w.id, y.id, slices_of_v[j+1][0].id] 
        return [y.id, v.id, w.id, slices_of_v[j][0].id]

    def report_p4_of_plus(self, v, j, slices_of_v, y ,w):
        if y not in v.links:
            return [v.id, w.id, y.id, slices_of_v[j+1][0].id]
        elif w in y.links:
            return [slices_of_v[j][0].id, w.id, y.id, slices_of_v[j+1][0].id] 
        return [y.id, v.id, w.id, slices_of_v[j][0].id]
        
    def report_p4(self, v, j, slices_of_v, is_minus=False):
        v_j_local = calculate_local_neighborhood(v, slices_of_v[0:j], slices_of_v[j], is_minus)
        v_j_1_local = calculate_local_neighborhood(v, slices_of_v[0:j+1], slices_of_v[j+1], is_minus)
        
        w = lists_intersection(subtract_list(v_j_local, v_j_1_local), slices_of_v[0])[0]
        y = subtract_list(v_j_1_local, v_j_local)[-1]
        
        if is_minus:
            return self.report_p4_of_minus(v, j, slices_of_v, y, w)
        return self.report_p4_of_plus(v, j, slices_of_v, y, w)

class P4ReporterTest(unittest.TestCase):
    reporter = P4Reporter()
    cograph_generator = CographGenerator()
                
    def test_simple_report_p4(self):
        graph = Graph()
          
        graph.add_edge('a', 'b')
        graph.add_edge('b', 'c')
        graph.add_edge('c', 'd')
          
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
          
        self.assertEqual(['a', 'b', 'c', 'd'], self.reporter.report_p4(graph.node('a'), 1, slices['a']))
    def test_second_case(self):
        graph = Graph()
         
        graph.add_edge('c', 'a')
        graph.add_edge('b', 'c')
        graph.add_edge('a', 'd')
        graph.add_edge('b', 'd')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'f')
        graph.add_edge('e', 'a')
         
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
                
        self.assertEqual(['d', 'a', 'e', 'f'], self.reporter.report_p4(graph.node('c'), 1, slices['c']))
 
    def test_third_case(self):
        graph = Graph()
          
        graph.add_edge('c', 'a')
        graph.add_edge('b', 'c')
        graph.add_edge('a', 'd')
        graph.add_edge('b', 'd')
        graph.add_edge('c', 'e')
        graph.add_edge('e', 'f')
          
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
                 
        self.assertEqual(['e', 'c', 'a', 'd'], self.reporter.report_p4(graph.node('c'), 1, slices['c']))
         
    def test_first_case_minus(self):
        cotree = Tree("(((b,c)1,(d,e)0)0,((f,(g,(h,(i,j)1)0)1)0,a)0)0;",format=8)
          
        graph = self.cograph_generator.generate_cograph_from_cotree(cotree)
          
        graph.add_edge('g', 'k')
        graph.add_edge('k', 'l')
          
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
                   
        self.assertEqual(['g', 'l', 'j', 'k'], self.reporter.report_p4(graph.node('g'), 1, slices_minus['g'], True))
 
    def test_second_case_minus(self):
        graph = Graph()
           
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'a')
        graph.add_edge('b', 'c')
        graph.add_edge('b', 'd')
        graph.add_edge('c', 'e')
         
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
 
        self.assertEqual(['b', 'e', 'd', 'c'], self.reporter.report_p4(graph.node('a'), 1, slices_minus['a'], True))
         
    def test_third_case_minus(self):
        graph = Graph()
           
        graph.add_edge('a', 'c')
        graph.add_edge('b', 'e')
        graph.add_edge('c', 'd')
        graph.add_edge('d', 'a')
        graph.add_edge('d', 'b')
        graph.add_edge('d', 'c')
        graph.add_edge('e', 'c')
             
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
                  
        self.assertEqual(['b', 'a', 'e', 'd'], self.reporter.report_p4(graph.node('a'), 1, slices_minus['a'], True))
    
    def check_if_p4(self, graph, p4):
        first_in_p4 = graph.node(p4[0])
        second_in_p4 = graph.node(p4[1])
        third_in_p4 = graph.node(p4[2])
        fourth_in_p4 = graph.node(p4[3])
        
        if (third_in_p4 in first_in_p4.links or fourth_in_p4 in first_in_p4.links) or second_in_p4 not in first_in_p4.links:
            return False
        
        if fourth_in_p4 in second_in_p4.links or (third_in_p4 not in second_in_p4.links or first_in_p4 not in second_in_p4.links):
            return False
        
        if first_in_p4 in third_in_p4.links or (second_in_p4 not in third_in_p4.links or fourth_in_p4 not in third_in_p4.links):
            return False

        if (first_in_p4 in fourth_in_p4.links or second_in_p4 in fourth_in_p4.links) or third_in_p4 not in fourth_in_p4.links:
            return False
        
        return True
    def test_p4_of_random_graphs(self):
        for i in range(10):
            graph = create_p4_graph(10)
            checker = NeighborhoodSubsetPropertyChecker()
                    
            sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
            
            nsp_answer = checker.check_NSP(sigma, slices)
            nsp_minus_answer = checker.check_NSP(sigma_minus, slices_minus, True)
            
            if nsp_answer[0] == False:
                p4 = self.reporter.report_p4(nsp_answer[1], nsp_answer[2], slices[nsp_answer[1].id])
                self.assertTrue(self.check_if_p4(graph, p4))
            
            if nsp_minus_answer[0] == False:
                p4 = self.reporter.report_p4(nsp_minus_answer[1], nsp_minus_answer[2], slices_minus[nsp_minus_answer[1].id], True)  
                complement_graph = get_complement(graph)          
                self.assertTrue(self.check_if_p4(complement_graph, p4))
        