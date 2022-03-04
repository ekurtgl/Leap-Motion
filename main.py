import struct
import time

import Leap
import sys
import ctypes
import os
import argparse

# Create the parser
parser = argparse.ArgumentParser()

# Add an argument
parser.add_argument('--filename', type=str, required=True)
parser.add_argument('--duration', type=int, required=True)

# Parse the argument
args = parser.parse_args()


class LeapMotionListener(Leap.Listener):
    finger_names = ['Thumb', 'Index', 'Middle', 'Ring', 'Pinky']
    bone_names = ['Metacarpal', 'Proximal', 'Intermediate', 'Distal']
    state_names = ['STATE_INVALID', 'STATE_START', 'STATE_UPDATE', 'STATE_END']
    cnt = 1  # num of frames
    filename = 'frame.data'
    duration = 1  # data recording in sec
    start_time = time.time()

    def on_init(self, controller):
        print('Initialized')

    def on_connect(self, controller):
        print('Motion sensor connected')

        controller.enable_gesture(Leap.Gesture.TYPE_CIRCLE)
        controller.enable_gesture(Leap.Gesture.TYPE_KEY_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SCREEN_TAP)
        controller.enable_gesture(Leap.Gesture.TYPE_SWIPE)

    def on_disconnect(self, controller):
        print('Motion sensor disconnected')

    def on_exit(self, controller):

        with open(os.path.realpath(self.filename), 'wb') as data_file:
            for f in range(self.cnt):
                frame = controller.frame(self.cnt - f)
                serialized_tuple = frame.serialize
                serialized_data = serialized_tuple[0]
                serialized_length = serialized_tuple[1]
                data_address = serialized_data.cast().__long__()
                buffer_temp = (ctypes.c_ubyte * serialized_length).from_address(data_address)

                data_file.write(struct.pack('i', serialized_length))
                data_file.write(buffer_temp)

        print('Exited')

    def on_frame(self, controller):
        # frame = controller.frame()

        ''' print('Frame ID: ' + str(frame.id) +
              ', Timestamp: ' + str(frame.timestamp) +
              ', # of Hands: ' + str(len(frame.hands)) +
              ', # of Fingers: ' + str(len(frame.fingers)) +
              ', # of Tools: ' + str(len(frame.tools)) +
              ', # of Gestures: ' + str(len(frame.gestures()))) '''

        '''for hand in frame.hands:
            handType = 'Left Hand' if hand.is_left else 'Right Hand'

            print(handType + ', Hand ID: ' + str(hand.id) + ', Palm position: ' +
                  str(hand.palm_position))'''

        if time.time() - self.start_time >= self.duration:
            self.on_exit(controller)

        print 'Frame: ' + str(self.cnt)

        self.cnt += 1


def main():
    listener = LeapMotionListener()
    listener.filename = args.filename
    listener.duration = args.duration
    controller = Leap.Controller()
    controller.add_listener(listener)
    begin_time = time.time()

    print('Press enter to quit')

    while True:
        if time.time() - begin_time >= listener.duration:
            break
    controller.remove_listener(listener)

    # try:
    #     sys.stdin.readline()
    #     # print 'passss'
    #     # pass
    # except KeyboardInterrupt:
    #     pass
    # finally:
    #     controller.remove_listener(listener)


if __name__ == '__main__':
    main()
