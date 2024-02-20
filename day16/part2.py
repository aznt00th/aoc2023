from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def move_direction(direction, row, col):
    if direction == 'r':
        return row, col + 1
    if direction == 'l':
        return row, col - 1
    if direction == 'u':
        return row - 1, col
    return row + 1, col

def rotate(direction, char):
    if char == '/':
        if direction == 'r':
            return 'u'
        if direction == 'l':
            return 'd'
        if direction == 'u':
            return 'r'
        if direction == 'd':
            return 'l'
    if char == '\\':
        if direction == 'r':
            return 'd'
        if direction == 'l':
            return 'u'
        if direction == 'u':
            return 'l'
        if direction == 'd':
            return 'r'
        

def dp(lines, energized, memo, direction, row, col):
    key = (direction, row, col)
    if key in memo:
        return
    memo[key] = True
    if row <  0 or row >= len(lines) or col < 0 or col >= len(lines[0]):
        return
    char = lines[row][col]
    while char == '.' or (direction in 'lr' and char == '-') or (direction in 'ud' and char == '|') or (char in '\\/'):
        key = (direction, row, col)
        memo[key] = True
        if (char in '\\/'):
            energized[row][col] = '#'
            direction = rotate(direction, char)
            row, col =  move_direction(direction, row, col)
        else:
            energized[row][col] = '#'
            row, col = move_direction(direction, row, col)
        if row <  0 or row >= len(lines) or col < 0 or col >= len(lines[0]):
            return
        char = lines[row][col]
    if char in '-':
        energized[row][col] = '#'
        dp(lines, energized, memo, 'l', row, col - 1)
        dp(lines, energized, memo, 'r', row, col + 1)
    else:
        energized[row][col] = '#'
        dp(lines, energized, memo, 'u', row - 1, col)
        dp(lines, energized, memo, 'd', row + 1, col)

def calc_energy(lines, width, height, direction, row, col):
    energized = [ ["."] * width for _ in range(height)]
    dp(lines, energized, {}, direction, row, col)
    cnt = 0
    for row_num, line in enumerate(energized):
        for col_num, char in enumerate(line):
            if char == '#':
                cnt += 1
    return cnt

def compute(s: str) -> int:
    lines = s.splitlines()
    width, height = len(lines[0]), len(lines)
    res = 0
    for col in range(width):
        res = max(res, calc_energy(lines, width, height, 'd', 0, col))
        res = max(res, calc_energy(lines, width, height, 'u', height - 1, col))
    for row in range(height):
        res = max(res, calc_energy(lines, width, height, 'r', row, 0))
        res = max(res, calc_energy(lines, width, height, 'l', row, width - 1))
    return res


INPUT_S = r'''.|...\....
|.-.\.....
.....|-...
........|.
..........
.........\
..../.\\..
.-.-/..|..
.|....-|.\
..//.|....
'''
EXPECTED = 51


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
