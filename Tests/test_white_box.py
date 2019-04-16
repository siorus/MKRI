#!/usr/bin/python3

import sys
import subprocess
import os
import csv
import platform
import re

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
      os.mkdir("white_box_out",0o777)
      out_sample = open("white_box_out/sample"+str(i),"w+")
      out_mkri = open("white_box_out/mkri"+str(i),"w+")
    if (first_line):
      first_line = False
      continue
    if (row[0] == "str"):
      if (platform.system() == "Windows"):
        mkri = subprocess.run(["python.exe","../mkrihash.py","-m","-d","-i",row[1]],stdout=out_mkri)
        sample = subprocess.run(["python.exe","./support_script_wb.py","i",row[1]],stdout=out_sample)
      else:
        mkri = subprocess.run(["../mkrihash.py","-m","-d","-i",row[1]],stdout=out_mkri)
        sample = subprocess.run(["./support_script_wb.py","i",row[1]],stdout=out_sample)
    elif (row[0] == "binf"):
      if (platform.system() == "Windows"):
        mkri = subprocess.run(["python.exe","../mkrihash.py","-m","-d","-b",row[1]],stdout=out_mkri)
        sample = subprocess.run(["python.exe","./support_script_wb.py","b",row[1]],stdout=out_sample)
      else:
        mkri = subprocess.run(["../mkrihash.py","-m","-d","-b",row[1]],stdout=out_mkri)
        sample = subprocess.run(["./support_script_wb.py","b",row[1]],stdout=out_sample)
    elif (row[0] == "texf"):
      if (platform.system() == "Windows"):
        mkri = subprocess.run(["python.exe","../mkrihash.py","-m","-d","-t",row[1]],stdout=out_mkri)
        sample = subprocess.run(["python.exe","./support_script_wb.py","t",row[1]],stdout=out_sample)
      else:
        mkri = subprocess.run(["../mkrihash.py","-m","-d","-t",row[1]],stdout=out_mkri)
        sample = subprocess.run(["./support_script_wb.py","t",row[1]],stdout=out_sample)
    if (platform.system() == "Windows"):
      arg1 = "white_box_out\sample"+str(i)
      arg2 = "white_box_out\mkri"+str(i)
    else:
      arg1 = "white_box_out/sample"+str(i)
      arg2 = "white_box_out/mkri"+str(i)
    
    if (platform.system() == "Windows"):
      diff = subprocess.run(["fc",arg1,arg2],stdout=subprocess.PIPE)
    else:
      diff = subprocess.run(["diff",arg1,arg2],stdout=subprocess.PIPE)
    
    diff = diff.stdout.decode("utf-8")

    if((diff == "") or (re.search(".*FC\: no differences encountered.*",diff) != None)):
      print("\n------------------------------")
      print("Message/File" + 10*" " + row[1])
      print("Status" + 16*" " + "PASS")
    else:
      print("Message/File" + 10*" " + row[1])
      print("Status" + 16*" " + "FAIL")
      print(diff)
      print("\n------------------------------")

    i = i+ 1
