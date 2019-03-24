#!/usr/bin/python3
# coding: utf-8

'''
  File name: mkrihash.py
  Author: Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky
  Date created: 12/2/2019
  Date last modified: 24/3/2019
  Python Version: 3.5
'''

__author__ = 'Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky'
__copyright__ = 'Copyright 2019, Juraj Korcek, Karel Kuchar, Eva Holasova, Lukas Hrboticky'
__license__ = 'GPL'
__version__ = '3'
__email__ = 'jurajkorcek@gmail.com'
__status__ = 'Development'

import sys
import argparse

DEBUG = False

class InitRegisters:
  """
  Initial value for registers which is used for first iteration.
  Note that, registers are in little-endian, RFC 1321 shows their
  values in big-endian. Source: RFC 1321.

  Attributes:
      reg_a (:obj: `int`): register A init value
      reg_b (:obj: `int`): register B init value
      reg_c (:obj: `int`): register C init value
      reg_d (:obj: `int`): register D init value 
  """
  reg_a = 0x67452301
  reg_b = 0xefcdab89
  reg_c = 0x98badcfe
  reg_d = 0x10325476

class ShiftConst:
  """
  Shift constants for each iteration within one round. Source: RFC 1321. 

  Attributes:
      values (:obj: `tuple` of :obj: `int`): Shift constants for each round.
  """
  values = (7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
            5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
            4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
            6, 10, 15, 21, 6, 10, 15, 21 , 6, 10, 15, 21, 6, 10, 15, 21)

class TConst:
  """
  T constants, which can be computed during round or at the begining of 
  runtime or a table for faster computation can be used. Constants are
  computed from equation T[i] = abs(sin(i)) & 2^32, where i = <1,64>.
  Values are in little-endian. Source: https://en.wikipedia.org/wiki/MD5. 

  Attributes:
      values (:obj: `tuple` of :obj: `int`): Holds 'T' constants.
  """  
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
    self.input_data_len = 0
    self.num_of_blocks = 0

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
  
  def set_num_of_blocks(self):
    """
    Sets number of 512 bit blocks from which consists padded input data
    """
    self.num_of_blocks = len(self.input_data) // 64 # 64 bytes = 512 bits / 8
 
  def byte_length_alignment(self):
    """
    Adds bits for proper padding to multiplication of 512.
    """
    
    self.set_input_data_len()
    """
    Does not add one bit, but adds byte '10000000'. Although RFC 1321 says
    only bit '1' must be added, PC cannot add just one bit, it must be whole
    byte.
    """
    self.input_data += 0x80.to_bytes(1, byteorder="little")
    modulo = len(self.input_data) % 64

    #black magic which determines number of zeroes to add
    if modulo != 56:
      if modulo > 56:
        zeroes_to_add = 56 + (64-modulo)
      else:
        zeroes_to_add = 56 - modulo
      self.input_data += zeroes_to_add * 0x00.to_bytes(1, byteorder="little")
    
    self.input_data += self.input_data_len.to_bytes(8, byteorder="little")  #add len of input string before bit padding
    self.set_num_of_blocks()  #sets number of 512 bit blocks

  def set_input_data_len(self):
    """
    Sets length of input_data before bit padding
    """
    self.input_data_len = (len(self.input_data) * 8)

class Md5:
  """
  Provides operations for MD5 algorithm.
  """
  
  def __init__(self,init_registers):
    """
    Args:
        init_registers (:obj: `InitRegisters` of :obj: `int`): Values of init registers A,B,C,D.

    Attributes:
        reg_a (:obj: `int`): Register A for intermediate computations and result.
        reg_b (:obj: `int`): Register B for intermediate computations and result.
        reg_c (:obj: `int`): Register C for intermediate computations and result.
        reg_d (:obj: `int`): Register D for intermediate computations and result.
    """
    self.reg_a = init_registers.reg_a
    self.reg_b = init_registers.reg_b
    self.reg_c = init_registers.reg_c
    self.reg_d = init_registers.reg_d

  def function_f(self,reg_b,reg_c,reg_d):
    """
    Function F for MD5 round.

    Args:
        reg_b (:obj: `int`): Register B for computations
        reg_c (:obj: `int`): Register C for computations
        reg_d (:obj: `int`): Register D for computations
    
    Returns:
        Result of function F.
    """
    f = (reg_b & reg_c) | (~reg_b & reg_d)
    return f

  def function_g(self,reg_b,reg_c,reg_d):
    """
    Function G for MD5 round.

    Args:
        reg_b (:obj: `int`): Register B for computations
        reg_c (:obj: `int`): Register C for computations
        reg_d (:obj: `int`): Register D for computations
    
    Returns:
        Result of function G.
    """
    g = (reg_b & reg_d) | (reg_c & ~reg_d)
    return g

  def function_h(self,reg_b,reg_c,reg_d):
    """
    Function H for MD5 round.

    Args:
        reg_b (:obj: `int`): Register B for computations
        reg_c (:obj: `int`): Register C for computations
        reg_d (:obj: `int`): Register D for computations
    
    Returns:
        Result of function H.
    """
    h = (reg_b ^ reg_c ^ reg_d)
    return h

  def function_i(self,reg_b,reg_c,reg_d):
    """
    Function I for MD5 round.

    Args:
        reg_b (:obj: `int`): Register B for computations
        reg_c (:obj: `int`): Register C for computations
        reg_d (:obj: `int`): Register D for computations
    
    Returns:
        Result of function I.
    """
    i = reg_c ^ (reg_b | ~reg_d)
    return i

  def left_bit_rotate(self,bits_to_rotate,nth_rotation):
    """
    Left bit rotation

    Args:
        bits_to_rotate (:obj: `int`): Input which has to be rotated.
        nth_rotation (:obj: `int`): Determines number of bits which has to be rotated.

    Returns:
        Left bit rotation of input.
    """
    return ((bits_to_rotate << nth_rotation) | (bits_to_rotate >> (32 - nth_rotation))) 

  """
  def swap_byte_order(self,to_be_swapped):
    
    Swap byte order from little to big endian.

    Args:
        to_be_swapped (:obj: `int`): Input for byte swap.
    
    Returns:
        Swapped data from little to big endian.
    
    return int.from_bytes(to_be_swapped.to_bytes(4,byteorder='little'), byteorder='big')
  """

  def produce_hash(self):
    """
    Creates resulting hash from final values of registers.

    Returns:
        Hash in hexadecimal interpretation.
    """
    hash = 0x0
    hash = hash | self.reg_d
    hash = hash << 32 | self.reg_c  #append to result varible and align bits by shifting
    hash = hash << 32 | self.reg_b
    hash = hash << 32 | self.reg_a
    """
    Metod 'format' creates output in hexadecimal with 32 positions for number and append leading 
    zeroes when the length of output would be less than 32 digits. Python function 'hex' causes 
    some inconsistency of resulting hash that's why 'fromat is used'. 
    """
    hash = '{:032x}'.format(int.from_bytes(hash.to_bytes(16, byteorder='little'), byteorder='big'))

    return hash

  def rounds(self,input_data):
    """
    Performs MD5 rounds.

    Args:
        input_data (:obj: `InputData`): Input data which have to be hashed.

    Returns:
        Hash of input data.
    """
    for nth_block in range(input_data.num_of_blocks):  #loop over every 512bit parts of input
      reg_a, reg_b, reg_c, reg_d = self.reg_a, self.reg_b, self.reg_c, self.reg_d  #store registers in temporary variable
      for i in range(64):  #loop over every byte
        data_512bit = input_data.input_data[64*nth_block:64*(nth_block+1)]  #take nth byte
        if (i <= 15):
          fun_ret = self.function_f(reg_b,reg_c,reg_d)  #first 16 steps an F function will be processing input
          nth_word = i
        elif (i <= 31):
          fun_ret = self.function_g(reg_b,reg_c,reg_d)  #second 16 steps an G function will be processing input
          nth_word = (5*i + 1) % 16   #offsets bytes in input string, G starts with input [1] then [6] then [11]
        elif (i <= 47):
          fun_ret = self.function_h(reg_b,reg_c,reg_d)  #third 16 steps an H function will be processing input
          nth_word = (3*i + 5) % 16
        else:
          fun_ret = self.function_i(reg_b,reg_c,reg_d)  #last 16 steps an I function will be processing input
          nth_word = (7*i) % 16

        #every operation has to be masked to ensure 32 bit length (addition modulo)
        addition_chain = (((((reg_a + fun_ret) & 0xFFFFFFFF) + int.from_bytes(data_512bit[4*nth_word:4*(nth_word + 1)],byteorder="little")) & 0xFFFFFFFF) + TConst.values[i]) & 0xFFFFFFFF
        reg_a = reg_d
        reg_d = reg_c
        reg_c = reg_b
        reg_b = (reg_b + self.left_bit_rotate(addition_chain,ShiftConst.values[i])) & 0xFFFFFFFF
      
        if (DEBUG):
          print("i: " + str(i))
          print("CHUNK START: " + str(4*nth_word))
          print("CHUNK END: " + str(4*nth_word+4))
          print("FUN: " + str(hex(fun_ret)))
          print("DATA: " + str(hex(int.from_bytes(data_512bit[4*nth_word:4*(nth_word + 1)],"little"))))
          print("REG A: " + str(hex(reg_a)))
          print("REG B: " + str(hex(reg_b)))
          print("REG C: " + str(hex(reg_c)))
          print("REG D: " + str(hex(reg_d)))
      if (DEBUG):  
        print("KONIEC BLOKU " + str(nth_block))
      
      #final result assignments to registers
      self.reg_a = (self.reg_a + reg_a) & 0xFFFFFFFF
      self.reg_b = (self.reg_b + reg_b) & 0xFFFFFFFF
      self.reg_c = (self.reg_c + reg_c) & 0xFFFFFFFF
      self.reg_d = (self.reg_d + reg_d) & 0xFFFFFFFF

    return self.produce_hash()           

if __name__ == "__main__":
  version = 1.0
  parser = argparse.ArgumentParser(prog="mkrihash.py", description="MD5 hash generator",formatter_class=argparse.ArgumentDefaultsHelpFormatter)
  parser.add_argument("-v","--version",action="version", version="%(prog)s"+" version "+str(version))
  parser.add_argument("-m","--machine-readable",help="prints output in machine readable form, only result hash",action="store_true")
  parser.add_argument("-d","--debug",help="Debugging mode, shows intermediate hash results",action="store_true")
  special_run = parser.add_mutually_exclusive_group(required=True)
  special_run.add_argument("-i","--inline-text",help="input for MD5 is text and written after this argument",action="store")
  special_run.add_argument("-t","--text-file",metavar="FILE",help="input for MD5 is text file and specify path to it",action="store")
  special_run.add_argument("-b","--binary-file",help="input for MD5 is binary file and specify path to it",action="store")
  args = parser.parse_args()

  if (args.debug):
    DEBUG = True

  if (args.text_file):
    data_type = ""
    input_data = InputData(args.text_file,data_type,True)
  elif (args.inline_text):
    data_type = ""
    input_data = InputData(args.inline_text,data_type,False)  #is_file bool is false, inline input
  else:
    data_type = "b"  #input file is binary
    input_data = InputData(args.binary_file,data_type,True)

  input_data.byte_length_alignment()
  md5 = Md5(InitRegisters)
  hash = md5.rounds(input_data)
  if (args.machine_readable):
    print(hash)
  else:
    if (args.inline_text):
      print("INLINE TEXT: " + args.inline_text)
    elif(args.text_file):
      print("TEXT FILE: " + args.text_file)
    elif(args.binary_file):
      print("BINARY FILE: " + args.binary_file)
    print("MD5 HASH: " + hash)
  #my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5" #DELETE
  