import pytest
import sys
import os
sys.path.insert(0, os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from main import has_cycle, find_cycle

def test_tree_is_acyclic():
    g = {
        'A':['B','C'],
        'B':['A','D'],
        'C':['A'],
        'D':['B']
    }
    assert has_cycle(g) is False
    assert find_cycle(g) is None

def test_simple_triangle_cycle():
    g = {
        'A':['B','C'],
        'B':['A','C'],
        'C':['A','B']
    }
    assert has_cycle(g) is True
    cyc = find_cycle(g)
    assert cyc[0] == cyc[-1]
    assert set(cyc[:-1]) == {'A','B','C'}

def test_self_loop_is_cycle():
    g = {'X':['X']}
    assert has_cycle(g) is True
    assert find_cycle(g) == ['X','X']

def test_disconnected_with_one_cycle():
    g = {
        'A':['B'], 'B':['A'],
        'C':['D','E'], 'D':['C','E'], 'E':['C','D'],
        'Z':[]
    }
    assert has_cycle(g) is True
    cyc = find_cycle(g)
    assert cyc[0] == cyc[-1]
    assert set(cyc[:-1]) == {'C','D','E'}

def test_square_cycle():
    g = {
        'A':['B','D'],
        'B':['A','C'],
        'C':['B','D'],
        'D':['A','C']
    }
    assert has_cycle(g) is True
    cyc = find_cycle(g)
    assert cyc[0] == cyc[-1]
    assert set(cyc[:-1]) == {'A','B','C','D'}

@pytest.mark.parametrize("extra_edge", [(), (('E','F'),('F','E'))])
def test_large_acyclic_with_optional_island(extra_edge):
    g = {
        'R':['S'], 'S':['R','T'], 'T':['S','U'], 'U':['T'],
    }
    for e in extra_edge:
        u,v = e
        g.setdefault(u, []).append(v)
    assert has_cycle(g) is False
    assert find_cycle(g) is None

def test_cycle_with_tail():
    g = {
        'A':['B'],
        'B':['A','C'],
        'C':['B','D','E'],
        'D':['C','E'],
        'E':['C','D','F'],
        'F':['E']
    }
    assert has_cycle(g) is True
    cyc = find_cycle(g)
    assert cyc[0] == cyc[-1]
    assert set(cyc[:-1]).issuperset({'C','D','E'})
