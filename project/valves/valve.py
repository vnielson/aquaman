from enum import Enum
import piplates.RELAYplate as RELAY

##############################################################################
###### Customize the names of your relays by changing the labels below: ######
labels = ['Relay 1', 'Relay 2', 'Relay 3', 'Relay 4', 'Relay 5', 'Relay 6', 'Relay 7']
##############################################################################

RELAY.RESET(ppADDR)
status = range(7)
for i in range(7):
    status[i] = 'OFF'


@app.route("/")
@app.route("/<state>")
def update_relay(state=None):
    if state != None:
        rly = int(state[0])  # parse relay number
        action = state[2]  # parse action: 'n' for on and 'f' for off
        if action == 'n':
            RELAY.relayON(ppADDR, rly)
        if action == 'f':
            RELAY.relayOFF(ppADDR, rly)
        # Update the relay status
        mask = 1


class valve:

    class ValveStatus(Enum):
        CLOSED = 1
        OPEN   = 2
        ERROR  = 3

    def __init__(self, id, relayID ):
        self.id = id
        self.relayID = int(relayID)
        self.relayAddress = 0
        self.relayMask = 1 << relayID
        # set up the pin for output


    def valve_status(self):
        # returns the current valve status open, closed, error
        relayStates = RELAY.relaySTATE(self.relayAddress)
        valveStatus = ValveStatus.CLOSED
        if ((relayStates & self.relayMask) == 1):
            valveStatus = ValveStatus.OPEN

        return valveStatus


    def open_valve(self):
        # opens the valve and returns True on success or False on failure to open valve
        # if the valve is already open, True is returned

        return True


    def close_valve(self):
        # closes the valve and returns True on success or False on failure to close valve
        # if the valve is already closed, True is returned

        return True

