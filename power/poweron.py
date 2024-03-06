'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-06 14:30:55
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 14:31:23
FilePath: /scripts/power/poweron.py
Description: this file is used to set power monitor's voltage

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import argparse
import Monsoon.HVPM as HVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op

parser = argparse.ArgumentParser()
parser.add_argument('--voltage', type=str, required=True, help="Voltage to supply smarthphone")
args = parser.parse_args()
volt = float(args.voltage)

Mon = HVPM.Monsoon()
Mon.setup_usb()
Mon.calibrateVoltage()
# Mon.calibrateVoltage()

Mon.setVout(volt)