from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    times = lines[0].split(':')[1].split()    
    distances = lines[1].split(':')[1].split()
    total_time = 0
    for time in times:
        total_time = 10**len(time) * total_time + int(time)
    total_dist = 0
    for dist in distances:
        total_dist = 10**len(dist) * total_dist + int(dist)
    win = 0
    for i in range(total_time):
        if i * (total_time - i) > total_dist:
            win +=1
    # TODO: implement solution here!
    return win


INPUT_S = '''Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 71503


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
