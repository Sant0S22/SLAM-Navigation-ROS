#!/usr/bin/env python3

import rospy
import yaml
from progetto_robot.msg import StartMsg
from progetto_robot.srv import Waypoint, WaypointResponse

class ChoosePoint:

	def __init__(self):
		rospy.init_node("choose_point", anonymous = True)
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "r") as f:
			self.data = yaml.safe_load(f)
		#print(self.data)
		self.startTopic = rospy.Subscriber("/startnavigation", StartMsg, self.interface )
		#self.navigationTopic = rospy.Publisher("/go_waypoint", Waypoint, queue_size=10 )

	def save_param(self,pose):
		rospy.set_param("destination/x",pose[0])
		rospy.set_param("destination/y",pose[1])
		rospy.set_param("destination/z",pose[2])

	def choose(self):
		print("Choose between these rooms where you want navigate to")
		n = 0
		for waypoint in self.data.keys():
			print("%s %s"%(n,waypoint))
			n = n + 1
		while True:
			place = input("Here -> ")
			if place in self.data:
				break
			else:
				print("Please choose a correct place from the listed up there")
		return place
	
	def interface(self, bool):
		while not rospy.is_shutdown():
			place = self.choose()
			point = self.data[place]
			rospy.wait_for_service("navigation_service")
			try :
				self.save_param(point)
				navigator = rospy.ServiceProxy("navigation_service",Waypoint)
				navigator(point[0],point[1],point[2])
			except rospy.ServiceException as e:
				print("Service has fallen")
				print(e)

if __name__ == "__main__":
	while not rospy.is_shutdown():
		choose = ChoosePoint()
		rospy.spin()
