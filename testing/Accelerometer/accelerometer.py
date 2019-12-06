import smbus
#add more import statements as necessary

def execute():
	#this function will be called very rapidly
	#if 100 ms have elapsed since the last time this program published data, publish data again (hint - use a global variable to track when you last sent a message)
	#	publish a accelerometer_data.lcm message to the appropriate channel, containing the accelerometer's x, y, and z data (as floats)
	#	use a try-catch block while using the smbus functions, in case the accelerometer is disconnected.
	#		if the catch block is executed it can be assumed the accelerometer is not working. the accelerometer_data message should contain all 0's at that point
	
	
def main():

	lcm_ = lcm.LCM()

	#insert lcm.subscribe statements here to make sure the lcm messages are subscribed to the right channel

	while (True):
		lcm_.handle()
		execute()

	exit()

if __name__ == "__main__":
	main()