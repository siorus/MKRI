#!/usr/bin/python3
# coding: utf-8

'''
  File name: md5sum.py
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

import binascii
import sys

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

  def __init__(self,input_data,input_type):
    """ Description
    :type self:
    :param self:

    :type input_data:
    :param input_data:

    :type input_type:
    :param input_type:

    :raises:

    :rtype:
    """
    self.input_data = input_data
    self.input_type = input_type
    self.input_data_bin = ""
    self.input_data_len = len(input_data)
    self.input_data_bin_len = 0  # in decimal len of input data in binary without padding
    self.padded_data_bin_len = 0  #in binary with leading zeros
    self.num_of_bin_blocks = 0

  def transform_to_bits(self):
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    hex_string = str(binascii.hexlify(self.input_data.encode('utf-8')))[2:-1] #slicing removes leading "'b" and trailing "'"
    for i in range(len(hex_string) // 2):
      self.input_data_bin += format(int(hex_string[2*i:2*i+2],16),"0>8b") # "0>8b" means add leading zeroes when num in binnary is not in 8 bit representation
    self.set_input_len_bin()

  def set_input_len_bin(self):
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    self.input_data_bin_len = len(self.input_data_bin)

  def set_num_of_bin_blocks(self):
    self.num_of_bin_blocks = len(self.input_data_bin) // 512

  def get_input_data_bin(self):
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    return self.input_data_bin

  def get_input_data_bin_len(self):
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    return self.input_data_bin_len

  def bit_length_alignment(self):
    
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    self.input_data_bin += "1"
    modulo = len(self.input_data_bin) % 512
    if modulo != 448:
      zeroes_to_add = 448 - modulo
      print("ADDED ZEROES: " + str(zeroes_to_add))
      self.input_data_bin += zeroes_to_add * "0"
    self.transform_message_length()
    self.input_data_bin += self.padded_data_bin_len
    self.set_num_of_bin_blocks()

  def transform_message_length(self):
    
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    padded_data_bin_len = self.input_data_bin_len
    self.padded_data_bin_len = format(padded_data_bin_len,"0>64b")

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

  def rounds(self,input_data):
    reg_a, reg_b, reg_c, reg_d = self.reg_a, self.reg_b, self.reg_c, self.reg_d



    for nth_block in range(input_data.num_of_bin_blocks): #loop over 512bit parts of input
      #for nth_32bit_block in range(16):
      #  data_32bit = input_data.input_data_bin[512*nth_block:512*(nth_block+1)][32*nth_32bit_block:32*(nth_32bit_block+1)]
      for i in range(64):
        #print(hex(int(input_data.input_data_bin[512*nth_block:512*(nth_block+1)],2)))
        #data_32bit = input_data.input_data_bin[512*nth_block:512*(nth_block+1)][32*(i % 16):32*((i % 16 +1))]
        #data_32bit = self.swap_byte_order(int(data_32bit,2))
        data_512bit = input_data.input_data_bin[512*nth_block:512*(nth_block+1)]
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
        #data_32bit = 
        addition_chain = (((((reg_a + fun_ret) & 0xFFFFFFFF) + self.swap_byte_order(int(data_512bit[32*nth_word:32*(nth_word + 1)],2))) & 0xFFFFFFFF) + TConst.values[i]) & 0xFFFFFFFF
        reg_a = reg_d
        reg_d = reg_c
        reg_c = reg_b
        reg_b = (reg_b + self.left_bit_rotate(addition_chain,ShiftConst.values[i])) & 0xFFFFFFFF
      """
        print("i: " + str(i))
        print("CHUNK START: " + str(4*nth_word))
        print("CHUNK END: " + str(4*nth_word+4))
        print("FUN: " + str(hex(fun_ret)))
        print("DATA: " + str(hex(int(data_512bit[32*nth_word:32*(nth_word + 1)],2))))
        print("DATA2: " + str(hex(self.swap_byte_order(int(data_512bit[32*nth_word:32*(nth_word + 1)],2)))))
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
      
    print(hex(self.reg_a))
    print(hex(self.reg_b))
    print(hex(self.reg_c))
    print(hex(self.reg_d))
      
    return str(self.reg_a) + str(self.reg_b) + str(self.reg_c) + str(self.reg_c)           

if __name__ == "__main__":
  my_str = "THIS IS MY TEXT"
  #my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5"
  input_data = InputData(my_str,"text")
  input_data.transform_to_bits()
  print(input_data.get_input_data_bin())
  print(input_data.get_input_data_bin_len())
  input_data.bit_length_alignment()
  print(input_data.padded_data_bin_len)
  print("\n")
  print(hex(int(input_data.input_data_bin,2)))
  print(bin(int(input_data.input_data_bin,2)))
  print(hex(int.from_bytes(int(input_data.input_data_bin,2).to_bytes(len(input_data.input_data_bin)//8,byteorder='little'), byteorder='big')))
  print("NUM OF INT BLOCKS: " + str(input_data.num_of_bin_blocks))
  md5 = Md5(InitRegisters)
  print(hex(int(md5.rounds(input_data))))

  #TODO ARGUMENTS
  #TODO PYDOC
  
