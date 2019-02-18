#!/usr/bin/python3
# coding: utf-8

'''
  File name: mkrihash.py
  Author: Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky
  Date created: 12/2/2019
  Date last modified: 18/2/2019
  Python Version: 3.5
'''

__author__ = 'Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky'
__copyright__ = 'Copyright 2019, Juraj Korcek & Co.'
__license__ = 'GPL'
__version__ = '3'
__email__ = 'jurajkorcek@gmail.com'
__status__ = 'Development'

import sys
import argparse
import hashlib


class InputData:

  def __init__(self,input_data,input_type,is_file):
    if (is_file):
      self.input_data = self.open_file(input_data,input_type)
    else:
      self.input_data = input_data
    self.input_type = input_type
    self.input_data_byte = 0

  def open_file(self,file_name,file_type):
    file_descr = open(file_name,"r"+file_type)
    file_data = file_descr.read()
    file_descr.close()
    return file_data

  def transform_to_bytes(self,data_type):
    if (data_type == "b"):
      self.input_data_byte = self.input_data
    else:
      self.input_data_byte = bytearray(self.input_data.encode('utf-8'))
      
if __name__ == "__main__":
  version = 1.0
  parser = argparse.ArgumentParser(prog="mkrihashlib.py", description="MD5 hash generator with hashlib",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-v","--version",action="version", version="%(prog)s"+" version "+str(version))
  parser.add_argument("-m","--machine-readable",help="prints output in machine readable form, only result hash",action="store_true")
  special_run = parser.add_mutually_exclusive_group(required=True)
  special_run.add_argument("-i","--inline-text",help="input for MD5 is text and written after this argument",action="store")
  special_run.add_argument("-t","--text-file",metavar="FILE",help="input for MD5 is text file and specify path to it",action="store")
  special_run.add_argument("-b","--binary-file",help="input for MD5 is binary file and specify path to it",action="store")
  args = parser.parse_args()

  if (args.text_file):
    data_type = ""
    input_data = InputData(args.text_file,data_type,True)
  elif (args.inline_text):
    data_type = ""
    input_data = InputData(args.inline_text,data_type,False)
  else:
    data_type = "b"
    input_data = InputData(args.binary_file,data_type,True)

  input_data.transform_to_bytes(data_type)
  md5 = hashlib.md5()
  md5.update(input_data.input_data_byte)
  if (args.machine_readable):
    print(md5.hexdigest())
  else:
    if (args.inline_text):
      print("INLINE TEXT: " + args.inline_text)
    elif(args.text_file):
      print("TEXT FILE: " + args.text_file)
    elif(args.binary_file):
      print("BINARY FILE: " + args.binary_file)
    print("MD5 HASH: " + str(md5.hexdigest()))
  #my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5"
  #TODO PYDOC
  