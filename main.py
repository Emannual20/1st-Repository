import os
import time

import halcon as ha


def display1(img,window):
    ha.dis_obj(img, window)
    time.sleep(2)

list_x = []
list_y = []
i = 1
if __name__ == '__main__':
    def open_framegrabber():
        return ha.open_framegrabber(
            name='',
            horizontal_resolution=0,
            vertical_resolution=0,
            image_width=0,
            image_height=0,
            start_row=0,
            start_column=0,
            field='default',
            bits_per_channel=-1,
            color_space='default',
            generic=-1,
            external_trigger='default',
            camera_type='board/board.seq',
            device='default',
            port=1,
            line_in=-1
        )
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


    def select_shape():
        return ha.select_shape(
            input='default',
            output='default',
            feature='area',
            operation='and',
            min=0,
            max=0
        )

    def area_center():
        return ha.area_center(
            region='default',
            area=0,
            row=0,
            column=0
        )
    AcqHandle = ha.open_framegrabber('USB3Vision', 0, 0, 0, 0, 0, 0, 'progressive', -1, 'default', -1, 'false', 'default', '199E32124240_TheImagingSourceEuropeGmbH_DMK33UX264', 0, -1)
    img = ha.grab_image(AcqHandle)
    width, height = ha.get_image_size_s(img)
    window_handle = open_window(width/4, height/4)
    ha.disp_obj(img, window_handle)
    input("Exit")
    region = ha.threshold(img, 192, 255)
    connected_regions = ha.connection(region)
    selected_region = ha.select_shape(connected_regions, 'area', 'and', 90000, 10000000)
    selected_region_1 = ha.select_shape(selected_region, 'circularity', 'and', 0.5, 1)


num_regions = ha.count_obj(ha.connection(selected_region_1))
coin_info = ha.area_center(selected_region_1)

while i <= num_regions:
    list_x.append(coin_info[1])
    list_y.append(coin_info[2])

print(list_x)
print(list_y)
print(num_regions)
print(coin_info)