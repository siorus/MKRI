#!/usr/bin/python3

import sys
import subprocess
import os
import csv

csv.field_size_limit(sys.maxsize)
with open("md5_vectors.csv") as csv_file:
  csv_reader = csv.reader(csv_file,delimiter=',')
  first_line = True
  i = 0
  for row in csv_reader:
    md5 = ""
    diff = ""
    try:
      out_sample = open("white_box_out/sample"+str(i),"w")
      out_mkri = open("white_box_out/mkri"+str(i),"w")
    except FileNotFoundError:
      out_sample = open("white_box_out/sample"+str(i),"w+")
      out_mkri = open("white_box_out/mkri"+str(i),"w+")
    if (first_line):
      first_line = False
      continue
    if (row[0] == "str"):
      mkri = subprocess.run(["../mkrihash.py","-m","-d","-i",row[1]],stdout=out_mkri)
      sample = subprocess.run(["./support_script_wb.py","i",row[1]],stdout=out_sample)
    elif (row[0] == "binf"):
      mkri = subprocess.run(["../mkrihash.py","-m","-d","-b",row[1]],stdout=out_mkri)
      sample = subprocess.run(["./support_script_wb.py","b",row[1]],stdout=out_sample)
    elif (row[0] == "texf"):
      mkri = subprocess.run(["../mkrihash.py","-m","-d","-t",row[1]],stdout=out_mkri)
      sample = subprocess.run(["./support_script_wb.py","t",row[1]],stdout=out_sample)
    arg1 = "white_box_out/sample"+str(i)
    arg2 = "white_box_out/mkri"+str(i)
    
    diff = subprocess.run(["diff",arg1,arg2],stdout=subprocess.PIPE)
    diff = diff.stdout.decode("utf-8")
    if(diff == ""):
      print("\n------------------------------")
      print("Message/File" + 10*" " + row[1])
      print("Status" + 16*" " + "PASS")
    else:
      print("Message/File" + 10*" " + row[1])
      print("Status" + 16*" " + "FAIL")
      print(diff)
      print("\n------------------------------")

    i = i+ 1