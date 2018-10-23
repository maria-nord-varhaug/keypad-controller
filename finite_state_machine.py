from rule import Rule
from kpc import KPC


class FSM():
    def __init__(self, kpc):
        self.rules = []
        self.states = ['S-init', 'S-read', 'S-verify', 'S-active',
                       'S-read-2', 'S-verify-2', 'S-logout', 'S-led',
                       'S-time', 'S-done']
        self.current_state = self.states[0]  # S-init
        assert isinstance(kpc, KPC)
        self.kpc = kpc

    def add_rule(self, rule):
        # add new rule to FSM's rule list
        assert isinstance(rule, Rule)
        self.rules.append(rule)

    def get_next_signal(self):
        # query KPC agent for next sinal
        return self.kpc.get_next_signal()

    def run_rules(self, symbol):
        # go through rule list; fire first matching rule
        for rule in self.rules:
            if rule.match(self.current_state, symbol):
                self.fire_rule(rule, symbol)
                return

    def fire_rule(self, rule, symbol):
        # change FSM state and call kpc action method
        self.current_state = rule.state2
        rule.action(self.kpc, symbol)

    def rule_init(self):
        self.add_rule(Rule(self.state('S-init'), self.state('S-read'), self.all_signals, KPC.init_passcode_entry))

        self.add_rule(Rule(self.state('S-read'), self.state('S-read'), self.all_digits, KPC.append_next_password_digit))
        self.add_rule(Rule(self.state('S-read'), self.state('S-verify'), '*', KPC.verify_password))
        self.add_rule(Rule(self.state('S-read'), self.state('S-read'), self.all_signals, KPC.reset_agent))

        self.add_rule(Rule(self.state('S-verify'), self.state('S-active'), 'Y', KPC.fully_active_agent))
        self.add_rule(Rule(self.state('S-verify'), self.state('S-read'), self.all_signals, KPC.reset_agent))

        self.add_rule(Rule(self.state('S-active'), self.state('S-read-2'), '*', KPC.reset_password_accumulator))
        self.add_rule(Rule(self.state('S-active'), self.state('S-led'), self.all_digits, KPC.set_led_id))
        self.add_rule(Rule(self.state('S-active'), self.state('S-logout'), '#', KPC.do_nothing))

        self.add_rule(Rule(self.state('S-led'), self.state('S-led'), self.all_digits, KPC.set_led_id))
        self.add_rule(Rule(self.state('S-led'), self.state('S-time'), '*', KPC.do_nothing))
        self.add_rule(Rule(self.state('S-led'), self.state('S-active'), self.all_signals, KPC.fully_active_agent))

        self.add_rule(Rule(self.state('S-time'), self.state('S-time'), self.all_digits, KPC.append_next_time_digit))
        self.add_rule(Rule(self.state('S-time'), self.state('S-active'), self.all_signals, KPC.turn_on_led))

        self.add_rule(Rule(self.state('S-read-2'), self.state('S-read-2'), self.all_digits, KPC.append_next_password_digit))
        self.add_rule(Rule(self.state('S-read-2'), self.state('S-verify-2'), '*', KPC.verify_new_password))
        self.add_rule(Rule(self.state('S-read-2'), self.state('S-active'), self.all_signals, KPC.fully_active_agent))

        self.add_rule(Rule(self.state('S-verify-2'), self.state('S-active'), 'Y', KPC.set_new__password))
        self.add_rule(Rule(self.state('S-verify-2'), self.state('S-active'), self.all_signals, KPC.fully_active_agent))

        self.add_rule(Rule(self.state('S-logout'), self.state('S-init'), '#', KPC.shut_down))
        self.add_rule(Rule(self.state('S-logout'), self.state('S-active'), self.all_signals, KPC.fully_active_agent))

    def state(self, state):
        assert state in self.states, 'State not in self.states'
        return state

    def main_loop(self):
        # begin in FSM's default init state, repeatedly call
        # get_next_signal and run_rules until the FSM enter its
        # deafult final state
        self.current_state = self.state('S-init')
        self.rule_init()
        while self.current_state != self.state('S-done'):
            symbol = self.get_next_signal()
            self.run_rules(symbol)

    # Methods for rule:
    @staticmethod
    def all_digits(signal):
        return 48 <= ord(signal) <= 57

    @staticmethod
    def all_signals(signal):
        return signal is not None

    def all_states(self, state):
        return self.state(state)


