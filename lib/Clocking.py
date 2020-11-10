import time
import os
import subprocess
import logging
import threading

from . import routes, Utils

_logger = logging.getLogger(__name__)

class Clocking:
	def __init__(self, hardware):

		self.Buzz = hardware[0]  # Passive Buzzer
		self.Disp = hardware[1]  # Display
		self.Reader = hardware[2]  # Card Reader
		self.B_Down = hardware[3]  # Button Down
		self.B_OK = hardware[4]  # Button OK

		self.clockingMethods = {
				"sync": {
					"notDefined"          : self.notDefined  ,
					"syncClockable"       : self.syncClocking  ,
					"instanceDown"        : self.instanceDown  ,
					"noInternet"          : self.noInternet  ,
					"userNotValidAnymore" : self.userNotValidAnymore 
				},
				"async": {
					"notDefined"          : self.asynchronousHandler  ,
					"syncClockable"       : self.asynchronousHandler  ,
					"instanceDown"        : self.asynchronousHandler  ,
					"noInternet"          : self.asynchronousHandler  ,
					"userNotValidAnymore" : self.asynchronousHandler
				}
			}
		
		self.action = {
			"check_in": "check_out",
			"check_out": "check_in",
			"FALSE":"FALSE"
		}

	def registerLastAttendanceLocally(self, card, attendanceID, employeeName, checkINorCheckOUT):
		Utils.parameters["knownRFIDcards"][card] = {"attendanceID": attendanceID, "employeeName": employeeName, "checkINorCheckOUT": checkINorCheckOUT }
		print("in registerLocally - registered for card:", card, "Utils.parameters[knownRFIDcards][card]: ", Utils.parameters["knownRFIDcards"][card])
		Utils.storeJsonData(Utils.fileKnownRFIDcards,Utils.parameters["knownRFIDcards"])

	#@Utils.timer
	def asynchronousHandler(self): 
		print( "in asynchronousHandler ")
		try:
			attendanceID = time.strftime("%Y%m%d%H%M%S", time.gmtime() )
			now = Utils.attendanceIDtoTimestamp(attendanceID)			
			print( "in asynchronousHandler - attendanceID: ", attendanceID)
			print( "in asynchronousHandler - now: ", now)
			card = self.Reader.card
			self.employeeName = Utils.parameters["knownRFIDcards"][card]["employeeName"]
			self.msg = self.action[Utils.parameters["knownRFIDcards"][card]["checkINorCheckOUT"]]
			self.registerLastAttendanceLocally(card, attendanceID, self.employeeName, self.msg)
			#self.storeAttendanceInOdoo(card, attendanceID)
		except Exception as e:
			print("exception in asynchronousHandler e:", e)

	def storeAttendanceInOdoo(self, card, attendanceID): 
		print( "in storeAttendanceInOdoo ")
		try:
			timestamp = Utils.attendanceIDtoTimestamp(attendanceID)			
			print( "in storeAttendanceInOdoo - card: ", card)
			print( "in storeAttendanceInOdoo - timestamp: ", timestamp)
			res = Utils.registerAttendanceWithRASownTimestamp(card, timestamp)
			if res:
				print("in storeAttendanceInOdoo - res: ", res)
				success = True
			else:
				success = False
		except Exception as e:
			print("exception in storeAttendanceInOdoo e:", e)
			success = False
		finally:
			return success

	#@Utils.timer
	def syncClocking(self):
		try:
			res = Utils.registerAttendanceSync(self.Reader.card)
			if res:
				self.employeeName = res["employee_name"]
				self.msg = res["action"]
				print("in syncClockable - res: ", res)
				attendanceID = time.strftime("%Y%m%d%H%M%S", time.gmtime() )
				self.registerLastAttendanceLocally(self.Reader.card, attendanceID, self.employeeName, res["action"])
			else:
				self.msg = "comm_failed"
		except Exception as e:
				print("exception in dotheclocking e:", e)

	def notDefined(self):
		self.msg = "comm_failed"

	def instanceDown(self):
		self.Disp.display_msg("noRouteToHost")
		time.sleep(1.5)
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

		print("clocking method ", self.clockingMethods[Utils.settings["clockingSyncOrAsync"]][Utils.parameters["odooReachability"].name])
		self.clockingMethods[Utils.settings["clockingSyncOrAsync"]][Utils.parameters["odooReachability"].name]()
		
		self.Disp.display_msg(self.msg, self.employeeName)
		self.Buzz.Play(self.msg)

		time.sleep(Utils.settings["timeToDisplayResultAfterClocking"])
		self.Disp.lockForTheClock = False
		self.Disp.displayTime()

