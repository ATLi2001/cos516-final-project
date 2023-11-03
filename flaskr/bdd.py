from collections import deque
import networkx as nx
import pydot
import matplotlib.pyplot as plt

# one node in BDD
class Node:
  # var is the variable of the node
  # var_assign is the variable assignment so far
  def __init__(self, var: str, var_assign: dict) -> None:
    # low, high links to successor Nodes in BDD
    self.low = None
    self.high = None
    self.var = var
    self.var_assign = var_assign
    # value of formula, only for terminal nodes (e.g. True or False)
    self.value = None

  def to_string(self) -> str:
    if self.value is not None:
      return str(self.value)
    
    return self.var


# BDD
class BDD:
  def __init__(self, ordering: list, formula) -> None:
    self.root = Node(ordering[0], {})
    self.ordering = ordering
    self.formula = formula
    self.graph = nx.DiGraph()
    self.graph.add_node(self.root)
    self.graphNodeLabel = {self.root: ordering[0]}
    self.graphEdgeLabel = {}

    self.create()
  
  # create the entire BDD
  def create(self) -> None:
    # create subtree with parent given
    # ordering_index corresponding to the variable in the ordering
    # value is the boolean value that the variable should take for this node
    def create_subtree(parent: Node, ordering_index: int, value: bool) -> Node:
      # no more unassigned variables so evaluate the formula
      if ordering_index == len(self.ordering):
        terminal_node = Node("", parent.var_assign)
        # terminal_node.value = self.formula.evaluate(parent.var_assign)

        self.graph.add_node(terminal_node)
        self.graph.add_edge(parent, terminal_node)
        self.graphNodeLabel[terminal_node] = "TF"
        self.graphEdgeLabel[(parent, terminal_node)] = int(value)

        return terminal_node
      
      # otherwise new node
      curr_var_assign = parent.var_assign.copy()
      var = self.ordering[ordering_index]
      curr_var_assign[var] = value
      x = Node(var, curr_var_assign)

      # fill out graph
      self.graph.add_node(x)
      self.graph.add_edge(parent, x)
      self.graphNodeLabel[x] = var
      self.graphEdgeLabel[(parent, x)] = int(value)

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
  
  # visualize the graph of the bdd
  def visualize(self) -> None:

    # generate the coordinates each node should be
    def generate_positions() -> dict:
      positions = {}

      vertical_space = 1 / (len(self.ordering) * 1.5)
      horizontal_space = 1 / (len(self.ordering) * 2.5)

      # do bfs on (node, x, y, level)
      queue = deque([(self.root, 0.5, 0.9, 0)])
      while len(queue) > 0:
        curr_node, x, y, level = queue.popleft()
        positions[curr_node] = (x, y)

        # need more horizontal space so nodes don't overlap
        dx = horizontal_space * 0.5**level

        if curr_node.low:
          queue.append((curr_node.low, x - dx, y - vertical_space, level+1))
        if curr_node.high:
          queue.append((curr_node.high, x + dx, y - vertical_space, level+1))
      
      return positions


    pos = generate_positions()
    nx.draw(self.graph, pos, labels=self.graphNodeLabel, with_labels=True)
    nx.draw_networkx_edge_labels(self.graph, pos, edge_labels=self.graphEdgeLabel)
    plt.show()


if __name__ == "__main__":
  bdd = BDD(["a", "b", "c", "d"], "")

  print(bdd.level_order())

  bdd.visualize()
