#!/usr/bin/env python3

import rospy
from progetto_robot.msg import StartMsg
from geometry_msgs.msg import PoseWithCovarianceStamped
from nav_msgs.msg import Odometry

class InitialPose:

	# Initialize the node and set the topics where it will publish
	def __init__(self):
		rospy.init_node("set_initial_point", anonymous = True)
		self.poseTopic = rospy.Publisher("/initialpose", PoseWithCovarianceStamped, queue_size = 2)
		self.navigationTopic = rospy.Publisher("/startnavigation", StartMsg, queue_size = 2)

	# Get the Pose from Gazebo and set it on Rviz, than shutdown
	def set_pose(self):
		pose_msg = PoseWithCovarianceStamped()
		pose_msg.header.frame_id = "map"
		gazebo_pose = rospy.wait_for_message("/odom", Odometry)
		pose_msg.pose.pose = gazebo_pose.pose.pose
		rospy.loginfo("Pose setted on: %s"%pose_msg)
		self.poseTopic.publish(pose_msg)
		self.save_param(gazebo_pose.pose.pose.position)
		rospy.loginfo("Pose Published, ready to shutdown the node")
		start_msg = StartMsg()
		start_msg.start = True
		start_msg.msg = "Here we go"
		self.navigationTopic.publish(start_msg)
		rospy.signal_shutdown("My job here is done *skatuuush*")

	# Save the Pose of the robot on Server Parameter
	def save_param(self,pose):
		rospy.set_param("pose/x",pose.x)
		rospy.set_param("pose/y",pose.y)
		rospy.set_param("pose/z",pose.z)

if __name__ == "__main__":
	try:
        pose = InitialPose()
		pose.set_pose()
    except Exception as e:
        print(e)
        pass
	
