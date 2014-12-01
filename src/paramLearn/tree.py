from node import *
import sys

class Tree:

  # edgeFile  = e.g. train3.gph
  def __init__(self, edgeFile):
    self.nodeDict = dict()
    self.loadNodes(edgeFile)

  def getNode(self, id_num):
    return self.nodeDict[id_num]

  def retrieveOrCreateNode(self,id_num):
    if id_num in self.nodeDict:
      return self.nodeDict[id_num]
    else:
      self.nodeDict[id_num] = Node(id_num)
      return self.nodeDict[id_num]

  #read in .gph file and populate nodes with data
  def loadNodes(self, edgeFile):
    fo = open(edgeFile)
    line = fo.readline().rstrip()
    while line:
      node_ids = line.split(', ')
      node1 = self.retrieveOrCreateNode(node_ids[0]) 
      node2 = self.retrieveOrCreateNode(node_ids[1])
      node1.addChild(node2)
      node2.addParent(node1)
      line = fo.readline().rstrip()

def main(argv):
  edgeFile = argv[1]
  tree = Tree(edgeFile)
  print str(len(tree.nodeDict)) + " nodes loaded to tree."

if __name__ == "__main__":
  main(sys.argv)