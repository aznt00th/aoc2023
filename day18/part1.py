from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    max_right = 0
    max_down = 0
    curr_r = 0
    curr_d = 0
    min_right = 0
    min_down = 0
    for line in lines:
        char, dist, _ = line.split()
        dist = int(dist)
        if char == 'R':
            curr_r += dist
        if char == 'D':
            curr_d += dist
        if char == 'L':
            curr_r -= dist
        if char == 'U':
            curr_d -= dist
        max_right = max(max_right, curr_r)
        max_down = max(max_down, curr_d)
        min_right = min(min_right, curr_r)
        min_down = min(min_down, curr_d)
        
    grid = [['.'] * (max_right + 1- min_right) for _ in range(max_down + 1- min_down)]
    curr_r, curr_d = -min_right, -min_down
    prev_dir = 'R'
    tot_dist = 0
    for line in lines:
        char, dist, _ = line.split()
        dist = int(dist)
        tot_dist += dist
        if prev_dir == 'R' and char == 'D':
            grid[curr_d][curr_r] = '7'
        if prev_dir == 'R' and char == 'U':
            grid[curr_d][curr_r] = 'J'
        if prev_dir == 'L' and char == 'D':
            grid[curr_d][curr_r] = 'F'
        if prev_dir == 'L' and char == 'U':
            grid[curr_d][curr_r] = 'L'
        if prev_dir == 'U' and char == 'L':
            grid[curr_d][curr_r] = '7'
        if prev_dir == 'U' and char == 'R':
            grid[curr_d][curr_r] = 'F'
        if prev_dir == 'D' and char == 'L':
            grid[curr_d][curr_r] = 'J'
        if prev_dir == 'D' and char == 'R':
            grid[curr_d][curr_r] = 'L'
        for i in range(dist):
            if char == 'R':
                curr_r += 1
            if char == 'D':
                curr_d += 1
            if char == 'L':
                curr_r -= 1
            if char == 'U':
                curr_d -= 1
            if char in 'LR':
                grid[curr_d][curr_r] = '-'
            if char in 'UD':
                grid[curr_d][curr_r] = '|'
                
        prev_dir = char
    grid[-min_down][-min_right] = 'F'
    inside = 0
    cnt = 0
    for row_num, line in enumerate(grid):
        inside = False
        for col_num, char in enumerate(line):
            if char in "|JL":
                inside = not inside
            elif inside and char == '.':
                cnt += 1
    return cnt  + tot_dist


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
EXPECTED = 62


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
