from controller import Robot
from controller import GPS
from Algorithms.GoToTarget import GoToTarget
import json
import math

class Simulation:
    DEVICE_TYPES = ['HingeJoint', 'Compass', 'GPS']
    SENSOR_TYPES = ['Compass', 'GPS']
    SERVO_TYPES = ['HingeJoint']
        
    def __init__(self, robot, devices_file, algorithm):
        self.robot = robot
        self.devices_file = devices_file
        self.algorithm = algorithm
        
    def make_devices(self):
        f = open(self.devices_file)
        devices_dict = json.load(f)

        
        self.devices = {}
        for i in devices_dict['Children']:
            if i['NodeType'] in Simulation.DEVICE_TYPES:
                self.devices[i['name']] = {'device': self.robot.getDevice(i['name']), 'type' : i['NodeType']}
            
            if i['NodeType'] in Simulation.SERVO_TYPES:
                self.devices[i['name']]['device'].setPosition(float('inf'))
                self.devices[i['name']]['device'].setVelocity(0.0)
            
            if i['NodeType'] in Simulation.SENSOR_TYPES:
                self.devices[i['name']]['device'].enable(1)
        
    def set_values(self):
        for i, j in self.devices.items():
            if j['type'] in Simulation.SENSOR_TYPES:
                j['value'] = j['device'].getValues()

    def run_algorithm(self):
        self.algorithm.set_actions(self.devices)
        
    def set_actions(self):
        for i, j in self.devices.items():
            if j['type'] in Simulation.SERVO_TYPES:
                j['device'].setVelocity(j['action'])
    
    def run_simulation(self):
        self.set_values()
        self.run_algorithm()
        self.set_actions()

            
    
# initiate
TIME_STEP = 64

robot = Robot()
algorithm = GoToTarget('Globe_GPS', 'Compass', 'paperbot_left_drive_servo_h', 'paperbot_right_drive_servo_h')
simulation = Simulation(robot, 'graph-model.json', algorithm)
simulation.make_devices()


while robot.step(TIME_STEP) != -1:
    simulation.run_simulation()
