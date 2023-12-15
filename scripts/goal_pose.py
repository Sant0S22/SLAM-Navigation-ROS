#!/usr/bin/env python3

import rospy
import actionlib
from move_base_msgs.msg import MoveBaseAction, MoveBaseGoal
from progetto_robot.srv import Waypoint

# Callbacks definition

def navigate(point):
    navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
    print("waito")
    navclient.wait_for_server()
    print("hooo waiitato")

        # Example of navigation goal
    goal = MoveBaseGoal()
    goal.target_pose.header.frame_id = "map"
    goal.target_pose.header.stamp = rospy.Time.now()

    goal.target_pose.pose.position.x = 2
    goal.target_pose.pose.position.y = 2
    goal.target_pose.pose.position.z = 0
    goal.target_pose.pose.orientation.x = 0.0
    goal.target_pose.pose.orientation.y = 0.0
    goal.target_pose.pose.orientation.z = 0.0
    goal.target_pose.pose.orientation.w = 0.0

    navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
    #navclient.send_goal(goal)
    finished = navclient.wait_for_result()

    if not finished:
        rospy.logerr("Action server not available!")
    else:
        rospy.loginfo ( navclient.get_result())
    return("bella zi")


def active_cb():
    rospy.loginfo("Goal pose being processed")

def feedback_cb(feedback):
    rospy.loginfo("Current location: "+str(feedback))

def done_cb(status, result):
    if status == 3:
        rospy.loginfo("Goal reached")
    if status == 2 or status == 8:
        rospy.loginfo("Goal cancelled")
    if status == 4:
        rospy.loginfo("Goal aborted")
    

rospy.init_node('navigate_to',anonymous=True)
#service = rospy.Service("navigation_service", Waypoint, navigate)
navclient = actionlib.SimpleActionClient('move_base',MoveBaseAction)
print("waito")
navclient.wait_for_server()
print("hooo waiitato")

        # Example of navigation goal
goal = MoveBaseGoal()
goal.target_pose.header.frame_id = "map"
goal.target_pose.header.stamp = rospy.Time.now()

goal.target_pose.pose.position.x = 2
goal.target_pose.pose.position.y = 2
goal.target_pose.pose.position.z = 0
goal.target_pose.pose.orientation.x = 0.0
goal.target_pose.pose.orientation.y = 0.0
goal.target_pose.pose.orientation.z = 0.666
goal.target_pose.pose.orientation.w = 0.777

navclient.send_goal(goal, done_cb, active_cb, feedback_cb)
    #navclient.send_goal(goal)
finished = navclient.wait_for_result()

if not finished:
    rospy.logerr("Action server not available!")
else:
    rospy.loginfo ( navclient.get_result())


