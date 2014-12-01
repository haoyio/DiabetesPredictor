import sys
from probabilityTable import *

class ParamLearn:
  
  # countFile = e.g. train2.csv 
  def __init__(self, countFile):
    self.pTable = PTable(countFile)

  def getParentChildJointProb(self, node_id, node_val, parentDict, childDict):
    
    jointParams = dict(parentDict.items()+childDict.items())
    jointCount = self.pTable.getCounts(jointParams)

    #posteriorCount
    jointParams[node_id] = node_val
    postCount = self.pTable.getCounts(jointParams)

    return postCount*1.0 / jointCount  

  def getParentJointProb(self, node_id, node_val, parentDict):
     
    #parentCount
    params = parentDict
    parentCount = self.pTable.getCounts(params)
    #posteriorCount
    params = parentDict
    params[node_id] = node_val
    postCount = self.pTable.getCounts(params)

    return postCount*1.0 / parentCount

def main(argv):
  countFile = argv[1]
  pLearn = ParamLearn(countFile)

if __name__ == "__main__":
  main(sys.argv)