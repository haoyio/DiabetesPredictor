import sys
sys.path.insert(0, 'paramLearn')

import csv
import random
from paramLearn import *
from tree import *
import time
from numpy import cumsum, sort, sum, searchsorted
from numpy.random import rand

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

# initialize tree and paramLearn objects
graph = Tree('output/train3.gph')
print graph.nodeDict.keys()
print str(len(graph.nodeDict)) + " nodes loaded into graph"

pLearn = ParamLearn('train2.csv')

nameMap = {}
names = []
data = []
withheldData = []
labels = []
probabilities = []
with open('test2.csv', 'rb') as csvfile:
  testreader = csv.reader(csvfile, dialect='excel')
  for row in testreader:
    for i in range(len(row)):
      nameMap[row[i]] = i
      names.append(row[i])
    break
  for row in testreader:
    labels.append(row[nameMap["diabetes"]])
    data.append(row)
del names[nameMap["diabetes"]]

# delete features adjacent to diabetes from each row
childrenNodes = graph.getNode("diabetes").getChildren()
parentNodes = graph.getNode("diabetes").getParents()
for row in data:  
  withheld = {}
  for child in childrenNodes:
    withheld[child.id] = 0
  for parent in parentNodes:
    withheld[parent.id] = 0
  withheld["diabetes"] = 0
  withheldData.append(withheld)


def weightedChoice(objects, weights):
  """
  Weighted random selection
  returns n_picks random indexes.
  the chance to pick the index i 
  is give by the weight weights[i].
  """
  n_picks = 1
  t = cumsum(weights)
  s = sum(weights)
  return objects[searchsorted(t,rand(n_picks)*s)]


# Gibbs sampling
iterNum = 20
nSamples = 50

print "Running Gibbs sampling for " + str(nSamples) + " samples"
tNet = time.time()

for row in range(nSamples):
  
  t = time.time()

  # initialize withheldData[row]'s contents random values
  for name in withheldData[row]:
    withheldData[row][name] = random.choice(domains[name])
  
  # TODO: we need to have some convergence criteria; too slow!
  for iterIdx in range(iterNum):
    newWithheld = {}
    
    # loop through labels in withheldData[row] and random sample 
    # based on weights to form newWithheld
    for name in withheldData[row]:
      
      jProbs = []
      for nodeValue in domains[name]:
        
        # get parent and child values in dictionary
        parentValues = {parent.id : data[row][nameMap[parent.id]] \
                        for parent in graph.getNode(name).getParents()}
        childrenValues = {child.id : data[row][nameMap[child.id]] \
                          for child in graph.getNode(name).getChildren()}
        
        # populate unknown variable with randomly chosen values
        for nm in withheldData[row]:
          if nm in parentValues:
            parentValues[nm] = withheldData[row][nm]
          if nm in childrenValues:
            childrenValues[nm] = withheldData[row][nm]

        # compute weight/probability
        jProbs.append(pLearn.getParentChildJointProb( \
                      name, nodeValue, parentValues, childrenValues))
      
      # assign value to unknown variable via weighted random sampling
      newWithheld[name] = weightedChoice(domains[name], jProbs)
      # withheldData[row][name] = newWithheld[name]

    # set unknown variables to newly sampled values; something weird with this
    withheldData[row] = newWithheld
  
  # record inferred value for current row
  childrenValues = {child.id : data[row][nameMap[child.id]] \
                        for child in graph.getNode("diabetes").getChildren()}
  parentValues = {parent.id : data[row][nameMap[parent.id]] \
                        for parent in graph.getNode("diabetes").getParents()}
  for nm in withheldData[row]:
    if nm in parentValues:
      parentValues[nm] = withheldData[row][nm]
    if nm in childrenValues:
      childrenValues[nm] = withheldData[row][nm]
  probabilities.append(pLearn.getParentChildJointProb("diabetes", \
                        1, parentValues, childrenValues))
                       #withheldData[row]["diabetes"], parentValues))
  
  print "Sample number " + str(row + 1) + " took " + str(time.time() - t) + " sec"

# sort through probabilities and labels arrays and compare results
LABEL_TOL = 0.5
nCorrect = 0
nFalsePos = 0
nFalseNeg = 0
for i in range(nSamples):
  if labels[i] == '1' and probabilities[i] >= LABEL_TOL:
    nCorrect += 1
  elif labels[i] == '0' and probabilities[i] <= LABEL_TOL:
    nCorrect += 1
  elif labels[i] == '0' and probabilities[i] > LABEL_TOL:
    nFalsePos += 1
  else:
    nFalseNeg += 1

pCorrect = float(nCorrect) / nSamples

compareDict = {str(i) : (labels[i], probabilities[i]) for i in range(nSamples)}

print compareDict
print "There were " + str(nCorrect) + " correct labels out of " + str(nSamples) + " samples"
print "The error rate was " + str(1 - pCorrect)
print "The false positive rate was " + str(float(nFalsePos)/nSamples)
print "The false negative rate was " + str(float(nFalseNeg)/nSamples)
print "Total cpu time was " + str(time.time() - tNet) + " sec"
