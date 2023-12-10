from __future__ import annotations

import argparse
import os.path

import pytest

import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')


def cheat(s):
    G=s.split("\n")
    H=len(G)
    W=len(G[0])

    O = [[0]*W for _ in range(H)] # part 2

    ax = -1
    ay = -1
    for i in range(H):
        for j in range(W):
            if "S" in G[i]:
                ax=i
                ay=G[i].find("S")
    # print(ax,ay)

    # rightward downward leftward upward
    dirs = [(0,1),(1,0),(0,-1),(-1,0)]
    happy = ["-7J", "|LJ", "-FL", "|F7"]
    Sdirs = []
    for i in range(4):
        pos = dirs[i]
        bx = ax+pos[0]
        by = ay+pos[1]
        if bx>=0 and bx<=H and by>=0 and by<=W and G[bx][by] in happy[i]:
            Sdirs.append(i)
    # print(Sdirs)
    Svalid = 3 in Sdirs # part 2

    # rightward downward leftward upward
    transform = {
        (0,"-"): 0,
        (0,"7"): 1,
        (0,"J"): 3,
        (2,"-"): 2,
        (2,"F"): 1,
        (2,"L"): 3,
        (1,"|"): 1,
        (1,"L"): 0,
        (1,"J"): 2,
        (3,"|"): 3,
        (3,"F"): 0,
        (3,"7"): 2,
    }

    curdir = Sdirs[0]
    cx = ax + dirs[curdir][0]
    cy = ay + dirs[curdir][1]
    ln = 1
    O[ax][ay] = 1 # Part 2
    while (cx,cy)!=(ax,ay):
        O[cx][cy] = 1 # Part 2
        ln += 1
        curdir = transform[(curdir,G[cx][cy])]
        cx = cx + dirs[curdir][0]
        cy = cy + dirs[curdir][1]
    # print(ln)
    # print(ln//2)

    # End Part 1
    # Begin Part 2

    ct = 0
    for i in range(H):
        inn = False
        for j in range(W):
            if O[i][j]:
                if G[i][j] in "|JL" or (G[i][j]=="S" and Svalid): inn = not inn
            else:
                ct += inn
    print(ct)

def compute(s: str) -> int:
    # cheat(s)
    # return
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
    s_adj = []
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
                    s_adj.append((start[0] - adjacency[0], start[1] - adjacency[1] ))
                    unchecked.append((*adjacency, 1))
                    max_steps = max(max_steps, 1)
            continue
        r, c, s = current
        visited[(r,c)] = s
        for r1, c1 in adjacencies[(r,c)]:
            if not (r1,c1) in visited:
                unchecked.append((r1, c1, s + 1))
                max_steps = max(max_steps, s+1)
    s_char = None
    if (-1, 0) in s_adj:
        if (0, -1) in s_adj:
            s_char = 'J'
        if (0, 1) in s_adj:
            s_char = 'L'
        if (1, 0) in s_adj:
            s_char = '|'
    if (0, -1) in s_adj:
        if (1, 0) in s_adj:
            s_char = '7'
        if (-1, 0) in s_adj:
            s_char = 'J'
        if (0, 1) in s_adj:
            s_char = '-'
    if not s_char:
        s_char = 'F'
    vert_parity = [False] * len(lines[0])
    vert_prev_char = [None] * len(lines[0])
    cnt = 0
    for row_num, line in enumerate(lines):
        horiz_parity = False
        prev_char = None
        for col_num, char in enumerate(line):
            if char == 'S':
                char = s_char
            if (row_num, col_num) in visited:
                if not prev_char:
                    prev_char = char
                    if char == '|':
                        horiz_parity = not horiz_parity
                else:
                    if prev_char == 'F':
                        if char == 'J':
                            horiz_parity = not horiz_parity
                            prev_char = None
                        if char == '7':
                            prev_char = None
                    elif prev_char == 'L':
                        if char == '7':
                            horiz_parity = not horiz_parity
                            prev_char = None
                        if char == 'J':
                            prev_char = None                            
                    elif prev_char == '|':
                        if char == '|':
                            horiz_parity = not horiz_parity
                            prev_char = None
                        else:
                            prev_char = char

                        
                if not vert_prev_char[col_num]:
                    vert_prev_char[col_num] = char
                    if char == '-':
                        vert_parity[col_num] = not vert_parity[col_num]
                else:
                    if vert_prev_char[col_num] == '7':
                        if char == 'L':
                            vert_parity[col_num] = not vert_parity[col_num]
                            vert_prev_char[col_num] = None
                        if char == 'J':
                            vert_prev_char[col_num] = None
                    elif vert_prev_char[col_num] == 'F':
                        if char == 'J':
                            vert_parity[col_num] = not vert_parity[col_num]
                            vert_prev_char[col_num] = None
                        if char == 'L':
                            vert_prev_char[col_num] = None
                    elif vert_prev_char[col_num] == '-':
                        if char == '-':
                            vert_parity[col_num] = not vert_parity[col_num]
                            vert_prev_char[col_num] = None
                        else:
                            vert_prev_char[col_num] = char
            elif horiz_parity and vert_parity[col_num]:
                cnt +=1
    return cnt


INPUT_S = '''\
FF7FSF7F7F7F7F7F---7
L|LJ||||||||||||F--J
FL-7LJLJ||||||LJL-77
F--JF--7||LJLJ7F7FJ-
L---JF-JLJ.||-FJLJJ7
|F|F-JF---7F7-L7L|7|
|FFJF7L7F-JF7|JL---7
7-L-JL7||F7|L7F-7F7|
L.L7LFJ|||||FJL7||LJ
L7JLJL-JLJLJL--JLJ.L
'''
EXPECTED = 10


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