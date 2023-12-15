from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:
    lines = s.splitlines()
    adjacencies = {}
    for row_num, line in enumerate(lines):
        for col_num, char in enumerate(line):
            if char == '.':
                continue
            if char == '-':
                adjacencies[(row_num, col_num)] = ((row_num, col_num - 1), (row_num, col_num + 1))
            if char == '|':
                adjacencies[(row_num, col_num)] = ((row_num-1, col_num ), (row_num+1, col_num))
            if char == '7':
                adjacencies[(row_num, col_num)] = ((row_num, col_num - 1), (row_num+1, col_num))
            if char == 'J':
                adjacencies[(row_num, col_num)] = ((row_num, col_num - 1), (row_num -1, col_num))
            if char == 'F':
                adjacencies[(row_num, col_num)] = ((row_num+ 1, col_num), (row_num, col_num + 1))
            if char == 'L':
                adjacencies[(row_num, col_num)] =  ((row_num - 1, col_num), (row_num, col_num + 1))
            if char == 'S':
                start = (row_num, col_num)
    unchecked = [(*start, 0)]
    visited = {}
    max_steps = 0
    while True:
        if len(unchecked) == 0:
            break
        current = unchecked.pop()
        if current in visited:
            continue
        if current == (*start,0):
            visited[start] = 0
            adj_8 = [(start[0] + i, start[1] + j) for i in [-1, 0, 1] for j in [-1, 0, 1] if (i!=0) or (j!=0)]
            for adjacency in adj_8:
                if not adjacencies.get(adjacency):
                    continue
                if start in adjacencies[adjacency]:
                    unchecked.append((*adjacency, 1))
                    max_steps = max(max_steps, 1)
            continue
        r, c, s = current
        visited[(r,c)] = s
        for r1, c1 in adjacencies[(r,c)]:
            if not (r1,c1) in visited:
                unchecked.append((r1, c1, s + 1))
                max_steps = max(max_steps, s+1)
    return int((max_steps + 1)/ 2)


            
                
    # TODO: implement solution here!
    return 0


INPUT_S = '''\
..F7.
.FJ|.
SJ.L7
|F--J
LJ...
'''
EXPECTED = 8


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