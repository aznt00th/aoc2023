from __future__ import annotations

import argparse
import os.path

import pytest
import itertools
import support
import math

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    instructions = lines[0]
    tree = {}
    current = []
    for line in lines[1:]:
        if not line:
            continue
        key = line.split('=')[0].replace(' ','')
        if key[2] == 'A':
            current.append(key)
        left, right = line.split('=')[1].split(',')[0], line.split('=')[1].split(',')[1]
        left = left.strip().replace('(', '')
        right = right.strip().replace(')','')
        tree[key] = (left, right)



    steps = 0
    cycle_lengths = []
    p = False
    print(current)
    for curr in current:
        cycle_length = 0
        start = None
        steps = 0
        end = None
        visited = {}
        while True :
            instruction = instructions[steps%len(instructions)]
            if instruction == 'R':
                curr = tree[curr][1]
            if instruction == 'L':
                curr = tree[curr][0]
            cycle_length += 1
            instruction = instruction + str(steps%len(instructions))
            steps +=1
            if curr not in visited:
                visited[curr] = {}
                visited[curr][instruction] = (0, cycle_length)
            else:
                if not instruction in visited[curr]:
                    visited[curr][instruction] = (0, cycle_length)
                else:
                    if not start:
                        start = visited[curr][instruction][1]
                    else:
                        if curr.endswith('Z'):
                            offset = visited[curr][instruction][1]
                    visited[curr][instruction] = (visited[curr][instruction][0] + 1, visited[curr][instruction][1])
                    if visited[curr][instruction][0] == 2:
                        end = cycle_length
                        break
        cycle_lengths.append([start, offset, end-start])
    return math.lcm(*[i[1] for i in cycle_lengths])


INPUT_S = '''\
LR

11A = (11B, XXX)
11B = (XXX, 11Z)
11Z = (11B, XXX)
22A = (22B, XXX)
22B = (22C, 22C)
22C = (22Z, 22Z)
22Z = (22B, 22B)
XXX = (XXX, XXX)
'''
EXPECTED = 6


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
