from robolink import *       # import the robolink library (bridge with RoboDK)
RDK = Robolink()                    # establish a link with the simulator
robot = RDK.Item('test')           # retrieve the robot
print(robot.Joints().list())
robot.MoveJ([0,0,0,90])      # set all robot axes to zero