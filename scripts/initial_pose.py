#!/usr/bin/env python3

import rospy
from progetto_robot.msg import StartMsg
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

class InitialPose:

	def __init__(self):
		rospy.init_node("set_initial_point")
		self.poseTopic = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size = 2)
		self.navigationTopic = rospy.Publisher("/startnavigation", StartMsg, queue_size = 2)

	def set_pose(self):
		pose_msg = PoseWithCovarianceStamped()
		pose_msg.header.frame_id = "map"

		gazebo_pose = rospy.wait_for_message("/odom", Odometry)
		pose_msg.pose.pose = gazebo_pose.pose.pose

		rospy.sleep(1)
		rospy.loginfo("Pose setted on: %s"%pose_msg)
		self.poseTopic.publish(pose_msg)
		rospy.loginfo("Pose Published, ready to shutdown the node")
		start_msg = StartMsg()
		start_msg.start = True
		start_msg.msg = "Here we go"
		self.navigationTopic.publish(start_msg)
		rospy.signal_shutdown("My job here is done *skatuuush*")


if __name__ == "__main__":
	pose = InitialPose()
	pose.set_pose()
