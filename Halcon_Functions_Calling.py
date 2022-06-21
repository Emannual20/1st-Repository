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
        # ha.clear_window(self.window)
        ha.disp_obj(img, self.window)
        time.sleep(1)

    def set_color(self, color):
        ha.set_color(self.window, color)

    def close_window(self):
        ha.close_window(self.window)

    def display1(img, window):
        ha.disp_obj(img, window)
        time.sleep(3)

def DMKCamera_Calibration_Points():
    list_x = []
    list_y = []
    AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
    img = ha.grab_image(AcqHandle)
    width, height = ha.get_image_size_s(img)
    # change the threshold here
    region = ha.threshold(img, 19, 100)
    region = ha.connection(region)
    # change the minimum and maximum area here
    region = ha.select_shape(region, 'area', 'and', 1000, 50000)
    region = ha.select_shape(region, 'circularity', 'and', 0.5, 1)
    coin_info = ha.area_center(region)
    num_regions = ha.count_obj(ha.connection(region))
    list_x.append(coin_info[1])
    list_y.append(coin_info[2])
    list_a = list_x[0]
    list_b = list_y[0]
    num = 1
    i = 0
    while i < num_regions:
        print(num, ')' + ' X axis: ', list_b[i], 'Y axis: ', list_a[i])
        num += 1
        i += 1
    return list_a, list_b

def find_component():
    AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
    img = ha.grab_image(AcqHandle)
    width, height = ha.get_image_size_s(img)
    # change threshold here
    region = ha.threshold(img, 19, 125)
    region = ha.connection(region)
    # change the minimum and maximum area here
    region = ha.select_shape(region, 'area', 'and', 11000, 20000)
    display = DisplayHobject(width / 4, height / 4)
    display.set_color('yellow')
    display.disp(region)
    region = ha.select_shape(region, 'circularity', 'and', 0.3, 1)
    component_info = ha.area_center(region)
    display.set_color('red')
    display.disp(region)
    list_1 = []
    list_2 = []
    list_1.append(component_info[1])
    list_2.append(component_info[2])
    list_3 = list_1[0]
    list_4 = list_2[0]
    print('Component Co-ordinates: X axis: ', list_3[0], 'Y axis: ', list_4[0])
    return list_3, list_4

def DMKCamera_Calibration_Bar():
    list_x = []
    list_y = []
    list_a = []
    list_b = []
    AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
    img = ha.grab_image(AcqHandle)
    img = ha.invert_image(img)
    width, height = ha.get_image_size_s(img)
    region = ha.threshold(img, 0, 157)
    region = ha.connection(region)
    region = ha.select_shape(region, 'area', 'and', 1000, 30000)
    region = ha.select_shape(region, 'circularity', 'and', 0.9, 1)
    coin_info = ha.area_center(region)
    num_regions = ha.count_obj(ha.connection(region))
    list_x.append(coin_info[1])
    list_y.append(coin_info[2])
    list_a = list_x[0]
    list_b = list_y[0]
    num = 1
    i = 0
    while i < num_regions:
        print(num, ')' + ' X axis: ', list_b[i], 'Y axis: ', list_a[i])
        num += 1
        i += 1

    return list_a, list_b

def find_bar():
    list_1 = []
    list_2 = []
    AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false','default','199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
    img = ha.grab_image(AcqHandle)
    img = ha.invert_image(img)
    width, height = ha.get_image_size_s(img)
    # change the threshold here
    region = ha.threshold(img, 0, 157)
    display = DisplayHobject(width / 4, height / 4)
    region = ha.connection(region)
    # change the minimum and maximum area here
    region = ha.select_shape(region, 'area', 'and', 10000, 30000)
    region = ha.select_shape(region, 'rectangularity', 'and', 0.6, 1)
    component_info = ha.area_center(region)
    display.set_color('red')
    display.disp(region)
    list_1.append(component_info[1])
    list_2.append(component_info[2])
    list_3 = list_1[0]
    list_4 = list_2[0]
    print('Component Co-ordinates: X axis: ', list_3[0], 'Y axis: ', list_4[0])
    return list_3, list_4