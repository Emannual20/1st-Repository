import math
from Halcon_Functions_Calling import Halcon_Functions
import Calculation
from UR_Functions import UR_Control
import numpy as np
from rtde_manager import RTDEManager
import os

if __name__ == '__main__':
    folder = os.path.dirname(os.path.abspath(__file__))
    rtde = RTDEManager('192.168.1.13', 30004, 5, os.path.join(folder, 'rtde', 'output_configuration.xml'))
    ur = UR_Control('192.168.1.13', 30002)
    ur.connect()
    rtde.initialize()
    rtde.start()
    rtde.receiving()
    drop_off_point = [-0.54065, -0.52021, 0.16, 3.142, 0, 0]
    ready_position = [-0.139, 0.136, 0.25, 3.142, 0, 0]
    ur.movel(ready_position, 0.1)
    rtde.completed_move()
    ur.open_gripper()

    #list_a, list_b = Halcon_Functions.DMKCamera_Calibration_Bar()

    #inverse_matrix = IP_Address_and_PORT.camera_matrix(list_a, list_b)

    ur_array = np.array([[-0.29697, -0.35275, -0.65098], [0.12294,  -0.35811,  0.14902], [1, 1, 1]])

    #a = IP_Address_and_PORT.get_a(ur_array, inverse_matrix)
    a = np.array([[-2.60826129e-04, -2.82061655e-05, -2.15276903e-01], [2.34470669e-05, -2.56794674e-04, 1.49280244e-01], [0.00000000e+00,  8.55503277e-20,  1.00000000e+00]])
    #theta = IP_Address_and_PORT.get_rotation_angle(a)
    theta = -1.481141921574807

    i = 0
    while True:
        x, y, angle = Halcon_Functions.find_bar()
        x, y = Calculation.get_array(a, x[0], y[0])
        coin_position = [x, y, 0.150, 3.142, 0, 0]
        ur.movel(coin_position, 0.1)
        rtde.completed_move()
        ur.rotate_gripper(math.degrees(theta - angle[0] - (math.pi/2)), 0.1)
        rtde.completed_move()
        ur.close_gripper()
        ur.movel(drop_off_point, 0.1)
        rtde.completed_move()
        ur.open_gripper()
        ur.movel(ready_position, 0.1)
        rtde.completed_move()
        i += 1