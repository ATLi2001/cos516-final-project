from flaskr.bdd import BDD, Node
from typing import Optional, List
from collections import Counter
import pdb

# ROBDD that can go step by step
class ROBDD:
  def __init__(self, bdd: BDD) -> None:
    self.curr_robdd = bdd
  
  # take one step to final ROBDD
  # return true if step taken, false otherwise
  def next(self) -> bool:
    if not self.merge_duplicate():
      return False
    
    # now check for redundancy
    while True:
      if not self.remove_redundant():
        break
    return True
  
  # find duplicate subtrees, then merge them
  def merge_duplicate(self) -> bool:
    # find a duplicate subtree in current tree
    # no guarantee on which duplicate subtree
    def find_duplicate_subtree(x: Optional[Node]) -> List[Optional[Node]]:
      ans = {}
      count = Counter()

      def encode(x: Optional[Node]) -> str:
        if not x:
          return ""
        
        encoded = x.to_string() + "#" + encode(x.low) + "#" + encode(x.high)

        count[encoded] += 1
        # first appearance
        if count[encoded] == 1:
          ans[encoded] = [x]
        # duplicate detected
        else:
          if x not in ans[encoded]:
            ans[encoded].append(x)
        return encoded
      
      encode(x)

      if len(ans) > 0:
        for k in ans.keys():
          v = ans[k]
          if len(v) > 1:
            return v
      
      return None
    
    dup = find_duplicate_subtree(self.curr_robdd.root)
    if not dup:
      return False
    
    # dup has all duplicates, take first two
    assert(len(dup) >= 2)
    dup1 = dup[0]
    dup2 = dup[1]

    # highlight the subtrees rooted at dup1, dup2
    dup_subtrees = dup1.get_subtree() + dup2.get_subtree()
    self.curr_robdd.visualize(dup_subtrees)

    # all parents now point to only one of the duplicates
    for parent in dup2.parent:
      if parent.low == dup2:
        parent.low = dup1
      else:
        parent.high = dup1

      if parent not in dup1.parent:
        dup1.parent.append(parent)

    del dup2

    return True
  
  # remove redundant node (node with low and high the same)
  def remove_redundant(self) -> bool:
    # find one redundant node 
    def find_redundant(x: Optional[Node]) -> Optional[Node]:
      if not x:
        return None
      
      # both children not none and the same node
      if x.low and x.high and x.low == x.high:
        return x
      
      low_result = find_redundant(x.low)
      if low_result:
        return low_result
      
      high_result = find_redundant(x.high)
      if high_result:
        return high_result
      
      return None
    
    redundant_node = find_redundant(self.curr_robdd.root)

    if not redundant_node:
      return False
    
    # check if redundant_node is root
    if redundant_node == self.curr_robdd.root:
      self.curr_robdd.root = redundant_node.low
    else:
      # parent can point around redundant_node
      for parent in redundant_node.parent:
        if parent.low == redundant_node:
          parent.low = redundant_node.low
        else:
          parent.high = redundant_node.low
        
        redundant_node.low.parent.remove(redundant_node)
        if parent not in redundant_node.low.parent:
          redundant_node.low.parent.append(parent)
    
    del redundant_node
    
    return True
  
# TODO: somehwere here parents are getting messed up
if __name__ == "__main__":
  bdd = BDD(["a", "b", "c"], "")
  print(bdd.level_order())
  bdd.visualize()

  pdb.set_trace()

  robdd = ROBDD(bdd)
  while(robdd.next()):
    robdd.curr_robdd.visualize()
