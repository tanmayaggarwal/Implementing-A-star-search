
from math import sqrt, inf

def shortest_path(M, start, goal):
    
    new_map = Graph(start, goal)
    new_map.create_intersections(M.intersections)
    new_map.add_roads(M.roads)
    
    start_node = new_map.nodes[start]
    end_node = new_map.nodes[goal]
    
    distance_dict = {node: inf for node in new_map.nodes}
    distance_dict[start_node] = 0
    
    visited = set()
    came_from = {}
    cumulative_path_cost = {start_node: 0}
   
    while distance_dict:
        # Pop the shortest path 
        current_node, node_distance = sorted(distance_dict.items(), key=lambda x: x[1])[0]
        distance_dict.pop(current_node)
        
        if current_node in visited:
            continue
            
        if current_node.name == goal:
            reverse_path = [goal]
            while goal != start:
                goal = came_from[goal]
                reverse_path.append(goal)
            return list(reversed(reverse_path))
        
        visited.add(current_node)
        
        for road in current_node.roads:
            if road.node in visited:
                continue
            if road.node in distance_dict:
                new_node_cumulative_path_cost = cumulative_path_cost[current_node] + road.path_cost
                new_node_f = new_node_cumulative_path_cost + road.node.est_distance
                if distance_dict[road.node] > new_node_f:
                    distance_dict[road.node] = new_node_f
                if (road.node not in cumulative_path_cost or new_node_cumulative_path_cost < cumulative_path_cost[road.node]):
                    cumulative_path_cost[road.node] = new_node_cumulative_path_cost
                    came_from[road.node.name] = current_node.name
                    
    print("shortest path called")
    return None

class Graph(object):
    def __init__(self, start, goal):
        self.start = start
        self.goal = goal
        self.nodes = []
    
    def create_intersections(self, intersections):
        goal_coordinates = intersections[self.goal]
        
        for intersection, coordinates in intersections.items():
            if intersection == self.start:
                self.nodes.append(GraphNode(intersection, coordinates, goal_coordinates, True))
            else:
                self.nodes.append(GraphNode(intersection, coordinates, goal_coordinates, False))
        
    def add_roads(self, roads):
        for node1 in self.nodes:
            for intersection in roads[node1.name]:
                node2 = self.nodes[intersection]
                path_cost = path_cost_g(node1.coordinates, node2.coordinates)
                node1.add_child(node2, path_cost)
            
class GraphNode(object):
    def __init__(self, intersection, coordinates, goal, start):
        self.name = intersection
        self.coordinates = coordinates
        self.roads = []
        self.est_distance = est_distance_h(self.coordinates, goal)
        self.is_start = start

    def add_child(self, intersection, path_cost):
        self.roads.append(GraphEdge(intersection, path_cost))
    
class GraphEdge(object):
    def __init__(self, intersection, path_cost):
        self.node = intersection
        self.path_cost = path_cost

def distance(point_a, point_b):
    x_a, y_a = point_a[0], point_a[1]
    x_b, y_b = point_b[0], point_b[1]
    
    return (sqrt((x_b - x_a)**2 + (y_b - y_a)**2))

def path_cost_g(point_x, point_y):
    return distance(point_x, point_y)

def est_distance_h(point_y, goal_coordinates):    
    return distance(point_y, goal_coordinates)*0.95       # To ensure h is admissable and less than the true cost

