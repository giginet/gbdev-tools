import struct
from enum import Enum
from functools import reduce

class Pixel(Enum):
    BLACK = 0
    GREY = 1
    LIGHTGREY = 2
    WHITE = 3

data = open('giginyan.bmp', 'rb').read()

HEADER = '<bbIHHI IIiHHIIIIII'
header = struct.unpack_from(HEADER, data, 0)
if not chr(header[0]) == 'B' or not chr(header[1]) == 'M':
    print("Unexpected format")

width = header[7]
height = abs(header[8])
header_length = 54

def convert_to_pixel(r):
    if r > 192:
        return Pixel.WHITE
    elif r > 128:
        return Pixel.LIGHTGREY
    elif r > 64:
        return Pixel.GREY
    return Pixel.BLACK

def to_binary(pixel):
    if pixel == Pixel.WHITE:
        return 0b00
    elif pixel == Pixel.LIGHTGREY:
        return 0b01
    elif pixel == Pixel.GREY:
        return 0b10
    return 0b11

pixels = []
for i in range(width * height):
    r, g, b, a = struct.unpack_from("BBBB", data, header_length + i * 4)
    pixel = convert_to_pixel(r)
    pixels.append(pixel)

output = []
for i in range(int(width * height / 8)):
    ps = [to_binary(p) for p in pixels[i*8:(i+1)*8]]
    first = map(lambda a: int(not (a & 0b01) == 0), ps)
    second = map(lambda a: int(not (a & 0b10) == 0), ps)
    f2 = [v << i for i, v in enumerate(first)]
    s2 = [v << i for i, v in enumerate(second)]
    f3 = reduce(lambda a, b: a | b, f2, 0)
    s3 = reduce(lambda a, b: a | b, s2, 0)
    output.append(hex(f3))
    output.append(hex(s3))
     
array = ','.join(output)
print("unsigned char sprite[] = {" + array + "};")
