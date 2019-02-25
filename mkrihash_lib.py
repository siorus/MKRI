#!/usr/bin/python37
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

class Hash:

  def __init__(self):
    hash_value = None

  def hash_it(self,input_data, algorithm):
    if (algorithm == "md5"):
      self.hash_value = hashlib.md5()
      self.hash_value.update(input_data)
    elif (algorithm == "sha1"):
      self.hash_value = hashlib.sha1()
      self.hash_value.update(input_data)
    elif (algorithm == "sha2"):
      self.hash_value = hashlib.sha512()
      self.hash_value.update(input_data)
    elif (algorithm == "sha3"):
      self.hash_value = hashlib.sha3_512()
      self.hash_value.update(input_data)
    elif (algorithm == "blake2"):
      self.hash_value = hashlib.blake2b()
      self.hash_value.update(input_data)

if __name__ == "__main__":
  version = 1.0
  parser = argparse.ArgumentParser(prog="mkrihashlib.py", description="MD5 hash generator with hashlib",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-v","--version",action="version", version="%(prog)s"+" version "+str(version))
  parser.add_argument("-m","--machine-readable",help="prints output in machine readable form, only result hash",action="store_true")
  parser.add_argument("-a","--algorithm",help="defines hashing algorithm",action="store",choices=["md5","sha1","sha2","sha3","blake2"],required=True)
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
  hash_obj = Hash() 
  hash_obj.hash_it(input_data.input_data_byte,args.algorithm)

  if (args.machine_readable):
    print(hash_obj.hash_value.hexdigest())
  else:
    if (args.inline_text):
      print("INLINE TEXT: " + args.inline_text)
    elif(args.text_file):
      print("TEXT FILE: " + args.text_file)
    elif(args.binary_file):
      print("BINARY FILE: " + args.binary_file)
    print((args.algorithm).upper() + " HASH: " + str(hash_obj.hash_value.hexdigest()))
  #my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5"
  #TODO PYDOC
  