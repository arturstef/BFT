import random


class Graph:
  def __init__(self, vertices = [], edges = {}, edges_array = []):
    self.vertices = vertices
    self.edges = edges
    self.edges_array = edges_array
    self.create_edges_array(self.edges)

  def __str__(self):
    return "Nodes: " + str(self.vertices) + "\nEdges: " + str(self.edges) + "\nEdges Array: " + str(self.edges_array)
  
  def find_node_by_position(self, x, y):
    for node in self.vertices:
      if node.position[0] == x and node.position[1] == y:
        return node
    return None
  
  def create_edges_array(self, edges):
    self.edges_array = []
    edges = self.edges.keys()
    for edge in edges:
      edge = edge.split(',')
      edge = [int(i) for i in edge]
      # print(edge)
      self.edges_array.append(edge)
    # print(self.edges_array)

  def get_node_neighbours(self, node_id):
    neighbours = []
    for i in range(len(self.edges_array)):
      if self.edges_array[i][0] == node_id:
        neighbours.append(self.edges_array[i][1])
      elif self.edges_array[i][1] == node_id:
        neighbours.append(self.edges_array[i][0])
    return neighbours
  
  def get_node_by_id(self, node_id):
    for node in self.vertices:
      if node.node_id == node_id:
        return node
    return None

  def set_nodes_faulty_percent(self, faulty_percent = 50): # call it to set the nodes to be faulty
    print(f'vertices: {self.vertices}, len: {len(self.vertices)}')
    faulty_nodes = []
    n = int(len(self.vertices) * faulty_percent)/100
    while len(faulty_nodes) < n:
      node = random.choice(self.vertices)
      if node not in faulty_nodes:
        faulty_nodes.append(node)

    for node in faulty_nodes:
      node.is_faulty = True


  def set_nodes_choice_percent(self, choice_percent = 50): # call it to set the nodes to set the choice
    attackers = []
    n = int(len(self.vertices) * choice_percent)/100
    while len(attackers) < n:
      node = random.choice(self.vertices)
      if node not in attackers:
        attackers.append(node)

    for node in attackers:
      node.current_choice = True

  def copy(self):
    vertices_copy = []
    for vertex in self.vertices:
      vertices_copy.append(vertex.copy())
    return Graph(vertices_copy, self.edges.copy(), self.edges_array.copy())