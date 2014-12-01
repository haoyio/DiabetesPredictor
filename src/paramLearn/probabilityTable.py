#from collections import Counter

import sqlite3
class PTable:

  def __init__(self, filename):
    self.conn = sqlite3.connect('example.db')
    c = self.conn.cursor()
    c.execute('''DROP TABLE if EXISTS counts''')
    c.execute('''CREATE TABLE counts
              ( state    string, 
                gender   string, 
                age      string, 
                height   string, 
                weight   string,
                BMI      string,
                sBP      string, 
                dBP      string,
                diabetes string,
                code001139 string,
                code140239 string,
                code240279 string,
                code280289 string,
                code290319 string,
                code320359 string,
                code360389 string,
                code390459 string,
                code460519 string,
                code520579 string,
                code580629 string,
                code630679 string,
                code680709 string,
                code710739 string,
                code740759 string,
                code760779 string,
                code780799 string,
                code800999 string)''')

    c.execute('''PRAGMA table_info(counts);''')
    headers = c.fetchall()
    for header in headers:
        c.execute('''CREATE INDEX %s_index ON counts (%s);''' %(header[1], header[1]))

    self.loadTable(filename)


  def loadTable(self, filename):
    fo = open(filename)
    c = self.conn.cursor()

    headers = fo.readline().rstrip()
    headers = headers.split(',')
    self.headers = ", ".join( ["["+str(h)+"]" for h in headers] )

    line = fo.readline().rstrip()
    while line:
      row = line.split(',')
      c.execute("INSERT INTO counts (%s) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)" %self.headers, row)
      line = fo.readline().rstrip()

    c.execute("SELECT count(*) FROM counts")
    print str(c.fetchone()[0]) + " rows loaded"


  def getCounts(self, paramsDict):
    colNames = []
    colVals  = []
    for key, val in paramsDict.iteritems():
      colNames.append(key)
      colVals.append(val)
    query = "SELECT count(*) from counts WHERE "
    query += " AND ".join(e + "=?" for e in colNames)

    c = self.conn.cursor()
    return c.execute(query, colVals).fetchone()[0]





    
    
