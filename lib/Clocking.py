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

		self.timeToDisplayResult = Utils.settings["timeToDisplayResultAfterClocking"] #1.4 seconds for example

		self.msg = False    # determines Melody to play and/or Text to display depending on Event happened: for example check in,
												# check out, communication with odoo not possible ...

		self.employeeName       = None

	#@Utils.timer
	def doTheClocking(self):
		try:
			res = self.Odoo.registerAttendanceSync(self.Reader.card)
			if res:
				self.employeeName = res["employee_name"]
				self.msg = res["action"]
			else:
				self.msg = "comm_failed"
		except Exception as e:
				print("exception in dotheclocking e:", e)

	#@Utils.timer
	def card_logging(self):
		self.Disp.lockForTheClock = True
		self.Disp.display_msg("connecting")

		if self.Odoo.uid and self.odooReachable: # check if the uid was set after running SetParams
				# print("do the Clocking ")
				if self.isWifiStable():
						self.doTheClocking()
				else:
						self.msg = "no_wifi"
		else:
				self.msg = "comm_failed"
		
		self.Disp.display_msg(self.msg, self.employeeName)
		self.Buzz.Play(self.msg)

		time.sleep(self.timeToDisplayResult)
		self.Disp.lockForTheClock = False
		self.Disp._display_time(Utils.parameters["wifiSignalQualityMessage"], Utils.parameters["odooReachabilityMessage"])

