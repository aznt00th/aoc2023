from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def compute(s: str) -> int:

    lines = s.splitlines()
    instructions = lines[0]
    tree = {}
    for line in lines[1:]:
        if not line:
            continue
        key = line.split('=')[0].replace(' ','')
        left, right = line.split('=')[1].split(',')[0], line.split('=')[1].split(',')[1]
        left = left.strip().replace('(', '')
        right = right.strip().replace(')','')
        tree[key] = (left, right)
    steps = 0
    current = 'AAA'
    while current != 'ZZZ':
        instruction = instructions[steps%len(instructions)]
        if instruction == 'R':
            current = tree[current][1]
        if instruction == 'L':
            current = tree[current][0]
        steps +=1
    # TODO: implement solution here!
    return steps


INPUT_S = '''\
LLR

AAA = (BBB, BBB)
BBB = (AAA, ZZZ)
ZZZ = (ZZZ, ZZZ)'''
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
