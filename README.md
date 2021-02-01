# Grip-Combat-Racing-RC-Car
A project to create a radio controlled car inspired by the game GRIP: Combat Racing (and Rollcage) 

### Todo (Grip-RC-Car_L293D-Shield-Prototype):
* Better handling when connection is dropped (Client .py)
* Reduce unnecessary network packets (Client and Server .py)
* Better error/exception handling (Client and Server .py)
* Python scripts: Argparser options, with default values. e,g. --verbose, --serial-device=..., --rc-car-server-host=..., --rc-car-server-port=... etc (Client and Server .py)
* Do more with receivedBytes[2-6] (client .py, server .py and Arduino .ino)
* Implement parity with receivedBytes[7] (Client .py, Server .py and Arduino .ino)
* Replace convertThrottleAndSteeringToWheelSpeed = [...] lookup table with xyz mathematical equation(s)? (Server .py)
* Accelerometer code (Client .py or Arduino .ino)
* Add schematics / build info / documentation
* Reduce latency even more

### Todo (Grip-RC-Car/Direct-Control):

### Todo (Grip-RC-Car/Fly-By-Wire):
