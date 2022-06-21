import os
import time
import halcon as ha
import time

DEBUG = True


class DisplayHobject():
    def __init__(self, width, height) -> None:
        if os.name == 'nt':
            ha.set_system('use_window_thread', 'true')

        self.window = ha.open_window(
            row=0,
            column=0,
            width=width,
            height=height,
            father_window=0,
            mode='visible',
            machine=''
            )

    def disp(self, img):
        ha.disp_obj(img, self.window)
        time.sleep(1)

    def set_color(self, color):
        ha.set_color(self.window, color)

    def close_window(self):
        ha.close_window(self.window)


class HalconManager(object):
    def __init__(self) -> None:
        pass

    def auto_connect_camera(self, interface_name):
        result = ha.info_framegrabber (interface_name, 'info_boards')
        if result.__len__() <= 1:
            return False
        device_list = result[1]
        print('There %d device found in the system' % len(device_list))
        print('Select the first device: ', device_list[0])
        self.acqhandle = ha.open_framegrabber(interface_name, 0, 0, 0, 0, 0, 0, 'default', -1, 'default', -1, 'false','default', device_list[0], 0, -1)
        return True
    
    def grab_image(self):
        img = ha.grab_image(self.acqhandle)
        width, height = ha.get_image_size_s(img)
        print(width, height)
        if DEBUG: 
            self.display = DisplayHobject(width/4, height/4)
            self.display.disp(img)
        return img
    
    def load_image(self, image_path):
        img = ha.read_image(image_path)
        width, height = ha.get_image_size_s(img)
        print(width, height)
        if DEBUG: 
            self.display = DisplayHobject(width, height)
            self.display.disp(img)
        return img

    def invert_image(self, img):
        inverted_img = ha.invert_image(img)
        if DEBUG: 
            self.display.disp(inverted_img)
        return inverted_img

    def connection(self, region):
        connection_region = ha.connection(region)
        if DEBUG: 
            self.display.disp(connection_region)
        return connection_region

    def fill_up(self, region):
        fill_up_region = ha.fill_up(region)
        if DEBUG: 
            self.display.disp(fill_up_region)
        return fill_up_region

    def find_target_locations(self, img, threshold_min, threshold_max, filters): 
        colors = ['green', 'yellow', 'red']      
        # change the threshold here
        region = ha.threshold(img, threshold_min, threshold_max)
        if DEBUG:
            self.display.disp(region)

        region = ha.connection(region)
        if DEBUG: 
            self.display.disp(region)

        # apply filters here
        for i in range(len(filters)):
            filter = filters[i]
            region = ha.select_shape(region, filter['name'], filter['operation'], filter['min'], filter['max'])
            if DEBUG:
                self.display.set_color(colors[i])
                self.display.disp(region)

        target_centers = ha.area_center(region)
        num_regions = ha.count_obj(ha.connection(region))
        targets = list()
        for i in range(num_regions):
            target = dict(area=target_centers[0][i], x=target_centers[1][i], y=target_centers[2][i])
            targets.append(target)
        return targets, region

    def find_goldbar_locations(self, img, threshold_min, threshold_max, filters): 
        colors = ['green', 'yellow', 'red']      
        # change the threshold here
        region = ha.threshold(img, threshold_min, threshold_max)
        if DEBUG:
            self.display.disp(region)

        region = ha.connection(region)
        if DEBUG: 
            self.display.disp(region)

        # apply filters here
        for i in range(len(filters)):
            filter = filters[i]
            region = ha.select_shape(region, filter['name'], filter['operation'], filter['min'], filter['max'])
            if DEBUG:
                self.display.set_color(colors[i])
                self.display.disp(region)
            if filter['name'] == 'area':
                region = self.fill_up(region)

        target_centers = ha.area_center(region)
        num_regions = ha.count_obj(ha.connection(region))
        targets = list()
        for i in range(num_regions):
            target = dict(area=target_centers[0][i], x=target_centers[1][i], y=target_centers[2][i])
            targets.append(target)
        return targets

    def calibration_points_order(self, region, img, calib_point_number):
        calibration_point = ha.select_obj(region, calib_point_number)
        self.display.disp(img)
        self.display.set_color("blue")
        self.display.disp(calibration_point)




if __name__ == '__main__':
    hm = HalconManager()
    connect_result = hm.auto_connect_camera('GigEVision2')
    if connect_result:
        img = hm.grab_image()
    else:
        img = hm.load_image(r'D:/coin1.jpg')

    # invert image
    img = hm.invert_image(img)

    # create filters
    filters = list()
    filter_area = dict(name="area", operation="and", min=1000, max=99999)
    filters.append(filter_area)
    filter_circularity = dict(name="circularity", operation="and", min=0.7, max=1)
    filters.append(filter_circularity)

    # find targets
    targets, region = hm.find_target_locations(img, 0, 125, filters)
    print(targets)
    hm.calibration_points_order(region, img)
