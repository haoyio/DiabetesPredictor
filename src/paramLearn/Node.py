class Node:
  def __init__(self, number):
    self.parents = []
    self.children = []
    self.id = number

  def getParents(self):
    return self.parents

  def getChildren(self):
    return self.children

  def addParent(self, node):
    self.parents.append(node)

  def addChild(self, node):
    self.children.append(node)

  def getID(self):
    return self.id