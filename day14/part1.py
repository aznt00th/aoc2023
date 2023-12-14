from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    squares = [0] * len(lines[0])
    rocks = [0] * len(lines[0])
    total_rows = len(lines)
    total_load = 0
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            if char == '#':
                squares[col_num] = row_num + 1
                rocks[col_num] = 0
            elif char == 'O':
                total_load += total_rows - squares[col_num] - rocks[col_num]
                rocks[col_num] += 1
    return total_load


INPUT_S = '''\
O....#....
O.OO#....#
.....##...
OO.#O....O
.O.....O#.
O.#..O.#.#
..O..#O..O
.......O..
#....###..
#OO..#....
'''
EXPECTED = 136


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
