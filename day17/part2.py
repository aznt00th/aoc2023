from __future__ import annotations

import argparse
import os.path
import sys
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def update_visited(visited, key, lines, current_dist):
    row, col, drow, dcol, consecutive = key
    if row < 0 or row >= len(lines) or col < 0 or col >= len(lines[0]):
        return False, None
    new_dist = current_dist + int(lines[row][col])
    if not key in visited:
        visited[key] = [sys.maxsize] * 10 # 0th index is 1 consecutive
        for i in range(consecutive - 1, 10):
            visited[key][i] = new_dist
        return True, new_dist
    else:
        updated = False
        current =  visited[key]
        for i in range(9, consecutive - 2, -1):
            if new_dist < current[i]:
                current[i] = new_dist
                updated = True
    return updated, new_dist
    

def compute(s: str) -> int:
    lines = s.splitlines()
    width, height = len(lines[0]), len(lines)
    current_mins = {} # key: []
    to_explore = [( 1,0, 1,0, 1, int(lines[1][0])), ( 0,1, 0,1, 1, int(lines[0][1]))] # (pos) (dir), consecutive, dist
    while to_explore:
        (row, col, drow, dcol, consecutive, dist) = to_explore.pop(0)
        if row == height - 1 and col == width - 1 and consecutive >=4 and consecutive < 10:
            return dist
        if drow:
            rotated_drow = 0
            rotated_dcol = 1
        else:
            rotated_drow = 1
            rotated_dcol = 0 
        first_key = (row + rotated_drow, col + rotated_dcol, rotated_drow, rotated_dcol, 1)
        second_key = (row - rotated_drow, col - rotated_dcol, -rotated_drow, -rotated_dcol, 1)
        third_key = (row + drow, col + dcol, drow, dcol, consecutive + 1)
        if consecutive >= 4:
            updated, new_dist = update_visited(current_mins, second_key, lines, dist)
            if updated:
                to_explore.append((*second_key, new_dist))
            updated, new_dist = update_visited(current_mins, first_key, lines, dist)
            if updated:
                to_explore.append((*first_key, new_dist))
        if consecutive < 10:
            updated, new_dist = update_visited(current_mins, third_key, lines, dist)
            if updated:
                to_explore.append((*third_key, new_dist))
        to_explore.sort(key=lambda x: x[5])

        
    return 0


INPUT_S = '''\
2413432311323
3215453535623
3255245654254
3446585845452
4546657867536
1438598798454
4457876987766
3637877979653
4654967986887
4564679986453
1224686865563
2546548887735
4322674655533
'''
EXPECTED = 94


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
