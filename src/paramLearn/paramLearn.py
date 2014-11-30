import sys
from tree import *
from probabilityTable import *

#from gibbsinference
domains = {}
domains["state"] = ["AK","AL","AR","AZ","CA","CO","CT","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
domains["gender"] = ["M","F"]
domains["age"] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
domains["height"] = range(40,90)
domains["weight"] = range(0,490,10)
domains["BMI"] = range(0, 170)
domains["sBP"] = range(10, 225, 5)
domains["dBP"] = range(0, 150, 5)
domains["diabetes"] = [0,1]


domains["code001139"] = [0,1]
domains["code140239"] = [0,1]
domains["code240279"] = [0,1]
domains["code280289"] = [0,1]
domains["code290319"] = [0,1]
domains["code320359"] = [0,1]
domains["code360389"] = [0,1]
domains["code390459"] = [0,1]
domains["code460519"] = [0,1]
domains["code520579"] = [0,1]
domains["code580629"] = [0,1]
domains["code630679"] = [0,1]
domains["code680709"] = [0,1]
domains["code710739"] = [0,1]
domains["code740759"] = [0,1]
domains["code760779"] = [0,1]
domains["code780799"] = [0,1]
domains["code800999"] = [0,1]

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