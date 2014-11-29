using BayesNets
using DataFrames
using Graphs

testfile = "test.csv"
trainfile = "train.csv"

testset = readtable(testfile)
trainset = readtable(trainfile)

for arg = 1:length(ARGS)
  inname = ARGS[arg]
  bTest = BayesNet(names(testset))
  bTest.domains = [DiscreteDomain([x for x in unique(testset[label])]) 
                   for label in names(testset)]
  bTrain = BayesNet(names(trainset))
  bTrain.domains = [DiscreteDomain([x for x in unique(trainset[label])]) 
                    for label in names(trainset)]

  fin = open(inname, "r")
  lines = readlines(fin)
  close(fin)
  for line in lines
    nodes = split(line, ", ")
    src = convert(Symbol, nodes[1])
    tgt = convert(Symbol, nodes[2][1:end-1])
    addEdge!(bTest, src, tgt)
    addEdge!(bTrain, src, tgt)
  end # for line

  @printf("\nThe logBayesScore for %s on %s is %.4f\n", 
          inname, testfile, logBayesScore(bTest, testset))
  @printf("The logBayesScore for %s on %s is %.4f\n", 
          inname, trainfile, logBayesScore(bTrain, trainset))
end # for arg