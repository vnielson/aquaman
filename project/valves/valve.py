from enum import Enum
import piplates.RELAYplate as RELAY
import RPi.GPIO as GPIO  # import RPi.GPIO module
from project.core.aqualogger import valvelog

##############################################################################
###### Customize the names of your relays by changing the labels below: ######
labels = ['Relay 1', 'Relay 2', 'Relay 3', 'Relay 4', 'Relay 5', 'Relay 6', 'Relay 7']
##############################################################################

# RELAY.RESET(ppADDR)
# status = range(7)
# for i in range(7):
#     status[i] = 'OFF'


# def update_relay(state=None):
#     if state != None:
#         rly = int(state[0])  # parse relay number
#         action = state[2]  # parse action: 'n' for on and 'f' for off
#         if action == 'n':
#             RELAY.relayON(ppADDR, rly)
#         if action == 'f':
#             RELAY.relayOFF(ppADDR, rly)
#         # Update the relay status
#         mask = 1

# 1 = 0001
# 2 = 0010
# 3 = 0100
# 4 = 1000
class valve:

    def __init__(self, id, relayID ):
        GPIO.setmode(GPIO.BCM)  # choose BCM or BOARD
        # GPIO.setup(AA, GPIO.OUT)
        self.id = id
        self.relayID = int(relayID)
        self.relayAddress = 0
        self.relayMask = 1 << (relayID-1)
        # set up the pin for output

    def __del__(self):
        valvelog.debug("Valve Destructor called for Relay: ")
        valvelog.debug(self.relayID)

    def __str__(self):
        mask = "{0:b}".format(self.relayMask)
        ret_string = "Valve ID: {}  Relay Controller: {} Relay Address: {} Relay Mask: {}".format(self.id,self.relayID, self.relayAddress, mask)

        return ret_string

    def valve_status(self):
        valvelog.debug("Get Valve Status")
        valvelog.debug(self)
        # returns the current valve status open, closed, error
        relayStates = RELAY.relaySTATE(self.relayAddress)
        valvelog.debug("Relay States:")
        valvelog.debug(relayStates)
        valvelog.debug("Relay Mask:")
        valvelog.debug("{0:b}".format(self.relayMask))
        valvelog.debug(self.relayMask)
        valvelog.debug((relayStates & self.relayMask))
        valveStatus = "CLOSED"
        if ((relayStates & self.relayMask) != 0):
            valvelog.debug("Valve is open!")
            valveStatus = "OPEN"

        return valveStatus


    def open_valve(self):
        # opens the valve and returns True on success or False on failure to open valve
        # if the valve is already open, True is returned
        RELAY.relayON(0, self.relayID)

        vs = self.valve_status()
        valvelog.info("Open valve / relay : %d", self.relayID)

        if (vs == "OPEN"):
            valvelog.info("Open Success")
            return True
        else:
            valvelog.error("Open Failed on relay: %d ", self.relayID)
            return False


    def close_valve(self):
        # closes the valve and returns True on success or False on failure to close valve
        # if the valve is already closed, True is returned

        RELAY.relayOFF(0, self.relayID)

        vs = self.valve_status()
        valvelog.info("Close valve / relay : %d", self.relayID)

        if (vs == "CLOSED"):
            valvelog.info("Close Success")
            return True
        else:
            valvelog.error("Close Failed on relay: %d ", self.relayID)
            return False

