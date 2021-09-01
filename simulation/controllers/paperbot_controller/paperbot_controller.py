from controller import Robot
from controller import GPS
import math
import json

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

class Algorithm:
    def __init__(self):
        self.gps_name = 'Globe_GPS'
        self.compass_name = 'Compass'
        self.left_servo_name = 'paperbot_left_drive_servo_h'
        self.right_servo_name = 'paperbot_right_drive_servo_h'
    
    def set_actions(self, devices):
        
        target_location = [0, 0.8]  # in 2D
        target_location_x = target_location[0]
        target_location_y = target_location[1]
        
        L = 0.097
        R = 0.04
        
        x_old = 0
        y_old = -0.072
        e_old = 0
        dist_old = 0

        P_phi = 0.55
        D_phi = 0.05
        P_dist = 0.075
        D_dist = 0.05

        x_current = []
        y_current = []
        
        xyz_current = devices[self.gps_name]['value']
        x_current = xyz_current[0]
        y_current = xyz_current[2]
        
        compass_value = devices[self.compass_name]['value']
        cv_x = compass_value[0]
        cv_y = compass_value[2]
        cv_rad = math.atan2(cv_x, cv_y)
        cv_deg = (cv_rad - 1.5708) / 3.1416 * 180.0
        if x_current < 0 and y_current < 0:
            if cv_deg < 0.0:
                cv_deg = cv_deg + 0
        else:
            if cv_deg < 0.0:
                cv_deg = cv_deg + 360
        
        phi = (cv_deg - 90) / 180.0 * 3.1416
        phi_d = math.atan2(- y_current + target_location_y, - x_current + target_location_x)
        
        
        
        e_phi = phi_d - phi
        e_phi_dot = e_phi - e_old

        dist = math.sqrt((target_location_x - x_current)**2 + (target_location_y - y_current)**2)
        
        e_dist = dist
        e_dist_dot = dist - dist_old

        omega = P_phi * e_phi + D_phi * e_phi_dot
        v = P_dist * e_dist + D_dist * e_dist_dot
        
        left_speed = - (2 * v - omega * L) / (2 * R)
        right_speed = - (2 * v + omega * L) / (2 * R)
        
        x_old = x_current
        y_old = y_current
        e_old = e_phi
        dist_old = dist
        
        
        devices[self.left_servo_name]['action'] = 1*left_speed
        devices[self.right_servo_name]['action'] = 1*right_speed
    
# initiate
TIME_STEP = 64

robot = Robot()
algorithm = Algorithm()
simulation = Simulation(robot, 'graph-model.json', algorithm)
simulation.make_devices()


while robot.step(TIME_STEP) != -1:
    simulation.run_simulation()
