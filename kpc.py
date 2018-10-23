from keyPad import KeyPad
from ledBoard import LedBoard
from pathlib import Path


class KPC():
    def __init__(self, keypad, led_board,):
        assert isinstance(keypad, KeyPad)
        assert isinstance(led_board, LedBoard)
        #assert isinstance(password, str)
        self.keypad = keypad
        self.led_board = led_board
        #self._password = password
        self.passcode_accumulator = ''
        self.override_signal = ''
        self.led_id = ''  # used for turning a led on for a specific length of time
        self.led_duration = 0
        self._filename = 'password.txt'

    # keypad and led_board methods:
    def get_next_signal(self):
        if len(self.override_signal) > 0:
            signal = self.override_signal
            self.override_signal = ''
            return signal
        return self.keypad.get_next_signal()

    def light_one_led(self, led, seconds):
        self.led_board.light_led(led, seconds)

    def flash_leds(self, seconds):
        self.led_board.flash_all_leds(seconds)

    def twinkle_leds(self, seconds):
        self.led_board.twinkle_all_leds(seconds)

    def exit_action(self):
        self.led_board.powerdown()

    def lightshow(self):
        self.led_board.lightshow()

    # password_file stuff
    def _get_password(self):
        path = str(Path(self._filename).resolve())
        file = open(path)
        line = next(file)
        line = str(line).strip()
        file.close()
        return line

    def _set_password(self, password):
        path = str(Path(self._filename).resolve())
        file = open(path, 'w')
        file.write(password)
        file.close()

    # fsm actions:
    def init_passcode_entry(self, signal):
        self.reset_password_accumulator(signal)
        self.led_board.powerup()

    def reset_password_accumulator(self, signal):
        self.passcode_accumulator = ''

    def append_next_password_digit(self, signal):
        self.passcode_accumulator += signal

    def verify_password(self, signacl):
        if self._get_password() == self.passcode_accumulator:
            self.override_signal = 'Y'
            self.twinkle_leds(3)
        else:
            self.override_signal = 'N'
            self.flash_leds(3)

    def reset_agent(self, signal):
        self.passcode_accumulator = ''
        self.override_signal = ''
        self.led_id = ''
        self.led_duration = 0

    def fully_active_agent(self, signal):
        self.reset_agent(signal)

    def verify_new_password(self, signal):
        if len(self.passcode_accumulator) >= 4:
            self.override_signal = 'Y'
            self.twinkle_leds(3)
        else:
            self.override_signal = 'N'
            self.flash_leds(3)

    def set_led_id(self, signal):
        self.led_id = int(signal)

    def do_nothing(self, signal):
        return

    def append_next_time_digit(self, signal):
        self.led_duration += signal

    def turn_on_led(self, signal):
        seconds = float(self.led_duration)
        if self.led_id <= 6 and  self.led_id >= 1:
            self.light_one_led(self.led_id, seconds)
        else:
            self.lightshow()
        self.reset_agent(signal)

    def set_new__password(self, signal):
        self._set_password(self.passcode_accumulator)

    def shut_down(self, signal):
        self.reset_agent(signal)
        self.exit_action()
