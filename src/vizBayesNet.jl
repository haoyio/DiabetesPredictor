using BayesNets
using DataFrames
using Graphs
using TikzGraphs
using TikzPictures

dataset = readtable("train.csv")

for arg = 1:length(ARGS)
  inname = ARGS[arg]
  title = splitext(inname)[1]
  outname = title * ".pdf"

  b = BayesNet(names(dataset))
  b.domains = [DiscreteDomain([x for x in unique(dataset[label])]) 
               for label in names(dataset)]

  fin = open(title * ".gph", "r")
  lines = readlines(fin)
  close(fin)
  for line in lines
    nodes = split(line, ", ")
    src = convert(Symbol, nodes[1])
    tgt = convert(Symbol, nodes[2][1:end-1])
    addEdge!(b, src, tgt)
  end # for line

  save(b::BayesNet, filename::String) = TikzPictures.save(PDF(filename), TikzGraphs.plot(b.dag, ASCIIString[string(s) for s in b.names]))
  save(b, outname)
  @printf("Output saved to %s\n", outname)
end # for arg