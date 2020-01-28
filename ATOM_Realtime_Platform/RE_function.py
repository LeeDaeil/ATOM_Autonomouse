
class restart_function:
    def __init__(self):
        pass

    def Comp_915(self, time, state):
        # time = float val
        # Component 915 Description: gas cylinder isolation valve
        if state == 'On':
            # 551 time 0 gt null 0 10.0 l -1.0 "PSV"
            out = f'551 time 0 gt null 0 1.e6 n -1.0 "Open"\n'
            return out
        elif state == 'Off':
            out = '551 time 0 gt null 0 10.0 l -1.0 "PSV"\n'
            return out
