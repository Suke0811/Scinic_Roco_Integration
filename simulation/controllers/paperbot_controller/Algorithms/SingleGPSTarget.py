from Algorithms.Algorithm import Algorithm
import math

class SingleGPSTarget(Algorithm):
    def __init__(self, gps_name, left_servo_name, right_servo_name):
        self.gps_name = gps_name
        self.left_servo_name = left_servo_name
        self.right_servo_name = right_servo_name
    
    def set_actions(self, devices):
                
        target = 0.5
            
        xyz_current = devices[self.gps_name]['value']
        x_current = xyz_current[0]
        y_current = xyz_current[2]
            
        if y_current < target:
            speed = 1
        else:
            speed = -1
                
        if target - 0.05 < y_current < target + 0.05:
            devices[self.left_servo_name]['action'] = 0
            devices[self.right_servo_name]['action'] = 0
            
        else:
            devices[self.left_servo_name]['action'] = speed
            devices[self.right_servo_name]['action'] = speed
            
           
