from __future__ import annotations

import argparse
import os.path
from collections import defaultdict
import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

def blocks_under_this(sx, ex, sy, ey, sz, ez, blocks, evaluating = False):
    under = []
    if len(blocks) == 0:
        return under
    for block_num, block_pos in blocks.items():
        ((bsx, bex), (bsy, bey), (bsz, bez)) = block_pos
        if evaluating and (bez != sz - 1):
            continue
        if sx > bex or ex < bsx or sy > bey or ey < bsy:
            continue
        under.append((block_num, block_pos))
    return under


def compute(s: str) -> int:
    lines = s.splitlines()
    start_pos = {}
    for row_num, line in enumerate(lines):
        vals = line.split('~')
        sx, sy, sz = [int(i) for i in vals[0].split(',')]
        ex, ey, ez = [int(i) for i in vals[1].split(',')]
        start_pos[row_num] = ((sx,ex), (sy,ey), (sz, ez))
    max_starting_z = max([pos[2][0] for pos in start_pos.values()])
    drop_pos = {}
    for i in range(1, max_starting_z + 1):
        for block_num, block_pos in start_pos.items():
            (sx,ex), (sy,ey), (sz, ez) = block_pos
            if sz == i:
                under = blocks_under_this(sx,ex, sy,ey, sz, ez, drop_pos)
                new_height = 1 + max([blocks[1][2][1] for blocks in under] + [0] )
                drop_pos[block_num] = ((sx,ex), (sy, ey), (new_height, new_height + ez-sz))
    cnt = 0
    supports = defaultdict(list)
    supported_by = defaultdict(list)
    for block_num, ((sx,ex), (sy,ey), (sz, ez)) in drop_pos.items():
        under = blocks_under_this(sx, ex, sy, ey, sz, ez, drop_pos, True)
        for under_num, _ in under:
            supported_by[block_num].append(under_num)
            supports[under_num].append(block_num)
    uniquely_supports = set([v[0] for k, v in supported_by.items() if len(v) == 1])
    return len(drop_pos) - len(uniquely_supports)


INPUT_S = '''\
1,0,1~1,2,1
0,0,2~2,0,2
0,2,3~2,2,3
0,0,4~0,2,4
2,0,5~2,2,5
0,1,6~2,1,6
1,1,8~1,1,9
'''
EXPECTED = 5


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
