#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from progetto_robot.srv import Waypoint, WaypointResponse

class NavigateTo:

	def  __init__(self):
		rospy.init_node("navigate_to", anonymous = True)
		self.service = rospy.Service("navigation_service", Waypoint, self.navigate)


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
		rospy.loginfo("Current Pose: %s"%feedback)


	def navigate(self, point):
		navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
		navclient.wait_for_server()

		goal = MoveBaseGoal()
		goal.target_pose.header.frame_id = "map"
		goal.target_pose.header.stamp = rospy.Time.now()

		print(point)

		goal.target_pose.pose.position.x = -6.4#point.x
		goal.target_pose.pose.position.y = -2#point.y
		goal.target_pose.pose.position.z = 0#point.z

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
