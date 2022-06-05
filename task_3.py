'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 3 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD (now MOE) project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:          NB_1375
# Author List:      Balasurya M
# Filename:         task_3.py
# Functions:        init_setup(rec_client_id), control_logic(center_x,center_y), change_setpoint(new_setpoint)
#                   servoLimit
# Global variables: client_id, setpoint=[]
# 					kp, ki, kd, current_time, last_time, x_err, x_derr, x_last_err, x_err_sum,y_err, y_derr, y_last_err, y_err_sum 


####################### IMPORT MODULES #########################
## You are not allowed to make any changes in this section.   ##
## You have to implement this task with the six available     ##
## modules for this task (numpy,opencv,os,sys,traceback,time) ##
################################################################
import numpy as np
import cv2
import os, sys
import traceback
import time
##############################################################

# Importing the sim module for Remote API connection with CoppeliaSim
try:
	import sim
	
except Exception:
	print('\n[ERROR] It seems the sim.py OR simConst.py files are not found!')
	print('\n[WARNING] Make sure to have following files in the directory:')
	print('sim.py, simConst.py and appropriate library - remoteApi.dll (if on Windows), remoteApi.so (if on Linux) or remoteApi.dylib (if on Mac).\n')
	sys.exit()


# Global variable "client_id" for storing ID of starting the CoppeliaSim Remote connection
# NOTE: DO NOT change the value of this "client_id" variable here
client_id = -1

# Global list "setpoint" for storing target position of ball on the platform/top plate
# The zeroth element stores the x pixel and 1st element stores the y pixel
# NOTE: DO NOT change the value of this "setpoint" list
setpoint = [640,640]

# Global variable "vision_sensor_handle" to store handle for Vision Sensor
# NOTE: DO NOT change the value of this "vision_sensor_handle" variable here
vision_sensor_handle = 0

# You can add your global variables here
##############################################################

# Declaration and Initialization of global variables

global kp, ki, kd
global current_time, last_time
global x_err, x_derr, x_last_err, x_err_sum
global y_err, y_derr, y_last_err, y_err_sum

# PID Parameters
kp, ki, kd = 1.65, 0, 3.6

x_err_sum, y_err_sum = 0, 0
x_last_err, y_last_err = 0, 0
last_time = time.time()
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

# This function is used to limit the rotation of the revolute joint within -90 to +90 degrees

def servoLimit(angle):

	if angle > 1.67: angle = 1.67
	elif angle < -1.67: angle = -1.67

	return angle

##############################################################


def init_setup(rec_client_id):
	"""
	Purpose:
	---
	This function should:
	
	1. Get all the required handles from the CoppeliaSim scene and store them in global variables.
	2. Initialize the vision sensor in 'simx_opmode_streaming' operation mode (if required). 
	   Teams are allowed to choose the appropriate the oeration mode depending on their code and logic.

	Input Arguments:
	---
	`rec_client_id` 	:  [ integer ]
		the client_id generated from start connection remote API in Task 2A, should be stored in a global variable
	
	Returns:
	---
	None
	
	Example call:
	---
	init_setup()
	
	"""
	global client_id, vision_sensor_handle

	# since client_id is defined in task_2a.py file, it needs to be assigned here as well.
	client_id = rec_client_id

	##############	ADD YOUR CODE HERE	##############

	# Declaring and getting the handles of the servos and vision sensors

	global servo_1, servo_2, servo_3, servo_4, vision_sensor_handle

	return_code, servo_1 = sim.simxGetObjectHandle(client_id, 'revolute_joint_fs_1', sim.simx_opmode_blocking)
	return_code, servo_2 = sim.simxGetObjectHandle(client_id, 'revolute_joint_fs_2', sim.simx_opmode_blocking)
	return_code, servo_3 = sim.simxGetObjectHandle(client_id, 'revolute_joint_fs_3', sim.simx_opmode_blocking)
	return_code, servo_4 = sim.simxGetObjectHandle(client_id, 'revolute_joint_fs_4', sim.simx_opmode_blocking)

	return_code, vision_sensor_handle = sim.simxGetObjectHandle(client_id, 'vision_sensor_1', sim.simx_opmode_blocking)
	
	##################################################


def control_logic(center_x,center_y):
	"""
	Purpose:
	---
	This function should implement the control logic to balance the ball at a particular setpoint on the table.

	The orientation of the top table should "ONLY" be controlled by the servo motor as we would expect in a 
	practical scenario.

	Hence "ONLY" the shaft of the servo motor or in other words the revolute joint between servo and servo fin 
	should have 'motor enabled' and 'control loop enabled option' checked. Refer documentation for further understanding of 
	these options.

	This function should use the necessary Legacy Python Remote APIs to control the revolute joints.

	NOTE: In real life, a 180 degree servo motor can rotate between -90 to +90 degrees or -1.57 to 1.57 radians only. 
		  Hence the command to be sent to servo motor should be between this range only. When the top plate is parallel to
		  base plate, the revolute joint between servo and servo fin should be at 0 degrees orientation. Refer documentation
		  for further understanding.

	NOTE: Since the simulation is dynamic in nature there should not by any bottlenecks in this code due to which the 
		  processing may take a lot of time. As a result 'control_logic' function should be called in every iteration of 
		  the while loop. Use global variables instead of reinitialising the variables used in this function.
	
	Input Arguments:
	---
	`center_x` 	:  [ int ]
		the x centroid of the ball
	
	`center_y` 	:  [ int ]
		the y centroid of the ball
	
	Returns:
	---
	None
	
	Example call:
	---
	control_logic(center_x,center_y)
	
	"""
	global setpoint, client_id
	
	##############	ADD YOUR CODE HERE	##############

	# Getting the current time in seconds
	current_time = time.time()

	# Calling the global variables
	global last_time
	global x_last_err, y_last_err
	global x_err_sum, y_err_sum

	# Getting the time difference between last time and current time
	time_diff = current_time - last_time

	# Error is divided into two --> x Error and y Error
	# Here divided by 1280 to normalize the error value between -1 and 1
	x_err = (setpoint[0] - center_x) / 1280
	y_err = (setpoint[1] - center_y) / 1280

	# Adding to the sum for Integral part
	x_err_sum += x_err * time_diff
	y_err_sum += y_err * time_diff

	# Finding the xderr and yderr for Derivative Part
	x_derr = (x_err - x_last_err) / time_diff
	y_derr = (y_err - y_last_err) / time_diff

	# Finding the output value after summing up P, I, D values
	x_output = (kp * x_err) + (ki * x_err_sum) + (kd * x_derr)
	y_output = (kp * y_err) + (ki * y_err_sum) + (kd * y_derr)




	# x --> servos 2, 4
	# y --> servos 1, 3

	# Scaling the output by 1.2 because we initially normalised the value 
	# We use 1.2 instead of 1.74 because to have the output much between around 60 degrees
	# Also, in case of any abnormalities,  we check if the value is between +90 and -90 degrees

	servo2_pos = servoLimit(1.2 * x_output)
	servo4_pos = servoLimit(-1.2 * x_output)
	servo1_pos = servoLimit(1.2 * y_output)
	servo3_pos = servoLimit(-1.2 * y_output)

	# Setting the joint positions
	sim.simxSetJointTargetPosition(client_id, servo_1, servo1_pos, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetPosition(client_id, servo_2, servo2_pos, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetPosition(client_id, servo_3, servo3_pos, sim.simx_opmode_oneshot)
	sim.simxSetJointTargetPosition(client_id, servo_4, servo4_pos, sim.simx_opmode_oneshot)


	last_time = current_time
	x_last_err = x_err
	y_last_err = y_err



	

	##################################################


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    change_setpoint
#        Inputs:    list of new setpoint-
#						new_setpoint=[x_pixel,y_pixel]
#       Outputs:    None
#       Purpose:    The function updates the value of global "setpoint" list after every 15 seconds of simulation time.
#					This will be ONLY called by executable file. 
def change_setpoint(new_setpoint):

	global setpoint
	setpoint=new_setpoint[:]


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function does the following:
# 						- imports 'task_1b' file as module
# 						- imports 'task_1a_part1' file as module
#						- imports 'task_2a' file as module
# 						- calls init_remote_api_server() function in 'task_2a' to connect with CoppeliaSim Remote API server
# 						- then calls start_simulation() function in 'task_2a' to start the simulation
#						- then calls init_setup() function to store the required handles in respective global variables and complete initializations if required
# 						- then calls get_vision_sensor_image() function in 'task_2a' to capture an image from the Vision Sensor in CoppeliaSim scene
# 						- If the return code is 'simx_return_ok':
# 									- then calls transform_vision_sensor_image() function in 'task_2a' to transform the captured image
# 						  			  to a format compatible with OpenCV. 
#			 						- then the transformed image is given as input and Perspective Transform is applied
#			 						  by calling applyPerspectiveTransform function	from 'task_1b'
#			 						- then the output of warped_img is given to 'scan_image' function from 'task_1a_part1'
#			 			- then calls control_logic() function to command the servo motors

# NOTE: Write your solution ONLY in the space provided in the above functions. Main function should not be edited.

if __name__ == "__main__":

	# Import 'task_1b.py' file as module
	try:
		import task_1b

	except ImportError:
		print('\n[ERROR] task_1b.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1b.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_1b.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()
	
	# Import 'task_1a_part1.py' file as module
	try:
		import task_1a_part1

	except ImportError:
		print('\n[ERROR] task_1a_part1.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_1a_part1.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_1a_part1.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()
	
	# Import 'task_2a.py' file as module
	try:
		import task_2a

	except ImportError:
		print('\n[ERROR] task_2a.py file is not present in the current directory.')
		print('Your current directory is: ', os.getcwd())
		print('Make sure task_2a.py is present in this current directory.\n')
		sys.exit()
		
	except Exception as e:
		print('Your task_2a.py throwed an Exception. Kindly debug your code!\n')
		traceback.print_exc(file=sys.stdout)
		sys.exit()

	# Initiate the Remote API connection with CoppeliaSim server
	print('\nConnection to CoppeliaSim Remote API Server initiated.')
	print('Trying to connect to Remote API Server...')

	try:
		client_id = task_2a.init_remote_api_server()

		if (client_id != -1):
			print('\nConnected successfully to Remote API Server in CoppeliaSim!')

			# Starting the Simulation
			try:
				return_code = task_2a.start_simulation()

				if (return_code == sim.simx_return_novalue_flag):
					print('\nSimulation started correctly in CoppeliaSim.')
					
					# Storing the required handles in respective global variables.
					try:
						init_setup(client_id)
					except Exception:
						print('\n[ERROR] Your init_setup() function throwed an Exception. Kindly debug your code!')
						print('Stop the CoppeliaSim simulation manually if started.\n')
						traceback.print_exc(file=sys.stdout)
						print()
						sys.exit()

				else:
					print('\n[ERROR] Failed starting the simulation in CoppeliaSim!')
					print('start_simulation function in task_2a.py is not configured correctly, check the code!')
					print()
					sys.exit()

			except Exception:
				print('\n[ERROR] Your start_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()
		
		else:
			print('\n[ERROR] Failed connecting to Remote API server!')
			print('[WARNING] Make sure the CoppeliaSim software is running and')
			print('[WARNING] Make sure the Port number for Remote API Server is set to 19997.')
			print('[ERROR] OR init_remote_api_server function in task_2a.py is not configured correctly, check the code!')
			print()
			sys.exit()

	except Exception:
		print('\n[ERROR] Your init_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually if started.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
	
	# Initialising the center_x and center_y variable to the current position of the ball
	center_x = 1063
	center_y = 1063
	
	init_simulation_time = 0
	curr_simulation_time = 0

	# Storing time when the simulation started in variable init_simulation_time
	return_code_signal,init_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_streaming)

	if(return_code_signal==0):
		init_simulation_time=float(init_simulation_time_string)

	# Running the coppeliasim simulation for 15 seconds
	while(curr_simulation_time - init_simulation_time <=15):
		
		return_code_signal,curr_simulation_time_string=sim.simxGetStringSignal(client_id,'time',sim.simx_opmode_buffer)
		
		if(return_code_signal == 0):
			curr_simulation_time=float(curr_simulation_time_string)
		
		try:
			vision_sensor_image, image_resolution, return_code = task_2a.get_vision_sensor_image(vision_sensor_handle)

			if ((return_code == sim.simx_return_ok) and (len(image_resolution) == 2) and (len(vision_sensor_image) > 0)):
				# print('\nImage captured from Vision Sensor in CoppeliaSim successfully!')

				# Get the transformed vision sensor image captured in correct format
				try:
					transformed_image = task_2a.transform_vision_sensor_image(vision_sensor_image, image_resolution)

					if (type(transformed_image) is np.ndarray):

						# cv2.imshow('transformed image', transformed_image)
						# cv2.waitKey(0)
						# cv2.destroyAllWindows()

						# Get the resultant warped transformed vision sensor image after applying Perspective Transform
						try:
							warped_img = task_1b.applyPerspectiveTransform(transformed_image)
							
							if (type(warped_img) is np.ndarray):
								
								# Get the 'shapes' dictionary by passing the 'warped_img' to scan_image function
								try:
									shapes = task_1a_part1.scan_image(warped_img)

									if (type(shapes) is dict and shapes!={}):
										print('\nShapes detected by Vision Sensor are: ')
										print(shapes)
										
										# Storing the detected x and y centroid in center_x and center_y variable repectively
										center_x = shapes['Circle'][1]
										center_y = shapes['Circle'][2]

									elif(type(shapes) is not dict):
										print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.')
										print('Stop the CoppeliaSim simulation manually.')
										print()
										sys.exit()
								
								except Exception:
									print('\n[ERROR] Your scan_image function in task_1a_part1.py throwed an Exception. Kindly debug your code!')
									print('Stop the CoppeliaSim simulation manually.\n')
									traceback.print_exc(file=sys.stdout)
									print()
									sys.exit()
							
							else:
								print('\n[ERROR] applyPerspectiveTransform function is not configured correctly, check the code.')
								print('Stop the CoppeliaSim simulation manually.')
								print()
								sys.exit()
						
						except Exception:
							print('\n[ERROR] Your applyPerspectiveTransform function in task_1b.py throwed an Exception. Kindly debug your code!')
							print('Stop the CoppeliaSim simulation manually.\n')
							traceback.print_exc(file=sys.stdout)
							print()
							sys.exit()

					else:
						print('\n[ERROR] transform_vision_sensor_image function in task_2a.py is not configured correctly, check the code.')
						print('Stop the CoppeliaSim simulation manually.')
						print()
						sys.exit()

				except Exception:
					print('\n[ERROR] Your transform_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
					print('Stop the CoppeliaSim simulation manually.\n')
					traceback.print_exc(file=sys.stdout)
					print()
					sys.exit()
			
			try:
				control_logic(center_x,center_y)
			
			except:
				print('\n[ERROR] Your control_logic function throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()

		except Exception:
			print('\n[ERROR] Your get_vision_sensor_image function in task_2a.py throwed an Exception. Kindly debug your code!')
			print('Stop the CoppeliaSim simulation manually.\n')
			traceback.print_exc(file=sys.stdout)
			print()
			sys.exit()

	# Ending the Simulation
	try:
		return_code = task_2a.stop_simulation()
		
		if (return_code == sim.simx_return_novalue_flag):
			print('\nSimulation stopped correctly.')

			# Stop the Remote API connection with CoppeliaSim server
			try:
				task_2a.exit_remote_api_server()

				if (task_2a.start_simulation() == sim.simx_return_initialize_error_flag):
					print('\nDisconnected successfully from Remote API Server in CoppeliaSim!')

				else:
					print('\n[ERROR] Failed disconnecting from Remote API server!')
					print('[ERROR] exit_remote_api_server function in task_2a.py is not configured correctly, check the code!')

			except Exception:
				print('\n[ERROR] Your exit_remote_api_server function in task_2a.py throwed an Exception. Kindly debug your code!')
				print('Stop the CoppeliaSim simulation manually.\n')
				traceback.print_exc(file=sys.stdout)
				print()
				sys.exit()
		
		else:
			print('\n[ERROR] Failed stopping the simulation in CoppeliaSim server!')
			print('[ERROR] stop_simulation function in task_2a.py is not configured correctly, check the code!')
			print('Stop the CoppeliaSim simulation manually.')
		
		print()
		sys.exit()

	except Exception:
		print('\n[ERROR] Your stop_simulation function in task_2a.py throwed an Exception. Kindly debug your code!')
		print('Stop the CoppeliaSim simulation manually.\n')
		traceback.print_exc(file=sys.stdout)
		print()
		sys.exit()
