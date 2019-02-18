#!/usr/bin/python3
# coding: utf-8

'''
  File name: mkrihash.py
  Author: Juraj Korcek
  Date created: 12/2/2019
  Date last modified: 12/2/2019
  Python Version: 3.5
'''

__author__ = 'Juraj Korcek, Credit others'
__copyright__ = 'Copyright 2019, Juraj Korcek & Co.'
__credits__ = ['Others']
__license__ = 'GPL'
__version__ = '3'
__email__ = 'jurajkorcek@gmail.com'
__status__ = 'Development'

import sys
import argparse

class InitRegisters:
  reg_a = 0x67452301
  reg_b = 0xefcdab89
  reg_c = 0x98badcfe
  reg_d = 0x10325476

class ShiftConst:
  values = (7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21 , 6, 10, 15, 21, 6, 10, 15, 21)

class TConst:
  values = (0xd76aa478, 0xe8c7b756, 0x242070db, 0xc1bdceee, 
            0xf57c0faf, 0x4787c62a, 0xa8304613, 0xfd469501, 
            0x698098d8, 0x8b44f7af, 0xffff5bb1, 0x895cd7be, 
            0x6b901122, 0xfd987193, 0xa679438e, 0x49b40821, 
            0xf61e2562, 0xc040b340, 0x265e5a51, 0xe9b6c7aa, 
            0xd62f105d, 0x02441453, 0xd8a1e681, 0xe7d3fbc8, 
            0x21e1cde6, 0xc33707d6, 0xf4d50d87, 0x455a14ed, 
            0xa9e3e905, 0xfcefa3f8, 0x676f02d9, 0x8d2a4c8a, 
            0xfffa3942, 0x8771f681, 0x6d9d6122, 0xfde5380c, 
            0xa4beea44, 0x4bdecfa9, 0xf6bb4b60, 0xbebfbc70, 
            0x289b7ec6, 0xeaa127fa, 0xd4ef3085, 0x04881d05, 
            0xd9d4d039, 0xe6db99e5, 0x1fa27cf8, 0xc4ac5665, 
            0xf4292244, 0x432aff97, 0xab9423a7, 0xfc93a039, 
            0x655b59c3, 0x8f0ccc92, 0xffeff47d, 0x85845dd1, 
            0x6fa87e4f, 0xfe2ce6e0, 0xa3014314, 0x4e0811a1, 
            0xf7537e82, 0xbd3af235, 0x2ad7d2bb, 0xeb86d391) 

class InputData:

  def __init__(self,input_data,input_type,is_file):
    if (is_file):
      self.input_data = self.open_file(input_data,input_type)
    else:
      self.input_data = input_data
    self.input_type = input_type
    self.input_data_byte = 0
    self.input_data_len = 0
    self.num_of_blocks = 0

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
      
  def set_num_of_blocks(self):
    self.num_of_blocks = len(self.input_data_byte) // 64
 
  def byte_length_alignment(self):
    
    self.set_input_data_len()
    self.input_data_byte += 0x80.to_bytes(1, byteorder="little")
    modulo = len(self.input_data_byte) % 64

    if modulo != 56:
      zeroes_to_add = 56 - modulo
      self.input_data_byte += zeroes_to_add * 0x00.to_bytes(1, byteorder="little")
    
    self.input_data_byte += self.input_data_len.to_bytes(8, byteorder="little")
    self.set_num_of_blocks() 

  def set_input_data_len(self):
    self.input_data_len = (len(self.input_data_byte) * 8)

class Md5:
  
  def __init__(self,init_registers):
    self.reg_a = init_registers.reg_a
    self.reg_b = init_registers.reg_b
    self.reg_c = init_registers.reg_c
    self.reg_d = init_registers.reg_d

  def function_f(self,reg_b,reg_c,reg_d):
    f = (reg_b & reg_c) | (~reg_b & reg_d)
    return f

  def function_g(self,reg_b,reg_c,reg_d):
    g = (reg_b & reg_d) | (reg_c & ~reg_d)
    return g

  def function_h(self,reg_b,reg_c,reg_d):
    h = (reg_b ^ reg_c ^ reg_d)
    return h

  def function_i(self,reg_b,reg_c,reg_d):
    i = reg_c ^ (reg_b | ~reg_d)
    return i

  def left_bit_rotate(self,bits_to_rotate,nth_rotation):
    return ((bits_to_rotate << nth_rotation) | (bits_to_rotate >> (32 - nth_rotation)))

  def swap_byte_order(self,to_be_swapped):
    return int.from_bytes(to_be_swapped.to_bytes(4,byteorder='little'), byteorder='big')

  def produce_hash(self,reg_a,reg_b,reg_c,reg_d):
    hash = 0x0
    hash = hash | int.from_bytes(self.reg_a.to_bytes(32,byteorder="little"), byteorder='big')
    hash = hash << 32 | int.from_bytes(self.reg_b.to_bytes(32,byteorder="little"), byteorder='big')
    hash = hash << 32 | int.from_bytes(self.reg_c.to_bytes(32,byteorder="little"), byteorder='big')
    hash = hash << 32 | int.from_bytes(self.reg_d.to_bytes(32,byteorder="little"), byteorder='big')
    return hash

  def rounds(self,input_data):

    for nth_block in range(input_data.num_of_blocks): #loop over 512bit parts of input
      reg_a, reg_b, reg_c, reg_d = self.reg_a, self.reg_b, self.reg_c, self.reg_d
      for i in range(64):
        data_512bit = input_data.input_data_byte[64*nth_block:64*(nth_block+1)]
        if (i <= 15):
          fun_ret = self.function_f(reg_b,reg_c,reg_d)
          nth_word = i
        elif (i <= 31):
          fun_ret = self.function_g(reg_b,reg_c,reg_d)
          nth_word = (5*i + 1) % 16
        elif (i <= 47):
          fun_ret = self.function_h(reg_b,reg_c,reg_d)
          nth_word = (3*i + 5) % 16
        else:
          fun_ret = self.function_i(reg_b,reg_c,reg_d)
          nth_word = (7*i) % 16

        addition_chain = (((((reg_a + fun_ret) & 0xFFFFFFFF) + int.from_bytes(data_512bit[4*nth_word:4*(nth_word + 1)],byteorder="little")) & 0xFFFFFFFF) + TConst.values[i]) & 0xFFFFFFFF
        reg_a = reg_d
        reg_d = reg_c
        reg_c = reg_b
        reg_b = (reg_b + self.left_bit_rotate(addition_chain,ShiftConst.values[i])) & 0xFFFFFFFF
      """
        print("i: " + str(i))
        print("CHUNK START: " + str(4*nth_word))
        print("CHUNK END: " + str(4*nth_word+4))
        print("FUN: " + str(hex(fun_ret)))
        print("DATA: " + str(hex(int.from_bytes(data_512bit[4*nth_word:4*(nth_word + 1)],"little"))))
        print("REG A: " + str(hex(reg_a)))
        print("REG B: " + str(hex(reg_b)))
        print("REG C: " + str(hex(reg_c)))
        print("REG D: " + str(hex(reg_d)))
      print("KONIEC BLOKU")
      """
      self.reg_a = (self.reg_a + reg_a) & 0xFFFFFFFF
      self.reg_b = (self.reg_b + reg_b) & 0xFFFFFFFF
      self.reg_c = (self.reg_c + reg_c) & 0xFFFFFFFF
      self.reg_d = (self.reg_d + reg_d) & 0xFFFFFFFF

    """
    print(hex(hash))
    print(hex(int.from_bytes(self.reg_a.to_bytes(32,byteorder="little"), byteorder='big')))
    print(hex(self.reg_a))
    print(hex(self.reg_b))
    print(hex(self.reg_c))
    print(hex(self.reg_d))
    """
    return self.produce_hash(reg_a,reg_b,reg_c,reg_d)           

if __name__ == "__main__":
  version = 1.0
  parser = argparse.ArgumentParser(prog="mkri_hash.py", description="MD5 hash generator",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
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
  input_data.byte_length_alignment()
  md5 = Md5(InitRegisters)
  if (args.machine_readable):
    print(hex(md5.rounds(input_data))[2:34])
  else:
    if (args.inline_text):
      print("INLINE TEXT: " + args.inline_text)
    elif(args.text_file):
      print("TEXT FILE: " + args.text_file)
    elif(args.binary_file):
      print("BINARY FILE: " + args.binary_file)
    print("MD5 HASH: " + str(hex(md5.rounds(input_data))[2:34]))
  #my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5"
  #TODO PYDOC
  