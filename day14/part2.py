from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def spin_n(grid, width, height):
    tmp = [['.' for i in range(width)] for j in range(height)]
    for col in range(width):
        offset = 0
        for row in range(height):
            if grid[row][col] == '#':
                offset = row + 1
                tmp[row][col] = '#'
            elif grid[row][col] == 'O':
                tmp[offset][col] = 'O'
                offset += 1
    return tmp

def spin_s(grid, width, height):
    tmp = [['.' for i in range(width)] for j in range(height)]
    for col in range(width):
        offset = height - 1
        for row in range(1, height + 1):
            if grid[height - row][col] == '#':
                offset = height - row - 1
                tmp[height - row][col] = '#'
            if grid[height - row][col] == 'O':
                tmp[offset][col] = 'O'
                offset -= 1
    return tmp

def spin_w(grid, width, height):
    tmp = [['.' for i in range(width)] for j in range(height)]
    for row in range(height):
        offset = 0
        for col in range(width):
            if grid[row][col] == '#':
                offset = col + 1
                tmp[row][col] = '#'
            if grid[row][col] == 'O':
                tmp[row][offset] = 'O'
                offset += 1
    return tmp

def spin_e(grid, width, height):
    tmp = [['.' for i in range(width)] for j in range(height)]
    for row in range(height):
        offset = width - 1
        for col in range(1, width + 1):
            if grid[row][width - col] == '#':
                offset = width - col - 1
                tmp[row][width - col] = '#'
            if grid[row][width - col] == 'O':
                tmp[row][offset] = 'O'
                offset -= 1
    return tmp

def compute(s: str) -> int:
    lines = s.splitlines()
    squares = []
    circles = []
    width, height =len(lines[0]), len(lines)
    total_load = 0
    grid = [[''] * width for _ in range(height)]
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            grid[row_num][col_num] = char
    memo = {}
    TIMES = 1000000000
    for cnt in range(TIMES):
        grid = spin_n(grid, width, height)
        grid = spin_w(grid, width, height)
        grid = spin_s(grid, width, height)
        grid = spin_e(grid, width, height)
        key = tuple(tuple(i) for i in grid)
        if key in memo:
            diff = cnt - memo[key]
            TIMES = (TIMES - cnt) % diff - 1
            break
        memo[key] = cnt
    for cnt in range(TIMES):
        grid = spin_n(grid, width, height)
        grid = spin_w(grid, width, height)
        grid = spin_s(grid, width, height)
        grid = spin_e(grid, width, height)

    m,n = len(lines), len(lines[0])
    return sum((m-i) for i in range(m) for j in range(n) if grid[i][j] == 'O')


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
EXPECTED = 64


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
