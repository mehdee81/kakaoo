import random

class Graph:
    def __init__(self, edges):
        self.edges = edges
        self.adj_dict = {}
        self.create_adj_dict()

    def create_adj_dict(self):
        for start, dist in self.edges:
            if start in self.adj_dict:
                self.adj_dict[start].append(dist)
            else:
                self.adj_dict[start] = [dist]

        for dist, start in self.edges:
            if start in self.adj_dict:
                self.adj_dict[start].append(dist)
            else:
                self.adj_dict[start] = [dist]

    # greedy
    def greedy_coloring(self):
        num_colors = len(self.adj_dict.keys())
        colors = {node: None for node in self.adj_dict.keys()}
        for node in self.adj_dict.keys():
            available_colors = set(range(num_colors)) - set(
                colors[nei] for nei in self.adj_dict[node] if colors[nei] is not None
            )
            if available_colors:
                colors[node] = min(available_colors)

        output_dict = {}
        for key, value in colors.items():
            if value in output_dict:
                output_dict[value].append(key)
            else:
                output_dict[value] = [key]
        return output_dict

    # backtracking
    def backtracking_coloring(self):

        num_colors = len(self.adj_dict)

        node_colors = {node: None for node in self.adj_dict}

        def is_valid_color(node, color):
            for neighbor in self.adj_dict[node]:
                if node_colors[neighbor] == color:
                    return False
            return True

        def color_node(node, color):
            if color > num_colors:
                return False

            if node_colors[node] is not None:
                return True

            for i in range(1, color + 1):
                if is_valid_color(node, i):
                    node_colors[node] = i
                    if all(
                        color_node(neighbor, color) for neighbor in self.adj_dict[node]
                    ):
                        return True
                    node_colors[node] = None

            return False

        color_node(next(iter(self.adj_dict)), num_colors)

        output_dict = {}
        for key, value in node_colors.items():
            if value not in output_dict:
                output_dict[value] = [key]
            else:
                output_dict[value].append(key)
        return output_dict