#!/usr/bin/python
# -*- coding:utf-8 -*-
import sys
import os
picdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'pic')
libdir = os.path.join(os.path.dirname(os.path.dirname(os.path.realpath(__file__))), 'lib')
if os.path.exists(libdir):
    sys.path.append(libdir)

import logging
from waveshare_epd import epd3in52
import time
from PIL import Image,ImageDraw,ImageFont
import traceback
import ffmpeg

logging.basicConfig(level=logging.DEBUG)

try:
    #ffmpeg.input('/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/examples/test.mp4',ss=0).output('/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/pic/first_frame.bmp', vframes=1, s=f'{360}*{240}').run(overwrite_output=True)
    
    
    
    logging.info("epd3in52 Demo")
    
    epd = epd3in52.EPD()
    logging.info("init and Clear")
    epd.init()
    epd.display_NUM(epd.WHITE)
    epd.lut_GC()
    epd.refresh()

    epd.send_command(0x50)
    epd.send_data(0x17)
    time.sleep(2)
 
    
    total_frames = int(ffmpeg.probe('/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/examples/movie1.mp4')['streams'][0]['nb_frames'])
    for frame_number in range(total_frames):
        ffmpeg.input('/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/examples/movie1.mp4',ss=frame_number/30).output('/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/pic/frame.bmp', vframes=1, s=f'{360}*{240}').run(overwrite_output=True)
        logging.info(f"display frame {frame_number + 1}/{total_frames}")
        Himage = Image.open(os.path.join(picdir, 'frame.bmp'))
        epd.display(epd.getbuffer(Himage))
        epd.lut_GC()
        time.sleep(3)
        epd.refresh()
        
    
        
    


    logging.info("Clear...")
    epd.Clear()
    
    logging.info("Goto Sleep...")
    epd.sleep()
    
except IOError as e:
    logging.info(e)
    
except KeyboardInterrupt:    
    logging.info("ctrl + c:")
    epd3in52.epdconfig.module_exit(cleanup=True)
    exit()

video_path = '/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/examples/test.mp4'
output_path = '/home/pi/project/Demo/e_paper/e_paper_test/RaspberryPi_JetsonNano/python/pic/first_frame.png'
