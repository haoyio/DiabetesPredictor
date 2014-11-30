import sys
from Node import *

class Tree:
  def __init__(self, edgeFile):
    self.nodeDict = dict()
    self.loadNodes(edgeFile)
  #read in .gph file and populate nodes with data
  def loadNodes(self, edgeFile):
    fo = open(edgeFile)
    line = fo.readline()
    while line:
      node_ids = line.split()
      id1 = node_ids[0]
      id2 = node_ids[1]
      node1 = None 
      node2 = None
      if id1 in self.nodeDict:
        node1 = self.nodeDict[id1]
      else:
        node1 = Node(id1)
      if id2 not in self.nodeDict:
        node2 = Node(id2)
      line = fo.readline()

def main(argv):
  edgeFile = argv[0]
  emrFile  = argv[1]
  tree = Tree(edgeFile)

if __name__ == "__main__":
  main(sys.argv)