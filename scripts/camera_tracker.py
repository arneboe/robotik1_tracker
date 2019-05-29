#!/usr/bin/env python
import rospy
import tf
from tf.transformations import quaternion_inverse, euler_from_quaternion, quaternion_from_euler, rotation_matrix
import sys
from geometry_msgs.msg import PoseStamped, TransformStamped
from std_msgs.msg import Header

import numpy as np


def pose_received(data):
    global current_pose
    current_pose = data

def getKey():
    key = sys.stdin.read(1)
    return key

def toYaw(q):
    euler = euler_from_quaternion(q)
    #roll = euler[0]
    #pitch = euler[1]
    yaw = euler[2]
    return yaw

def listener():
    global current_pose
    rospy.init_node('robotik1_listener')
    rospy.Subscriber("aruco_single/pose", PoseStamped, pose_received)

    rate = rospy.Rate(10.0)

    print("Press s + enter to set current pose as start pose\nPress e + enter to set end pose\nPress q + enter to quit")

    t = tf.TransformerROS()

    start_pos = np.zeros(3)#xyz
    start_rot = np.zeros(4) #xyzw
    end_pos = np.zeros(3)

    while not rospy.is_shutdown():
        key = getKey()

        if key == 's':
            print("START (x,y,z| yaw):")
            print(current_pose.pose.position.x, current_pose.pose.position.y, current_pose.pose.position.z,
                  toYaw([current_pose.pose.orientation.x, current_pose.pose.orientation.y, current_pose.pose.orientation.z, current_pose.pose.orientation.w]))

            start_pos[0] = current_pose.pose.position.x
            start_pos[1] = current_pose.pose.position.y
            start_pos[2] = current_pose.pose.position.z
            start_rot[0] = current_pose.pose.orientation.x
            start_rot[1] = current_pose.pose.orientation.y
            start_rot[2] = current_pose.pose.orientation.z
            start_rot[3] = current_pose.pose.orientation.w

        elif key == 'e':
            print("END (x,y,z|w,x,y,z):")
            print(current_pose.pose.position.x, current_pose.pose.position.y, current_pose.pose.position.z,
                  toYaw([current_pose.pose.orientation.x, current_pose.pose.orientation.y, current_pose.pose.orientation.z, current_pose.pose.orientation.w]))

            end_pos[0] = current_pose.pose.position.x
            end_pos[1] = current_pose.pose.position.y
            end_pos[2] = current_pose.pose.position.z

            diff_pos = np.subtract(end_pos, start_pos)
            diff_pos = np.array([diff_pos[0], diff_pos[1], diff_pos[2], 1])

            yaw_rot = - toYaw(start_rot)

            yaw_rot_mat = rotation_matrix(yaw_rot, [0, 0, 1])
            diff_pos_rot = yaw_rot_mat.dot(diff_pos)
            diff_yaw = toYaw([current_pose.pose.orientation.x, current_pose.pose.orientation.y, current_pose.pose.orientation.z, current_pose.pose.orientation.w]) - toYaw(start_rot)

            print("DIFF (x, y, z, yaw)")
            print(diff_pos_rot[0], diff_pos_rot[1], diff_pos_rot[2], diff_yaw)

        elif key == 'q':
            print("quit")
            break

        rate.sleep()


if __name__ == '__main__':
    current_pose = PoseStamped
    listener()
