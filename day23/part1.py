from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

dr = [0, 1, 0, -1]
dc = [1, 0, -1, 0]
direction_symbols = '>v<^'
reverse_symbols = '<^>v'

def valid_neighbours(r,c,traversed, grid):
    valid = []
    
    num_rows, num_cols = len(grid), len(grid[0])
    for i in range(4):
        new_r = r + dr[i]
        new_c = c + dc[i]
        if new_c <0 or new_c >= num_cols or new_r < 0 or new_r >= num_rows:
            continue
        if grid[new_r][new_c] != '#' and (new_r, new_c) not in traversed and reverse_symbols[i] != grid[new_r][new_c]:
            valid.append((new_r, new_c))
    return valid


def dfs(memo, grid, num_rows, num_cols, traversed, r, c):
    if r == num_rows - 1 and c == num_cols -2:
        return 0
    key = (r, c)
    if key in memo:
        return memo[key]
    res = 0
    cnt = 0
    traversed = set(traversed)
    traversed.add(key)
    
    while grid[r][c] in direction_symbols or (grid[r][c] == '.' and len(valid_neighbours(r,c, traversed, grid)) == 1):
        if grid[r][c] in direction_symbols:
            index = direction_symbols.index(grid[r][c])
            r = r + dr[index]
            c = c + dc[index]
        else:
            r,c = valid_neighbours(r,c, traversed, grid)[0]
        traversed.add((r, c))
        cnt += 1
    if r == num_rows - 1 and c == num_cols -2:
        res = cnt
    elif grid[r][c] == '.':
        vis = True
        for i in range(4):
            new_r = r + dr[i]
            new_c = c + dc[i]
            if new_c <0 or new_c >= num_cols or new_r < 0 or new_r >= num_rows:
                continue
            if grid[new_r][new_c] != '#' and (new_r, new_c) not in traversed and reverse_symbols[i] != grid[new_r][new_c]:
                res = max(res, 1 + cnt + dfs(memo, grid, num_rows, num_cols, traversed, new_r, new_c))
    memo[key] = res
    return res

def compute(s: str) -> int:
    lines = s.splitlines()
    start = (0, 1)
    num_rows, num_cols = len(lines), len(lines[0])
    return dfs({}, lines, num_rows, num_cols, (), start[0], start[1])
    # TODO: implement solution here!
    return 0


INPUT_S = '''\
#.#####################
#.......#########...###
#######.#########.#.###
###.....#.>.>.###.#.###
###v#####.#v#.###.#.###
###.>...#.#.#.....#...#
###v###.#.#.#########.#
###...#.#.#.......#...#
#####.#.#.#######.#.###
#.....#.#.#.......#...#
#.#####.#.#.#########v#
#.#...#...#...###...>.#
#.#.#v#######v###.###v#
#...#.>.#...>.>.#.###.#
#####v#.#.###v#.#.###.#
#.....#...#...#.#.#...#
#.#########.###.#.#.###
#...###...#...#...#.###
###.###.#.###v#####v###
#...#...#.#.>.>.#.>.###
#.###.###.#.###.#.#v###
#.....###...###...#...#
#####################.#
'''
EXPECTED = 154


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
