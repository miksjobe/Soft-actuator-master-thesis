import serial
import scipy.io
import numpy as np
from apscheduler.schedulers.blocking import BlockingScheduler
import time
import math

ser=serial.Serial("COM3",9600,bytesize=serial.EIGHTBITS,timeout=0.05,stopbits=serial.STOPBITS_ONE)

def job_list():
    my_time=time.localtime()
    curve=bytes([int(time.strftime("%S",my_time))])
    if ser.in_waiting<=1:
        #data_bytes=bytes([10])+bytes("\r\n",'utf-8')
        ser.write(curve)
    analog=ser.readline()
    print(analog,int(time.strftime("%S",my_time)))
    time.sleep(0.05)

def job_list2():
    my_time=time.localtime()
    if ser.in_waiting>0:
        #print("I read when the input buffer was:",ser.in_waiting)
        analog=ser.readline()
        #print(analog)
        curve=bytes([int(time.strftime("%S",my_time))])
        #ser.write(curve)
        print(analog,curve,int(time.strftime("%S",my_time)),ser.in_waiting,ser.out_waiting)
        #print(analog,ser.in_waiting,ser.out_waiting)
        #print("I have now sent, the out buffer is:",ser.out_waiting)
        #print("i cleared the buffer!",ser.in_waiting)
        ser.reset_input_buffer()
    #time.sleep(0.05)

scheduler = BlockingScheduler()
scheduler.add_job(job_list2,'interval',seconds=0.05,id='job_list2',misfire_grace_time=10,coalesce=True)
scheduler.start()
ser.reset_input_buffer()
#while True:
#    job_list2()
