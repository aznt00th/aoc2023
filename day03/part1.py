from __future__ import annotations

import argparse
import os.path
from typing import Dict
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def find_symbols(s: str)-> Dict:
    lines = s.splitlines()
    res = []
    for row, line in enumerate(lines):
        for col, char in enumerate(line):
            if not char.isdigit() and not char.isalpha() and char != '.':
                res += [(row + x_off, col + y_off) for x_off in [-1, 0, 1] for y_off in [-1, 0, 1]]
    return res



def compute(s: str) -> int:
    lines = s.splitlines()
    symbol_locations = find_symbols(s)
    res = 0
    for row, line in enumerate(lines):
        col=0
        curr = 0
        adj = False

        while col<len(line):
            if line[col].isdigit():
                curr = curr * 10 + int(line[col])
                if (row, col) in symbol_locations:
                    adj = True
                col+=1
            else:
                if adj:
                    res += curr
                adj = False
                curr = 0
                col += 1
        if adj:
            res += curr
    return res


INPUT_S = '''\
467..114..
...*......
..35..633.
......#...
617*......
.....+.58.
..592.....
......755.
...$.*....
.664.598..
'''
EXPECTED = 4361


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