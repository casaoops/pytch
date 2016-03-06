from __future__ import print_function
from __future__ import unicode_literals
from collections import defaultdict
from math import radians, cos, sin
import sys

from .types import TurnMode, Block

__all__ = ['Actor']

actor_methods = defaultdict(list)
def create_category(category):
    def category_decorator(fn):
        actor_methods[category].append(fn)
        return fn
    return category_decorator
    
motion = create_category('motion')
looks = create_category('looks')
sensing = create_category('sensing')
    
    
class Actor(object):   
    def __init__(self, x=0.0, y=0.0, direction=90.0, size=100.0, turn_mode=TurnMode.can_rotate):
        self._x = x
        self._y = y
        self._direction = direction
        self.costumes = ['Costumes\Animals\cat1-a.gif', 'Costumes\Animals\cat1-b.gif']
        self.current_costume = 0
        self.turn_mode = turn_mode

    @motion
    def turn_left(self, angle):
        '''TODO docstrings for all 'blocks' in actor.'''
        self._direction = _normalise_angle(self._direction - angle)
        
    @motion
    def turn_right(self, angle):
        self._direction = _normalise_angle(self._direction + angle)

    @motion
    def point_in_direction(self, angle):
        self._direction = _normalise_angle(angle)

    @motion
    def move(self, distance):
        self._x += sin(radians(self._direction)) * distance
        self._y += cos(radians(self._direction)) * distance

    @motion
    def change_x_by(self, dx):
        self._x += dx

    @motion
    def change_y_by(self, dy):
        self._y += dy
        
    @motion
    def set_x_to(self, x):
        self._x = x

    @motion
    def set_y_to(self, y):
        self._y = y

    @motion
    def go_to(self, x, y):
        self._x, self._y = x, y

    @motion
    def x_position(self):
        return self._x

    @motion
    def y_position(self):
        return self._y

    @motion
    def direction(self):
        return self._direction

    @looks
    def next_costume(self):
        self.current_costume = (self.current_costume + 1) % len(self.costumes)
        
    @property
    def costume(self):
        return self.costumes[self.current_costume]
        


#TODO get nose to run doctests automagically
def _normalise_angle(angle):
    '''
    >>> _normalise_angle(100.0)
    100.0
    >>> _normalise_angle(-200.0)
    160.0
    >>> _normalise_angle(-179.0)
    -179.0
    >>> _normalise_angle(-180.0)
    180.0
    >>> _normalise_angle(-179.9)
    -179.9
    >>> _normalise_angle(720.0)
    0.0

    '''
    norm = 180.0 - sys.float_info.epsilon
    return ((angle + norm) % 360.0) - norm
    
