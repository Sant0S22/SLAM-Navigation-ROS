#!/usr/bin/env python3

import rospy
import yaml
from nav_msgs.msg import Odometry

class RegisterPoints:

	# Initialize the node and load the waypoints file from disk
	def __init__(self):
		rospy.init_node("register_points", anonymous = True)
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "r") as f:
			self.data = yaml.safe_load(f)
		#print(self.data)

	# Save the waypoints in the waypoints file
	def save_yaml(self):
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "w") as f:
			yaml.safe_dump(self.data,f)

	# Shows the interface to name the waypoint created by the actual position of the robot
	def interface(self):
		while True:
			print("-----------------------------")
			print("Write a name for the waypoint")
			print("Type quit to interrupt")
			name = input("Here ->")
			if name == "quit":
				break
			gazebo_pose = rospy.wait_for_message("/odom", Odometry)
			point = [gazebo_pose.pose.pose.position.x, gazebo_pose.pose.pose.position.y, gazebo_pose.pose.pose.position.z]
			self.data[name] = point
		self.save_yaml()


if __name__ == "__main__":
	try:
		register = RegisterPoints()
		register.interface()
	except Exception as e:
		print(e)
		pass