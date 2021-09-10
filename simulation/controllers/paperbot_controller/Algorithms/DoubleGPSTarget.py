from Algorithms.Algorithm import Algorithm
import math

class DoubleGPSTarget(Algorithm):
    def __init__(self, gps1_name, gps2_name, left_servo_name, right_servo_name):
        self.gps1_name = gps1_name
        self.gps2_name = gps2_name
        self.left_servo_name = left_servo_name
        self.right_servo_name = right_servo_name
    
    def set_actions(self, devices):
                
        target = 0.5
            
        xyz_current1 = devices[self.gps1_name]['value']
        y_current1 = xyz_current1[2]
            
        xyz_current2 = devices[self.gps2_name]['value']
        y_current2 = xyz_current2[2]
            
        if target - 0.05 < y_current1 < target + 0.05 or target - 0.1 < y_current2 < target:
            devices[self.left_servo_name]['action'] = 0
            devices[self.right_servo_name]['action'] = 0
        else:
            devices[self.left_servo_name]['action'] = 1
            devices[self.right_servo_name]['action'] = 1
            
           
