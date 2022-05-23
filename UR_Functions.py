import socket
import os
import time
import urx
import numpy as np

dir_path = os.path.dirname(os.path.realpath(__file__))
class UR_Control():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def close(self):
        self.s.close()

    def movel(self, pos, speed):  # [x, y, z, rx, ry, rz]
        movel = ("def test():\r\n" + "movel(p[{},{},{},{},{},{}], a=0.15, v={}, t=0, r=0)\r\n".format(
            pos[0], pos[1], pos[2], pos[3], pos[4], pos[5], speed) + "end\r\n")
        movel_as_bytes = str.encode(movel)
        type(movel_as_bytes)
        self.s.sendall(movel_as_bytes)

    def freedrive(self, timeout):
        cmd = "def test():\r\n" + \
              "  freedrive_mode()\r\n" + \
              "  sleep(%d)\r\n" % timeout + \
              "end\r\n"
        cmd_as_bytes = str.encode(cmd)
        self.s.sendall(cmd_as_bytes)

    def exit_freedrive(self):
        cmd = "def test():\r\n" + \
              "  freedrive_mode()\r\n" + \
              "end\r\n"
        cmd_as_bytes = str.encode(cmd)
        self.s.sendall(cmd_as_bytes)

    def _send_file(self, filename):
        with open(filename, 'r') as reader:
            script = reader.read()
            self.s.sendall(script.encode('utf-8'))

    def init_gripper(self):
        script = os.path.join(dir_path, "(NYP) ur_scripts", "initialize_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(3)

    def open_gripper(self):
        script = os.path.join(dir_path, "(NYP) ur_scripts", "open_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)

    def close_gripper(self):
        script = os.path.join(dir_path, "(NYP) ur_scripts", "close_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)

    def reset_gripper(self):
        script = os.path.join(dir_path, "(NYP) ur_scripts)", "reset_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)

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
        print('Change the UR mode to REMOTE, move UR away from calibration point.')
        user_input = input('Done changing? (y) ')
        return ur_array

    def rotate_gripper(self, angle, speed):
        cmd = "movel(pose_trans(get_actual_tcp_pose(),p[0,0,0,0,0,d2r(%d)]), a=0.15, v=%f, t=0, r=0)\r\n" % (angle, speed)
        cmd_as_bytes = str.encode(cmd)
        self.s.sendall(cmd_as_bytes)


