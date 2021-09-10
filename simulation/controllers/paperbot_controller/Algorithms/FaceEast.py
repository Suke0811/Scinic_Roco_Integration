from Algorithms.Algorithm import Algorithm
import math

class FaceEast(Algorithm):
    def __init__(self, compass_name, left_servo_name, right_servo_name):
        self.compass_name = compass_name
        self.left_servo_name = left_servo_name
        self.right_servo_name = right_servo_name
    
    def set_actions(self, devices):
                
        compass_value = devices[self.compass_name]['value']
        cv_x = compass_value[0]
        cv_y = compass_value[2]
        cv_rad = math.atan2(cv_x, cv_y)
        cv_deg = (cv_rad - 1.5708) / 3.1416 * 180.0
            
        if 85.0 < cv_deg < 95.0:
            devices[self.left_servo_name]['action'] = 0
            devices[self.right_servo_name]['action'] = 0
        else:
            devices[self.left_servo_name]['action'] = 1
            devices[self.right_servo_name]['action'] = -1
                
           
