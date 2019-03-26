#!/usr/bin/python3

import csv
import sys
import subprocess
import os

#fd = open("md5_vectors.csv","r")
csv.field_size_limit(sys.maxsize)
with open("md5_vectors.csv") as csv_file:
  csv_reader = csv.reader(csv_file,delimiter=',')
  first_line = True
  for row in csv_reader:
    md5 = ""
    if (first_line):
      first_line = False
      continue
    if (row[0] == "str"):
      md5 = subprocess.run(["../mkrihash.py","-m","-i",row[1]],stdout=subprocess.PIPE)
      md5 = md5.stdout.decode("utf-8")
    elif (row[0] == "binf"):
      md5 = subprocess.run(["../mkrihash.py","-m","-b",row[1]],stdout=subprocess.PIPE)
      md5 = md5.stdout.decode("utf-8")
    elif (row[0] == "texf"):
      md5 = subprocess.run(["../mkrihash.py","-m","-t",row[1]],stdout=subprocess.PIPE)
      md5 = md5.stdout.decode("utf-8")
    
    print("-----------------------------")
    print("Message/File:")
    print(row[1]+"\n")
    print("Expected hash" + 27*" " + "Computed hash" + 27*" " + "Status")
    if (md5.strip() == row[2]):
      print(row[2] + 8*" " + md5.strip() + 8*" " + "PASS")
    else:
      print(row[2] + 8*" " + md5.strip() + 8*" " + "FAIL")      
    