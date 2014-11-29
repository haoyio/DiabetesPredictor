using BayesNets
using DataFrames
using Graphs
using TikzGraphs
using TikzPictures

inname = ARGS[1]
title = splitext(inname)[1]
dataset = readtable(title * ".csv")
outname = @sprintf("%s.pdf", title)

b = BayesNet(names(dataset))
fin = open(inname, "r")
lines = readlines(fin)
close(fin)
for line in lines
  nodes = split(line, ", ")
  src, tgt = convert(Symbol, nodes[1]), convert(Symbol, nodes[2][1:end-1])
  addEdge!(b, src, tgt)
end # for line

save(b::BayesNet, filename::String) = TikzPictures.save(PDF(filename), TikzGraphs.plot(b.dag, ASCIIString[string(s) for s in b.names]))
save(b, outname)
@printf("Output saved to %s", outname)