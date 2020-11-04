import os
import time
import json
import logging

from enum import Enum, unique, auto

from dicts import tz_dic

import xmlrpc.client as xmlrpclib
from socket import setdefaulttimeout as setTimeout

from . import Utils

_logger = logging.getLogger(__name__)


class OdooXMLrpc:
    def __init__(self, Display):
        self.display            = Display
        self.adm                = False
        Utils.parameters["odooReachability"] = Utils.OdooState.notDefined
        Utils.parameters["odooIpPortOpen"]   = False
        self.getUIDfromOdoo()
        _logger.debug("Odoo XMLrpc Class Initialized")

    #@Utils.timer
    def getUIDfromOdoo(self):
        #print("in method getUIDfromOdoo , the Odoo Params are: ", Utils.settings["odooParameters"])
        Utils.setTimeZone()
        Utils.setOdooUrlTemplate()
        Utils.setOdooIpPort()
        self.setUserID()
        print("got user id from Odoo ", self.uid)                                                                  
         
    #@Utils.timer
    def setUserID(self):
        self.uid = False
        returnValue = False
        try:
            loginServerProxy = Utils.getServerProxy("/xmlrpc/common")
            setTimeout(float(Utils.settings["timeoutToGetOdooUID"]) or None)
            #print("timeoutToGetOdooUID: ", float(Utils.settings["timeoutToGetOdooUID"]) or None )
            user_id = loginServerProxy.login(
                Utils.settings["odooParameters"]["db"][0],
                Utils.settings["odooParameters"]["user_name"][0],
                Utils.settings["odooParameters"]["user_password"][0])
            if user_id:
                print("got user id from Odoo ", user_id)
                self.uid = user_id
                Utils.storeOptionInDeviceCustomization("odooConnectedAtLeastOnce", True)
                returnValue =  True
            else:
                print("NO user id from Odoo ", user_id)
                returnValue =  False
        except ConnectionRefusedError as e:
            print("ConnectionRefusedError registerAttendanceSync odoo ln139", e)
            _logger.debug(ConnectionRefusedError)
            returnValue =  False
        except socket.timeout as e:
            print("timeout registerAttendanceSync odoo ln139", e)
            returnValue = False
        except OSError as osError:
            print("osError registerAttendanceSync odoo ln139", osError)
            _logger.debug(OSError)
            if "No route to host" in str(osError):
                self.display.display_msg("noRouteToHost")
                time.sleep(1.5)
            returnValue =  False 
        except Exception as e:
            _logger.exception(e)
            print("exception in method setUserID: ", e)
            returnValue =  False
        finally:
            setTimeout(None)
            return returnValue

    #@Utils.timer
    def registerAttendanceSync(self, card):
        res=False
        try:
            serverProxy = Utils.getServerProxy("/xmlrpc/object")
            if serverProxy:
                setTimeout(float(Utils.settings["timeoutToregisterAttendanceSync"]) or None)
                #print("timeoutToregisterAttendanceSync: ", float(Utils.settings["timeoutToregisterAttendanceSync"]) or None )
                res = serverProxy.execute(
                    Utils.settings["odooParameters"]["db"][0],
                    self.uid,
                    Utils.settings["odooParameters"]["user_password"][0],
                    "hr.employee",
                    "register_attendance",
                    card,
                )
        except Exception as e:
            print("Odoo ln127 - registerAttendanceSync - exception e:",e)
            _logger.exception(e)
            res = False
        except socket.timeout as e:
            print("timeout registerAttendanceSync odoo ln139", e)
            res=False
        finally:
            setTimeout(None)
            return res