#!/usr/bin/python3

###########
# Imports #
###########
import argparse, math, pygame, socket, sys, time


#############
# Functions #
#############
def convertAxisTo127(axisValueArg): # For axisValues -1.0 to 1.0, returns 0-127
	axisValue = round(axisValueArg, 2)
	return int(round(((axisValue + 1) / 2) * 127, 0))

def convertTo255(valueArg): # For valueArg = -1.0 to 1.0, returns 1-255
	if valueArg > 0:
		returnValue = ((valueArg + 1) * 128) - 1
	elif valueArg < 0:
		returnValue = ((valueArg + 1) * 128) + 1
	else:
		returnValue = 128

	return int(round(returnValue,0))

def convertThrottleAndSteeringToWheelSpeed(wheelSideArg, throttleArg, steeringArg): # For throttleArg and steeringArg = -1.0 to 1.0, returns -1.0 to 1.0 based on lookup table for left wheels
	wheelSpeedLookupTable = [
[-1,   -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,    -1,   -0.95, -0.9,  -0.85, -0.8,  -0.75, -0.7,  -0.65, -0.6, -0.55, -0.5],
[-1,   -0.99, -0.98, -0.97, -0.96, -0.95, -0.94, -0.93, -0.92, -0.91, -0.9, -0.85, -0.8,  -0.75, -0.7,  -0.65, -0.6,  -0.55, -0.5, -0.45, -0.4],
[-1,   -0.98, -0.96, -0.94, -0.92, -0.9,  -0.88, -0.86, -0.84, -0.82, -0.8, -0.75, -0.7,  -0.65, -0.6,  -0.55, -0.5,  -0.45, -0.4, -0.35, -0.3],
[-1,   -0.97, -0.94, -0.91, -0.88, -0.85, -0.82, -0.79, -0.76, -0.73, -0.7, -0.65, -0.6,  -0.55, -0.5,  -0.45, -0.4,  -0.35, -0.3, -0.25, -0.2],
[-1,   -0.96, -0.92, -0.88, -0.84, -0.8,  -0.76, -0.72, -0.68, -0.64, -0.6, -0.55, -0.5,  -0.45, -0.4,  -0.35, -0.3,  -0.25, -0.2, -0.15, -0.1],
[-1,   -0.95, -0.9,  -0.85, -0.8,  -0.75, -0.7,  -0.65, -0.6,  -0.55, -0.5, -0.45, -0.4,  -0.35, -0.3,  -0.25, -0.2,  -0.15, -0.1, -0.05, 0   ],
[-1,   -0.94, -0.88, -0.82, -0.76, -0.7,  -0.64, -0.58, -0.52, -0.46, -0.4, -0.34, -0.28, -0.22, -0.16, -0.1,  -0.04, 0.02,  0.08, 0.14,  0.2 ],
[-1,   -0.93, -0.86, -0.79, -0.72, -0.65, -0.58, -0.51, -0.44, -0.37, -0.3, -0.23, -0.16, -0.09, -0.02, 0.05,  0.12,  0.19,  0.26, 0.33,  0.4 ],
[-1,   -0.92, -0.84, -0.76, -0.68, -0.6,  -0.52, -0.44, -0.36, -0.28, -0.2, -0.12, -0.04, 0.04,  0.12,  0.2,   0.28,  0.36,  0.44, 0.52,  0.6 ],
[-1,   -0.91, -0.82, -0.73, -0.64, -0.55, -0.46, -0.37, -0.28, -0.19, -0.1, -0.01, 0.08,  0.17,  0.26,  0.35,  0.44,  0.53,  0.62, 0.71,  0.8 ],
[-1,   -0.9,  -0.8,  -0.7,  -0.6,  -0.5,  -0.4,  -0.3,  -0.2,  -0.1,  0,    0.1,   0.2,   0.3,  0.4,    0.5,   0.6,   0.7,   0.8,  0.9,   1   ],
[-0.8, -0.71, -0.62, -0.53, -0.44, -0.35, -0.26, -0.17, -0.08, 0.01,  0.1,  0.19,  0.28,  0.37, 0.46,   0.55,  0.64,  0.73,  0.82, 0.91,  1   ],
[-0.6, -0.52, -0.44, -0.36, -0.28, -0.2,  -0.12, -0.04, 0.04,  0.12,  0.2,  0.28,  0.36,  0.44, 0.52,   0.6,   0.68,  0.76,  0.84, 0.92,  1   ],
[-0.4, -0.33, -0.26, -0.19, -0.12, -0.05, 0.02,  0.09,  0.16,  0.23,  0.3,  0.37,  0.44,  0.51, 0.58,   0.65,  0.72,  0.79,  0.86, 0.93,  1   ],
[-0.2, -0.14, -0.08, -0.02, 0.04,  0.1,   0.16,  0.22,  0.28,  0.34,  0.4,  0.46,  0.52,  0.58, 0.64,   0.7,   0.76,  0.82,  0.88, 0.94,  1   ],
[0,    0.05,  0.1,   0.15,  0.2,   0.25,  0.3,   0.35,  0.4,   0.45,  0.5,  0.55,  0.6,   0.65, 0.7,    0.75,  0.8,   0.85,  0.9,  0.95,  1   ],
[0.1,  0.15,  0.2,   0.25,  0.3,   0.35,  0.4,   0.45,  0.5,   0.55,  0.6,  0.64,  0.68,  0.72, 0.76,   0.8,   0.84,  0.88,  0.92, 0.96,  1   ],
[0.2,  0.25,  0.3,   0.35,  0.4,   0.45,  0.5,   0.55,  0.6,   0.65,  0.7,  0.73,  0.76,  0.79, 0.82,   0.85,  0.88,  0.91,  0.94, 0.97,  1   ],
[0.3,  0.35,  0.4,   0.45,  0.5,   0.55,  0.6,   0.65,  0.7,   0.75,  0.8,  0.82,  0.84,  0.86, 0.88,   0.9,   0.92,  0.94,  0.96, 0.98,  1   ],
[0.4,  0.45,  0.5,   0.55,  0.6,   0.65,  0.7,   0.75,  0.8,   0.85,  0.9,  0.91,  0.92,  0.93, 0.94,   0.95,  0.96,  0.97,  0.98, 0.99,  1   ],
[0.5,  0.55,  0.6,   0.65,  0.7,   0.75,  0.8,   0.85,  0.9,   0.95,  1,    1,     1,     1,    1,      1,     1,     1,     1,    1,     1   ]
]

	throttleIndex = int(round((throttleArg + 1) * 10, 0))
	steeringIndex = 10

	if wheelSideArg.lower() == 'left':
		steeringIndex = int(round((steeringArg + 1) * 10, 0)) # By default the table above is for the left track
	elif wheelSideArg.lower() == 'right':
		steeringIndex = int(round((-steeringArg + 1) * 10, 0)) # To get values for the right track, we flip the table in the steering or 'y' axis by inverting steeringArg
	else:
		print('Unknown side specified in convertThrottleAndSteeringToWheelSpeed(). Speed set to 0 for safety')
		throttleIndex = 10

	print('wheelSideArg:  ' + wheelSideArg)
	print('throttleIndex: ' + str(throttleIndex))
	print('steeringIndex: ' + str(steeringIndex))

	return wheelSpeedLookupTable[throttleIndex][steeringIndex]


#################
# Main Function #
#################
def main():
	print()
	print()


	###################
	# Parse Arguments #
	###################
	parser = argparse.ArgumentParser(description='description')

	parser.add_argument('-v', '--verbose', help='Be Verbose and print debug output')

	args = parser.parse_args()

	if args.verbose:
		print('Argument verbose: %s' % args.verbose)


	############
	# Settings #
	############
	PACKET_RATE        = 5 # In Hz, how many times per second to send commands to the client

	FPS_TICK           = 30

	RC_CAR_SERVER_HOST = 'megasaturnv-pc.lan' # The host to connect to
	RC_CAR_SERVER_PORT = 47524                # The port to open

	STEERING_DEADZONE  = 0.2 # Steering deadzone. 0.0 to 1.0. 0.0 = no deadzone. 1.0 = all deadzone, so no steering will be interpreted
	THROTTLE_DEADZONE  = 0.2 # Throttle deadzone. 0.0 to 1.0. 0.0 = no deadzone. 1.0 = all deadzone, so no throttle will be interpreted


	#################################
	# Variable Setup & Calculations #
	#################################
	packetRateInterval = 1/PACKET_RATE
	
	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.bind((RC_CAR_SERVER_HOST, RC_CAR_SERVER_PORT))
	sock.listen()


	###############
	# Pygame Init #
	###############
	pygame.init()
	pygame.joystick.init()
	clock = pygame.time.Clock()

	joystick = []

	print('Number of joysticks: ' + str(pygame.joystick.get_count()))
	for i in range(pygame.joystick.get_count()):
		joystick.append(pygame.joystick.Joystick(i)) # Create joystick object(s)
		joystick[i].init() # Initialize joystick
		print('Detected joystick ' + str(i) + ': ' + str(joystick[i].get_name())) # Print a statement telling what the name of the controller is


	###############
	# Car control #
	###############	
	print('Waiting for a connection')
	connection, client_address = sock.accept()
	print('Connection made by: ' + str(client_address))

	try:
		startTime = time.time()
		running = True
		while running:

			for event in pygame.event.get():
				if event.type == pygame.QUIT:
					running = False
					pygame.quit()

				# Possible joystick actions: JOYAXISMOTION JOYBALLMOTION JOYBUTTONDOWN JOYBUTTONUP JOYHATMOTION
				#if event.type == pygame.JOYBUTTONDOWN:
				#	print('Joystick button pressed.')
				#if event.type == pygame.JOYBUTTONUP:
				#	print('Joystick button released.')

			if joystick[0].get_button(7) == 1: # Start button
				running = False
				pygame.quit()

			if startTime + packetRateInterval < time.time():
				startTime = time.time()

				# Axis 0 = Steering. -1 = left, 0 = centre, 1 = right
				# Axis 2 = Reverse.  -1 = raised, 1 = depressed
				# Axis 5 = Forward.  -1 = raised, 1 = depressed

				# z = (0.5*x) + (-0.5*y), where x = fw, y = rev, z = throttle
				throttle = (0.5 * joystick[0].get_axis(5)) + (-0.5 * joystick[0].get_axis(2))

				steering = joystick[0].get_axis(0)

				if abs(throttle) < THROTTLE_DEADZONE:
					throttle = 0
				if abs(steering) < STEERING_DEADZONE:
					steering = 0

				print('Throttle: ' + str(throttle))
				print('Steering: ' + str(steering))

				leftWheels = convertTo255(convertThrottleAndSteeringToWheelSpeed('left',throttle, steering))
				rightWheels = convertTo255(convertThrottleAndSteeringToWheelSpeed('right', throttle, steering))

				serialValList = [leftWheels,rightWheels,0,0,0,0,0,0]

				try:
					print(serialValList)
					connection.sendall(bytearray(serialValList))
				except socket.error:
					print('Socket.error')

			pygame.time.Clock().tick(FPS_TICK)
	
	finally:
		connection.close()


#############################
# if __name__ == '__main__' #
#############################
if __name__ == '__main__':
	main()

#	try:
#		main()
#	except Exception as e:
#		...

