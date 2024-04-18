import sys
sys.path.append('/home/wakaba/Desktop/huawei0318')
import basic_tools.freq_setting as fs
import configparser
import subprocess
import re
import time
from collections import deque
from threading import Thread, Lock
import numpy as np

config = configparser.ConfigParser()
config.read('/home/wakaba/Desktop/huawei0318/unified_process/config.ini')

device_name = 'huawei'
cpu_type = fs.check_soc()
cpu_type = len(cpu_type)

freq_lists = {
	2: ['little_freq_list','big_freq_list'],
	3: ['little_freq_list', 'big_freq_list', 'super_freq_list']
}
if cpu_type in freq_lists:
	cpu_freq_list = [config.get(device_name, freq).split() for freq in freq_lists[cpu_type]]
else:
	print("Unsupported CPU type")
	raise ValueError

def execute(cmd):
	cmds = [ 'su',cmd, 'exit']
	obj = subprocess.Popen("adb shell", shell= True, stdin=subprocess.PIPE, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
	info = obj.communicate(("\n".join(cmds) + "\n").encode('utf-8'));
	return info[0].decode('utf-8')

def get_view():
	focus_index = [2,5,8]
	# focus_index= [4,8]
	out = execute('dumpsys SurfaceFlinger | grep -i focus -A 10')
	a = out.split('\n')
	view = a[8]
	view = view.strip()
	print(f'current view:{view}')
		
	out = execute('dumpsys SurfaceFlinger --list')
	a = out.split('\n')
	# pattern = r'SurfaceView\[com\.miHoYo\.Yuanshen\/com\..*?\.GetMobileInfo\.MainActivity\]\(BLAST\)#0'
	escaped_text = re.escape(view)
	pattern = escaped_text.replace(re.escape('[...]'), '.*?')
	print(pattern)

	result = re.findall(pattern, out)

	print(f'current result is {result}')
	return re.escape(result[0])

class FPSGet():
	def __init__(self, view):
		self.view = view
		self.fps = 0
		self.t = 0

		out = execute(' '.join(['dumpsys', 'SurfaceFlinger', '--latency-clear']))
		time.sleep(1)
	
		(refresh_period, timestamps) = self.get_frame_data()
		self.base_timestamp = 0
		for timestamp in timestamps:
			if timestamp != 0:
				self.base_timestamp = timestamp
				break
		if self.base_timestamp == 0:
			raise RuntimeError("Initial frame collect failed")	

		self.last_timestamp = timestamps[-2]
		
		# missed = execute(' '.join(['dumpsys', 'SurfaceFlinger', '|', 'grep', 'missed']))
		# self.last_total_missed = int(missed.splitlines()[0].split()[-1])
		# self.last_hwc_missed = int(missed.splitlines()[1].split()[-1])
		# self.last_gpu_missed = int(missed.splitlines()[2].split()[-1])
		self.frame_queue = deque(maxlen=500)
		self.frame_queue += [timestamp for timestamp in timestamps]
		self.lock = Lock()

	def start(self):
		fps_thread = Thread(target=self.get_frame_data_thread, args=())
		fps_thread.start()

	def get_frame_data_thread(self):
		while self.while_flag:
			time.sleep(0.5)
			refresh_period, new_timestamps = self.get_frame_data()
			if len(new_timestamps) <= 120:
				continue
			print("len : {}".format(len(new_timestamps)))
			with self.lock:
				self.frame_queue += [timestamp for timestamp in new_timestamps if timestamp > self.last_timestamp]
			if len(new_timestamps):
					self.last_timestamp = new_timestamps[-1]

	def get_fps(self):
		time.sleep(1)
		if self.view is None:
			raise RuntimeError("Fail to get current SurfaceFligner view")
		old_timestamps = []
		# calculate fps in past 1 second
		adjusted_timestamps = []
		with self.lock:
			for index in range(len(self.frame_queue)):
					seconds = self.frame_queue[index]
					seconds -= self.base_timestamp
					if seconds > 1e6: # too large, just ignore
						continue
					adjusted_timestamps.append(seconds)


		from_time = adjusted_timestamps[-1] - 1.0
		fps_count = 0
		for seconds in adjusted_timestamps:
			if seconds > from_time:
				fps_count += 1
		self.fps = min(fps_count, 60)
		return self.fps

	def get_frame_data(self):
		results = execute(' '.join(['dumpsys', 'SurfaceFlinger', '--latency', self.view]))
		results = results.splitlines()
		# print(results)

		if not len(results):
			raise RuntimeError("Frame Data is Empty.")
			return -1
		timestamps = []
		nanoseconds_per_second = 1e9
	
		refresh_period = int(results[0]) / nanoseconds_per_second
		pending_fence_timestamp = (1 << 63) - 1		
		
		for line in results[1:]:
			fields = line.split()
			if len(fields) != 3:
				continue
			(start, submitting, submitted) = map(int, fields)
			if submitting == 0:
				continue
			timestamp = int(fields[1])
			if timestamp == pending_fence_timestamp:
				continue
			timestamp /= nanoseconds_per_second
			timestamps.append(timestamp)


		return (refresh_period, timestamps)


view = get_view()
view = 'com.futuremark.dmandroid.application/com.futuremark.dmandroid.application.attan.AttanVulkanNativeActivity#0'
# view = 'SurfaceView[com.tencent.qqlive/com.tencent.qqlive.ona.activity.VideoDetailActivity]\(BLAST\)#2166'
# print(view)
fps = FPSGet(view=view)

fps.while_flag = True
# fps_thread = Thread(target=fps.get_frame_data_thread, args=())
fps.start()
while True:
	cur_fps = fps.get_fps()
	print(cur_fps)

for super_freq in cpu_freq_list[2][0::1]:
	for big_freq in cpu_freq_list[1][3::1]:
		for little_freq in cpu_freq_list[0][3::3]:
			fs.set_cpu_governor('powersave')
			fs.set_cpu_freq([little_freq, big_freq, super_freq])
			assert [little_freq, big_freq, super_freq] == fs.get_cpu_freq()
			t = 0
			count = 0
			temp = []
			while t <= 20:
				t += 1
				print(t)
				cur_fps = fps.get_fps()
				print(f'cur fps is {cur_fps}')
				temp.append(cur_fps)
			print(f'===========avg is {np.mean(temp)}')

			if np.mean(temp) > 59.5:
				print('=============succeed')
				print(super_freq, big_freq, little_freq)
				exit(0)
			else:
				print('failed')
				print(super_freq, big_freq, little_freq)
				
