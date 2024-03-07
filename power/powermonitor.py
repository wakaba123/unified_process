'''
Author: wakaba blues243134@gmail.com
Date: 2024-03-06 14:27:42
LastEditors: wakaba blues243134@gmail.com
LastEditTime: 2024-03-06 21:59:54
FilePath: /unified_process/power/powermonitor.py
Description: this file is used to control power monitor

Copyright (c) 2024 by ${git_name_email}, All Rights Reserved. 
'''
import Monsoon.HVPM as HVPM
import Monsoon.sampleEngine as sampleEngine
import Monsoon.Operations as op
import time
import threading
import argparse


class PowerMonitor:
	def __init__(self):
		self.power = 0
		self.power_data = []

		self.Mon = HVPM.Monsoon()
		self.Mon.setup_usb()
		self.engine = sampleEngine.SampleEngine(self.Mon)
		self.engine.disableCSVOutput()
		self.engine.ConsoleOutput(False)

		self._thread = None
		self._stop_event = threading.Event()

	def start(self):
		assert not self._thread
		self.power_data= [] 
		self.progress_bar = 0
		self._stop_event.clear()
		self._thread = threading.Thread(target=self.get_power, args=(1000, )) # 1 second
		self._thread.start()

	def get_power(self, sampleNum):
		#default channel is main current
		while True: 
			power = []
			self.engine.startSampling(sampleNum)
			sample = self.engine.getSamples()
			self.Mon.stopSampling()	
			print("=" * (self.progress_bar % 100), end="\r")
			for i in range(len(sample[sampleEngine.channels.MainCurrent])):
				current = sample[sampleEngine.channels.MainCurrent][i]
				voltage = sample[sampleEngine.channels.MainVoltage][i]
				power.append(current * voltage)
				if power == 0:
					print("power is zero")
			self.power = sum(power) / len(power)
			self.power_data.append(self.power)
			self.progress_bar = self.progress_bar + 1
			if self._stop_event.is_set():
				break
            
	def stop(self):
		# assert self._thread
		if self._thread:
			self._stop_event.set()
			self._thread.join()
			print("Stop Get Power Thread")
			self._thread = None

	def powerOff(self):
		self.Mon.setVout(0)

a = PowerMonitor()
a.stop()