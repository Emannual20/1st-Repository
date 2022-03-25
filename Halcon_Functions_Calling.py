import halcon as ha
import os
import time


def open_framegrabber():
    ha.open_framegrabber(
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