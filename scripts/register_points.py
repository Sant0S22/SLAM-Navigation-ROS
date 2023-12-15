#!/usr/bin/env python3

import rospy
import yaml
from nav_msgs.msg import Odometry

class RegisterPoints:

	def __init__(self):
		rospy.init_node("register_points")
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "r") as f:
			self.data = yaml.safe_load(f)
		print(self.data)

	def save_yaml(self):
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "w") as f:
			yaml.safe_dump(self.data,f)

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
	register = RegisterPoints()
	register.interface()