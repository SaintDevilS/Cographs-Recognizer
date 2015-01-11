import unittest
from ete2 import Tree
from CotreeGenerator import CotreeGenerator
from CographGenerator import CographGenerator
from LexBFS import get_sigmas_and_slices
from NSP import NeighborhoodSubsetPropertyChecker
from ReportP4 import P4Reporter
from CotreeGeneratorFromCograph import CotreeGeneratorFromCograph
from helper_functions import get_graph_like_in_the_article
from RandomGraphGenerator import RandomGraphGenerator
from GraphDrawer import draw_graph
from nodebox.graphics.physics import Graph

class CographRecognizer(object):
    def recognize(self, graph):
        NSP_checker = NeighborhoodSubsetPropertyChecker()
        p4_reporter = P4Reporter()
        cotree_generator = CotreeGeneratorFromCograph() 
        
        sigma, slices, sigma_minus, slices_minus = get_sigmas_and_slices(graph)
        
        NSP_answer = NSP_checker.check_NSP(sigma, slices)
        NSP_minus_answer = NSP_checker.check_NSP(sigma_minus, slices_minus, True)
        
        if NSP_answer[0] == False:
            return ['p4', p4_reporter.report_p4(NSP_answer[1], NSP_answer[2], slices[NSP_answer[1].id])]

        if NSP_minus_answer[0] == False:
            return ['p4', p4_reporter.report_p4(NSP_minus_answer[1], NSP_minus_answer[2], slices_minus[NSP_minus_answer[1].id], True)] 
        
        return ['cotree', cotree_generator.generate_cotree(sigma[0], slices, slices_minus)]
class CographRecognizerTest(unittest.TestCase):
    cograph_recognizer = CographRecognizer()
    def test_recognize_graph_from_article(self):
        cograph = get_graph_like_in_the_article()
    
        answer = self.cograph_recognizer.recognize(cograph)
        
        self.assertNotEqual('p4', answer[0])
        
        
#         answer[1].show()
        
    def test_on_random_graph(self):
        random_generator = RandomGraphGenerator()        
        graph = random_generator.generate_random_graph(10)
         
        answer = self.cograph_recognizer.recognize(graph)
        
        print answer
        
#         draw_graph(graph)

    def test_c4s(self):
        graph = Graph()
        
        graph.add_edge('b', 'e')
        graph.add_edge('a', 'b')
        graph.add_edge('b', 'c')
        graph.add_edge('c', 'd')
        graph.add_edge('a', 'd')

        graph.add_edge('a', 'e')
        graph.add_edge('d', 'e')

        answer = self.cograph_recognizer.recognize(graph)
        print answer[1].write(format=8)
        draw_graph(graph)
        print answer
        
        