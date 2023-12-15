from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    curr = []
    patterns = []
    res = 0
    for line in lines:
        if line:
            curr.append(line)
        else:
            patterns.append(curr)
            curr = []
    patterns.append(curr)
    for pattern in patterns:
        row_reflections = 0
        col_reflections = 0
        for row_num, line in enumerate(pattern[:-1]):
            match = 0
            for col_num in range(len(line)):
                i = 0
                while True:
                    if row_num - i < 0:
                        break
                    if row_num + i + 1 >= len(pattern):
                        break
                    if pattern[row_num - i][col_num] != pattern[row_num + i+ 1][col_num]:
                        match +=1
                    if match > 1:
                        break
                    i+=1
                if match > 1:
                    break
            if match == 1:
                row_reflections += row_num + 1
        for col_num in range(len(pattern[0])-1):
            match = 0
            for row_num in range(len(pattern)):
                i = 0
                while True:
                    if col_num - i < 0:
                        break
                    if col_num + i + 1 >= len(pattern[0]):
                        break
                    if pattern[row_num][col_num - i] != pattern[row_num][col_num + i + 1]:
                        match += 1
                    if match > 1:
                        break
                    i += 1 
                if match > 1:
                    break
            if match == 1:
                col_reflections += col_num + 1
        res += row_reflections * 100 + col_reflections
    return res


INPUT_S = '''\
#.##..##.
..#.##.#.
##......#
##......#
..#.##.#.
..##..##.
#.#.##.#.

#...##..#
#....#..#
..##..###
#####.##.
#####.##.
..##..###
#....#..#
'''
EXPECTED = 400


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
