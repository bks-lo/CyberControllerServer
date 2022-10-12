import keyboard
import time
from screen_shot import ScreenCapture
import io

class KeyboardListener:
	def __init__(self, tcpServer):
		self.tcpServer = tcpServer
		self.t = 0
		self.c = 0
		self.key_state_map={}
		self.screen_capture = None

	def listen_keyboard(self,callback):
		self.callback = callback
		keyboard.hook(self.onKeyEvent)
		keyboard.wait()

	def onImgCapture(self,pic):
		imgByteArr = io.BytesIO()
		pic.save(imgByteArr, format='JPEG')
		bytes_data = imgByteArr.getvalue()
		self.tcpServer.send_img(bytes_data)

	def isKeyHolding(self,key):
		return (key in self.key_state_map and self.key_state_map[key]=='down')

	def isCtrlHolding(self):
		return self.isKeyHolding('ctrl') or self.isKeyHolding('left ctrl') or self.isKeyHolding('right ctrl')

	def isAltHolding(self):
		return self.isKeyHolding('alt') or self.isKeyHolding('left alt') or self.isKeyHolding('right alt')

	def isShiftHolding(self):
		return self.isKeyHolding('shift') or self.isKeyHolding('left shift') or self.isKeyHolding('right shift')


	def onKeyEvent(self,key):
		#update key_state_map
		self.key_state_map[key.name.lower()]=key.event_type

		#is screenshoot?

		if  self.isAltHolding()\
			and key.event_type=="down"\
			and key.name.lower()=="z":
			self.screen_capture = ScreenCapture()
			self.screen_capture.are_capture(self.onImgCapture)

		print(self.key_state_map)
		#is triple c?
		if  key.event_type=="down" \
			and key.name.lower()=="c" \
			and self.isCtrlHolding():

			if self.t == 0:
				self.t=time.time()
				self.c += 1
				print("wait for nex c",self.c)
				return

			if (time.time()-self.t<0.5):
				self.t=time.time()
				self.c += 1
				print("wait for nex c:",self.c)

			else:
				self.c = 0
				self.t=0
				print("wait for nex c",self.c)

			if self.c>=2:
				self.c=0
				print("need trans")
				if self.callback:
					self.callback()
