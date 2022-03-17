import Leap
import ctypes
import struct
import numpy as np

controller = Leap.Controller()
data_path = 'C:\\Users\\emrek\\PycharmProjects\\RadarGui\\data\\'
fname = data_path + 'frame.data'

with open(fname, "rb") as data_file:
    # The first 4 bytes of the file to determine how much data to read to get an entire frame
    # https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Serialization.html

    next_block_size = data_file.read(4)
    cnt = 0
    while next_block_size:
        size = struct.unpack('i', next_block_size)[0]
        data = data_file.read(size)
        leap_byte_array = Leap.byte_array(size)
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, data, size)

        frame = Leap.Frame()
        frame.deserialize((leap_byte_array, size))
        next_block_size = data_file.read(4)

        print('Cnt:' + str(cnt) +
              ', Frame ID: ' + str(frame.id) +
              ', Timestamp: ' + str(frame.timestamp) +
              ', # of Hands: ' + str(len(frame.hands)) +
              ', # of Fingers: ' + str(len(frame.fingers)) +
              ', # of Tools: ' + str(len(frame.tools)) +
              ', # of Gestures: ' + str(len(frame.gestures())))
        cnt += 1

