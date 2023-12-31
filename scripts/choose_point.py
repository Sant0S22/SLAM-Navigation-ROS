#!/usr/bin/env python3

import rospy
import yaml
from progetto_robot.msg import StartMsg
from progetto_robot.srv import Waypoint, WaypointResponse

class ChoosePoint:

	# Initialize the node, load the waypoints and subscriibe to the topic
	def __init__(self):
		rospy.init_node("choose_point", anonymous = True)
		with open("/home/nick/catkin_ws/src/progetto_robot/scripts/waypoints.yaml", "r") as f:
			self.data = yaml.safe_load(f)
		#print(self.data)
		self.startTopic = rospy.Subscriber("/startnavigation", StartMsg, self.interface )

	# Print all the named waypoints and verify if the choosen one is from the listed
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
	
	# Shows the interface and manage the interaction with the Navigation Service
	def interface(self, bool):
		rospy.sleep(2)
		while not rospy.is_shutdown():
			place = self.choose()
			point = self.data[place]
			rospy.wait_for_service("navigation_service")
			try :
				navigator = rospy.ServiceProxy("navigation_service",Waypoint)
				navigator(point[0],point[1],point[2])
			except rospy.ServiceException as e:
				print("Navigation Service has fallen")
				print(e)

if __name__ == "__main__":
	try:
		choose = ChoosePoint()
		while not rospy.is_shutdown():
			rospy.spin()
	except Exception as e:
		print(e)
		pass
