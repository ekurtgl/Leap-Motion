import Leap
import ctypes
import struct
import numpy as np
import matplotlib.pyplot as plt
from mpl_toolkits.mplot3d import Axes3D

controller = Leap.Controller()
data_path = 'C:\\Users\\emrek\\PycharmProjects\\RadarGui\\data\\'
fname = data_path + 'frame.data'
fig = plt.figure()
ax = fig.gca(projection='3d')

with open(fname, "rb") as data_file:
    # The first 4 bytes of the file to determine how much data to read to get an entire frame
    # https://developer-archive.leapmotion.com/documentation/python/devguide/Leap_Serialization.html

    next_block_size = data_file.read(4)
    cnt = 0
    time_now = controller.now()

    while next_block_size:
        size = struct.unpack('i', next_block_size)[0]
        data = data_file.read(size)
        leap_byte_array = Leap.byte_array(size)
        address = leap_byte_array.cast().__long__()
        ctypes.memmove(address, data, size)

        frame = Leap.Frame()
        frame.deserialize((leap_byte_array, size))
        next_block_size = data_file.read(4)
        ims = frame.images
        # print(ims[0])
        # print('Cnt:' + str(cnt) +
        #       ', Frame ID: ' + str(frame.id) +
        #       ', Timestamp: ' + str(frame.timestamp) +
        #       ', # of Hands: ' + str(len(frame.hands)) +
        #       ', # of Fingers: ' + str(len(frame.fingers)) +
        #       ', # of Tools: ' + str(len(frame.tools)) +
        #       ', # of Gestures: ' + str(len(frame.gestures())))

        cnt += 1
        if cnt > 100:
            break

        # print(dir(frame))
        fps = frame.current_frames_per_second
        average = Leap.Vector()
        print('Frame:', str(cnt))
        print('num frame.fingers:', str(len(frame.fingers)))
        # finger_to_average = frame.fingers[0]
        # print('finger_to_average:', str(finger_to_average))
        # print('finger_to_average dict:', str(dir(finger_to_average)))
        # print(finger_to_average.joint_position)
        # finger_from_frame = frame.finger(finger_to_average.id)
        # print('finger_from_frame:', str(finger_from_frame))
        # print('finger_from_frame dir:', str(dir(finger_from_frame)))
        # finger_pos = finger_to_average.tip_position
        # print('finger_pos:', str(finger_pos))

        if len(frame.fingers) != 0:

            for hand in frame.hands:
                # hand_x_basis = hand.basis.x_basis
                # ax.scatter3D(hand_x_basis[0], hand_x_basis[1], hand_x_basis[2], s=20, c='b', marker='o')
                # print(hand_x_basis)
                # hand_y_basis = hand.basis.y_basis
                # ax.scatter3D(hand_y_basis[0], hand_y_basis[1], hand_y_basis[2], s=20, c='b', marker='o')
                # print(hand_y_basis)
                # hand_z_basis = hand.basis.z_basis
                # ax.scatter3D(hand_z_basis[0], hand_z_basis[1], hand_z_basis[2], s=20, c='b', marker='o')
                # print(hand_z_basis)
                hand_origin = hand.palm_position
                ax.scatter3D(hand_origin[0], hand_origin[1], hand_origin[2], s=30, c='g', marker='o')
                # print(hand_origin)

                arm = hand.arm
                if arm.is_valid:
                    width = arm.width
                    wrist_pos = arm.wrist_position
                    # print(wrist_pos)
                    ax.scatter3D(wrist_pos[0], wrist_pos[1], wrist_pos[2], s=30, c='g', marker='o')
                    elbow_pos = arm.elbow_position
                    # print(elbow_pos)
                    ax.scatter3D(elbow_pos[0], elbow_pos[1], elbow_pos[2], s=30, c='g', marker='o')
                    displacement = arm.wrist_position - arm.elbow_position
                    length = displacement.magnitude
                    # print('length', length)
                    ax.plot([wrist_pos[0], elbow_pos[0]], [wrist_pos[1], elbow_pos[1]],
                                                          [wrist_pos[2], elbow_pos[2]],
                            linewidth=3, c='y')

                for finger in hand.fingers:
                    # finger_pos = finger.stabilized_tip_position
                    # print(finger_pos)
                    # ax.scatter3D(finger_pos[0], finger_pos[1], finger_pos[2], s=20, c='r', marker='o')

                    for i in range(4):
                        bone = finger.bone(i)
                        width = bone.width
                        length = bone.length
                        middle = bone.center
                        direction = bone.direction
                        bone_type = bone.type

                        if bone.is_valid:
                            bone_end = bone.next_joint
                            ax.scatter3D(bone_end[0], bone_end[1], bone_end[2], s=20, c='r', marker='o')
                            bone_start = bone.prev_joint
                            ax.scatter3D(bone_start[0], bone_start[1], bone_start[2], s=20, c='r', marker='o')

                            # draw bone
                            ax.plot([bone_end[0], bone_start[0]], [bone_end[1], bone_start[1]],
                                    [bone_end[2], bone_start[2]],
                                    linewidth=3, c='y')

                            if i == 0:
                                ax.plot([wrist_pos[0], bone_start[0]], [wrist_pos[1], bone_start[1]],
                                                                       [wrist_pos[2], bone_start[2]],
                                        linewidth=3, c='y')

        plt.title('Time:' + str(round((controller.now() - time_now) / 1e6, 1)) + ', Frame: ' +
                  str(cnt) + ', FPS: ' + str(round(fps)))
        time_now = controller.now()
        plt.draw()
        plt.pause(1e-3)
        ax.clear()




