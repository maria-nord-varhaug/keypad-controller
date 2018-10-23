# The ﬁle for this code should also include the all-important
# declarations of which Raspberry Pi pins
# serve as inputs and outputs to the keypad code.

# Keypad object that serves as an interface between the Keypad
# Controller agent and the physical keypad

import RPi.GPIO as GPIO
import time

_row0 = 18
_row1 = 23
_row2 = 24
_row3 = 25
_rowpins = [_row0, _row1, _row2, _row3]

_col0 = 17
_col1 = 27
_col2 = 6 #22
_colpins = [_col0, _col1, _col2]


class KeyPad():
#setup, do polling og get next signal metoder

    def __init__(self):
        self.ordliste = {1: '1', 2: '2', 3: '3', 4: '4', 5: '5', 6: '6', 7: '7', 8: '8', 9: '9', 10: '*', 11: '0', 12: '#'}
        GPIO.setmode(GPIO.BCM) #GPIO.BCM option means that you are referring to the pins
        for rp in _rowpins:
            GPIO.setup(rp, GPIO.OUT)
        for cp in _colpins:
            GPIO.setup(cp, GPIO.IN, pull_up_down = GPIO.PUD_DOWN) #The use of PUD DOWN declares that the pin will employ a pull-down resistor

    def is_actually_high(self, cp):
        x = 0
        is_still_high = True
        while x <= 20 and is_still_high is True:
            x += 1
            if GPIO.input(cp) == GPIO.HIGH:
                is_still_high = True
            else:
                is_still_high = False
            time.sleep(0.01)
        return is_still_high


#går igjennom radene først
    def do_pulling(self): #used to determine which (if any) key is currently being pressed
        for rp in _rowpins:
            GPIO.output(rp, GPIO.HIGH) #må sette den høy for at det skal kunne gå strøm
            for cp in _colpins:
                if GPIO.input(cp) == GPIO.HIGH:
                    keydict = 1 + 3*_rowpins.index(rp) + _colpins.index(cp)
                    if self.is_actually_high(cp):
                        return self.ordliste[keydict]
            GPIO.output(rp, GPIO.LOW)
        return None


    def get_next_signal(self):
        x = self.do_pulling()
        while x is None:
            x = self.do_pulling()
        print(x)  # TODO remove
        return x

    def __exit__(self, exc_type, exc_val, exc_tb):
        GPIO.cleanup()


def test_keypad():
    try:
        k = KeyPad()
        while True:
            signal = k.get_next_signal()
            print(signal)
    except KeyboardInterrupt:
        print('CTRL + C')
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    test_keypad()
