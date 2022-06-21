import socket
import time
import urx
import logging
import IP_Address_and_PORT
import halcon as ha
import numpy as np


class UR_Control():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def movel(self, pos, speed, waittime):# [x, y, z, rx, ry, rz]
        movel = ("def test():\r\n" + "movel(p[{},{},{},{},{},{}], a=0.15, v={}, t=0, r=0)\r\n".format(
            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], speed) + "end\r\n")
        movel_as_bytes = str.encode(movel)
        type(movel_as_bytes)
        self.s.sendall(movel_as_bytes)
        time.sleep(waittime)


    # def movel():
    #     with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
    #         s.connect((IP_Address_and_PORT.HOST, IP_Address_and_PORT.PORT))
    #         IP_Address_and_PORT.way_point()
    #         movel = ("def test():\r\n" + "movel(p[{},{},{},{},{},{}], a=0.01, v=0.03, t=0, r=0)\r\n".format(IP_Address_and_PORT.x, IP_Address_and_PORT.y, IP_Address_and_PORT.z, IP_Address_and_PORT.angle_x, IP_Address_and_PORT.angle_y, IP_Address_and_PORT.angle_z) + "end\r\n")
    #         movel_as_bytes = str.encode(movel)
    #         type(movel_as_bytes)
    #         s.sendall(movel_as_bytes)
    #         data = s.recv(1024)
    #         time.sleep(8)
    #         robot = urx.Robot(IP_Address_and_PORT.HOST)
    #         rob_position = robot.getl()
    #         list_k.append(rob_position)
    #         print(list_k)

    def get_position(self):
        robot = urx.Robot(IP_Address_and_PORT.HOST)
        rob_position = robot.getl()
        list_k.append(rob_position)
        print(list_k)


    def UR_Origin_Point(self):
        robot = urx.Robot(IP_Address_and_PORT.HOST)
        robot.set_freedrive(val='', timeout=30)
        print('Move the UR to the first Calibration Circle.')
        while True:
            move_ur = input('Completed moving? (y)')
            if move_ur == 'y':
                break
            else:
                print('Invalid Input')
        rob_position = robot.getl()
        list_k.append(rob_position)
        print(list_k)
        time.sleep(2)
        print('Move the UR to the second Calibration Circle.')
        while True:
            move_ur = input('Completed moving? (y)')
            if move_ur == 'y':
                break
            else:
                print('Invalid Input')
        rob_position = robot.getl()
        list_k.append(rob_position)
        print(list_k)
        time.sleep(2)

    def calibration_movement(self, x, y):

        movel = ("def test():\r\n" + "movel(p[{},{},0.15,3.142,0,0], a=0.01, v=0.03, t=0, r=0)\r\n".format(x, y) + "end\r\n")
        movel_as_bytes = str.encode(movel)
        type(movel_as_bytes)
        self.s.sendall(movel_as_bytes)

    def movel_clibration_circle(self, x, y):
        movel = ("def test():\r\n" + "movel(p[{},{},0.251,3.142,0,0], a=0.01, v=0.03, t=0, r=0)\r\n".format(x, y) + "end\r\n")
        movel_as_bytes = str.encode(movel)
        type(movel_as_bytes)
        self.s.sendall(movel_as_bytes)
        data = self.s.recv(1024)
        time.sleep(5)
        logging.basicConfig(level=logging.INFO)

    def get_origin_point(self, list_a, list_b):
        origin_1 = []
        origin_point_x = min(list_a)
        index_origin_point_x = list_a.index(origin_point_x)
        origin_1.append(origin_point_x)
        origin_1.append(list_b[index_origin_point_x])
        print('Point 1: ', origin_1)

        origin_2 = []
        origin_point_x = max(list_a)
        index_origin_point_x = list_a.index(origin_point_x)
        origin_2.append(origin_point_x)
        origin_2.append(list_b[index_origin_point_x])
        print('Point 2: ', origin_2)

    def component_position(self, img):
        min = int(input('Enter the minimum threshold: '))
        max = int(input('Enter the maximum threshold: '))
        region = ha.threshold(img, min, max)
        display = DisplayHobject(width / 4, height / 4)
        display.disp(region)

        region = ha.connection(region)
        min = int(input('Enter the minimum area: '))
        max = int(input('Enter the maximum area: '))
        region = ha.select_shape(region, 'area', 'and', min, max)
        display.set_color('yellow')
        display.disp(region)
        time.sleep(3)

        min = float(input('Enter the minimum circularity: '))
        region = ha.select_shape(region, 'circularity', 'and', min, 1)
        component_info = ha.area_center(region)
        display.set_color('red')
        display.disp(region)

        list_1.append(component_info[1])
        list_2.append(component_info[2])
        list_3 = list_1[0]
        list_4 = list_2[0]

    def Calibration_Points_UR_Coordinate(self, list_a, list_b):
        list_q = []
        list_k = []
        list_p = []
        robot = urx.Robot(self.ip)
        print('Move the UR to the point: ', list_a[0], ',', list_b[0])
        input('Completed moving? ')
        rob_position = robot.getl()
        list_q.append(rob_position[0])
        list_q.append(rob_position[1])
        print(list_q)
        print('Move the UR to the point: ', list_a[1], ',', list_b[1])
        input('Completed moving? ')
        rob_position = robot.getl()
        list_k.append(rob_position[0])
        list_k.append(rob_position[1])
        print(list_k)
        print('Move the UR to the point: ', list_a[2], ',', list_b[2])
        input('Completed moving? ')
        rob_position = robot.getl()
        list_p.append(rob_position[0])
        list_p.append(rob_position[1])
        print(list_p)
        ur_array = np.array([[list_q[0], list_k[0], list_p[0]], [list_q[1], list_k[1], list_p[1]], [1, 1, 1]])
        print(ur_array)
        #ur_array = np.array([[-0.37670, -0.38019, -0.63731], [-0.30783, 0.03228, 0.11227], [1, 1, 1]])
        print('Change the UR mode to REMOTE, move UR away from calibration point.')
        user_input = input('Done changing? (y) ')
        return ur_array

    def Calibration_Points_UR_Coordinate_mock(self):
        ur_array = np.array([[-0.53256829, -0.52507624, -0.73619182], [-0.31788099,  0.08844638,  0.09128409], [1, 1, 1]])
        print('mock calibration')
        return ur_array