
class restart_function:
    def __init__(self):
        pass

    def Comp_915(self, time, state):
        # time = float val
        # Component 915 Description: gas cylinder isolation valve
        if state == 'On':
            out = f'508 time 0 gt null 0 {time-1} n -1.0 "Open"\n'
            return out
        elif state == 'Off':
            out = '508 time 0 gt null 0 1.e6 n -1.0 "Off"\n'
            return out
