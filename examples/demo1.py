from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals

from pytch import *
            
scratch = Actor(
    x=100.0, 
    y=0.0, 
    direction=90.0, 
    size=100.0,
    turn_mode=TurnMode.can_rotate,
)
    
@when_flag_clicked()
def flag_clicked():
    print('start')
    for n in range(10):
        next_costume()
        move(10)


@when_key_pressed(' ')
def do_something():
    next_costume()
        
@when_key_pressed(Key.up)
def on_up(scratch):
    move(10)
    next_costume()
        
@when_key_pressed(Key.down)
def on_down():
    move(-10)
    next_costume()

@when_key_pressed(Key.left)
def on_left():
    direction -= 10

@when_key_pressed(Key.right)
def on_right():
    direction += 10


