import threading
import time
import json
import os
import socket
import copy
import functools
import subprocess

import xmlrpc.client as xmlrpclib

from enum import Enum, unique, auto

from socket import setdefaulttimeout as setTimeout

from dicts import tz_dic

WORK_DIR                      = "/home/pi/ras/"
fileDeviceCustomization       = WORK_DIR + "dicts/deviceCustomization.json"
fileDeviceCustomizationSample = WORK_DIR + "dicts/deviceCustomization.sample.json"
fileDataJson                  = WORK_DIR + "dicts/data.json"
fileCredentials               = WORK_DIR + "dicts/credentials.json"
dirAttendanceData             = WORK_DIR + "attendanceData/"
fileKnownRFIDcards            = dirAttendanceData + "knownRFIDcards.json"

settings                      = {} # settings are more permanent than parameters, they are user defined and stored in a file 
parameters                    = {} # parameters change more frequently and show the different states in the device
defaultMessagesDic            = {}
credentialsDic                = {}
defaultCredentialsDic         = {"username": ["admin"], "new password": ["admin"], "old password": ["password"]}

@unique
class OdooState(Enum): # Odoo Reachability State
    toBeDefined             =auto()
    syncClockable           =auto()
    instanceDown            =auto()
    noInternet              =auto()
    userNotValidAnymore     =auto()

# syncClockingMethods = {
#   "toBeDefined"          : self.toBeDefined  ,
#   "syncClockable"       : self.syncClockable  ,
#   "instanceDown"        : self.instanceDown  ,
#   "noInternet"          : self.noInternet  ,
#   "userNotValidAnymore" : self.userNotValidAnymore  ,
# }

# asyncClockingMethods = {
#   "toBeDefined"          : self.asyncClocking  ,
#   "syncClockable"       : self.syncClockable  ,
#   "instanceDown"        : self.asyncClocking ,
#   "noInternet"          : self.asyncClocking  ,
#   "userNotValidAnymore" : self.asyncClocking  ,
# }

def timer(func):
  @functools.wraps(func)
  def wrapper_timer(*args, **kwargs):
    tic = time.perf_counter()
    value = func(*args, **kwargs)
    toc = time.perf_counter()
    elapsed_time = toc - tic
    print("Elapsed time: {1:0.4f} seconds - Function: {0}".format(func, elapsed_time))
    return value
  return wrapper_timer

class Timer:
  def __init__(self, howLong):
    self.reset()
    self.howLong = howLong

  def reset(self):
    self.startTime = time.perf_counter()

  def elapsedTime(self):
    return (time.perf_counter()- self.startTime)

  def isElapsed(self):
    if self.elapsedTime() > self.howLong:
      return True
    return False

def returnAlwaysValidFlag(externalExitFlag = None):
  if externalExitFlag:
    exitFlag= externalExitFlag
  else:
    exitFlag = threading.Event()
    exitFlag.clear()
  
  return exitFlag

def waitUntilOneButtonIsPressed(button1, button2, externalExitFlag = None):
   
  exitFlag = returnAlwaysValidFlag(externalExitFlag)

  periodScan = 0.2 # seconds

  waitTilButtonOnePressed = threading.Thread(target=button1.threadWaitTilPressed, args=(exitFlag,periodScan,))
  waitTilButtonTwoPressed = threading.Thread(target=button2.threadWaitTilPressed, args=(exitFlag,periodScan,))

  waitTilButtonOnePressed.start()
  waitTilButtonTwoPressed.start()

  waitTilButtonOnePressed.join()
  waitTilButtonTwoPressed.join() 

def bothButtonsPressedLongEnough (button1, button2, periodCheck, howLong, externalExitFlag = None):
  
  exitFlag = returnAlwaysValidFlag(externalExitFlag)

  ourTimer = Timer(howLong)
  button1.poweron()
  button2.poweron()
  
  exitFlag.wait(periodCheck) # we have to wait, the buttons dont work inmediately after power on

  while not exitFlag.isSet():
    while button1.isPressed() and button2.isPressed():
      exitFlag.wait(periodCheck)
      if ourTimer.isElapsed():
        return True
    ourTimer.reset()

  return False # this should never happen

def setButtonsToNotPressed(button1,button2):
  if button1: button1.pressed=False
  if button2: button2.pressed=False

#@timer
def getJsonData(filePath):
  try:
    with open(filePath) as f:
      data = json.load(f)
    return data  
  except Exception as e:
    print("exception while getting/loading data from json file: ", filePath, " -exception: ", e)
    #_logger.exception(e):
    return None

def storeJsonData(filePath,data):
  try:
    with open(filePath, 'w+') as f:
      json.dump(data,f, sort_keys=True, indent=2)
    return True
  except:
    return False

def beautifyJsonFile(filePath):
  try:
    data=getJsonData(filePath)
    storeJsonData(filePath,data)
    return True
  except:
    return False

def storeOptionInJsonFile(filePath,option,optionValue):
  data = getJsonData(filePath)
  if data:
      data[option] = optionValue
      if storeJsonData(filePath, data):
          return True
      else:
          return False
  else:
      return False

@timer
def isPingable(address):
  response = os.system("ping -c 1 " + address)
  if response == 0:
      pingstatus = True
  else:
      pingstatus = False # ping returned an error
  return pingstatus

def isIpPortOpen(ipPort): # you can not ping ports, you have to use connect_ex for ports
  s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
  try:
    s.settimeout(2)
    canConnectResult = s.connect_ex(ipPort)
    if canConnectResult == 0:
      #print("Utils - IP Port OPEN ", ipPort)
      ipPortOpen = True
    else:
      #print("Utils - IP Port CLOSED ", ipPort)
      ipPortOpen = False
  except Exception as e:
    print("Utils - exception in method isIpPortOpen: ", e)
    ipPortOpen = False
  finally:
    s.close()
  return ipPortOpen

def getOptionFromKey(dataDic, key):
  try:
    value = dataDic[key]
    return value
  except:
    return None

def getOptionFromDeviceCustomization(option, defaultValue):
  try:
    data = getJsonData(fileDeviceCustomization)
    value = getOptionFromKey(data,option) or defaultValue
    storeOptionInDeviceCustomization(option,value)
    return value
  except:
    return None

def storeOptionInDeviceCustomization(option,value):
  try:
    storeOptionInJsonFile(fileDeviceCustomization,option,value) # stores in file
    settings[option]= value # stores on the running program
    return True
  except:
    return False

def initializeSettings(): # getSettingsFromDeviceCustomization
  settings["language"]                = getOptionFromDeviceCustomization("language"                 , defaultValue = "ENGLISH")
  settings["showEmployeeName"]        = getOptionFromDeviceCustomization("showEmployeeName"         , defaultValue = "yes")
  settings["fileForMessages"]         = getOptionFromDeviceCustomization("fileForMessages"          , defaultValue = "messagesDicDefault.json")
  settings["messagesDic"]         = getJsonData(WORK_DIR + "dicts/" + settings["fileForMessages"])
  settings["SSIDreset"]               = getOptionFromDeviceCustomization("SSIDreset"                , defaultValue = "__RAS__")
  settings["defaultMessagesDic"]  = getJsonData(WORK_DIR + "dicts/messagesDicDefault.json")
  settings["odooParameters"]          = getOptionFromDeviceCustomization("odooParameters"           , defaultValue = None)
  settings["odooConnectedAtLeastOnce"]= getOptionFromDeviceCustomization("odooConnectedAtLeastOnce" , defaultValue = False)
  settings["flask"]                   = getOptionFromDeviceCustomization("flask"                    , defaultValue = defaultCredentialsDic)
  settings["timeoutToGetOdooUID"]     = getOptionFromDeviceCustomization("timeoutToGetOdooUID"      , defaultValue = 6.0)
  settings["ssh"]                     = getOptionFromDeviceCustomization("ssh"                      , defaultValue = "enable")
  settings["sshPassword"]             = getOptionFromDeviceCustomization("sshPassword"              , defaultValue = "raspberry")  
  settings["firmwareVersion"]         = getOptionFromDeviceCustomization("firmwareVersion"          , defaultValue = "v1.4.4+")
  settings["timeoutToRegisterAttendanceSync"]   = getOptionFromDeviceCustomization("timeoutToRegisterAttendanceSync"  , defaultValue = 3.0)
  settings["periodEvaluateReachability"]        = getOptionFromDeviceCustomization("periodEvaluateReachability"       , defaultValue = 5.0)
  settings["periodDisplayClock"]                = getOptionFromDeviceCustomization("periodDisplayClock"               , defaultValue = 10.0)
  settings["timeToDisplayResultAfterClocking"]  = getOptionFromDeviceCustomization("timeToDisplayResultAfterClocking" , defaultValue = 1.2)
  settings["clockingSyncOrAsync"]                = getOptionFromDeviceCustomization("clockingSyncOrAsync"           , defaultValue = "sync")
  settings["periodSyncOStime"]                    = getOptionFromDeviceCustomization("periodSyncOStime"               , defaultValue = 3610)

def getMsg(textKey):
  try:
    return settings["messagesDic"][textKey] 
  except KeyError:
    return settings["defaultMessagesDic"][textKey]
  except:
    return None

def getMsgTranslated(textKey):
  try:
    print("textKey in getMsgTranslated ", textKey)
    msgTranslated = getMsg(textKey)[settings["language"]]       
    return copy.deepcopy(msgTranslated)
  except Exception as e:
    print("in getMsgTranslated() exception: ", e)
    if textKey == "listOfLanguages":
      return ["ENGLISH"]
    else:
      return [[0, 0], 20," "]

def getListOfLanguages(defaultListOfLanguages = ["ENGLISH"]):
  try:
    return getMsg("listOfLanguages")
  except:
    return defaultListOfLanguages

def transferDataJsonToDeviceCustomization(deviceCustomizationDic):
  dataJsonOdooParameters = getJsonData(fileDataJson)
  if dataJsonOdooParameters:
    deviceCustomizationDic["odooParameters"] = dataJsonOdooParameters
    deviceCustomizationDic["odooConnectedAtLeastOnce"] = True
  else:
    deviceCustomizationDic["odooConnectedAtLeastOnce"] = False
  return deviceCustomizationDic

def storeOdooParamsInDeviceCustomization(newOdooParams):
  try:
    storeOptionInDeviceCustomization("odooParameters",newOdooParams)
    return True
  except:
    return False

def handleMigratioOfDeviceCustomizationFile():
  '''
  if there is no "DeviceCustomization" File,
  take the sample file
  if there is a "DeviceCustomization" File,
  add the Fields in newOptionsList
  '''
  deviceCustomizationDic        = getJsonData(fileDeviceCustomization)
  deviceCustomizationSampleDic  = getJsonData(fileDeviceCustomizationSample)
  newOptionsList = ["SSIDreset","fileForMessages","firmwareVersion","ssh",
        "sshPassword", "timeoutToGetOdooUID", "timeoutToCheckAttendance",
        "periodEvaluateReachability", "periodDisplayClock", "timeToDisplayResultAfterClocking",
        "clockingSyncOrAsync", "periodSyncOStime" ]
  if deviceCustomizationDic:
    for option in newOptionsList:
      if not(option in deviceCustomizationDic) and (option in deviceCustomizationSampleDic):
        deviceCustomizationDic[option] = deviceCustomizationSampleDic[option]
  else:
    deviceCustomizationDic = copy.deepcopy(deviceCustomizationSampleDic)
    deviceCustomizationDic = transferDataJsonToDeviceCustomization(deviceCustomizationDic)
  #print("deviceCustomizationDic: ", deviceCustomizationDic)
  storeJsonData(fileDeviceCustomization,deviceCustomizationDic)

def handleMigrationOfCredentialsJson():
  credentialsDic = getJsonData(fileCredentials)
  if not credentialsDic:
    credentialsDic = defaultCredentialsDic
  storeOptionInDeviceCustomization("flask",credentialsDic)

def ensureNtplibModule():
  print("in module ensureNtplibModule")
  try:
    import ntplib
  except ImportError:
    print("trying to install ntplib module")
    os.system("sudo pip3 install ntplib")
    print("module ntplib installed!")

def handleMigrationOfDataJson():
  try:
    data = getJsonData(fileDataJson)
    print("in handleMigrationOfDataJson - read dict from data.json", data)
    if data and storeOptionInDeviceCustomization("odooParameters",data): # in data.json the Odoo Params are stored when a successful connection was made
      if os.path.isfile(Utils.fileDataJson):
        os.system("sudo rm " + Utils.fileDataJson)
      storeOptionInDeviceCustomization("odooConnectedAtLeastOnce", True)
  except Exception as e:
    print("in handleMigrationOfDataJson - Exception while trying to transfer data.json to deviceCustomization file: ", e)

def initializeParameters():
  parameters["wifiSignalQualityMessage"]  = getMsgTranslated("noWiFiSignal")[2]
  parameters["wifiStable"] = False
  parameters["odooReachability"] = OdooState.toBeDefined
  parameters["odooReachabilityMessage"] = getMsgTranslated(parameters["odooReachability"].name)[2]
  parameters["odooUid"] = None
  parameters["odooIpPortOpen"]   = False
  parameters["callsUntilSyncOStime"] = -1
  odooReachabilityMessage      = parameters["odooReachability"].name

def initializeKnownRFIDCards():
  parameters["knownRFIDcards"] = getJsonData(fileKnownRFIDcards)
  if not parameters["knownRFIDcards"]:
    print("in Utils.initializeParameters() - trying to create fileKnownRFIDcards")
    parameters["knownRFIDcards"] ={}
    try:
      os.mkdir(dirAttendanceData)
    except FileExistsError:
      try: 
        os.mknod(fileKnownRFIDcards)
      except FileExistsError:
        print("in Utils.initializeParameters() - fileKnownRFIDcards existed already")


  print("in Utils.initializeParameters() - parameters[knownRFIDcards]", parameters["knownRFIDcards"])
  print("in Utils.initializeParameters() - parameters[odooReachability].name ", parameters["odooReachability"].name)
  print("in Utils.initializeParameters() - wifiSignalQualityMessage: ", parameters["wifiSignalQualityMessage"])
  print("in Utils.initializeParameters() - odooReachabilityMessage: ", parameters["odooReachabilityMessage"])
 
def isOdooUsingHTTPS():
  if  "https" in settings["odooParameters"].keys():
    if settings["odooParameters"]["https"]== ["https"]:
      return True
  return False

def getOwnIpAddress():
  command = "hostname -I | awk '{ print $1}' "
  ipAddress = (subprocess.check_output(command, shell=True).decode("utf-8").strip("\n"))
  storeOptionInDeviceCustomization("ownIpAddress",[ipAddress])
  return ipAddress

def enableSSH():
  try:
    os.system("sudo systemctl enable ssh")
    os.system("sudo service ssh start")
  except Exception as e:
    print("Exception in method Utils.enableSSH: ", e)

def disableSSH():
  try:
    os.system("sudo systemctl disable ssh")
    os.system("sudo service ssh stop")
  except Exception as e:
    print("Exception in method Utils.disableSSH: ", e)

def isWlan0Active():
  iwconfig_out = subprocess.check_output("iwconfig wlan0", shell=True).decode("utf-8")
  if "Access Point: Not-Associated" in iwconfig_out:
    wlan0Active = False
  else:
    wlan0Active = True
  return wlan0Active

  #@Utils.timer

def getDictWithWlan0Status():
  iwresult = subprocess.check_output("iwconfig wlan0", shell=True).decode("utf-8")
  resultdict = {}
  for iwresult in iwresult.split("  "):
    if iwresult:
      if iwresult.find(":") > 0:
        datumname = iwresult.strip().split(":")[0]
        datum = (
            iwresult.strip()
            .split(":")[1]
            .split(" ")[0]
            .split("/")[0]
            .replace('"', "")
        )
        resultdict[datumname] = datum
      elif iwresult.find("=") > 0:
        datumname = iwresult.strip().split("=")[0]
        datum = (
            iwresult.strip()
            .split("=")[1]
            .split(" ")[0]
            .split("/")[0]
            .replace('"', "")
        )
        resultdict[datumname] = datum
  return resultdict

#@Utils.timer
def evaluateWlan0Stability():
  if isWlan0Active():
    strength = int(getDictWithWlan0Status()["Signal level"])  # in dBm
    if strength >= 79:
      parameters["wifiSignalQualityMessage"]  = "\u2022" * 1 + "o" * 4
      parameters["wifiStable"] = False
    elif strength >= 75:
      parameters["wifiSignalQualityMessage"]  = "\u2022" * 2 + "o" * 3
      parameters["wifiStable"] = True
    elif strength >= 65:
      parameters["wifiSignalQualityMessage"]  = "\u2022" * 3 + "o" * 2
      parameters["wifiStable"] = True
    elif strength >= 40:
      parameters["wifiSignalQualityMessage"]  = "\u2022" * 4 + "o" * 1
      parameters["wifiStable"] = True
    else:
      parameters["wifiSignalQualityMessage"]  = "\u2022" * 5
      parameters["wifiStable"] = True
  else:
    parameters["wifiSignalQualityMessage"]  = getMsgTranslated("noWiFiSignal")[2]
    parameters["wifiStable"] = False

  print("in Utils.evaluateWlan0Stability() - wifiSignalQualityMessage: ", parameters["wifiSignalQualityMessage"])
  print("in Utils.evaluateWlan0Stability() - odooReachabilityMessage: ", parameters["odooReachabilityMessage"])

#@Utils.timer
def evaluateOdooReachability():
  try:
    evaluateWlan0Stability()

    print("in evaluateOdooReachability(), settings[odooIpPort] ", settings["odooIpPort"] )

    parameters["odooIpPortOpen"]  = isIpPortOpen(settings["odooIpPort"])

    if not parameters["wifiStable"]:
      parameters["odooReachability"] = OdooState.noInternet
    elif not parameters["odooIpPortOpen"]:
      parameters["odooReachability"] = OdooState.instanceDown
    elif not parameters["odooUid"]:   
      setUserID()
      if parameters["odooUid"]:
        parameters["odooReachability"] = OdooState.syncClockable
      else:         
        parameters["odooReachability"] = OdooState.userNotValidAnymore
    else:
      parameters["odooReachability"] = OdooState.syncClockable            

    print("odooIpPortOpen ", parameters["odooIpPortOpen"])
    print("wifiStable ", parameters["wifiStable"])
    print("odooReachability State Name ", parameters["odooReachability"].name)

    parameters["odooReachabilityMessage"] = getMsgTranslated(parameters["odooReachability"].name)[2]

    print("odooReachabilityMessage", parameters["odooReachabilityMessage"])
  except Exception as e:
    print("exception in evaluateOdooReachability ", e)
    parameters["odooIpPortOpen"]    = False
    parameters["wifiStable"]        = False
    parameters["odooReachability"]  = OdooState.toBeDefined

def setOdooIpPort():
  settings["odooIpPort"] = None
  try:
    print( "settings[""odooParameters""][""odoo_port""][0] ",settings["odooParameters"]["odoo_port"][0])
    if settings["odooParameters"]["odoo_port"]!=[""]: 
        portNumber =  int(settings["odooParameters"]["odoo_port"][0])                          
    elif isOdooUsingHTTPS():
        portNumber =   443
    settings["odooIpPort"] = (settings["odooParameters"]["odoo_host"][0], portNumber)
    print("in setOdooIpPort() ", settings["odooIpPort"])
    return True
  except Exception as e:
    print("exception in method setOdooIpPort: ", e)
    return False

def setTimeZone():
  try:
    os.environ["TZ"] = tz_dic.tz_dic[settings["odooParameters"]["timezone"][0]]
    time.tzset()
    print("in setTimeZone() tz:", tz_dic.tz_dic[settings["odooParameters"]["timezone"][0]])
    return True
  except Exception as e:
    print("exception in method setTimeZone: ", e)
    return False

def setOdooUrlTemplate():
  try:
    
    if isOdooUsingHTTPS():
      settings["odooUrlTemplate"] = "https://%s" % settings["odooParameters"]["odoo_host"][0]
    else:
      settings["odooUrlTemplate"] = "http://%s" % settings["odooParameters"]["odoo_host"][0]

    if settings["odooParameters"]["odoo_port"][0]:
      settings["odooUrlTemplate"] += ":%s" % settings["odooParameters"]["odoo_port"][0]
    print("in setOdooUrlTemplate() - settings[odooUrlTemplate] ",settings["odooUrlTemplate"] )
    return True
  except Exception as e:
    settings["odooUrlTemplate"]    = None
    # print("exception in method setOdooUrlTemplate: ", e)
    return False

def getServerProxy(url):
  try:
    serverProxy = xmlrpclib.ServerProxy(settings["odooUrlTemplate"] + str(url))
    print("in serverProxy etServerProxy(url): ", serverProxy)
    return serverProxy
  except Exception as e:
    print("exception in serverProxy :", e)
    return False 

def resetOdooParams():
  storeOptionInDeviceCustomization("odooConnectedAtLeastOnce", False)
  storeOptionInDeviceCustomization("odooParameters", None)

def syncOStimeWithTimeServer():
  try:
    import ntplib
    client = ntplib.NTPClient()
    response = client.request('pool.ntp.org')
    os.system('date ' + time.strftime('%m%d%H%M%Y.%S',time.localtime(response.tx_time)))
    print('in syncWithTimeServer - Succesfully sync :', response.tx_time)    
  except Exception as e:
    print('in syncWithTimeServer - Could not sync with time server. Exception:', e)

def syncOStimeWhenStipulated():
  if parameters["callsUntilSyncOStime"] <0:
    parameters["callsUntilSyncOStime"] = int(settings["periodSyncOStime"]/settings["periodDisplayClock"])+1 
    syncOStimeWithTimeServer()
  else:
    parameters["callsUntilSyncOStime"] -= 1
  print('in syncOStimeWhenStipulated - callsUntilSyncOStime at exit', parameters["callsUntilSyncOStime"])  

#@timer
def setUserID():
  parameters["odooUid"] = None
  returnValue = False
  try:
    loginServerProxy = getServerProxy("/xmlrpc/common")
    setTimeout(float(settings["timeoutToGetOdooUID"]) or None)
    print("timeoutToGetOdooUID: ", float(settings["timeoutToGetOdooUID"]) or None )
    user_id = loginServerProxy.login(
      settings["odooParameters"]["db"][0],
      settings["odooParameters"]["user_name"][0],
      settings["odooParameters"]["user_password"][0])
    if user_id:
        #print("_"*80)
        print("setUserID - got user id from Odoo ", user_id)
        #print("_"*80)
        parameters["odooUid"] = user_id
        storeOptionInDeviceCustomization("odooConnectedAtLeastOnce", True)
        returnValue =  True
    else:
        print("NO user id from Odoo ", user_id)
        returnValue =  False
  except ConnectionRefusedError as e:
      print("ConnectionRefusedError registerAttendanceSync odoo ln139", e)
      returnValue =  False
  except socket.timeout as e:
      print("timeout registerAttendanceSync odoo ln139", e)
      returnValue = False
  except OSError as osError:
      print("osError Utils.setuserID ", osError)
      # if "No route to host" in str(osError): pass
      returnValue =  False 
  except Exception as e:
      print("exception in method setUserID: ", e)
      returnValue =  False
  finally:
      setTimeout(None)
      return returnValue

#@timer
def getUIDfromOdoo():
    #print("in method getUIDfromOdoo , the Odoo Params are: ", settings["odooParameters"])
    setTimeZone()
    setOdooUrlTemplate()
    setOdooIpPort()
    setUserID()
    if not parameters["odooUid"] and not settings["odooConnectedAtLeastOnce"]:
      resetOdooParams()
    #print("getUIDfromOdoo - got user id from Odoo ", parameters["odooUid"] )

#@timer
def registerAttendanceWithRASownTimestamp(card, timestamp):
  res=False
  try:
    serverProxy = getServerProxy("/xmlrpc/object")
    if serverProxy:
      setTimeout(float(settings["timeoutToRegisterAttendanceSync"]) or None)
      res = serverProxy.execute(
        settings["odooParameters"]["db"][0],
        parameters["odooUid"],
        settings["odooParameters"]["user_password"][0],
        "hr.employee",
        "registerAttendanceWithExternalTimestamp",
        card,
        timestamp,
        )
  except Exception as e:
      print("registerAttendanceWithRASownTimestamp - exception e:",e)
      res = False
  except socket.timeout as e:
      print("timeout registerAttendanceWithRASownTimestamp", e)
      res=False
  finally:
      setTimeout(None)
      return res

def registerAttendanceSync(self, card):
  res=False
  try:
    serverProxy = getServerProxy("/xmlrpc/object")
    if serverProxy:
      setTimeout(float(settings["timeoutToRegisterAttendanceSync"]) or None)
      #print("timeoutToRegisterAttendanceSync: ", float(settings["timeoutToRegisterAttendanceSync"]) or None )
      res = serverProxy.execute(
        settings["odooParameters"]["db"][0],
        parameters["odooUid"],
        settings["odooParameters"]["user_password"][0],
        "hr.employee",
        "register_attendance",
        card,
        )
  except Exception as e:
    print("registerAttendanceSync - exception e:",e)
    res = False
  except socket.timeout as e:
    print("timeout registerAttendanceSync - ", e)
    res=False
  finally:
    setTimeout(None)
    return res

def migrationToCurrentVersion():
  handleMigratioOfDeviceCustomizationFile()
  handleMigrationOfCredentialsJson()
  handleMigrationOfDataJson()
  ensureNtplibModule()

def initializeDevice():
  migrationToCurrentVersion()
  initializeSettings()
  initializeParameters()
  initializeKnownRFIDCards()
  getUIDfromOdoo()

def attendanceIDtoTimestamp(id):
  try:
    now= id[0:4]+"-"+id[4:6]+"-"+id[6:8]+" "+id[8:10]+":"+id[10:12]+":"+id[12:]
  except Exception as e:
    print("exception in attendanceIDtoTimestamp - e:", e)
    now= False
  finally:
    return now

def registerLastAttendanceInFile(card, attendanceID, employeeName, checkINorCheckOUT):
  parameters["knownRFIDcards"][card] = {"attendanceID": attendanceID, "employeeName": employeeName, "checkINorCheckOUT": checkINorCheckOUT }
  print("in registerLastAttendanceInFile - registered for card:", card, "parameters[knownRFIDcards][card]: ", parameters["knownRFIDcards"][card])
  storeJsonData(fileKnownRFIDcards,parameters["knownRFIDcards"])

def storeAttendanceInFileToSendItToOdooLater(card, attendanceID, checkINorCheckOUT):
  pass