#!/usr/bin/python3
# coding: utf-8

'''
  File name: mkrihash_lib.py
  Author: Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky
  Date created: 12/2/2019
  Date last modified: 24/3/2019
  Python Version: 3.7.2
'''

__author__ = 'Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky'
__copyright__ = 'Copyright 2019, Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky'
__license__ = 'GPL'
__version__ = '3'
__email__ = 'jurajkorcek@gmail.com'
__status__ = 'Development'

import sys
import argparse
import hashlib


class InputData:
  """
  Loads and stores input data and transforms them.
  """

  def __init__(self,input_data,input_type,is_file):
    """
    InputData constructor.

    Args:
        input_data (Union[str, bytes]): Input to be hashed.
        input_type (:obj: `str`): Determine whether type of variable input_data is bytes or text.
        is_file (:obj: `bool`): Determine whether variable input_data is file path.

    Attributes:
        input_data (:obj: `bytes`): Stored input for hashing.
        input_data_len (:obj: `int`): Length of loaded input_data in bits.
        num_of_blocks (:obj: `int`): Number of 512 bit blocks.
    """
    if (is_file):
      if (input_type == "b"):
        self.input_data = self.open_file(input_data,input_type)
      else:
        self.input_data = bytearray((self.open_file(input_data,input_type)).encode('utf-8'))  #encode string and transform to bytes
    else: #is not file, string input inline
      if (input_type == "b"):
        self.input_data = input_data
      else:
        self.input_data = bytearray(input_data.encode('utf-8'))
    self.input_type = input_type

  def open_file(self,file_name,file_type):
    """
    Opens specified file.

    Args:
        file_name (:obj: `str`): Name of file to be opened.
        file_type (:obj: `str`): Determine whether type of file is bytes or text.

    Returns:
        File data from file.
    """
    file_descr = open(file_name,"r"+file_type)  #"r"+file_type rb - read bytes or r -read text
    file_data = file_descr.read()
    file_descr.close()
    return file_data

class Hash:
  """
  Provides methods and variables for hashing algorithms.
  """

  def __init__(self):
    """
    Hash constructor.

    Attributes:
        hash_value (:obj: `hashlib.HASH`): Stores hash result.
    """
    hash_value = None

  def hash_it(self,input_data, algorithm):
    """
    Hashes input with specified algorithm.

    Args:
        input_data (:obj: `bytes`): Stored input for hashing.
        algorithm (:obj: `string`): Defines used hashing algorithm.
    """
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
  parser.add_argument("-d","--debug",help="Debugging mode, shows intermediate hash results",action="store_true")
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
    input_data = InputData(args.inline_text,data_type,False)  #is_file bool is false, inline input
  else:
    data_type = "b"
    input_data = InputData(args.binary_file,data_type,True)

  hash_obj = Hash()
  hash_obj.hash_it(input_data.input_data,args.algorithm)

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
