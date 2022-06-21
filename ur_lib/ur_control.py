import os 
import time
import socket

dir_path = os.path.dirname(os.path.realpath(__file__))

class URControl():

    def __init__(self, ip, port):
        self.ip = ip
        self.port = port
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

    def connect(self):
        self.s.connect((self.ip, self.port))

    def close(self):
        self.s.close()

    def movel(self, pos, speed):# [x, y, z, rx, ry, rz]
        movel = ("def test():\r\n" + "movel(p[{},{},{},{},{},{}], a=0.1, v={}, t=0, r=0)\r\n".format(
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
            print(filename, "sent")
            self.s.sendall(script.encode('utf-8'))

    def init_gripper(self):
        script = os.path.join(dir_path, "scripts", "initialize_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(3)
    
    def open_gripper(self):
        script = os.path.join(dir_path, "scripts", "open_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)

    def close_gripper(self):
        script = os.path.join(dir_path, "scripts", "close_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)
        
    
    def reset_gripper(self):
        script = os.path.join(dir_path, "scripts", "reset_gripper.script")
        if os.path.exists(script):
            self._send_file(script)
            time.sleep(2)

    def rotate_gripper(self, angle, speed):
        cmd = "movel(pose_trans(get_actual_tcp_pose(),p[0,0,0,0,0,d2r(%d)]), a=0.15, v=%f, t=0, r=0)\r\n" % (angle, speed)
        cmd_as_bytes = str.encode(cmd)
        self.s.sendall(cmd_as_bytes)



if __name__ == "__main__":
    ur = URControl('192.168.1.12', 30002)
    ur.connect()
    home_position = [0.108, 0.28, 0.160, 2.401, -2.305, -2.429]
    ur.movel(home_position, 0.025)


