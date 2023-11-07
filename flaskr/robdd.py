from bdd import BDD, Node
from typing import Optional, List
from collections import Counter

# ROBDD that can go step by step
class ROBDD:
  def __init__(self, bdd: BDD) -> None:
    self.curr_robdd = bdd
  
  # take one step to final ROBDD
  # return true if step taken, false otherwise
  def next(self) -> bool:
    # find a duplicate subtree in current tree
    # no guarantee on which duplicate subtree
    def find_duplicate_subtree(x: Optional[Node]) -> List[Optional[Node]]:
      ans = {}
      count = Counter()

      def encode(x: Optional[Node]) -> str:
        if not x:
          return ""
        
        encoded = ""
        if x.value:
          encoded += x.value
        else:
          encoded += x.var 
        encoded += "#" + encode(x.low) + "#" + encode(x.high)

        count[encoded] += 1
        # first appearance
        if count[encoded] == 1:
          ans[encoded] = [x]
        # duplicate detected
        else:
          ans[encoded].append(x)
        return encoded
      
      encode(x)

      if len(ans) > 0:
        for k in ans.keys():
          v = ans[k]
          if len(v) > 1:
            print(k)
            return v
      
      return None
    
    dup = find_duplicate_subtree(self.curr_robdd.root)
    if not dup:
      return False
    
    # dup has all duplicates, take first two
    assert(len(dup) >= 2)
    dup1 = dup[0]
    dup2 = dup[1]

    # if duplicates have same parent, then parent is redundant
    if dup1.parent == dup2.parent:
      # if dup parent parent is None, then dup parent is root
      if not dup1.parent.parent:
        self.curr_robdd.root = dup1
      else:
        grandparent = dup1.parent.parent 
        if grandparent.low == dup1.parent:
          grandparent.low = dup1
        else:
          grandparent.high = dup1
      # change dup1 parent link
      dup1.parent = dup1.parent.parent
      
    # otherwise, parent links can both go to dup1
    else:
      if dup2.parent.low == dup2:
        dup2.parent.low = dup1
      else:
        dup2.parent.high = dup1
      
    # delete dup2
    del dup2

    return True
  

if __name__ == "__main__":
  bdd = BDD(["a", "b", "c"], "")
  print(bdd.level_order())
  bdd.visualize()

  robdd = ROBDD(bdd)
  while(robdd.next()):
    robdd.curr_robdd.visualize()
