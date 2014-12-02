import sys
import re


def loadDictionary(filename):
  d = dict()
  fo = open(filename)
  line = fo.readline().rstrip()
  while line:
    line = [x.strip() for x in line.split(",")]
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
    outline = []
    line = [x.strip() for x in line.split(",")]
    for elem in line:
      m=re.match('(?:code)([0-9]*)', elem)
      if m:
        outline.append(d[m.group(1)])
      else:
        outline.append(elem)

    outfile.write(",".join(outline)+"\n")
    line = infile.readline().rstrip()
if __name__ == "__main__":
  main(sys.argv)