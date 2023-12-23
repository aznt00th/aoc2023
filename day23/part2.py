from __future__ import annotations

import argparse
import os.path
from collections import deque
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
        if grid[new_r][new_c] != '#' and (new_r, new_c) not in traversed :
            valid.append((new_r, new_c))
    return valid

def compute(s: str) -> int:
    lines = s.splitlines()
    start = (0, 1)
    nodes = set()
    num_rows, num_cols = len(lines), len(lines[0])
    for row_num, row in enumerate(lines):
        for col_num, char in enumerate(row):
            if char != '#':
                if len(valid_neighbours(row_num,col_num,set(), lines)) >2:
                    nodes.add((row_num, col_num))
    nodes.add((0,1))
    nodes.add((num_rows - 1, num_cols - 2))
    edges = {}
    for (node_row, node_col) in nodes:
        edges[(node_row,node_col)] = []
        queue = deque([(node_row,node_col,0)])
        visited = set()
        while queue:
            row, col, dist = queue.popleft()
            if (row,col) in visited:
                continue
            visited.add((row, col))
            if (row, col) in nodes and (row, col) != (node_row, node_col):
                edges[(node_row, node_col)].append(((row, col), dist))
                continue
            for i in range(4):
                new_row = row + dr[i]
                new_col = col + dc[i]
                if 0 <= new_row < num_rows and 0<= new_col < num_cols and lines[new_row][new_col] != '#':
                    queue.append((new_row, new_col, dist + 1))
    ans = 0
    SEEN = [[False for _ in range(num_cols)] for _ in range(num_rows)]
    seen = set()
    def dfs(v,d):
        nonlocal ans
        r,c = v
        if SEEN[r][c]:
            return
        SEEN[r][c] = True
        if r==num_rows-1:
            ans = max(ans, d)
        for (y,yd) in edges[v]:
            dfs(y,d+yd)
        SEEN[r][c] = False
    dfs(start,0)
    return ans
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
