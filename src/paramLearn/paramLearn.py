import sys
from probabilityTable import *

class ParamLearn: 

  # countFile = e.g. train2.csv 
  def __init__(self, countFile):
    self.pTable = PTable(countFile)
    self.domains = {}
    self.domains["state"] = ["AK","AL","AR","AZ","CA","CO","CT","DE","FL","GA","HI","IA","ID","IL","IN","KS","KY","LA","MA","MD","ME","MI","MN","MO","MS","MT","NC","ND","NE","NH","NJ","NM","NV","NY","OH","OK","OR","PA","RI","SC","SD","TN","TX","UT","VA","VT","WA","WI","WV","WY"]
    self.domains["gender"] = ["M","F"]
    self.domains["age"] = [5, 10, 15, 20, 25, 30, 35, 40, 45, 50, 55, 60, 65, 70, 75, 80, 85, 90, 95]
    self.domains["height"] = range(40,90)
    self.domains["weight"] = range(0,490,10)
    self.domains["BMI"] = range(0, 170)
    self.domains["sBP"] = range(10, 225, 5)
    self.domains["dBP"] = range(0, 150, 5)
    self.domains["diabetes"] = [0,1]
    self.domains["code001139"] = [0,1]
    self.domains["code140239"] = [0,1]
    self.domains["code240279"] = [0,1]
    self.domains["code280289"] = [0,1]
    self.domains["code290319"] = [0,1]
    self.domains["code320359"] = [0,1]
    self.domains["code360389"] = [0,1]
    self.domains["code390459"] = [0,1]
    self.domains["code460519"] = [0,1]
    self.domains["code520579"] = [0,1]
    self.domains["code580629"] = [0,1]
    self.domains["code630679"] = [0,1]
    self.domains["code680709"] = [0,1]
    self.domains["code710739"] = [0,1]
    self.domains["code740759"] = [0,1]
    self.domains["code760779"] = [0,1]
    self.domains["code780799"] = [0,1]
    self.domains["code800999"] = [0,1]

  def getParentJointProb(self, node_id, node_val, params):
       
    #parentCount
    parentCount = self.pTable.getCounts(params)
    #posteriorCount
    params[node_id] = node_val
    postCount = self.pTable.getCounts(params)
    x= (postCount+1.0) / (parentCount+len(self.domains[node_id]))
    return x
  def getParentChildJointProb(self, node_id, node_val, parentDict, childDict):
    
    jointParams = dict(parentDict.items()+childDict.items())
    # jointCount = self.pTable.getCounts(jointParams)
    # #posteriorCount
    # jointParams[node_id] = node_val
    # postCount = self.pTable.getCounts(jointParams)
    # return postCount*1.0 / (jointCount+0.0000000001)  
    x = self.getParentJointProb(node_id, node_val, jointParams)
    return x

def main(argv):
  countFile = argv[1]
  pLearn = ParamLearn(countFile)

if __name__ == "__main__":
  main(sys.argv)