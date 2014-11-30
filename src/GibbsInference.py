import csv
import random

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


domains["code001to139"] = [0,1]
domains["code140to239"] = [0,1]
domains["code240to279"] = [0,1]
domains["code280to289"] = [0,1]
domains["code290to319"] = [0,1]
domains["code320to359"] = [0,1]
domains["code360to389"] = [0,1]
domains["code390to459"] = [0,1]
domains["code460to519"] = [0,1]
domains["code520to579"] = [0,1]
domains["code580to629"] = [0,1]
domains["code630to679"] = [0,1]
domains["code680to709"] = [0,1]
domains["code710to739"] = [0,1]
domains["code740to759"] = [0,1]
domains["code760to779"] = [0,1]
domains["code780to799"] = [0,1]
domains["code800to999"] = [0,1]

nameMap = {}
names = []
data = []
withheldData = []
labels = []
probabilities = []
with open('test.csv', 'rb') as csvfile:
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

# randomly delete 5 features from each row
numDelete = 5
random.seed(10)
for row in data:
	withheld = {}
	random.shuffle(names)
	for i in range(numDelete):
		withheld[names[i]] = 0
	withheld["diabetes"] = 0
	withheldData.append(withheld)

def weightedChoice(choices, weights):
	'''
	Weighted version of random.choice(); pass in choices and weights
	'''
 	total = sum(weights)
  r = random.uniform(0, total)
  upto = 0
  for c in choices:
  	for w in weights:
	    if upto + w > r:
	      return c
	    upto += w

# Gibbs Sampling
iterNum = 10000
for row in range(len(data)):
	
	# initialize withheldData[row]'s contents to random values
	for name in withheldData[row]:
		withheldData[row][name] = random.choice(domains[name])
	
	# NOTE: should we have some convergence criteria instead?
	for _ in range(iterNum):
		withheld = withheldData[row]
		newWithheld = {}
		
		# loop through labels in withheldData[row] and random sample 
		# based on weights to form newWithheld
		for name in withheldData[row]:
			
			jProbs = []
			for nodeValue in domains[name]:
				# store parent and child values in dictionary
				parentValues = {parent : data[row[nameMap[parent]]] \
				                for parent in graph.getNode(name).getParents()}
				childrenValues = {child : data[row[nameMap[child]]] \
				                  for child in graph.getNode(name).getChildren()}
				
				jProbs.append(getParentChildJointProb(name, parentValues, childrenValues))
			
			# assign value to unknown variable via weighted random sampling
			newWithheld[name] = weightedChoice(domains[name], jProbs)

		# set unknown variables to newly sampled values
		withheldData[row] = newWithheld
	
	# record inferred value for current row 
	parentValues = {parent : data[row[nameMap[parent]]] \
				          for parent in graph.getNode("diabetes").getParents()}
	probabilities.append(getParentJointProb("diabetes", parentValues))

# sort through probabilities and labels arrays and compare results
nCorrect = sum([1. if labels[i] - probabilities[i] > 0.2 else 0 for i in range(len(labels))])
pCorrect = nCorrect / len(labels)