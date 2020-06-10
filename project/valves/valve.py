from enum import Enum

class valve:

    class ValveStatus(Enum):
        CLOSED = 1
        OPEN   = 2
        ERROR  = 3

    def __init__(self, id, bcmpin):
        self.id = id
        self.bcmpin = int(bcmpin)
        # set up the pin for output


    def valve_status(self):
        # returns the current valve status open, closed, error

        print("Checking valve status for id {}:".format(self.id))
        current_status = ValveStatus.CLOSED

        return current_status


    def open_valve(self):
        # opens the valve and returns True on success or False on failure to open valve
        # if the valve is already open, True is returned

        return True


    def close_valve(self):
        # closes the valve and returns True on success or False on failure to close valve
        # if the valve is already closed, True is returned

        return True

