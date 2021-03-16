#!/usr/bin/env python
# -*- encoding: utf-8 -*-

from luma.core.interface.serial import i2c, spi
from luma.core.render import canvas
from luma.oled.device import ssd1306, ssd1325, ssd1331, sh1106
from PIL import Image, ImageDraw, ImageFont
import socket, time, psutil

# port 是i2c的端口编号，默认从1开始
# address 使用 i2cdetect -y 1  查看
serial = i2c(port=1, address=0x3C)

# 这里改ssd1306, ssd1325, ssd1331, sh1106
device = ssd1306(serial)

# 可以通过 fc-list :lang=zh-cn 查看支持的中文字体
font = ImageFont.truetype("wryh.ttf", 12)
font_width, font_height = font.getsize('你')

TIME_DURATION_UNITS = (
    ('week', 60 * 60 * 24 * 7),
    ('day', 60 * 60 * 24),
    ('hour', 60 * 60),
    ('min', 60),
    ('sec', 1)
)


def human_time_duration(seconds):
    if seconds == 0:
        return 'inf'
    parts = []
    for unit, div in (
            ('天', 60 * 60 * 24),
            ('时', 60 * 60),
            ('分', 60),
            ('秒', 1)):
        amount, seconds = divmod(int(seconds), div)
        if amount > 0:
            parts.append('{}{}'.format(amount, unit))
    return ''.join(parts)


def sizeof_fmt(num, suffix='B'):
    for unit in ['', 'K', 'M', 'G', 'T', 'P', 'E', 'Z']:
        if abs(num) < 1024.0:
            return "%3.1f%s%s" % (num, unit, suffix)
        num /= 1024.0
    return "%.1f%s%s" % (num, 'Yi', suffix)


def system_ip():
    try:
        return [(s.connect(('8.8.8.8', 53)), s.getsockname()[0], s.close()) for s in
                [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]
    except:
        return ""


def system_time():
    return time.strftime("%Y-%m-%d %H:%M:%S", time.localtime())


def system_uptime():
    with open('/proc/uptime', 'r') as f:
        second = float(f.read().split(' ')[0])
        return human_time_duration(int(second))


def system_temp():
    with open('/sys/class/thermal/thermal_zone0/temp', 'r') as f:
        temp = f.read()
        return float(temp) / 1000


def system_cpu_info():
    return "{}%".format(psutil.cpu_percent())


def memory_info():
    return "{}%".format(psutil.virtual_memory().percent)


def draw_info():
    with canvas(device) as draw:
        line = 0
        draw.text((0, font_height * line), "IP：%s" % system_ip(), fill="white", font=font)
        line += 1
        draw.text((0, font_height * line), "温度：%.1f℃" % (system_temp(),), fill="white", font=font)
        line += 1
        draw.text((0, font_height * line), "运行：%s" % system_uptime(), fill="white", font=font)
        line += 1
        draw.text((0, font_height * line), "CPU:%s MEM:%s" % (system_cpu_info(), memory_info()),
                  fill="white", font=font)
        line += 1


while True:
    draw_info()
    time.sleep(1)
