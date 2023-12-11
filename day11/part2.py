from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    galaxies = []
    lines = s.splitlines()
    cols = [False] * len(lines[0])
    rows = [False] * len(lines)
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            if char == '#':
                galaxies.append((row_num, col_num))
                rows[row_num] = True
                cols[col_num] = True
    for index, col in reversed(list(enumerate(cols))):
        if not col:
            for gi, (gr, gc) in enumerate(galaxies):
                if gc >= index:
                    galaxies[gi] = (gr, gc+999999)
    for index, row in reversed(list(enumerate(rows))):
        if not row:
            for gi, (gr, gc) in enumerate(galaxies):
                if gr >= index:
                    galaxies[gi] = (gr + 999999, gc)
    res = 0
    for i, (g1r, g1c) in enumerate(galaxies):
        for j, (g2r, g2c)  in enumerate(galaxies[i:]):
           res += abs(g2r - g1r) + abs(g2c - g1c)
    return res


INPUT_S = '''\
...#......
.......#..
#.........
..........
......#...
.#........
.........#
..........
.......#..
#...#.....
'''
EXPECTED = 1030


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
