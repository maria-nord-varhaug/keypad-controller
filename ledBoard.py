import RPi.GPIO as GPIO  # Burde vaere installert paa rp
import time

class LedBoard():
    #  0=L, 1=H, -1=Input
    def __init__(self):
        GPIO.setmode(GPIO.BCM)  # Gjeur at du ikke direkte kobler til pinnummeret, men til "label" pinnr
        self.pins = [18, 23, 24]
        self.ledmodes = [
            [1, 0, -1],  # led1
            [0, 1, -1],  # led2
            [-1, 1, 0],  # led3
            [-1, 0, 1],  # led4
            [1, -1, 0],  # led5
            [0, -1, 1]   # led6
        ]

    def set_io(self, pin, mode):
        if mode == -1:
            GPIO.setup(pin, GPIO.IN)
            return
        GPIO.setup(pin, GPIO.OUT)
        GPIO.output(pin, mode)  # GPIO.HIGH == 1, GPIO.LOW == 0 <3 <3 <3

    def _turn_on_led(self, led_nr):                                # Tar inn int mellom 0 5
        for pin_index, pin in enumerate(self.pins):             # (0,18),(1,23),(2,24)
            self.set_io(pin, self.ledmodes[led_nr][pin_index])   # (18, ledmodes[ledNr][0]) , ...

    def _turn_off_led(self):
        for pin_index, pin in enumerate(self.pins):             # setter rett og slett alle pinene til input
            self.set_io(pin, -1)                                # som er det samme som aa slaa av lysene

    def light_led(self, led_nr, duration):     # turn on one of the 6 leds for <duration> seconds
        self._turn_on_led(led_nr)              # and then making the appropriate HIGH/LOW settings on the output pins
        time.sleep(duration)
        self._turn_off_led()

    def flash_all_leds(self, duration):      # Flash all 6 LEDs on and off for <duration> seconds
        t = start_time = time.time()         # tiden i euyeblikket metoden blir kjeurt
        while t - start_time < duration:    # sjekker etter hver for loop om starttid - naatid < duration
            for led in range(0, 5):
                self.light_led(led, 0.01)     # Vet ikke helt hvor lenge hvert skal flashe
            time.sleep(1)                  # 0.5 sekunder mellom hvert blink <3
            t = time.time()

    def twinkle_all_leds(self, duration):  # Turn all LEDs on and off in sequence for <duration> seconds
        start_time = t = time.time()
        led_nr = 0
        while t - start_time < duration:   # For aa holde oss under duration
            self.light_led(led_nr % 6, 0.2)  # 0,1,2,3,4,5 -> 0,1,2,3,4,5 -> 0,1,2,3, ...
            led_nr += 1
            t = time.time()

    def powerup(self):                     # lyssekvens under oppstart, tar 6 sek.
        start_time = t = time.time()
        while t - start_time < 2:
            for led in range(0,2):
                self.light_led(led, 0.01)
        while t - start_time > 2 and t - start_time < 4:
            for led in range(0,4):
                self.light_led(led, 0.01)
        while t - start_time > 4 and t - start_time < 6:
            for led in range(0,6):
                self.light_led(led, 0.01)

    def powerdown(self):            # lyssekvens shutdown
        start_time = t = time.time()
        while t - start_time < 2:
            for led in range(0, 6):
                self.light_led(led, 0.01)
        while t - start_time > 2 and t - start_time < 4:
            for led in range(0, 4):
                self.light_led(led, 0.01)
        while t - start_time > 4 and t - start_time < 6:
            for led in range(0, 2):
                self.light_led(led, 0.01)

def ledTest():
    l = LedBoard()
    l.light_led(5,5)
    l.flash_all_leds(6)
    l.twinkle_all_leds(2)
    l.powerup()
    l.powerdown()

if __name__ == "__main__":
    ledTest()






