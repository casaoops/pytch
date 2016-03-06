import sys
import os
if __name__ == '__main__':
    sys.path.append(os.path.join(os.path.dirname(os.path.abspath(__file__)), '..'))
from pytch import Actor
from nose.tools import *
    
def test_point_tests():
    for to, expected in [
            (0, 0),
            (90, 90),
            (180.0, 180.0),
            (720.0, 0.0),
            (181, -179)]:
        yield point_in_direction, to, expected

def point_in_direction(to, expected):
    actor = Actor(direction=0)
    actor.point_in_direction(to)
    assert_equals(expected, actor.direction())


def test_direction_doesnt_overflow():
    actor = Actor(direction=0)
    actor.point_in_direction(720)
    assert_equals(0, actor.direction())


def _Hello_TestWorld():
    actor = Actor(direction=0)
    actor.point_in_direction(720)
    assert_equals(1, actor.direction())
    
    
if __name__ == '__main__':
    import nose
    nose.main()