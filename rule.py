from inspect import isfunction


class Rule():
    def __init__(self, state1, state2, signal, action):
        self.state1 = state1
        self.state2 = state2
        self.signal = signal
        self.action = action

    def match(self, state, symbol):
        if isfunction(self.signal) and isfunction(self.state1):
            return self.signal(symbol) and self.state1(state)
        if not isfunction(self.signal) and not isfunction(self.state1):
            return self.signal == symbol and state == self.state1
        if not isfunction(self.signal) and isfunction(self.state1):
            return self.signal == symbol and self.state1(state)
        if isfunction(self.signal) and not isfunction(self.state1):
            return self.signal(symbol) and state == self.state1
        else:
            print('Rule match error')
