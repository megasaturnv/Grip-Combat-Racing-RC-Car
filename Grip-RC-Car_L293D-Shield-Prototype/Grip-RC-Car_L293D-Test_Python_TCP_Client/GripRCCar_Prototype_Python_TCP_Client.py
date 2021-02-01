#!/usr/bin/python3

###########
# Imports #
###########
import argparse, math, serial, socket, sys, time


#############
# Functions #
#############
def serialReceive(serialPort):
	print(serialPort.inWaiting())
	#receivedMessage = serialPort.readline()
	receivedMessage = serialPort.readline().strip()
	#receivedMessage = bytearray(receivedMessage).decode('utf-8')
	return receivedMessage


#################
# Main Function #
#################
def main():
	print()

	###################
	# Parse Arguments #
	###################
	parser = argparse.ArgumentParser(description='description')

	parser.add_argument('-v', '--verbose', help='Be Verbose and print debug output')

	args = parser.parse_args()

	if args.verbose:
		print('Argument verbose: ' + str(args.verbose))


	############
	# Settings #
	############
	SERIAL_DEVICE      = '/dev/ttyACM0' # Location of the serial device
	SERIAL_BAUD_RATE   = 9600           # Baud rate
	SERIAL_TIMEOUT     = 30             # Serial port timeout time
	SERIAL_RATE        = 5              # In Hz, how many times per second to send commands to the Arduino

	FPS_TICK           = 30

	RC_CAR_SERVER_HOST = 'megasaturnv-pc.lan' # The host to connect to
	RC_CAR_SERVER_PORT = 47524                # The port to connect to


	#################################
	# Variable setup & Calculations #
	#################################
	serialRateInterval = 1/SERIAL_RATE

	port = serial.Serial(SERIAL_DEVICE, baudrate=SERIAL_BAUD_RATE, timeout=SERIAL_TIMEOUT)
	time.sleep(3)
	port.flushInput()
	port.flushOutput()

	# Create a TCP/IP socket
	sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
	sock.connect((RC_CAR_SERVER_HOST, RC_CAR_SERVER_PORT))


	###############
	# Car control #
	###############	
	startTime = time.time()
	running = True
	while running:
		if startTime + serialRateInterval < time.time():
			startTime = time.time()

			port.write(sock.recv(8))

		while port.inWaiting() > 0: #Collect data
			responseString = serialReceive(port)
			print(responseString)

		time.sleep(0.1)

	sock.close()


#############################
# if __name__ == '__main__' #
#############################
if __name__ == '__main__':
	main()

#	try:
#		main()
#	except Exception as e:
#		...

