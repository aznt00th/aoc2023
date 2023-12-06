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
    times = [int(time) for time in times]
    distances = [int(dist) for dist in distances]
    res = 1
    for time, dist in zip(times, distances):
        i = 0
        while True:
            if i*(time - i) > dist:
                break
            i += 1
        j = time
        while True:
            if j*(time - j) > dist:
                break
            j-=1
        res *= j - i + 1
    # TODO: implement solution here!
    return res


INPUT_S = '''Time:      7  15   30
Distance:  9  40  200
'''
EXPECTED = 288


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
