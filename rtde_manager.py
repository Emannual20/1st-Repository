import logging
import threading
import time
import rtde.rtde as rtde
import rtde.rtde_config as rtde_config
from rtde.deserializer import Deserializer

class RTDEManager(object):
    
    def __init__(self, ip, port, frequency, output_config) -> None:        
        conf = rtde_config.ConfigFile(output_config)
        self.output_names, self.output_types = conf.get_recipe('out')
        self.deserializer = Deserializer(self.output_names, self.output_types)
        self.con = rtde.RTDE(ip, port)
        self.frequency = frequency
        self.runtime_state = False
        self.tcp = [0, 0, 0, 0, 0, 0]

    def initialize(self):
        self.con.connect()
        self.con.get_controller_version()
        if not self.con.send_output_setup(self.output_names, self.output_types, self.frequency):
            logging.error('Unable to configure output')

    def start(self):
        if not self.con.send_start():
            logging.error('Unable to start synchronization')

    def receive(self) -> list:
        rtdt_output = []
        state = self.con.receive(False)
        # state = self.con.receive_buffered(False)
        if state is not None:
            rtdt_output = self.deserializer.deserialize(state)
        return rtdt_output
    
    def receiving(self) -> list:
        thread = threading.Thread(target=self.run, args=())
        thread.daemon = True                            # Daemonize thread
        thread.start()                                  # Start the execution

    def run(self):
        while True:
            rtdt_output = []
            state = self.con.receive(False)
            if state is not None:
                rtdt_output = self.deserializer.deserialize(state)
                self.tcp = rtdt_output[1:6]
                self.runtime_state = True if rtdt_output[-1] == 2 else False                

    def get_TCP(self):
        return self.tcp

    def get_runtime_state(self):
        return self.runtime_state

    def completed_move(self):
        keep_running = True
        time.sleep(0.5)
        while keep_running:
            if self.runtime_state == True:
                time.sleep(0.5)
            else:
                keep_running = False
        return