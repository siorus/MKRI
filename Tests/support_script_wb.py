#!/usr/bin/python3
import math
import sys
import argparse
 
rotate_amounts = [7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22, 7, 12, 17, 22,
                  5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20, 5,  9, 14, 20,
                  4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23, 4, 11, 16, 23,
                  6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21, 6, 10, 15, 21]
 
constants = [int(abs(math.sin(i+1)) * 2**32) & 0xFFFFFFFF for i in range(64)]
 
init_values = [0x67452301, 0xefcdab89, 0x98badcfe, 0x10325476]
 
functions = 16*[lambda b, c, d: (b & c) | (~b & d)] + \
            16*[lambda b, c, d: (d & b) | (~d & c)] + \
            16*[lambda b, c, d: b ^ c ^ d] + \
            16*[lambda b, c, d: c ^ (b | ~d)]
 
index_functions = 16*[lambda i: i] + \
                  16*[lambda i: (5*i + 1)%16] + \
                  16*[lambda i: (3*i + 5)%16] + \
                  16*[lambda i: (7*i)%16]
 
def left_rotate(x, amount):
    x &= 0xFFFFFFFF
    return ((x<<amount) | (x>>(32-amount))) & 0xFFFFFFFF
 
def md5(message):
 
    message = bytearray(message) #copy our input into a mutable buffer
    orig_len_in_bits = (8 * len(message)) & 0xffffffffffffffff
    message.append(0x80)
    while len(message)%64 != 56:
        message.append(0)
    message += orig_len_in_bits.to_bytes(8, byteorder='little')
 
    hash_pieces = init_values[:]
 
    for chunk_ofst in range(0, len(message), 64):
        a, b, c, d = hash_pieces
        chunk = message[chunk_ofst:chunk_ofst+64]
        for i in range(64):
            f = functions[i](b, c, d)
            g = index_functions[i](i)
            to_rotate = a + f + constants[i] + int.from_bytes(chunk[4*g:4*g+4], byteorder='little')
            new_b = (b + left_rotate(to_rotate, rotate_amounts[i])) & 0xFFFFFFFF
            a, b, c, d = d, new_b, b, c
            
            print("i: " + str(i))
            print("CHUNK START: " + str(4*g))
            print("CHUNK END: " + str(4*g+4))
            print("FUNCTION RET: " + str(hex(f)))
            print("DATA: " + str(hex(int.from_bytes(chunk[4*g:4*(g + 1)],"little"))))
            print("REG A: " + str(hex(a)))
            print("REG B: " + str(hex(b)))
            print("REG C: " + str(hex(c)))
            print("REG D: " + str(hex(d)))
        for i, val in enumerate([a, b, c, d]):
            hash_pieces[i] += val
            hash_pieces[i] &= 0xFFFFFFFF        
        print("END OF BLOCK " + str(chunk_ofst//64))
 
    return sum(x<<(32*i) for i, x in enumerate(hash_pieces))
 
def md5_to_hex(digest):
    raw = digest.to_bytes(16, byteorder='little')
    return '{:032x}'.format(int.from_bytes(raw, byteorder='big'))
 
if __name__=='__main__':
    if (sys.argv[1] == 'b'):
        fd = open(sys.argv[2],'rb')
        file_data = fd.read()
        print(md5_to_hex(md5(file_data)))
    elif (sys.argv[1] == 't'):
        fd = open(sys.argv[2],'r')
        file_data = fd.read()
        print(md5_to_hex(md5(bytearray(file_data.encode("utf-8")))))
    elif (sys.argv[1] == 'i'):
        print(md5_to_hex(md5(bytearray(sys.argv[2].encode("utf-8")))))
    
    
    

