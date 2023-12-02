from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

valid_digits = {'one': 1, 'two':2 , 'three':3, 'four':4,
                'five':5, 'six':6, 'seven':7,
                'eight':8, 'nine':9}

def parse_chunk(s:str)->int:
    if s[0] in '123456789':
        return int(s[0])
    for i in range(len(s)+1):
        if s[:i] in valid_digits:
            return valid_digits[s[:i]]
    raise ValueError

def compute(s: str) -> int:
    lines = s.splitlines()
    total = 0
    for line in lines:
        first_num, second_num = None, None
        for i in range(len(line)):
            try:
                val = parse_chunk(line[i:min(i+5, len(line))])
                if first_num is None:
                    first_num = val
                second_num = val
            except ValueError as e:
               pass
        total += 10 * first_num + second_num
    return total


INPUT_S = '''\
two1nine
eightwothree
abcone2threexyz
xtwone3four
4nineeightseven2
zoneight234
7pqrstsixteen
'''
EXPECTED = 281


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
