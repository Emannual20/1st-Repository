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

    list_a, list_b = Halcon_Functions.DMKCamera_Calibration_Bar()

    inverse_matrix = Calculation.camera_matrix(list_a, list_b)

    ur_array = np.array([[-0.29697, -0.35275, -0.65098], [0.12294,  -0.35811,  0.14902], [1, 1, 1]])

    a = Calculation.get_a(ur_array, inverse_matrix)

    theta = Calculation.get_rotation_angle(a)

    coin_x, coin_y, angle = Halcon_Functions.find_bar()
    i = 0
    while i < len(coin_x):
        coinx, coiny = Calculation.get_array(a, coin_x[i], coin_y[i])
        coin_position = [coinx, coiny, 0.15, 3.142, 0, 0]
        ur.movel(coin_position, 0.1)
        rtde.completed_move()
        ur.rotate_gripper(math.degrees(theta - angle[i] - (math.pi/2)), 0.1)
        rtde.completed_move()
        ur.close_gripper()
        ur.movel(drop_off_point, 0.1)
        rtde.completed_move()
        ur.open_gripper()
        ur.movel(ready_position, 0.1)
        rtde.completed_move()
        i += 1