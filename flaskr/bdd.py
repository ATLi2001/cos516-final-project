from collections import deque
from typing import List
import networkx as nx

import matplotlib.pyplot as plt
import os
import re

from flaskr.parse_utils import cleanFileName

import matplotlib
matplotlib.use('Agg')

# one node in BDD
class Node:
  # var is the variable of the node
  # var_assign is the variable assignment so far
  def __init__(self, var: str, var_assign: dict) -> None:
    # low, high links to successor Nodes in BDD
    self.low = None
    self.high = None
    # parent link
    self.parent = []
    # node's variable and assignment so far
    self.var = var
    self.var_assign = var_assign
    # value of formula, only for terminal nodes (e.g. True or False)
    self.value = None

  def to_string(self) -> str:
    if self.value:
      return str(self.value)
    
    return self.var
  
  # return all nodes (including self) that are in this subtree
  def get_subtree(self) -> List:
    out = [self]

    if self.low:
      out += self.low.get_subtree()
    if self.high: 
      out += self.high.get_subtree()
    
    return out


# BDD
class BDD:
  def __init__(self, ordering: list, formula) -> None:
    self.root = Node(ordering[0], {})
    self.ordering = ordering
    self.formula = formula
    self.graph = nx.DiGraph()
    self.graphNodeLabel = {}
    self.graphEdgeLabel = {}
    self.terminal_nodes = []

    self.create()
  
  # create the entire BDD
  def create(self) -> None:
    # create subtree with parent given
    # ordering_index corresponding to the variable in the ordering
    # value is the boolean value that the variable should take for this node
    def create_subtree(parent: Node, ordering_index: int, value: bool) -> Node:

      # Need to make sure var_assignment is based on the previous assignment
      curr_var_assign = parent.var_assign.copy()
      prev_var = self.ordering[ordering_index - 1]

      curr_var_assign[prev_var] = value
    
      # no more unassigned variables so evaluate the formula
      if ordering_index == len(self.ordering):
        print(curr_var_assign)
        terminal_node = Node("", curr_var_assign)
        terminal_node.parent.append(parent)
        value = self.formula.evaluate(curr_var_assign)
        if value == True:
          terminal_node.value = "T"
        if value == False:
          terminal_node.value = "F"
        #terminal_node.value = "TF"

        return terminal_node
      
      # otherwise new node
     
      var = self.ordering[ordering_index]
      x = Node(var, curr_var_assign)
      x.parent.append(parent)

      # recursively assign low and high
      x.low = create_subtree(x, ordering_index+1, False)
      x.high = create_subtree(x, ordering_index+1, True)

      return x
    
    self.root.low = create_subtree(self.root, 1, False)
    self.root.high = create_subtree(self.root, 1, True)
  
  # level order traversal of bdd
  def level_order(self) -> str:
    
    out_str = ""
    queue = deque([self.root])

    while len(queue) > 0:
      node = queue.popleft()
      out_str += node.to_string() + " "

      if node.low:
        queue.append(node.low)
      if node.high:
        queue.append(node.high)
    
    return out_str
  

  # regenerate graph, assuming create has been called
  def regen_graph(self) -> None:
    # reset graph attributes
    self.graph = nx.DiGraph()
    self.graphNodeLabel = {}
    self.graphEdgeLabel = {}
    self.terminal_nodes = []

    # add nodes, edges, and labels recursively
    def regen_graph_help(x: Node) -> None:
      self.graph.add_node(x)
      self.graphNodeLabel[x] = x.to_string()
      
      if x.low:
        self.graph.add_edge(x, x.low)
        self.graphEdgeLabel[(x, x.low)] = 0
        regen_graph_help(x.low)
      if x.high:
        self.graph.add_edge(x, x.high)
        self.graphEdgeLabel[(x, x.high)] = 1
        regen_graph_help(x.high)
      
      if not x.low and not x.high:
        self.terminal_nodes.append(x)

    regen_graph_help(self.root)

  
  # visualize the graph of the bdd
  def visualize(self, nodes_to_color=None, manual_readjust=False) -> None:

    # generate the coordinates each node should be
    # width, heightare overall rectangle space
    def generate_positions(width: float, height: float, manual_readjust: bool) -> dict:
      positions = {}

      vertical_space = height / (len(self.ordering) * 1.5)
      horizontal_space = width / (len(self.ordering) * 2.5)

      root_y = 0.9 * height

      # do bfs on (node, x, y, level)
      queue = deque([(self.root, 0.5 * width, root_y, 0)])
      # track the nodes on each level
      level_track = {}
      while len(queue) > 0:
        curr_node, x, y, level = queue.popleft()
        positions[curr_node] = (x, y)

        level_track[curr_node] = level

        # need more horizontal space so nodes don't overlap
        dx = horizontal_space * 0.5**level

        if curr_node.low:
          queue.append((curr_node.low, x - dx, y - vertical_space, level+1))
        if curr_node.high:
          queue.append((curr_node.high, x + dx, y - vertical_space, level+1))
      
      # manually readjust positions
      if manual_readjust:
        # go from level to nodes
        rev_level_track = {}
        for k, v in level_track.items():
          if v not in rev_level_track.keys():
            rev_level_track[v] = [k]
          else: 
            rev_level_track[v].append(k)

        # for each level, adjust positions
        for l, nodes in rev_level_track.items():
          nodes_with_xpos = []
          for n in nodes:
            nodes_with_xpos.append((n, positions[n][0]))
          
          # center the nodes from left to right
          for i, nx in enumerate(sorted(nodes_with_xpos, key=lambda nx: nx[1])):
            positions[nx[0]] = ((i+1) * width / (len(nodes) + 1), root_y - l * vertical_space)
      
      return positions

    # always reset graph before drawing
    self.regen_graph()
    scale = max(len(self.ordering) - 3, 1)
    height = 4.8 * scale
    width = 6.4 * scale
    pos = generate_positions(width, height, manual_readjust)
    plt.figure(figsize=(width, height))
    nx.draw(self.graph, pos, labels=self.graphNodeLabel, with_labels=True, node_color="#ffd7b5")
    # draw terminal nodes with different color
    red_node   = [v for v in self.terminal_nodes if v.value == "F"]
    green_node = [v for v in self.terminal_nodes if v.value == "T"]
    nx.draw_networkx_nodes(self.graph, pos, green_node, node_color="#00ff00")
    nx.draw_networkx_nodes(self.graph, pos, red_node, node_color="#ff0000")
    # draw low edges, high edges in different colors
    low_edges = [e for e in self.graphEdgeLabel.keys() if self.graphEdgeLabel[e] == 0]
    high_edges = [e for e in self.graphEdgeLabel.keys() if self.graphEdgeLabel[e] == 1]
    nx.draw_networkx_edges(self.graph, pos, low_edges, edge_color="#ff5252")
    nx.draw_networkx_edges(self.graph, pos, high_edges, edge_color="#000000")
    # highlight extra nodes
    if nodes_to_color:
      nx.draw_networkx_nodes(self.graph, pos, nodes_to_color, node_color="#ffff00")
    nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.graphEdgeLabel)
    #plt.show()

    # Instead of showing plot, save it to a unique file name.
    def uniquify(path):
      filename, extension = os.path.splitext(path)
      counter = 1

      #replace spaces with _ to faciliate image loading
      filename = cleanFileName(filename)
      path = filename + "(" + str(counter) + ")" + extension

      read_adjust = "_adjust" if manual_readjust else ""

      while os.path.exists(path):
          path = filename + "(" + str(counter) + ")" + read_adjust + extension
          counter += 1

      return path
  
    plt.savefig(uniquify(f"static/images/{self.formula.__str__()}.png"))
    plt.clf()

if __name__ == "__main__":
  bdd = BDD(["a", "b", "c", "d"], "")

  print(bdd.level_order())

  bdd.visualize()

