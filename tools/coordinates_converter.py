import numpy as np
import math

class CoordinatesConverter(object):
    def __init__(self) -> None:
        pass

    def calibrate(self, camera_pos, ur_pos):
        ur_matrix = np.array([
            [ur_pos[0]['x'], ur_pos[1]['x'], ur_pos[2]['x']],
            [ur_pos[0]['y'], ur_pos[1]['y'], ur_pos[2]['y']],
            [             1,              1,              1]
        ])
        
        camera_matrix = np.array([
            [camera_pos[0]['x'], camera_pos[1]['x'], camera_pos[2]['x']],
            [camera_pos[0]['y'], camera_pos[1]['y'], camera_pos[2]['y']],
            [                 1,                  1,                  1]
        ])
        inv_camera_matrix = np.linalg.inv(camera_matrix)
        self.transformation_matrix = np.dot(ur_matrix, inv_camera_matrix)

        return self.transformation_matrix
    
    def convert(self, camera_pos):
        camera_matrix = np.array([
            [camera_pos[0]['x']],
            [camera_pos[0]['y']],
            [              1]
        ])
        ur_matrix = np.dot(self.transformation_matrix, camera_matrix)
        ur_pos = dict(x=ur_matrix[0,0], y=ur_matrix[1,0])
        return ur_pos
    
    def get_rotation_angle(self, transformation_matrix):
        # transformation matrix = [x, y, z, q]
        theta = math.atan(transformation_matrix[1]/transformation_matrix[0])
        # Using theta, we can find Sx then Sy
        Sx = transformation_matrix[0]/math.cos(theta)
        Sy = transformation_matrix[3]/math.cos(theta)
        return theta

    def save_transformation_matrix(self, file):
        np.save(file, self.transformation_matrix)

    def load_transformation_matrix(self, file):
        self.transformation_matrix = np.load(file)
        print('Loaded Matrix:')
        print(self.transformation_matrix)

if __name__ == '__main__':
    converter = CoordinatesConverter()
    camera_pos = list()
    camera_pos.append(dict(x=0, y=1))
    camera_pos.append(dict(x=1, y=1))
    camera_pos.append(dict(x=1, y=0))

    print("camera:", camera_pos)

    ur_pos = list()
    ur_pos.append(dict(x=-1, y=0))
    ur_pos.append(dict(x=0, y=1))
    ur_pos.append(dict(x=1, y=0))
    print("ur:", camera_pos)

    converter.calibrate(camera_pos, ur_pos)
    print(converter.transformation_matrix)

    new_camera_pos = list()
    new_camera_pos.append(dict(x=0, y=0))
    print(converter.convert(new_camera_pos))
