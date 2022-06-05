'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
'''

# Team ID:			NB_1375
# Author List:		Balasurya M, Harshavarthan V, Kabilan V, Balaji S
# Filename:			task_1b.py
# Functions:		applyPerspectiveTransform, detectMaze, writeToCsv
# 					getBlockValue
# Global variables:	
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, csv)               ##
##############################################################
import numpy as np
import cv2
import csv
##############################################################


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################

def getBlockValue(img, point): 

	# This function is to get the value of a single block in the maze
	# By getting the ROI of the desired cell
	# The side of single square block is 128 (1280/10)
	size = 128
	
	# Point - The cell number ranging from (0,0) to (9,9)
	x0, y0 = point
	
	# Bottom-right co-ordinates of the cell
	x = int(size*(x0+1))
	y = int(size*(y0+1))
	
	# Top-left co-ordinates of the cell
	height = int(size*x0)
	width = int(size*y0)
	
	# Aquiring the ROI through slicing
	sliced = img[height:x,width:y]

	# Normalizing the block
	sliced = sliced / 255
	
	# Calculating the corresponding values
	# By getting the pixel value at the mid of the square lines

	west = sliced[int(size/2),0] *1
	
	north = sliced[0,int(size/2)] * 2
	
	east = sliced[int(size/2),int(size-1)] *4
	
	south = sliced[int(size-1),int(size/2)] * 8

	#Adding them up and returning the final value of the single block
	value = west + north + east + south
	
	return int(value)


##############################################################


def applyPerspectiveTransform(input_img):

	"""
	Purpose:
	---
	takes a maze test case image as input and applies a Perspective Transfrom on it to isolate the maze

	Input Arguments:
	---
	`input_img` :   [ numpy array ]
		maze image in the form of a numpy array
	
	Returns:
	---
	`warped_img` :  [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Example call:
	---
	warped_img = applyPerspectiveTransform(input_img)
	"""

	warped_img = None

	##############	ADD YOUR CODE HERE	##############

	# Converting to Grayscale
	try:
		gray = cv2.cvtColor(input_img, cv2.COLOR_BGR2GRAY)
	except:
		gray = input_img

	ret, otsu = cv2.threshold(gray,0,255,cv2.THRESH_BINARY+cv2.THRESH_OTSU)

	# Finding contours in the maze image
	contours, _ = cv2.findContours(otsu, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

	# We get the second contour because,
	# the first one corresponds to the border of the image
	# the second largest contour would be the borders of the maze
	approx_borders = []

	for cnt in contours:
		approx = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
		approx_borders.append(approx)

	border = np.array([[110, 110], [110, 910], [915, 915], [915, 110]])

	for approx_cnt in approx_borders:


		if approx_cnt[0][0][0] == 0 and approx_cnt[0][0][1] == 0:
			pass

		elif len(approx_cnt) == 4 and cv2.contourArea(approx_cnt) > 1e5:  
			border = approx_cnt
			
	# Reshaped (4,1,2) to (4,2) for understanding
	pts1 = border.reshape((4,2))

	# Sorting the 4 coordinates to
	# Top-left, top-right, bottom-left, botton-right
	pts1 = np.float32(pts1)
	pts1 = pts1.tolist()
	pts1 = sorted(pts1, key = lambda x: x[0])
	pts1[:2] = sorted(pts1[:2], key = lambda  x: x[1])
	pts1[-2:] = sorted(pts1[-2:], key = lambda  x: x[1])
	pts1 = np.float32(pts1)

	# Desired shape	
	pts2 = np.float32([[0,0],  [0,1280], [1280,0], [1280,1280]])

	#Applying transform
	M = cv2.getPerspectiveTransform(pts1,pts2)
	warped_img = cv2.warpPerspective(input_img, M, (1280, 1280))	

	##################################################

	return warped_img


def detectMaze(warped_img):

	"""
	Purpose:
	---
	takes the warped maze image as input and returns the maze encoded in form of a 2D array

	Input Arguments:
	---
	`warped_img` :    [ numpy array ]
		resultant warped maze image after applying Perspective Transform
	
	Returns:
	---
	`maze_array` :    [ nested list of lists ]
		encoded maze in the form of a 2D array

	Example call:
	---
	maze_array = detectMaze(warped_img)
	"""

	maze_array = []

	##############	ADD YOUR CODE HERE	##############
	
	# Converting to grayscale
	gray = cv2.cvtColor(warped_img, cv2.COLOR_BGR2GRAY)
	cv2.rectangle(gray, (0,0), (1279,1279), 0, 10)
	
	#Applying threshold
	_, thresh = cv2.threshold(gray, 40, 255, cv2.THRESH_BINARY_INV)
	
	# Dilating the thresholded image to enhance the blocks and make it easy to find values
	kernel = np.ones((5,5),np.uint8)
	dilated = cv2.dilate(thresh,kernel,iterations = 4)   

	# Iterate through each block and appending the value to maze_array
	for i in range (10):
		maze_array.append([])
		
		for j in range(10):
			
			N = (i,j)
			value = getBlockValue(dilated, N)
			maze_array[i].append(value)

	##################################################

	return maze_array


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
def writeToCsv(csv_file_path, maze_array):

	"""
	Purpose:
	---
	takes the encoded maze array and csv file name as input and writes the encoded maze array to the csv file

	Input Arguments:
	---
	`csv_file_path` :	[ str ]
		file path with name for csv file to write
	
	`maze_array` :		[ nested list of lists ]
		encoded maze in the form of a 2D array
	
	Example call:
	---
	warped_img = writeToCsv('test_cases/maze00.csv', maze_array)
	"""

	with open(csv_file_path, 'w', newline='') as file:
		writer = csv.writer(file)
		writer.writerows(maze_array)


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    This part of the code is only for testing your solution. The function first takes 'maze00.jpg'
# 					as input, applies Perspective Transform by calling applyPerspectiveTransform function,
# 					encodes the maze input in form of 2D array by calling detectMaze function and writes this data to csv file
# 					by calling writeToCsv function, it then asks the user whether to repeat the same on all maze images
# 					present in 'test_cases' folder or not. Write your solution ONLY in the space provided in the above
# 					applyPerspectiveTransform and detectMaze functions.

if __name__ == "__main__":

	# path directory of images in 'test_cases' folder
	img_dir_path = 'test_cases/'

	# path to 'maze00.jpg' image file
	file_num = 0
	img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

	print('\n============================================')
	print('\nFor maze0' + str(file_num) + '.jpg')

	# path for 'maze00.csv' output file
	csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
	
	# read the 'maze00.jpg' image file
	input_img = cv2.imread(img_file_path)

	# get the resultant warped maze image after applying Perspective Transform
	warped_img = applyPerspectiveTransform(input_img)

	if type(warped_img) is np.ndarray:

		# get the encoded maze in the form of a 2D array
		maze_array = detectMaze(warped_img)

		if (type(maze_array) is list) and (len(maze_array) == 10):

			print('\nEncoded Maze Array = %s' % (maze_array))
			print('\n============================================')
			
			# writes the encoded maze array to the csv file
			writeToCsv(csv_file_path, maze_array)

			cv2.imshow('warped_img_0' + str(file_num), warped_img)
			cv2.waitKey(0)
			cv2.destroyAllWindows()
		
		else:

			print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
			exit()
	
	else:

		print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
		exit()
	
	choice = input('\nDo you want to run your script on all maze images ? => "y" or "n": ')

	if choice == 'y':

		for file_num in range(1, 10):
			
			# path to image file
			img_file_path = img_dir_path + 'maze0' + str(file_num) + '.jpg'

			print('\n============================================')
			print('\nFor maze0' + str(file_num) + '.jpg')

			# path for csv output file
			csv_file_path = img_dir_path + 'maze0' + str(file_num) + '.csv'
			
			# read the image file
			input_img = cv2.imread(img_file_path)

			# get the resultant warped maze image after applying Perspective Transform
			warped_img = applyPerspectiveTransform(input_img)

			if type(warped_img) is np.ndarray:

				# get the encoded maze in the form of a 2D array
				maze_array = detectMaze(warped_img)

				if (type(maze_array) is list) and (len(maze_array) == 10):

					print('\nEncoded Maze Array = %s' % (maze_array))
					print('\n============================================')
					
					# writes the encoded maze array to the csv file
					writeToCsv(csv_file_path, maze_array)

					cv2.imshow('warped_img_0' + str(file_num), warped_img)
					cv2.waitKey(0)
					cv2.destroyAllWindows()
				
				else:

					print('\n[ERROR] maze_array returned by detectMaze function is not complete. Check the function in code.\n')
					exit()
			
			else:

				print('\n[ERROR] applyPerspectiveTransform function is not returning the warped maze image in expected format! Check the function in code.\n')
				exit()

	else:

		print('')

