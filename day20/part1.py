from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Flipflop():
    def __init__(self, dests, name):
        self.state = False
        self.dests = dests
        self.name = name

    def receive_pulse(self, pulse, source):
        if pulse:
            return None
        self.state = not self.state
        return self.state

    def get_state(self):
        return [self.state]

class Conjunction():
    def __init__(self, dests, name):
        self.state = {}
        self.dests = dests
        self.name = name

    def register_input(self, source):
        if source in self.state:
            return
        self.state[source] = False

    def receive_pulse(self,  pulse, source ):
        self.state[source] = pulse
        return not all([v for v in self.state.values()])
    def get_state(self):
        return [state for state in self.state.values()]

class Broadcaster():
    def __init__(self,dests):
        self.dests = dests
        self.name = 'broadcaster'
    def receive_pulse(self, pulse, source):
        return pulse


def compute(s: str) -> int:
    lines = s.splitlines()
    modules = {}
    for row_num, line in enumerate(lines):
        source, destinations = line.split(' -> ')[0], line.split(' -> ')[1]
        destinations = destinations.split(', ')
        if source == 'broadcaster':
            modules[source] = Broadcaster(destinations)
        elif source[0] == '%':
            modules[source[1:]] = Flipflop(destinations, source[1:])
        elif source[0] == '&':
            modules[source[1:]] = Conjunction(destinations, source[1:])
    initial_state= []
    for obj in modules.values():
        for dest in obj.dests:
            if isinstance(modules.get(dest), Conjunction):
                modules[dest].register_input(obj.name)
    for obj in modules.values():
        if not isinstance(obj, Broadcaster):
            initial_state += obj.get_state()
    tot_low = 0
    tot_high = 0
    num_iterations = 1000
    for iteration in range(num_iterations):
        curr_pulses = [('broadcaster', 0, 'button')]
        tot_low += 1
        while curr_pulses:
            signal = curr_pulses.pop(0)
            if signal[0] == 'output' or not modules.get(signal[0]):
                continue

            module = modules[signal[0]]
            pulse = signal[1]
            source = signal[2]

            response = module.receive_pulse(pulse, source)
            if response is not None:
                for dest in module.dests:
                    curr_pulses.append((dest, int(response), module.name))
                    if response:
                        tot_high += 1
                    else:
                        tot_low += 1
        current_state = []
        for obj in modules.values():
            if not isinstance(obj, Broadcaster):
                current_state += obj.get_state()
    return tot_low * tot_high


INPUT_S = '''\
broadcaster -> a
%a -> inv, con
&inv -> b
%b -> con
&con -> output
'''
EXPECTED = 11687500


@pytest.mark.parametrize(
    ('input_s', 'expected'),
    (
        (INPUT_S, EXPECTED),
    ),
)
def test(input_s: str, expected: int) -> None:
    assert compute(input_s) == expected


def main() -> int:
    parser = argparse.ArgumentParser()
    parser.add_argument('data_file', nargs='?', default=INPUT_TXT)
    args = parser.parse_args()

    with open(args.data_file) as f, support.timing():
        print(compute(f.read()))

    return 0


if __name__ == '__main__':
    raise SystemExit(main())
