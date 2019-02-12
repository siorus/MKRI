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

class ShiftConst:
  values = (7, 12, 17, 22, 5,  9, 14, 20, 4, 11, 16, 23,6, 10, 15, 21)

class TConst:
  values = (0xD76AA478,0xE8C7B756,0x242070DB,0xC1BDCEEE,
            0xF57C0FAF,0x698098D8,0x8B44F7AF,0xFFFF5BB1,
            0x895CD7BE,0x6B901122,0xF61E2562,0xC040B340,
            0x265E5A51,0xE9B6C7AA,0xD62F105D,0x21E1CDE6,
            0xC33707D6,0xF4D50D87,0x455A14ED,0xA9E3E905, 
            0xFFFA3942,0x8771F681,0x6D9D6122,0xFDE5380C,
            0xA4BEEA44,0x289B7EC6,0xEAA127FA,0xD4EF3085,
            0x04881D05,0xD9D4D039,0xF4292244,0x432AFF97,
            0xAB9423A7,0xFC93A039,0x655B59C3,0x6FA87E4F,
            0xFE2CE6E0,0xA3014314,0x4E0811A1,0xF7537E82)

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
    self.input_data_bin_len = 0
    self.padded_data_bin_len = 0

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
      self.input_data_bin += zeroes_to_add * "0"
    self.transform_message_length()
    self.input_data_bin += self.padded_data_bin_len

  def transform_message_length(self):
    
    """ Description
    :type self:
    :param self:
  
    :raises:
  
    :rtype:
    """
    padded_data_bin_len = self.input_data_bin_len
    self.padded_data_bin_len = format(padded_data_bin_len,"0>64b")


if __name__ == "__main__":
  #my_str = "THIS IS MY TEXTč"
  my_str = "THIS IS MY TEXTččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččččč5"
  input_data = InputData(my_str,"text")
  input_data.transform_to_bits()
  print(input_data.get_input_data_bin())
  print(input_data.get_input_data_bin_len())
  input_data.bit_length_alignment()
  print(input_data.padded_data_bin_len)
  print("\n")
  print(input_data.input_data_bin)


  #TODO ARGUMENTS
  #TODO PYDOC
  
