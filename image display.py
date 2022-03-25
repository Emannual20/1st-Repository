import halcon as ha
import os
import sys

def open_framegrabber():
    """Open file based image acquisition framegrabber."""
    return ha.open_framegrabber(
        name='File',
        horizontal_resolution=1,
        vertical_resolution=1,
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
    """Open native window for drawing."""
    if os.name == 'nt':
        # Windows applications wanting to perform GUI tasks, require an
        # application level event loop. By default console applications like
        # this do not have one, but HALCON can take care of this for us,
        # if we enable it by setting this system parameter.
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