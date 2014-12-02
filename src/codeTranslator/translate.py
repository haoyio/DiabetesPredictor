import sys
import re


def loadDictionary(filename):
  d = dict()
  fo = open(filename)
  line = fo.readline().rstrip()
  while line:
    line = line.split(", ")
    d[line[0]] = line[1]
    line = fo.readline().rstrip()

  fo.close()
  return d

# argv[1]: infile (file to replace words)
# argv[2]: outfile (w/e you want)
# argv[3]: dictionary
# USAGE: python translate.py ../output/train3.gph train3_translated.gph code_dictionary.csv
def main(argv):
  d = dict()
  d = loadDictionary(argv[3])
  
  infile = open(argv[1])
  outfile = open(argv[2], "w+")

  line = infile.readline().rstrip()
  while line:
    line = line.split(", ")
    elem1 = line[0]
    elem2 = line[1]
    m1 = re.match('(?:code)([0-9]*)', elem1)
    m2 = re.match('(?:code)([0-9]*)', elem2)

    if m1:
      elem1 = m1.group(1)
      print elem1
      if elem1 in d:
        elem1 = d[elem1]
    if m2:
      elem2 = m2.group(1)
      print elem2
      if elem2 in d:
        elem2 = d[elem2]

    outfile.write(elem1+", "+elem2+"\n")
    line = infile.readline().rstrip()
if __name__ == "__main__":
  main(sys.argv)