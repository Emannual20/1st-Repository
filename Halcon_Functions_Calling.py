import halcon as ha
import os
import time

def display1(img,window):
    ha.dis_obj(img, window)

def open_window(width, height):
    if os.name == 'nt':
        ha.set_system('use_window_thread', 'true')

    return ha.open_window(
        row=0,
        column=0,
        width=width,
        height=height,
        father_window=0,
        mode='visible',
        machine=''
    )
class DisplayHobject():
    def __init__(self, width, height) -> None:
        self.w = width
        self.h = height
        self.window = open_window(self.w, self.h)

    def disp(self, img):
        ha.disp_obj(img, self.window)
        time.sleep(1)

    def set_color(self, color):
        ha.set_color(self.window, color)

    def close_window(self):
        ha.close_window(self.window)

    def display1(img, window):
        ha.disp_obj(img, window)
        time.sleep(1)

class Halcon_Functions():
    def DMKCamera_Calibration_Bar():
        list_x = []
        list_y = []
        list_a = []
        list_b = []
        AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
        img = ha.grab_image(AcqHandle)
        img = ha.invert_image(img)
        width, height = ha.get_image_size_s(img)
        region = ha.threshold(img, 0, 0)
        region = ha.connection(region)
        region = ha.select_shape(region, 'area', 'and', 3000, 99999)
        region = ha.select_shape(region, 'circularity', 'and', 0.9, 1)
        coin_info = ha.area_center(region)
        list_x.append(coin_info[1])
        list_y.append(coin_info[2])
        list_a = list_x[0]
        list_b = list_y[0]
        return list_a, list_b

    def find_bar():
        list_1 = []
        list_2 = []
        list_3 = []
        list_4 = []
        list_5 = []
        list_6 = []
        AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
        img = ha.grab_image(AcqHandle)
        img = ha.invert_image(img)
        width, height = ha.get_image_size_s(img)
        region = ha.threshold(img, 0, 103)
        display = DisplayHobject(width / 4, height / 4)
        region = ha.connection(region)
        region = ha.select_shape(region, 'area', 'and', 3000, 99999)
        region = ha.select_shape(region, 'rectangularity', 'and', 0.9, 1)
        corner_points = ha.inner_rectangle1(region)
        list_5 = corner_points[1]
        list_6 = corner_points[3]
        component_info = ha.area_center(region)
        angle = ha.orientation_region(region)
        display.set_color('red')
        display.disp(region)
        list_1.append(component_info[1])
        list_2.append(component_info[2])
        list_3 = list_1[0]
        list_4 = list_2[0]
        return list_3, list_4, angle