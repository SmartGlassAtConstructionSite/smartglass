import time
import sys
import math
from PIL import Image
import spidev
from OLED.core.device import device
import OLED.core.error
import OLED.core.framebuffer
import OLED.const


class ssd1351(device):
    def __init__(self, serial_interface=None, width=128, height=128, rotate=0,
                 framebuffer="diff_to_previous", h_offset=0, v_offset=0, **kwargs):
        super(ssd1351, self).__init__(OLED.const.common, serial_interface)
        self.capabilities(width, height, rotate, mode="RGB")
        self.framebuffer = getattr(OLED.core.framebuffer, framebuffer)(self)

        settings = {
            (128, 128):  dict(width=0x7F, height=0x7F, displayoffset=0x00, startline=0x00, remap=0x00),
            (96, 96):    dict(width=0x6F, height=0x5F, displayoffset=0x00, startline=0x00, remap=0x02)
        }.get((width, height))

        if h_offset != 0 or v_offset != 0:
            def offset(bbox):
                left, top, right, bottom = bbox
                return (left + h_offset, top + v_offset, right + h_offset, bottom + v_offset)
            self.apply_offsets = offset
                
        else:
            self.apply_offsets = lambda bbox: bbox

        if settings is None:
        if (width, height) not in [(96, 96), (128, 128)]:
            raise OLED.core.error.DeviceDisplayModeError(
                "Unsupported display mode: {0} x {1}".format(width, height))

    
