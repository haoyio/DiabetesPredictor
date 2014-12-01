import sys
from tree import *
from probabilityTable import *

class ParamLearn:
  
  def __init__(self, edgeFile, countFile):
    self.tree = Tree(edgeFile)
    print str(len(tree.nodeDict)) + " nodes loaded to tree."
    self.pTable = PTable(countFile)

  def getParentChildJointProb(node_id, node_val, parentDict, childDict):
    
    jointParams = dict(parentDict.items()+childDict.items())
    jointCount = self.pTable.getCounts(jointParams)

    #posteriorCount
    jointParams[node_id] = node_val
    postCount = self.pTable.getCounts(jointParams)

    return postCount*1.0 / jointCount  

  def getParentJointProb(node_id,node_val, parentDict):
     
    #parentCount
    params = parentDict
    parentCount = self.pTable.getCounts()
    #posteriorCount
    params = parentDict
    params[node_id] = node_val
    postCount = self.pTable.getCounts()

    return postCount*1.0 / parentCount

def main(argv):
  edgeFile = argv[1]
  countFile = argv[2]
  pLearn = ParamLearn(edgeFile, countFile)

if __name__ == "__main__":
  main(sys.argv)