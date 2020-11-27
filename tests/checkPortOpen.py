import sys

sys.path.append("/home/pi/ras/lib")
sys.path.append("/home/pi/ras/dicts")
sys.path.append("/home/pi/ras")

print(sys.path)

#from lib import Display
from lib import Utils

print("is port open?",Utils.isIpPortOpen( ("marmenorda.com",443) ) )
