from keyPad import KeyPad
from ledBoard import LedBoard
from finite_state_machine import FSM
from kpc import KPC
import RPi.GPIO as GPIO


def main():
    led_board = LedBoard()
    keypad = KeyPad()
    kpc = KPC(keypad, led_board)
    fsm = FSM(kpc)
    try:
        fsm.main_loop()
    except KeyboardInterrupt:
        pass
    finally:
        GPIO.cleanup()


if __name__ == "__main__":
    main()
