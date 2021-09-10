from Algorithms.Algorithm import Algorithm
import math

class GoToTarget(Algorithm):
    def __init__(self, gps_name, compass_name, left_servo_name, right_servo_name):
        self.gps_name = gps_name
        self.compass_name = compass_name
        self.left_servo_name = left_servo_name
        self.right_servo_name = right_servo_name
    
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
    
