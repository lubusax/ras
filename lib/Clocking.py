import time
import os
import subprocess
import logging
import threading

from . import routes, Utils

_logger = logging.getLogger(__name__)

class Clocking:
	def __init__(self, odoo, hardware):
		self.Odoo = odoo
		self.Buzz = hardware[0]  # Passive Buzzer
		self.Disp = hardware[1]  # Display
		self.Reader = hardware[2]  # Card Reader
		self.B_Down = hardware[3]  # Button Down
		self.B_OK = hardware[4]  # Button OK

		self.syncClockingMethods = {
			"notDefined"          : self.notDefined  ,
			"syncClockable"       : self.syncClockable  ,
			"instanceDown"        : self.instanceDown  ,
			"noInternet"          : self.noInternet  ,
			"userNotValidAnymore" : self.userNotValidAnymore  ,
		}

		self.asyncClockingMethods = {
			"notDefined"          : self.asyncClocking  ,
			"syncClockable"       : self.syncClockable  ,
			"instanceDown"        : self.asyncClocking ,
			"noInternet"          : self.asyncClocking  ,
			"userNotValidAnymore" : self.asyncClocking  ,
		}

	#@Utils.timer
	def syncClockable(self):
		try:
			res = self.Odoo.registerAttendanceSync(self.Reader.card)
			if res:
				self.employeeName = res["employee_name"]
				self.msg = res["action"]
			else:
				self.msg = "comm_failed"
		except Exception as e:
				print("exception in dotheclocking e:", e)

	def notDefined(self):
		self.msg = "comm_failed"

	def instanceDown(self):
		self.msg = "comm_failed"

	def noInternet(self):
		self.msg = "comm_failed"

	def userNotValidAnymore(self):
		self.msg = "comm_failed"

	def asyncClocking(self):
		self.msg = "comm_failed"		

	#@Utils.timer
	def card_logging(self):
		self.Disp.lockForTheClock = True
		self.Disp.display_msg("connecting")
		self.msg = "comm_failed"
		self.employeeName  = None

		print("clocking method ", Utils.parameters["odooReachability"])
		self.syncClockingMethods[Utils.parameters["odooReachability"].name]()
		
		self.Disp.display_msg(self.msg, self.employeeName)
		self.Buzz.Play(self.msg)

		time.sleep(Utils.settings["timeToDisplayResultAfterClocking"])
		self.Disp.lockForTheClock = False
		self.Disp.displayTime()

