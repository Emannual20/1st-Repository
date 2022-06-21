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

    # Get Camera Pos
    hm = HalconManager()
    connect_result = hm.auto_connect_camera('GigEVision2')
    img = hm.grab_image()
    img = hm.invert_image(img)

    # create filters
    filters = list()
    filter_area = dict(name="area", operation="and", min=1000, max=30000)
    filters.append(filter_area)
    filter_circularity = dict(name="circularity", operation="and", min=0.8, max=1)
    filters.append(filter_circularity)

    # find targets
    targets, region = hm.find_target_locations(img, 0, 125, filters)

    # init UR control
    ur = URControl('192.168.1.12', 30002)
    ur.connect()

    # move to home position
    home_position = [0.10799, 0.18837, 0.211, 2.401, -2.305, -2.429]
    ur.movel(home_position, 0.025)
    rtde.completed_move()

    ##display the first calibration point
    #hm.calibration_points_order(region, img, 1)

    ## set UR to freedrive mode
    ##ur.freedrive(60)

    ## Get UR Pos
    #print("Move to the first calibration point")

    ##input('Confirm the first calibration position?')
    #first_calib_pos = rtde.get_TCP()
    #print("The first Position:", first_calib_pos)

    ## display the second calibration point
    #hm.calibration_points_order(region, img, 2)

    ## set UR to freedrive mode
    ##ur.freedrive(60)

    #print("Move to the first calibration point")
    ##input('Confirm the second calibration position?')
    #second_calib_pos = rtde.get_TCP()
    #print("The second Position:", second_calib_pos)

    ## display the third calibration point
    #hm.calibration_points_order(region, img, 3)

    ## set UR to freedrive mode
    ##ur.freedrive(60)

    #print("Move to the first calibration point")
    ##input('Confirm the third calibration position?')
    #third_calib_pos = rtde.get_TCP()
    #print("The third Position:", third_calib_pos)
    converter = CoordinatesConverter()
    ur_pos = list()
    #ur_pos.append(dict(x=first_calib_pos[0], y=first_calib_pos[1]))
    #ur_pos.append(dict(x=second_calib_pos[0], y=second_calib_pos[1]))
    #ur_pos.append(dict(x=third_calib_pos[0], y=third_calib_pos[1]))
    ur_pos.append(dict(x=0.1573591687799636, y=0.3269282097274549))
    ur_pos.append(dict(x=0.14447724817548395, y=0.616739878812097))
    ur_pos.append(dict(x=-0.096617312984956373, y=0.6084262524342434))

    # calculating the transformation matrix
    transformation_matrix = converter.calibrate(targets, ur_pos)

    # Get the gold coin position
    free = False
    while free:
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
        comp_ur_pos = converter.convert(targets)
        print('Components UR Position:X axis: ', comp_ur_pos['x'], 'Y axis: ', comp_ur_pos['y'])
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