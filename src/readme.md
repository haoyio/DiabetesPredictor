# Description
This directory contains all the source code for the project.

## Use of Julia files
1. ssh into one of the new corn machines on the farm servers (corn01, corn02, corn07, corn10 work best; otherwise use corn-new)
2. cd into the right directory, or copy over the files into any directory you want to work in
3. from the command line, type in
  - e.g., `julia structLearn.jl train.csv`
  - e.g., `julia evalBayesNet.jl train1.gph train2.gph train3.gph train4.gph train5.gph train6.gph train7.gph train8.gph`
  - e.g., `julia vizBayesNet.jl train1.gph train2.gph train3.gph train4.gph train5.gph train6.gph train7.gph train8.gph`
