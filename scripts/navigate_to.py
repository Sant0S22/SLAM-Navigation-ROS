#!/usr/bin/env python3

import rospy
import math
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from progetto_robot.srv import Waypoint, WaypointResponse

class NavigateTo:

	def  __init__(self):
		rospy.init_node("navigate_to", anonymous = True)
		self.service = rospy.Service("navigation_service", Waypoint, self.navigate)

	def save_param(self,pose):
		rospy.set_param("pose/x",pose.x)
		rospy.set_param("pose/y",pose.y)
		rospy.set_param("pose/z",pose.z)

	def get_param(self):
		x = rospy.get_param("destination/x")
		y = rospy.get_param("destination/y")
		z = rospy.get_param("destination/z")
		return x, y, z


	def successfull_nav(self, status, result):
		if status == 3:
			rospy.loginfo("Goal Reached")
		elif status == 2 or status == 8:
			rospy.loginfo("Goal Cancelled")
		elif status == 4:
			rospy.loginfo("Goal Aborted")

	def initial_log(self):
		rospy.loginfo("Goal Pose is being processed")

	def continous_feed(self,feedback):
		self.save_param(feedback.base_position.pose.position)
		x, y, z = self.get_param()

		actual_position = feedback.base_position.pose.position
		dist = math.sqrt((x-actual_position.x)**2 + (y-actual_position.y)**2 + (z-actual_position.z)**2)

		rospy.loginfo("Current Pose: %s"%feedback.base_position.pose.position)
		rospy.loginfo("Distance to reach the destination: %s"%dist)


	def navigate(self, point):
		navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		navclient.wait_for_server()

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()

		print(point)

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
			#rospy.loginfo(self.navclient.get_result())
			esito = str(navclient.get_result())
		return esito

if __name__ == "__main__":
	navigator = NavigateTo()
	while not rospy.is_shutdown():
		rospy.spin()
