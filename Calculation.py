import numpy as np
import math

def camera_matrix(list_a, list_b):
    calibration_matrix = np.array([[list_a[0], list_a[1], list_a[2]], [list_b[0], list_b[1], list_b[2]], [1, 1, 1]])
    calibration_matrix = np.linalg.inv(calibration_matrix)
    return calibration_matrix

def get_a(UR, calibration_matrix):
    a = np.dot(UR, calibration_matrix)
    return a

def get_rotation_angle(transformation_matrix):
    theta = math.atan(transformation_matrix[0, 0]/transformation_matrix[1, 0])
    return theta

def get_array(transformation_matrix, a, b):
    component_matrix = np.array([[a], [b], [1]])
    component_UR = np.dot(transformation_matrix, component_matrix)
    list_d = []
    f = float(component_UR[0])
    h = float(component_UR[1])
    list_d.append(f)
    list_d.append(h)
    print('Components UR Position:X axis: ', list_d[0], 'Y axis: ', list_d[1])
    return list_d


