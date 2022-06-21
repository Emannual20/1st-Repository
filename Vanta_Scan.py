import os
import sys
import time
sys.path.append('./ur_lib')
sys.path.append('./halcon_lib')

from ur_lib.rtde_manager import RTDEManager
from ur_lib.ur_control import URControl
from halcon_lib.halcon_manager import HalconManager
from tools.coordinates_converter import CoordinatesConverter

if __name__ == '__main__':
    # init rtde
    folder = os.path.dirname(os.path.abspath(__file__))
    print('current folder: ', folder)
    rtde = RTDEManager('192.168.1.12', 30004, 5, os.path.join(folder, 'ur_lib', 'rtde', 'output_configuration.xml'))
    rtde.initialize()
    rtde.start()
    rtde.receiving()

    # init UR control
    ur = URControl('192.168.1.12', 30002)
    ur.connect()

    # move to home position
    home_position = [0.10799, 0.18837, 0.211, 2.401, -2.305, -2.429]
    ur.movel(home_position, 0.025)
    rtde.completed_move()

    converter = CoordinatesConverter()
    file = "transformation_data.npy"
    converter.load_transformation_matrix(file)

    # Get the gold coin position
    free = True
    while free:

        # Apply filters to find the camera position of the gold coin
        hm = HalconManager()
        connect_result = hm.auto_connect_camera('GigEVision2')
        img = hm.grab_image()
        img = hm.invert_image(img)
        filters = list()
        filter_area = dict(name="area", operation="and", min=40000, max=99999)
        filters.append(filter_area)
        filter_circularity = dict(name="circularity", operation="and", min=0.6, max=1)
        filters.append(filter_circularity)
        targets, region = hm.find_target_locations(img, 0, 187, filters)

        # Convert the camera coordinates into UR coordinates
        comp_ur_pos = converter.convert(targets)
        print('Components UR Position:X axis: ', comp_ur_pos['x'], 'Y axis: ', comp_ur_pos['y'])

        # UR moves TCP to the coin and begins scan
        comp_pos = [comp_ur_pos['x'], comp_ur_pos['y'], 0.02, 2.401, -2.305, -2.429]
        ur.movel(comp_pos, 0.1)
        rtde.completed_move()
        comp_pos = [comp_ur_pos['x'], comp_ur_pos['y'], -0.019, 2.401, -2.305, -2.429]
        ur.movel(comp_pos, 0.1)
        rtde.completed_move()
        time.sleep(3)
        comp_pos = [comp_ur_pos['x'], comp_ur_pos['y'], 0.02, 2.401, -2.305, -2.429]
        ur.movel(comp_pos, 0.1)
        rtde.completed_move()
        ur.movel(home_position, 0.1)
        rtde.completed_move()
        input("")