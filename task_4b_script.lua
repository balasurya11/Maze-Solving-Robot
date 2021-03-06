--[[
*****************************************************************************************
*
*        		===============================================
*           		Nirikshak Bot (NB) Theme (eYRC 2020-21)
*        		===============================================
*
*  This Lua script is to implement Task 4B of Nirikshak Bot (NB) Theme (eYRC 2020-21).
*  
*  This software is made available on an "AS IS WHERE IS BASIS".
*  Licensee/end user indemnifies and will keep e-Yantra indemnified from
*  any and all claim(s) that emanate from the use of the Software or 
*  breach of the terms of this agreement.
*  
*  e-Yantra - An MHRD project under National Mission on Education using ICT (NMEICT)
*
*****************************************************************************************
]]--


--[[
# Team ID:			NB_1375
# Author List:		Balasurya M
# Filename:			task_4b_lua
# Functions:        existsIn
# Global variables:	
# 					[ List of global variables defined in this file ]
]]--

--[[
##################### GLOBAL VARIABLES #######################
## You can add global variables in this section according   ##
## to your requirement.                                     ##
## DO NOT TAMPER WITH THE ALREADY DEFINED GLOBAL VARIABLES. ##
##############################################################
]]--

base_children_list={} --Do not change or delete this variable
baseHandle = -1       --Do not change or delete this variable

--############################################################

--[[
##################### HELPER FUNCTIONS #######################
## You can add helper functions in this section according   ##
## to your requirement.                                     ##
## DO NOT MODIFY OR CHANGE THE ALREADY DEFINED HELPER       ##
## FUNCTIONS                                                ##
##############################################################
]]--
function existsIn(wallName, deletedWalls)

    for i = 0, #deletedWalls do
    
        if deletedWalls[i] == wallName then
            return 1
        end
    
    end
    return 0
end

--[[
**************************************************************
  YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION
**************************************************************
	Function Name : createWall()
	Purpose:
	---
	Creates a black-colored wall of dimensions 90cm x 10cm x 10cm

	Input Arguments:
	---
	None
	
	Returns:
	---
	wallObjectHandle : number
	
	returns the object handle of the wall created
	
	Example call:
	---
	wallObjectHandle = createWall()
**************************************************************	
]]--
function createWall()
	wallObjectHandle = sim.createPureShape(0, 8, {0.09, 0.01, 0.1}, 0.0001, nil)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/regularApi/simCreatePureShape.htm to understand the parameters passed to this function
	sim.setShapeColor(wallObjectHandle, nil, sim.colorcomponent_ambient_diffuse, {0, 0, 0})
	sim.setObjectInt32Parameter(wallObjectHandle,sim.shapeintparam_respondable_mask,65280)
	--Refer https://www.coppeliarobotics.com/helpFiles/en/apiFunctions.htm#sim.setObjectInt32Parameter to understand the various parameters passed. 	
	--The walls should only be collidable with the ball and not with each other.
	--Hence we are enabling only the local respondable masks of the walls created.
	sim.setObjectSpecialProperty(wallObjectHandle, sim.objectspecialproperty_collidable)
	--Walls may have to be set as renderable........................... 
	--This is required to make the wall as collidable
	return wallObjectHandle
end

--############################################################

--[[
**************************************************************
	Function Name : receiveData()
	Purpose:
	---
	Receives data via Remote API. This function is called by 
	simx.callScriptFunction() in the python code (task_2b.py)

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	These 4 variables represent the data being passed from remote
	API client(python) to the CoppeliaSim scene
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function receiveData(inInts,inFloats,inStrings,inBuffer)

	--*******************************************************
	--               ADD YOUR CODE HERE
    mazeArray = {}
    
    -- The recieved inInts is in the shape [100,]
    -- Converting back into [10, 10] table and storing in mazeArray
    
    for i = 0, 9 do
    
        temp = {}
        c = i * 10
        for j = 1, 10 do
        
            temp[#temp+1] = inInts[c+j]
        
        end
        mazeArray[#mazeArray+1] = temp
        
    end
	--*******************************************************
	return inInts, inFloats, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : generateHorizontalWalls()
	Purpose:
	---
	Generates all the Horizontal Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateHorizontalWalls()
**************************************************************	
]]--
function generateHorizontalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
     -- Adding Horizontal Walls at desired places
    --baseHandle = sim.getObjectHandle('force_sensor_pw_1')
    pre = 'H_WallSegment_'
    z = 0.375
    ny = 0
    
    for y = -0.45, 0.45, 0.1 do
        
        ny = ny + 1
        nx = 0
        
        for x = -0.5, 0.5, 0.1 do
            
            nx = nx + 1
        
            wallHandle = createWall()
            sim.setObjectPosition(wallHandle, -1, {x, y, z})
            sim.setObjectOrientation(wallHandle, -1, {0, 0, math.pi/2})
            objectName = pre..nx..'x'..ny
            sim.setObjectName(wallHandle, objectName)
            --sim.setObjectParent(wallHandle, baseHandle, false)
        
        end
    
    end
	--*******************************************************
end

--[[
**************************************************************
	Function Name : generateVerticalWalls()
	Purpose:
	---
	Generates all the Vertical Walls in the scene.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	generateVerticalWalls()
**************************************************************	
]]--
function generateVerticalWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
    --Adding and orienting vertical walls accordingly
    --baseHandle = sim.getObjectHandle('force_sensor_pw_1')
    pre = 'V_WallSegment_'
    nx = 0
    z = 0.375
    
    for x = -0.45, 0.45, 0.1 do
        
        nx = nx + 1
        ny = 0
        
        for y = -0.5, 0.5, 0.1 do
            
            ny = ny + 1
        
            wallHandle = createWall()
            sim.setObjectPosition(wallHandle, -1, {x, y, z})
            
            objectName = pre..nx..'x'..ny
            sim.setObjectName(wallHandle, objectName)
            --sim.setObjectParent(wallHandle, baseHandle, false)
        
        end
    
    end

	--*******************************************************
end

--[[
**************************************************************
	Function Name : deleteWalls()
	Purpose:
	---
	Deletes all the grouped walls in the given scene

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	deleteWalls()
**************************************************************	
]]--
function deleteWalls()

	--*******************************************************
	--               ADD YOUR CODE HERE
		local objectHandle = sim.getObjectHandle('walls_1')
        sim.removeObject(objectHandle)
	--*******************************************************
end


--[[
**************************************************************
  YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT PARAMETERS FOR THIS
						  FUNCTION
**************************************************************
	Function Name : createMaze()
	Purpose:
	---
	Creates the maze in the given scene by deleting specific 
	horizontal and vertical walls

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	createMaze()
**************************************************************	
]]--
function createMaze()
	
	--*******************************************************
	--               ADD YOUR CODE HERE
    -- To track the walls deleted while carving the maze
    deletedWalls = {}
    --Iterating through every cell
    for y = 1, 10 do
        
        for x = 1, 10 do
        
            
            --Names of the walls for a given cell X*Y
            westWall = 'V_WallSegment_'..y..'x'..x
            northWall = 'H_WallSegment_'..y..'x'..x
            eastWall = 'V_WallSegment_'..y..'x'..(x+1)
            southWall = 'H_WallSegment_'..(y+1)..'x'..x
            
            
            
            --SOUTH
            
            -- Checking south cell and deleting if an 8 does not exists in its weightage value
            
            if mazeArray[y][x]>= 8 then
                
                mazeArray[y][x] = mazeArray[y][x] - 8
                
            else
                
                exist = existsIn(southWall, deletedWalls)
                
                
                if exist==0 then
                
              
                    southWallHandle = sim.getObjectHandle(southWall)
                    if southWallHandle ~= -1 then
                        return_code = sim.removeObject(southWallHandle)
                        table.insert(deletedWalls, southWall)
                    end
                    
                end
            
            end
            
            -- EAST
            
            -- Checking east cell and deleting if a 4 does not exists in its weightage value            
            if mazeArray[y][x]>=4 then
                
                mazeArray[y][x] = mazeArray[y][x] - 4
                
            else
            
                exist = existsIn(eastWall, deletedWalls)
                
                if exist==0 then
                    
                  
                    eastWallHandle = sim.getObjectHandle(eastWall)
                    if eastWallHandle ~= -1 then
                        return_code = sim.removeObject(eastWallHandle)
                        table.insert(deletedWalls, eastWall)
                    end
                
                end
            end
            
            --NORTH
            
             -- Checking north cell and deleting if a 2 does not exists in its weightage value 
            
            if mazeArray[y][x]>=2 then
                
                mazeArray[y][x] = mazeArray[y][x] - 2
                
            else
                exist = existsIn(northWall, deletedWalls)
                
                if exist==0 then

                    northWallHandle = sim.getObjectHandle(northWall)
                    if northWallHandle ~= -1 then
                        return_code = sim.removeObject(northWallHandle)
                        table.insert(deletedWalls, northWall)
                    end
                    
                end
                
            end
            
            --SOUTH
            
            -- Checking west cell and deleting if a 1 does not exists in its weightage value 
        
            if mazeArray[y][x] >=1 then
                
                mazeArray[y][x] = mazeArray[y][x] - 1
                
            else
            
                exist = existsIn(westWall, deletedWalls)
                
                if exist==0 then

                    westWallHandle = sim.getObjectHandle(westWall)
                    if westWallHandle ~= -1 then
                        return_code = sim.removeObject(westWallHandle)
                        table.insert(deletedWalls, westWall)
                    end
                    
                end
            
            end
        
        
        
        
        
        end
    
    end
        

        
	--*******************************************************
end
--[[
	Function Name : groupWalls()
	Purpose:
	---
	Groups the various walls in the scene to one object.
	The name of the new grouped object should be set as 'walls_1'.

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	groupWalls()
**************************************************************	
]]--

function groupWalls()
	--*******************************************************
	--               ADD YOUR CODE HERE
    local index = 0
    remainingWalls = {}
    
    while true do
    
        local objectHandle = sim.getObjects(index, sim.object_shape_type)

        if objectHandle == -1 then
            break
        end        
        
        local objectName = sim.getObjectName(objectHandle)
        
        local sub = string.sub(objectName, 1, 6)
        
        if sub == 'H_Wall' or sub == 'V_Wall' then

            table.insert(remainingWalls, objectHandle)

        end
        
        index = index + 1
        
    end
    
    wallsGroupHandle = sim.groupShapes(remainingWalls)
    
    sim.setObjectName(wallsGroupHandle, 'walls_1')
    
    local force_sensor_pw_1 = sim.getObjectHandle('force_sensor_pw_1')
    
    sim.setObjectParent(wallsGroupHandle, force_sensor_pw_1, 1)
    
	--*******************************************************
end

--[[
	Function Name : addToCollection()
	Purpose:
	---
	Adds the 'walls_1' grouped object to the collection 'colliding_objects'.  

	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	addToCollection()
**************************************************************	
]]--

function addToCollection()
	--*******************************************************
	--               ADD YOUR CODE HERE
    
    collection_handle = sim.getCollectionHandle('colliding_objects')
    
    sim.addObjectToCollection(collection_handle, wallsGroupHandle, sim.handle_single, 0)
	--*******************************************************
end

--[[
	******************************************************************************
			YOU ARE ALLOWED TO MODIFY THIS FUNCTION DEPENDING ON YOUR PATH. 
	******************************************************************************
	Function Name : drawPath(inInts,path,inStrings,inBuffer)
	Purpose:
	---
	Builds blue coloured lines in the scene according to the
	path generated from the python file. 

	Input Arguments:
	---
	inInts : Table of Ints
	inFloats : Table of Floats (containing the path generated)
	inStrings : Table of Strings
	inBuffer : string
	
	Returns:
	---
	inInts : Table of Ints
	inFloats : Table of Floats
	inStrings : Table of Strings
	inBuffer : string
	
	Example call:
	---
	Shall be called from the python script
**************************************************************	
]]--
function drawPath(inInts,path,inStrings,inBuffer)
	posTable=sim.getObjectPosition(wallsGroupHandle,-1)
	print('=========================================')
	print('Path received is as follows: ')
	print(path)
	if not lineContainer then
		_lineContainer=sim.addDrawingObject(sim.drawing_lines,1,0,wallsGroupHandle,99999,{0.2,0.2,1})
		sim.addDrawingObjectItem(_lineContainer,nil)
		if path then
			local pc=#path/2
			for i=1,pc-1,1 do
				lineDat={path[(i-1)*2+1],path[(i-1)*2+2],posTable[3]-0.03,path[(i)*2+1],path[(i)*2+2],posTable[3]-0.03}
				sim.addDrawingObjectItem(_lineContainer,lineDat)
			end
		end
	end
	return inInts, path, inStrings, inBuffer
end

--[[
**************************************************************
	Function Name : sysCall_init()
	Purpose:
	---
	Can be used for initialization of parameters
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_init()
	--*******************************************************
	--               ADD YOUR CODE HERE

	--*******************************************************
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION.
		YOU CAN DEFINE YOUR OWN INPUT AND OUTPUT 
		PARAMETERS ONLY FOR CREATEMAZE() FUNCTION
**************************************************************
	Function Name : sysCall_beforeSimulation()
	Purpose:
	---
	This is executed before simulation starts
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_beforeSimulation()
	generateHorizontalWalls()
	generateVerticalWalls()
	createMaze()--You can define your own input and output parameters only for this function
    groupWalls()
	addToCollection()
    
end

--[[
**************************************************************
		YOU ARE NOT ALLOWED TO MODIFY THIS FUNCTION. 
**************************************************************
	Function Name : sysCall_afterSimulation()
	Purpose:
	---
	This is executed after simulation ends
	
	Input Arguments:
	---
	None
	
	Returns:
	---
	None
	
	Example call:
	---
	N/A
**************************************************************	
]]--
function sysCall_afterSimulation()
	-- is executed after a simulation ends
	deleteWalls()
    evaluation_screen_respondable=sim.getObjectHandle('evaluation_screen_respondable@silentError')
    if(evaluation_screen_respondable~=-1) then
        sim.removeModel(evaluation_screen_respondable)
    end
end

function sysCall_cleanup()
	-- do some clean-up here
end

-- See the user manual or the available code snippets for additional callback functions and details