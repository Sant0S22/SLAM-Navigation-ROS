#!/usr/bin/env python3

import rospy
from std_msgs.msg import Bool
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

class InitialPose:

	def __init__(self):
		rospy.init_node("set_initial_point")
		self.poseTopic = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size = 2)
		self.navigationTopic = rospy.Publisher("/startnavigation", Bool, queue_size = 2)

	def set_pose(self):
		pose_msg = PoseWithCovarianceStamped()
		pose_msg.header.frame_id = "map"

		gazebo_pose = rospy.wait_for_message("/odom", Odometry)
		pose_msg.pose.pose = gazebo_pose.pose.pose

		rospy.sleep(1)
		rospy.loginfo("Pose setted on: %s"%pose_msg)
		self.poseTopic.publish(pose_msg)
		rospy.loginfo("Pose Published, ready to shutdown the node")
		self.navigationTopic.publish(True)
		rospy.signal_shutdown("My job here is done *skatuuush*")


if __name__ == "__main__":
	pose = InitialPose()
	pose.set_pose()