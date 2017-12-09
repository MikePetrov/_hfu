#!/usr/bin/python
# -*- coding: utf-8 -*-#

#
# получаем температуру
#

import os
import glob
import time
import sys
import sqlite3

os.system('modprobe w1-gpio')
os.system('modprobe w1-therm')

conn = sqlite3.connect('\usr\local\hfu\hfu.sqlite3')
cursor = conn.cursor()

base_dir = '/sys/bus/w1/devices/'
device_folder = glob.glob(base_dir + '10*')[0]
device_file = device_folder + '/w1_slave'

def read_temp_raw():
    f = open(device_file, 'r')
    lines = f.readlines()
    f.close()
    return lines

def read_temp():
    lines = read_temp_raw()
    while lines[0].strip()[-3:] != 'YES':
        time.sleep(0.2)
        lines = read_temp_raw()
    equals_pos = lines[1].find('t=')
    if equals_pos != -1:
        temp_string = lines[1][equals_pos+2:]
        temp_c = float(temp_string) / 1000.0
        return temp_с


while True:
    cursor.execute("INSERT INTO {} VALUES ({})".format(f_pipe_temp (temperatyre), temp_c))
#	cursor.execute("INSERT INTO f_pipe_temp (temperatyre, TIME, DATE) VALUES(?, ?, ?)", (temp_c, current_time, current_date))
	print(read_temp())
    time.sleep(5)

conn.close()
