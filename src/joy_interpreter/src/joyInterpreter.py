#This will be the interpreter for the joystick.
#It will subscribe to the joystick topic
#Look for trigger on what type of interpretation
#Take calculation out of ik.py and put into here
#figure out what ik.py is looking for and give it that.
#it should just be used to calculate widths

#!/usr/bin/python
import rospy
from std_msgs.msg import Float32MultiArray
import numpy as np
from ik_helper import *
from sensor_msgs.msg import Joy

ik_pub = rospy.Publisher('/desired_position',Float32MultiArray,queue_size = 1)

max_radius = 7
class commandClass:
	def __init__(self,stage_):
		self.stage = stage_
		self.x = 0
		self.y = 0
		self.z = 92
		self.command = ik_legs(self.x,self.y,self.z)
	def updateXY(self,x,y,joy_rad):
		drad = axes_map(joy_rad,max_radius,0)
		r = np.sqrt(x**2+y**2)
		self.x = drad*(x/r)
		self.y = drad*(y/r)
	def updateZ(self,z):
		self.z = z
	def updateXYZ(self,x,y,z):
		r = np.sqrt(x**2+y**2) 
		if r > 7:
			self.x = 7*(x/r)
			self.y = 7*(y/r)
		else
			self.x = 7*x
			self.y = 7*y
		self.z = (92-173)*((z+1)/2)+173 #normalize axes 3 from 0 to 1, set Z to reverse scale of axes 3.
	def updateCommand(self):
		self.command = ik_legs(self.x,self.y,self.z)
	def getCommand(self):
		return self.command
	def getStage(self):
		return self.stage



command = [0]*9;
# z =92
# x= 0
# y= 0

z_min = 92
z_max = 173
nav = 0
def axes_map(js_sp,ax_max,ax_min):
	sp = (js_sp+1)/2.0
	out = (ax_max - ax_min)*sp+ax_min
	return out

def command_cb(msg):
	global command

	#Take joystick input to determine what navigation method to use
	if msg.buttons[3]:
		nav = 0
	elif msg.buttons[4]:
		nav = 1
	elif msg.buttons[5]:
		nav = 2

	if nav = 0:
		# XYZ
		if msg.buttons[8]:
			command3.updateZ(axes_map(msg.axes[3],z_max,z_min))
			command3.updateCommand()
		if msg.buttons[0]:
			command3.updateXY(msg.axes[0],msg.axes[1],msg.axes[3])
			command3.updateCommand()

		if msg.buttons[9]:
			command2.updateZ(axes_map(msg.axes[3],z_max,z_min))
			command2.updateCommand()
		if msg.buttons[1]:
			command2.updateXY(msg.axes[0],msg.axes[1],msg.axes[3])
			command2.updateCommand()

		if msg.buttons[11]:
			command1.updateZ(axes_map(msg.axes[3],z_max,z_min))
			command1.updateCommand()
		if msg.buttons[2]:
			command1.updateXY(msg.axes[0],msg.axes[1],msg.axes[3])
			command1.updateCommand()

	elif nav = 1:
		# Vector motion

		# same as above, X and Y are set by axes 0 and 1, Z is set by axes 3
		# have to make sure X and Y are within a circle of radius 7
		if msg.buttons[8]:
			command3.updateXYZ(msg.axes[0],msg.axes[1],msg.axes[3])
			command3.updateCommand()

		if msg.buttons[9]:
			command2.updateXYZ(msg.axes[0],msg.axes[1],msg.axes[3])
			command2.updateCommand()

		if msg.buttons[11]:
			command1.updateXYZ(msg.axes[0],msg.axes[1],msg.axes[3])
			command1.updateCommand()		

	elif nav = 2: 
		# gradient descent

	print command
	command[0:3] = command1.getCommand()
	print command
	command[3:6] = command2.getCommand()
	print command
	command[6:] = command3.getCommand()
	print command
	command_msg = Float32MultiArray(data = command)
	ik_pub.publish(command_msg)


def ik():
	print "Listening to joystick..."
	rospy.init_node('joyinterpreter')
	rospy.Subscriber('/joy', Joy, command_cb)
	rospy.spin()

if __name__ == '__main__':
	command1 = commandClass(1)
	command2 = commandClass(2)
	command3 = commandClass(3)
	ik()
	


