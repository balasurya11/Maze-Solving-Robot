'''
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This script is to implement Task 1A - Part 1 of Nirikshak Bot (NB) Theme (eYRC 2020-21).
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
# Filename:			task_1a_part1.py
# Functions:		scan_image
# 					findSlope, fourSides
# Global variables:	shapes
# 					


####################### IMPORT MODULES #######################
## You are not allowed to make any changes in this section. ##
## You have to implement this task with the three available ##
## modules for this task (numpy, opencv, os)                ##
##############################################################
import cv2
import numpy as np
import os
##############################################################


# Global variable for details of shapes found in image and will be put in this dictionary, returned from scan_image function
shapes = {}


################# ADD UTILITY FUNCTIONS HERE #################
## You can define any utility functions for your code.      ##
## Please add proper comments to ensure that your code is   ##
## readable and easy to understand.                         ##
##############################################################
    
def findSlope(P1, P2):

	# This function is used to find the slope of the line given the two coordinates, 
	# P1(x1 ,y1), P2(x2, y2)
    
    x1, y1 = P1
    x2, y2 = P2

    return (y2-y1)/(x2-x1)


def fourSides(coord):

	# This function classifies the given four sided figure into
	# Square/ Rhombus/ Parallelogram/ Trapezium/ Quadrilateral
	# The return value is the string of the above shapes

	# First we find the length of the 4 sides
    s1 = int(np.linalg.norm(coord[0]-coord[1]))
    s2 = int(np.linalg.norm(coord[1]-coord[2]))
    s3 = int(np.linalg.norm(coord[2]-coord[3]))
    s4 = int(np.linalg.norm(coord[3]-coord[0]))

    # Then, we find the diagonal lengths
    d1 = int(np.linalg.norm(coord[0]-coord[2]))
    d2 = int(np.linalg.norm(coord[1]-coord[3]))

    # We then find the difference between the diagonals
    diag_diff = round(d1-d2)

    # We find the difference between the sides this way because, it will be easy to classify a Square or a Rhombus
    sides_diff = round((s1+s3) - (s2+s4))

    # If the sides difference is zero, the figure either a Square or a Rhombus
    # We give a tolerance range of +/- 2, because of inaccuracy in computing raw Pixel values
    if sides_diff in range(-2, 2):

    	# If the diagonal difference is also zero, it is a Square, else it is a Rhombus
        if diag_diff in range(-2, 2):
            return 'Square'

        return 'Rhombus'

    # If all the sides are not equal, the figure is either a Parallelogram or a Trapezium or a Quadrilateral
    else:

    	# We find the find the slopes of all four sides
        slope1 = findSlope(coord[0], coord[1])
        slope2 = findSlope(coord[1], coord[2])
        slope3 = findSlope(coord[2], coord[3])
        slope4 = findSlope(coord[3], coord[0])

        # If one pair of opposite sides are parallel, then their diff in slopes is zero
        if round(slope1-slope3) in range(-2, 2):

        	# If the other pair is also parallel, it is a parallelogram
            if round(slope2-slope4) in range(-2, 2):
                return 'Parallelogram'

            # Else, i.e, Only one pair is parallel, it is a trapezium
            else:
                return 'Trapezium'

        # Another condtion for Trapezium
        elif round(slope2-slope4) in range(-2, 2):
            return 'Trapezium'

        # If none of these condtions are satisfied, it is a Quadrilateral
        return 'Quadrilateral'





##############################################################


def scan_image(img):

    """
    Purpose:
    ---
    this function takes image as an argument and returns dictionary
    containing details of colored (non-white) shapes in that image

    Input Arguments:
    ---
    `img` :		[ numpy array ]
        file path of image

    Returns:
    ---
    `shapes` :              [ dictionary ]
        details of colored (non-white) shapes present in image at img_file_path
        { 'Shape' : ['color', Area, cX, cY] }
    
    Example call:
    ---
    shapes = scan_image(img)
    """

    global shapes

    ##############	ADD YOUR CODE HERE	############## 

    shapes = {}
    

    # Converting the image into GrayScale
    #gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    gray = img

    # Applying threshold to convert it into a binary image
    _, thresh = cv2.threshold(gray, 240, 255, cv2.THRESH_BINARY)

    # Find contours in the threshold images
    contours, _ = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)

    # The first contour is omitted because the Border of the images is detected as a contour
    contours = contours[1:]


    # We approximate the detected contours, so that we get the minimal coordinates to represent a shape
    coordinates = []
    for cnt in contours:
        coord = cv2.approxPolyDP(cnt, 0.01*cv2.arcLength(cnt, True), True)
        coordinates.append(coord)

    out = []

    # For every detected contour, we perform following steps
    for i in range(len(contours)):

    	# We find the moments and use that to find the centroid and area of the shapes
        m = cv2.moments(contours[i])
        centroid_x = int(m["m10"] / m["m00"])
        centroid_y = int(m["m01"] / m["m00"])

        # To find the color of the contour, we find the b,g,r values at the centroid of the shape and find the colour
        '''
        b, g, r = img[centroid_y, centroid_x]
        col = max(b, g, r)
        if col == b: color = 'blue'
        elif col == g: color = 'green'
        else: color = 'red'
        '''
        # We find the number of sides by the approximated coordinates
        numberOfSides = len(coordinates[i])

        if numberOfSides == 3:
            shape = 'Triangle'

        # If the number of sides is 4, we call our helper function to classify it
        elif numberOfSides == 4:
            shape = fourSides(coordinates[i].reshape(-1, 2))

        elif numberOfSides == 5:
            shape = 'Pentagon'

        elif numberOfSides == 6:
            shape = 'Hexagon'

        else:
            shape = 'Circle'

        color = 'None'
        # We then create a temporary list to hold all the respective values
        value = [shape, color, centroid_x, centroid_y]

        out.append(value)



    # Appending the values to dictionary, inorder of color
    out.sort(key = lambda x: x[1])

    # Writing the output accordingly
    temp = []

    if len(out) == 1:

    	if out[0][0] == 'Circle':

    		temp = out[0][1:]

    else:

    	for item in out:

    		if item[0] == 'Circle':

    			temp.append(item[1:])

    shapes['Circle'] = temp

	##################################################
    
    return shapes


# NOTE:	YOU ARE NOT ALLOWED TO MAKE ANY CHANGE TO THIS FUNCTION
# 
# Function Name:    main
#        Inputs:    None
#       Outputs:    None
#       Purpose:    the function first takes 'Sample1.png' as input and runs scan_image function to find details
#                   of colored (non-white) shapes present in 'Sample1.png', it then asks the user whether
#                   to repeat the same on all images present in 'Samples' folder or not

if __name__ == '__main__':

    curr_dir_path = os.getcwd()
    print('Currently working in '+ curr_dir_path)

    # path directory of images in 'Samples' folder
    img_dir_path = curr_dir_path + '/Samples/'
    
    # path to 'Sample1.png' image file
    file_num = 1
    img_file_path = img_dir_path + 'Sample' + str(file_num) + '.png'

    print('\n============================================')
    print('\nLooking for Sample' + str(file_num) + '.png')

    if os.path.exists('Samples/Sample' + str(file_num) + '.png'):
        print('\nFound Sample' + str(file_num) + '.png')
    
    else:
        print('\n[ERROR] Sample' + str(file_num) + '.png not found. Make sure "Samples" folder has the selected file.')
        exit()
    
    print('\n============================================')

    try:
        print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
        shapes = scan_image(img_file_path)

        if type(shapes) is dict:
            print(shapes)
            print('\nOutput generated. Please verify.')
        
        else:
            print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
            exit()

    except Exception:
        print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
        exit()

    print('\n============================================')

    choice = input('\nWant to run your script on all the images in Samples folder ? ==>> "y" or "n": ')

    if choice == 'y':

        file_count = 2
        
        for file_num in range(file_count):

            # path to image file
            img_file_path = img_dir_path + 'Sample' + str(file_num + 1) + '.png'

            print('\n============================================')
            print('\nLooking for Sample' + str(file_num + 1) + '.png')

            if os.path.exists('Samples/Sample' + str(file_num + 1) + '.png'):
                print('\nFound Sample' + str(file_num + 1) + '.png')
            
            else:
                print('\n[ERROR] Sample' + str(file_num + 1) + '.png not found. Make sure "Samples" folder has the selected file.')
                exit()
            
            print('\n============================================')

            try:
                print('\nRunning scan_image function with ' + img_file_path + ' as an argument')
                shapes = scan_image(img_file_path)

                if type(shapes) is dict:
                    print(shapes)
                    print('\nOutput generated. Please verify.')
                
                else:
                    print('\n[ERROR] scan_image function returned a ' + str(type(shapes)) + ' instead of a dictionary.\n')
                    exit()

            except Exception:
                print('\n[ERROR] scan_image function is throwing an error. Please debug scan_image function')
                exit()

            print('\n============================================')

    else:
        print('')
