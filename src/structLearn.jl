#= 
filename: project1.jl
author:   Hao Yi Ong
last mod: Oct 10, 2014
=#

######################################################################
# Dependencies
######################################################################

using DataFrames
using BayesNets
using Graphs

######################################################################
# Main functions
######################################################################

function graphEnumeration(bn::BayesNet, dataSet::DataFrame)
  # Constants
  nData, nVar = size(dataSet) 
  allNodePerm, allEdgePerm, nNodePerm, nEdgePerm = getPermutations(nVar)
  
  # Initialize candidate structure
  bestScore = -Inf
  bestBayesNet = copyBayesNet(bn, dataSet)
  currBayesNet = copyBayesNet(bn, dataSet)

  # Brute force comparison amongst all possibilities
  for nodePerm = 1:nNodePerm
    for edgePerm = 1:nEdgePerm
      # Generate candidate structure
      currBayesNet.dag = simple_graph(length(currBayesNet.names))
      edges = getEdgesFromPerm(allNodePerm[:, nodePerm], 
                               allEdgePerm[edgePerm], 
                               currBayesNet.names)
      addEdges!(currBayesNet, edges)

      # Check for improvement
      currScore = logBayesScore(currBayesNet, dataSet)
      if currScore > bestScore
        bestBayesNet.dag.edges = currBayesNet.dag.edges
        bestScore = currScore
      end # if
    end # for edgePerm
  end # for nodePerm

  return bestBayesNet, bestScore
end # function graphEnumeration


function getPermutations(nVar::Int)
  # Constants
  nodeIdx = [1:nVar]
  nNodePerm = factorial(nVar)
  nEdgePerm = iround(2^(nVar * (nVar - 1) / 2))

  # Generate node permutations array
  allNodePerm = Array(Int, nVar, nNodePerm)
  for nodePerm = 1:nNodePerm
    allNodePerm[:, nodePerm] = nthperm(nodeIdx, nodePerm)
  end # for nodePerm

  # Generate array of DAG edge permutations array
  allEdgePerm = Array(Array, nEdgePerm, 1)
  for edgePerm = 1:nEdgePerm
    allEdgePerm[edgePerm] = getEdgePerm(edgePerm - 1, nVar)
  end # for edgePerm

  return allNodePerm, allEdgePerm, nNodePerm, nEdgePerm
end # function getPermutations


function getEdgePerm(edgePerm::Int, nVar::Int)
  nBits = iround(nVar * (nVar - 1) / 2)
  stringRepresentation = bits(edgePerm)[end + 1 - nBits:end]
  
  edgePerm = zeros(nVar, nVar)
  strIdx = 1 # counter for stringRepresentation
  for iRow = 2:nVar
    for iCol = 1:iRow - 1
      edgePerm[iRow, iCol] = char2int(stringRepresentation[strIdx])
      strIdx += 1
    end # for iCol
  end # for iRow

  return edgePerm
end # function getEdgePerm


function copyBayesNet(bn::BayesNet, dataSet::DataFrame)
  bnCopy = BayesNet(bn.names)
  bnCopy.domains = [DiscreteDomain([x for x in unique(dataSet[label])]) 
                    for label in bn.names]

  for edge = 1:length(bn.dag.edges)
    addEdge!(bnCopy, bn.names[source(bn.dag.edges[edge])], 
             bn.names[target(bn.dag.edges[edge])])
  end # for edge

  return bnCopy
end # function copyBayesNet


function getEdgesFromPerm(nodePerm::Array, edgePerm::Array, names::Array)
  nEdge = iround(sum(edgePerm))
  nVar = size(edgePerm, 1)

  edges = Array((Symbol, Symbol), nEdge, 1)
  edgeIdx = 1
  for iRow = 1:nVar
    for iCol = 1:nVar
      if edgePerm[iRow, iCol] == 1 
        edges[edgeIdx] = (names[nodePerm[iRow]], names[nodePerm[iCol]])
        edgeIdx += 1
      end # if
    end # for iCol
  end # for iRow

  return edges
end # function getEdgesFromPerm


function tabuSearch(bn::BayesNet, dataSet::DataFrame)
  # Constants
  nNode = length(bn.names)
  nEdgeOp = 3 # add, remove, flip
  nullOp = 0 # indicates null edge operator
  opIdx = 1
  srcIdx = 2
  tgtIdx = 3
  addOp = 1
  removeOp = 2
  flipOp = 3
  
  tabuSz = 7 # size of tabu list
  neighborhoodSz = 20 # stopping criterion
  tabuList = Dict{(Int, Symbol, Symbol), Bool}()
  opList = [(0, bn.names[1], bn.names[1])]
  maxNumNode = 20
  bayesScoreTol = 0.00001
  
  # Initialize candidate solution
  bestBayesNet = generateRandomCandidateSolution(bn, dataSet)
  currBayesNet = copyBayesNet(bestBayesNet, dataSet)
  bestScore = logBayesScore(bestBayesNet, dataSet)
  
  t = 1
  neighborhoodExpl = 0
  while neighborhoodExpl < neighborhoodSz
    currOp = (nullOp, bn.names[1], bn.names[1])
    bestNewScore = logBayesScore(currBayesNet, dataSet)

    edgeRange = 1:nEdgeOp
    srcRange = 1:nNode
    tgtRange = 1:nNode

    if nNode > maxNumNode
      # Choose random subset of search space
      srcRange = unique(rand(1:nNode, maxNumNode))
      tgtRange = unique(rand(1:nNode, maxNumNode))
    end # if

    for edgeOp = edgeRange
      for src = srcRange
        for tgt = tgtRange
          # for each possible operator
          if (hasEdge(currBayesNet, bn.names[src], bn.names[tgt]) &&
              (edgeOp == removeOp || edgeOp == flipOp)) ||
             (!hasEdge(currBayesNet, bn.names[src], bn.names[tgt]) &&
                 edgeOp == addOp)

            newOp = (edgeOp, bn.names[src], bn.names[tgt])

            if legalOp(newOp, tabuList)
              newBayesNet = copyBayesNet(currBayesNet, dataSet)
              execOp!(newBayesNet, newOp)

              if isValid(newBayesNet)
                if currOp[opIdx] == nullOp ||
                   logBayesScore(newBayesNet, dataSet) > bestNewScore
                  currOp = newOp
                  bestNewScore = logBayesScore(newBayesNet, dataSet)
                end # if
              end# if isValid
            end # if legalOp
          end # if hasEdge
        end # for tgt
      end # for src
    end # for edgeOp

    execOp!(currBayesNet, currOp)
    
    # Check for improvement
    if logBayesScore(currBayesNet, dataSet) > 
       logBayesScore(bestBayesNet, dataSet) + bayesScoreTol
      execOp!(bestBayesNet, currOp)
      lastImprovement = 0

      currscore = logBayesScore(bestBayesNet, dataSet)
      @printf("curr score = %.4f\n", currscore)
      @printf("curr normalized score = %.4f\n\n", currscore/size(dataSet,1))

    else
      neighborhoodExpl += 1
    end # if

    tabuList, opList = updateTabuList(tabuList, opList, currOp, t, tabuSz)
    t += 1
  end # while

  return bestBayesNet, logBayesScore(bestBayesNet, dataSet)
end # function tabuSearch


function generateRandomCandidateSolution(bn::BayesNet, dataSet::DataFrame)
  # Constants
  nNode = length(bn.names)
  addNodeOp = 1
  nVar = length(bn.names)
  upperBound = iround(nVar * (nVar - 1) / 2)
  
  # Empty edge set if large graph
  if nNode > 20
    return copyBayesNet(bn, dataSet)
  end # if

  # Generate permutation arrays
  nodePerm = randperm(nVar)
  nBits = iround(nVar * (nVar - 1) / 2)
  stringRepresentation = rand(0:1, nBits, 1)
  
  edgePerm = zeros(nVar, nVar)
  strIdx = 1 # counter for stringRepresentation
  for iRow = 2:nVar
    for iCol = 1:iRow - 1
      edgePerm[iRow, iCol] = stringRepresentation[strIdx]
      strIdx += 1
    end # for iCol
  end # for iRow

  # Generate candidate Bayes net
  candidateBayesNet = copyBayesNet(bn, dataSet)
  edges = getEdgesFromPerm(nodePerm, edgePerm, bn.names)
  addEdges!(candidateBayesNet, edges)
  return candidateBayesNet
end # function generateRandomCandidateSolution


function generateCandidateSolution(bn::BayesNet, dataSet::DataFrame)
  return copyBayesNet(bn, dataSet)
end # function generateCandidateSolution


function legalOp(op::(Int, Symbol, Symbol), tabuList::Dict)
  srcIdx = 2
  tgtIdx = 3

  if op[srcIdx] == op[tgtIdx]
    return false
  else
    if haskey(tabuList, op)
      return !tabuList[op]
    else
      return true
    end # if haskey
  end # if
end # function legalOp


function execOp!(bn::BayesNet, op::(Int, Symbol, Symbol))
  # Constants
  opIdx = 1
  srcIdx = 2
  tgtIdx = 3

  addOp = 1
  removeOp = 2
  flipOp = 3

  # Operation information
  src = op[srcIdx]
  tgt = op[tgtIdx]
  
  if src != tgt
    if op[opIdx] == addOp && !hasEdge(bn, src, tgt) && !hasEdge(bn, tgt, src)
      addEdge!(bn, src, tgt)
    elseif op[opIdx] == removeOp && hasEdge(bn, src, tgt)
      removeEdge!(bn, src, tgt)
    elseif op[opIdx] == flipOp && hasEdge(bn, src, tgt)
      removeEdge!(bn, src, tgt)
      addEdge!(bn, tgt, src)
    end # if
  end # if
end # function execOp!


function updateTabuList(tabuList::Dict, opList::Array, 
                        currOp::(Int, Symbol, Symbol), t::Int, L:: Int)
  # Constants
  opIdx = 1
  srcIdx = 2
  tgtIdx = 3

  addOp = 1
  removeOp = 2
  flipOp = 3

  if t >= L
    opToRemove = opList[t - L + 1]
    tabuList[opToRemove] = false
  end # if

  reverseOp = (Int, Symbol, Symbol)
  if currOp[opIdx] == addOp
    reverseOp = (removeOp, currOp[srcIdx], currOp[tgtIdx])
  elseif currOp[opIdx] == removeOp
    reverseOp = (addOp, currOp[srcIdx], currOp[tgtIdx])
  elseif currOp[opIdx] == flipOp
    reverseOp = (flipOp, currOp[srcIdx], currOp[tgtIdx])
  end # if

  opList = [opList; reverseOp]
  tabuList[reverseOp] = true
  return tabuList, opList
end # function updateTabuList!


function hasEdge(bn::BayesNet, sourceNode::NodeName, destNode::NodeName)
  numEdges = length(bn.dag.edges)
  for i = 1:numEdges
    if bn.names[source(bn.dag.edges[i])] == sourceNode && 
       bn.names[target(bn.dag.edges[i])] == destNode
      return true
    end # if
  end # for i
  return false
end

######################################################################
# Miscellaneous functions
######################################################################

function readDataSet(args::Array{UTF8String})
  if !isValidArgument(args)
    error("Please input a .csv file as the only argument")
  end # if

  fileName = args[1]
  dataSet = readtable(fileName)
  nData, nVar = size(dataSet)
  
  @printf("Input file: %s\n", fileName)
  @printf("# training samples: %d\n", nData) 
  @printf("# variables: %d\n", nVar)
  
  return dataSet, nData, nVar, fileName
end # function readDataSet


function isValidArgument(args::Array{UTF8String})
  fileExtension = ".csv"
  numberOfArguments = 1
  return length(args) == numberOfArguments &&
         splitext(args[1])[end] == fileExtension
end # function isValidArgument


function genOutputFile(fileName::String, bn::BayesNet)
  fileExtension = ".gph"
  outputFileName = @sprintf("%s%s-%s", splitext(fileName)[1], 
                            fileExtension, strftime(time()))
  outputFile = open(outputFileName, "w")
  
  for edge = bn.dag.edges
    srcNode = bn.names[source(edge, bn.dag)]
    tgtNode = bn.names[target(edge, bn.dag)]
    @printf(outputFile, "%s, %s\n", srcNode, tgtNode)
  end # for edge
  
  close(outputFile)
  @printf("Output file: %s\n", outputFileName)
end # function genOutputFile


function char2int(char::Char)
  asciiIdxFor0 = 48
  return int(char) - asciiIdxFor0
end # function char2int

######################################################################
# Main script
######################################################################

# Initialize Bayes net
dataSet, nData, nVar, fileName = readDataSet(ARGS)
bayesNet = BayesNet(names(dataSet))
bayesNet.domains = [DiscreteDomain([x for x in unique(dataSet[label])]) 
                    for label in names(dataSet)]

# Execute search algorithm over structure space
searchAlgorithm = (nVar <= 4 ? graphEnumeration : tabuSearch)
tic()
bestBayesNet, bestScore = searchAlgorithm(bayesNet, dataSet)

# Output results
@printf("CPU time: %.3f sec\n", toq())
@printf("Best score: %.3f\n", bestScore)
@printf("Normalized score: %.8f\n", bestScore / nData)
genOutputFile(fileName, bestBayesNet)