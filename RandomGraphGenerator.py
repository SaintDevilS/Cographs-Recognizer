from nodebox.graphics.physics import Graph
import string
import random

class RandomGraphGenerator:
    def generate_name(self, size, chars = string.ascii_uppercase):
        return ''.join(random.choice(chars) for _ in range(size))

    def add_edge_with_probability(self, g, node, other_node):
        is_edge = random.randint(0, 3)
        if is_edge == 1:
            g.add_edge(node, other_node)

    def generate_random_graph(self, num_of_nodes):
        g = Graph()
        for i in range(num_of_nodes):
            g.add_node(self.generate_name(4))
            
        for node in g.nodes:
            for other_node in g.nodes:
                if node != other_node:
                    self.add_edge_with_probability(g, node, other_node)
        
        return g      
            
        