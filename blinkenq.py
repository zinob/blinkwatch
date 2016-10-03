#!/usr/bin/python3
import RPi.GPIO as GPIO
from queue import Queue,Empty
from threading import Thread
from collections import namedtuple
from prioqueue import prio_queue
from time import time

event=namedtuple("blinkevent",["led","brightness","duration"])

class Blinkenq(Thread):
	def __init__(self):
		super().__init__()

		self._ioq=Queue()
		self._Off=namedtuple("off",["time","led"])
		leds=[2,3,4]

		GPIO.setwarnings(False)
		GPIO.setmode(GPIO.BCM)
		self.leds=[]
		for i in leds:
			GPIO.setup(i,GPIO.OUT)
			GPIO.output(i, False)
			p=GPIO.PWM(i, 200)
			p.start(0)
			self.leds.append(p)

	def blink(self,led,brightness,duration):
		self._ioq.put(event(led=led,brightness=brightness,duration=duration))
		
	def _led_on(self,led,brightness):
		#print("%f led %i ON @ %f"%(time(),led,brightness))
		self.leds[led].ChangeDutyCycle(brightness)
	
	def _led_off(self,led):
		#print("%f led %i OFF"%(time(),led))
		self.leds[led].ChangeDutyCycle(0)

	def _read_ioq(self,event_queue,timeout=60):
		ioq=self._ioq
		try:
			led,brightness,duration=ioq.get(timeout=timeout)
			self._led_on(led,brightness)
			event_queue.push(self._Off(time()+duration,led))
			#print("%f from %f, until %f"%(duration,time(),time()+duration))
		except Empty:
			pass

	def _consume_pending(self,q):
		while not q.is_empty() and q.peek().time <= time():
			t,led=q.pop()
			self._led_off(led)

	def run(self):
		q=prio_queue(key_index=0,dedup_key = 1)
		nextev=0
		while True:
			self._read_ioq(q,nextev)
			self._consume_pending(q)
			if not q.is_empty():
				nextev=max([.1,q.peek().time-time()])
				#print("wait from",q.peek().time,"to",time())
			else:
				nextev=600
			#print("next in",nextev,"at",time()+nextev)
			
	def _calc_wait_for_next(self,q):
		if not q.is_empty():
			pass

	def _stop(self):
		[i.stop() for i in self.leds]

if __name__ == "__main__":
	b=Blinkenq()
	b.setDaemon(True)
	b.start()
	b.blink(0,1,2)
	b.blink(1,1,1)
	b.blink(2,1,0.5)
	l=0
	br=0
	t=0
	while l>=0:
		try:
			l,br,t=input("l b t>").split()
			l,br,t=int(l), int(br), float(t)
			b.blink(l,br,t)
		except Exception as e:
			print("Caught %s"%e)
	
	
