using BayesNets
using DataFrames
using Graphs

############################################################
# Functions
############################################################

function getParentsAndDomains(node::Int64, b::BayesNet)
  #=
  Returns a list of node's parents, a list of the parents'
  domains, and a boolean indicating whether the node is a 
  source node.
  =#
  parents = Int64[]
  pDomains = DiscreteDomain[]
  for edge in b.dag.edges
    if edge.target == node
      push!(parents, edge.source)
      push!(pDomains, b.domains[edge.source])
    end # if
  end # for edge
  return parents, pDomains, isempty(parents)
end # function getParentsAndDomains

############################################################
# Main script
############################################################

# reconstruct Bayes net object
inname = ARGS[1]
title = splitext(inname)[1]
dataset = readtable(title * ".csv")

b = BayesNet(names(dataset))
b.domains = [DiscreteDomain([x for x in unique(dataset[label])]) 
             for label in names(dataset)]

name2index = b.index
index2name = Dict{Int64,Symbol}()
for key in keys(b.index)
  index2name[b.index[key]] = key
end # for key

fin = open(title * ".gph", "r")
lines = readlines(fin)
close(fin)
for line in lines
  nodes = split(line, ", ")
  src = convert(Symbol, nodes[1])
  tgt = convert(Symbol, nodes[2][1:end-1])
  addEdge!(b, src, tgt)
end # for line


# initialize counts (MLE w/ Laplace smoothing)
counts = Dict()
for name in b.names
  node = name2index[name]
  parents, pDomains, isSource = getParents(node, b)
  
end # for name


# count all training samples
samples = array(dataset)
nSamples = size(samples, 1)

for distribution in distributions
  for sample = 1:nSamples

  end # for sample
end # for distribution


# normalize over all cpds

