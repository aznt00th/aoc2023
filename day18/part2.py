from __future__ import annotations

import argparse
import os.path
import numpy as np
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

direction_map = 'RDLU'

def process_hex(line):
    h = line.split('#')[1]
    direction = int(h[-2])
    h = h[:-2]
    return direction_map[direction],int(h,16)

def compute(s: str) -> int:
    lines = s.splitlines()
    curr_r = 0
    curr_d = 0
    tot_dist = 0
    row_indices, col_indices = [], []
    for line in lines:
        char, dist  = process_hex(line)
        if char == 'R':
            curr_r += dist
        if char == 'D':
            curr_d += dist
        if char == 'L':
            curr_r -= dist
        if char == 'U':
            curr_d -= dist
        tot_dist += dist
        row_indices.append(curr_d)
        col_indices.append(curr_r)
    
    inside = 0
    cnt = 0
    x = 0.5*( np.abs(np.dot(row_indices, np.roll(col_indices,1)) - np.dot(col_indices, np.roll(row_indices, 1))) )
    return int(x + 1 + tot_dist/2) 


INPUT_S = '''\
R 6 (#70c710)
D 5 (#0dc571)
L 2 (#5713f0)
D 2 (#d2c081)
R 2 (#59c680)
D 2 (#411b91)
L 5 (#8ceee2)
U 2 (#caa173)
L 1 (#1b58a2)
U 2 (#caa171)
R 2 (#7807d2)
U 3 (#a77fa3)
L 2 (#015232)
U 2 (#7a21e3)
'''
EXPECTED = 952408144115


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
