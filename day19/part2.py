from __future__ import annotations

import argparse
import os.path

import pytest
import json
import support

INPUT_TXT = os.path.join(os.path.dirname(__file__), 'input.txt')

class Part():
    def __init__(self, x, m, a, s):
        self.x = int(x)
        self.m = int(m)
        self.a = int(a)
        self.s = int(s)

    def __repr__(self):
        return(f'[x={self.x:=}, m={self.m:=}, a={self.a:=}, s={self.s:=}]')

    def sum(self):
        return self.x + self.m + self.a + self.s

    def get_by_str(self, s):
        if s == 'x':
            return self.x
        if s == 'm':
            return self.m
        if s == 'a':
            return self.a
        if s == 's':
            return self.s

class Restriction():
    def __init__(self, x, m, a, s):
        self.x = x
        self.m = m
        self.a = a
        self.s = s

    def __repr__(self):
        return f"{self.x}, {self.m}, {self.a}, {self.s}"

    def update_lower(self, s, val):
        if s == 'x':
            if self.x[0] > val:
                return False
            self.x = (val+1, self.x[1])
        if s == 'm':
            if self.m[0] > val:
                return False
            self.m = (val+1, self.m[1])
        if s == 'a':
            if self.a[0] > val:
                return False
            self.a = (val+1, self.a[1])
        if s == 's':
            if self.s[0] > val:
                return False
            self.s = (val+1, self.s[1])
        return True

    def update_upper(self, s, val):
        if s == 'x':
            if self.x[1] < val:
                return False
            self.x = (self.x[0], val-1)
        if s == 'm':
            if self.m[1] < val:
                return False
            self.m = (self.m[0], val-1)
        if s == 'a':
            if self.a[1] < val:
                return False
            self.a = (self.a[0], val-1)
        if s == 's':
            if self.s[1] < val:
                return False
            self.s = (self.s[0], val-1)
        return True

    def apply_true_rule(self, rule):
        if rule == '_':
            return True
        if rule[1] == '>':
            return self.update_lower(rule[0], int(rule[2:]))
        elif rule[1] == '<':
            return self.update_upper(rule[0], int(rule[2:]))
        else:
            raise Exception(f'unkown comp value {rule}')

    def apply_false_rule(self, rule):
        if rule == '_':
            return False
        if rule[1] == '>':
            return self.update_upper(rule[0], int(rule[2:]) + 1)
        elif rule[1] == '<':
            return self.update_lower(rule[0], int(rule[2:]) - 1)
        else:
            raise Exception(f'unkown comp value {rule}')

    def get_combo(self):
        return (1+ self.x[1] - self.x[0]) * (1 + self.m[1] - self.m[0]) * (1 + self.a[1] - self.a[0]) * (1 + self.s[1] - self.s[0]) 

def check_rule(test, part):
    if test == '_':
        return True
    if test[1] == '>':
        return part.get_by_str(test[0]) > int(test[2:])
    elif test[1] == '<':
        return part.get_by_str(test[0]) < int(test[2:])
 
    else:
        raise Exception(f'unknown comp value {test}')


def format_str_to_dict(s: str):
    for char in 'xmas':
        s = s.replace(char, '"' + char + '"')
    return json.loads(s.replace('=', ':'))


def recursively_check_tree(rules, current_rule, res):
    tot = 0
    tmpf = Restriction(res.x, res.m, res.a, res.s)
    for rule in rules[current_rule]:
        tmpt = Restriction(tmpf.x, tmpf.m, tmpf.a, tmpf.s)
        if rule[1] == 'A':
            if tmpt.apply_true_rule(rule[0]):
                tot += tmpt.get_combo()
        elif rule[1] == 'R':
            pass
        else:
            if tmpt.apply_true_rule(rule[0]):
                tot += recursively_check_tree(rules, rule[1], tmpt)
        if not tmpf.apply_false_rule(rule[0]):
            break
    return tot

def compute(s: str) -> int:
    lines = s.splitlines()
    start = True
    mappings = {}
    parts = []
    for row_num, line in enumerate(lines):
        curr_parts = []
        if len(line) == 0:
            start = False   
            continue
        if start:
            rule_name, rules = line.split('{')[0], line.split('{')[1]
            mappings[rule_name] = []
            for rule in rules.split(','):
                test = rule.split(':')[0]
                dest = rule.split(':')[-1]
                if test == dest:
                    test = '_'
                    dest = dest[:-1]
                mappings[rule_name].append((test, dest))
        else:
            parts.append(Part(**format_str_to_dict(line)))
    tot = 0
    return recursively_check_tree(mappings, 'in', Restriction((1,4000), (1,4000), (1,4000), (1,4000)))


INPUT_S = '''\
px{a<2006:qkq,m>2090:A,rfg}
pv{a>1716:R,A}
lnx{m>1548:A,A}
rfg{s<537:gd,x>2440:R,A}
qs{s>3448:A,lnx}
qkq{x<1416:A,crn}
crn{x>2662:A,R}
in{s<1351:px,qqz}
qqz{s>2770:qs,m<1801:hdj,R}
gd{a>3333:R,R}
hdj{m>838:A,pv}

{x=787,m=2655,a=1222,s=2876}
{x=1679,m=44,a=2067,s=496}
{x=2036,m=264,a=79,s=2244}
{x=2461,m=1339,a=466,s=291}
{x=2127,m=1623,a=2188,s=1013}
'''
EXPECTED = 167409079868000


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
