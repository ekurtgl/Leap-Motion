import Leap
import ctypes
import struct
import numpy as np

controller = Leap.Controller()

with open("frame.data", "rb") as data_file:
    # The first 4 bytes of the file to determine how much data to read to get an entire frame
    # https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Serialization.html

    next_block_size = data_file.read(4)
    while next_block_size:
        size = struct.unpack('i', next_block_size)[0]
        data = data_file.read(size)
        leap_byte_array = Leap.byte_array(size)
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, data, size)

        frame = Leap.Frame()
        frame.deserialize((leap_byte_array, size))
        next_block_size = data_file.read(4)

