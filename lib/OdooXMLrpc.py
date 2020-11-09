import os
import time
import json

from enum import Enum, unique, auto

from dicts import tz_dic

import xmlrpc.client as xmlrpclib
from socket import setdefaulttimeout as setTimeout

from . import Utils

class OdooXMLrpc:
    def __init__(self, Display):
        Utils.parameters["odooReachability"] = Utils.OdooState.toBeDefined
        Utils.parameters["odooIpPortOpen"]   = False
        Utils.parameters["odooUid"] = False
        Utils.getUIDfromOdoo()

    #@Utils.timer
    def registerAttendanceWithRASownTimestamp(self, card, timestamp):
        res=False
        try:
            serverProxy = Utils.getServerProxy("/xmlrpc/object")
            if serverProxy:
                setTimeout(float(Utils.settings["timeoutToRegisterAttendanceSync"]) or None)
                #print("timeoutToRegisterAttendanceSync: ", float(Utils.settings["timeoutToRegisterAttendanceSync"]) or None )
                res = serverProxy.execute(
                    Utils.settings["odooParameters"]["db"][0],
                    Utils.parameters["odooUid"],
                    Utils.settings["odooParameters"]["user_password"][0],
                    "hr.employee",
                    "registerAttendanceWithExternalTimestamp",
                    card,
                    timestamp,
                )
        except Exception as e:
            print("Odoo ln127 - registerAttendanceSync - exception e:",e)
            res = False
        except socket.timeout as e:
            print("timeout registerAttendanceSync odoo ln139", e)
            res=False
        finally:
            setTimeout(None)
            return res

    def registerAttendanceSync(self, card):
        res=False
        try:
            serverProxy = Utils.getServerProxy("/xmlrpc/object")
            if serverProxy:
                setTimeout(float(Utils.settings["timeoutToRegisterAttendanceSync"]) or None)
                #print("timeoutToRegisterAttendanceSync: ", float(Utils.settings["timeoutToRegisterAttendanceSync"]) or None )
                res = serverProxy.execute(
                    Utils.settings["odooParameters"]["db"][0],
                    Utils.parameters["odooUid"],
                    Utils.settings["odooParameters"]["user_password"][0],
                    "hr.employee",
                    "register_attendance",
                    card,
                )
        except Exception as e:
            print("Odoo - registerAttendanceSync - exception e:",e)
            res = False
        except socket.timeout as e:
            print("Odoo - timeout registerAttendanceSync - ", e)
            res=False
        finally:
            setTimeout(None)
            return res