# PDC Project
# Authors: Thierry B., Niroshan V., Ignacio A.

import math
from bitstring import BitArray
from reedsolo import RSCodec
import zlib
import numpy as np


# transforms a list of lists into a list
flatten = lambda l: [item for sublist in l for item in sublist]

def distance(c1, c2):
    # Euclidian distance between vector c1 and c2
    return np.linalg.norm(c1 - c2)

def arrayToNumber(arr):
    # transforms an arr into int (e.g. [1, 3] -> 13)
    return int(''.join(map(str,arr)))

def encode(string, coding):
    #encode the text in bytes
    in_bytes = string.encode("utf-8")
    #compress the bytes
    compressed = zlib.compress(in_bytes, 9)
    # if coding!=0, add error correcting code
    if(coding):
        rs = RSCodec(coding)
        compressed = rs.encode(compressed)
    return compressed

def decode(compressed, coding):
    #correct errors if coding!=0
    if(coding):
        rs = RSCodec(coding)
        compressed = rs.decode(compressed)
    #decompress the bytes
    in_bytes = zlib.decompress(compressed)
    #decode the text in bytes
    string = in_bytes.decode("utf-8")
    return string

def color_creation(n_tons):
    #select the different values
    ton = [(i)*255//(n_tons-1) for i in range(n_tons)]
    
    # fill the color array
    colors = []
    for i in range(n_tons):
        for j in range(n_tons):
            for k in range (n_tons):
                color = ((ton[i], ton[j], ton[k]))
                colors.append(color)
    return colors

def base_change(in_array, in_base, out_base):
    starting_zeros = 0
    num = 0
    power = len(in_array)-1
    while in_array[0] == 0:
        in_array = in_array[1:]
        starting_zeros += 1
        power -= 1
    while power >= 0:
        adding = in_array[0]*(in_base**power)
        num += adding
        power -= 1
        in_array = in_array[1:]
    
    new_num_array = []
    current = num
    while current!=0:
        remainder=current%out_base
        new_num_array = [remainder] + new_num_array
        current = current // out_base
    return ([0]*starting_zeros) + new_num_array

def text_to_colors(text, n_tons, coding):
    n_colors = n_tons**3
    
    #encode the text with compression
    encoded = encode(text, coding)
    #takes the bits of the message
    bits = BitArray(encoded).bin
    #makes the bits as an array
    bits_array = list(map(int, bits))    
    #change the input bits in our "colors-base"
    colors = base_change(bits_array, 2, n_colors)
    return colors

def colors_to_text(colors, n_tons, coding):
    n_colors = n_tons**3
    
    bits_array = base_change(colors, n_colors, 2)    
    bit_string = ''.join(map(str, bits_array))
    bits = BitArray('0b' + bit_string)
    encoded = bits.tobytes()
    text = decode(encoded, coding)
    return text
