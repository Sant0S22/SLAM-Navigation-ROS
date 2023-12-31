#!/usr/bin/env python3

import rospy
import math
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from progetto_robot.srv import Waypoint, WaypointResponse

class NavigateTo:

	# Initialize the node and set the Server
	def  __init__(self):
		rospy.init_node("navigate_to", anonymous = True)
		self.service = rospy.Service("navigation_service", Waypoint, self.navigate)

	# Save the Pose of the robot on Server Parameter
	def save_param(self,pose):
		rospy.set_param("pose/x",pose.x)
		rospy.set_param("pose/y",pose.y)
		rospy.set_param("pose/z",pose.z)

	# It's executed when the navigation ends and print the status of the navigation
	def successfull_nav(self, status, result):
		if status == 3:
			rospy.loginfo("Goal Reached")
		elif status == 2 or status == 8:
			rospy.loginfo("Goal Cancelled")
		elif status == 4:
			rospy.loginfo("Goal Aborted")

	# It's executed just at the beginning of the navigation
	def initial_log(self):
		rospy.loginfo("Pose processed... Navigation is starting!")

	# Continuous feedback of the navigation with the pose and the remaining distance to reach the destination
	def continous_feed(self,feedback):
		self.save_param(feedback.base_position.pose.position)
		actual_position = feedback.base_position.pose.position
		dist = math.sqrt((self.destination.x-actual_position.x)**2 + (self.destination.y-actual_position.y)**2 + (self.destination.z-actual_position.z)**2)
		rospy.loginfo("Current Pose: %s"%feedback.base_position.pose.position)
		rospy.loginfo("Distance to reach the destination: %s"%dist)

	# Communicate to the Movement server the destination goal 
	def navigate(self, point):
		navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		navclient.wait_for_server()
		self.destination = point

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()
		goal.target_pose.pose.position.x = point.x
		goal.target_pose.pose.position.y = point.y
		goal.target_pose.pose.position.z = point.z
		goal.target_pose.pose.orientation.x = 0.0
		goal.target_pose.pose.orientation.y = 0.0
		goal.target_pose.pose.orientation.z = 0.666
		goal.target_pose.pose.orientation.w = 0.777

		navclient.send_goal(goal, self.successfull_nav, self.initial_log, self.continous_feed)
		finished = navclient.wait_for_result()

		if not finished: 
			rospy.loginfo("Problems with Action Server")
			esito = "Problems"
		else :
			esito = str(navclient.get_result())
		return esito

if __name__ == "__main__":
	try:
		navigator = NavigateTo()
		while not rospy.is_shutdown():
			rospy.spin()
	except Exception as e:
		print(e)
		pass
