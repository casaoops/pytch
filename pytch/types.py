from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from flufl.enum import Enum

__all__ = ('TurnMode', 'Key')

TurnMode = Enum('TurnMode', 'can_rotate only_face_left_right dont_rotate')
Key = Enum('Key', 'add alt back cancel capital category_arrow category_cut category_jump category_navigation category_paging category_tab clear command control control_a control_b control_c control_d control_e control_f control_g control_h control_i control_j control_k control_l control_m control_n control_o control_p control_q control_r control_s control_t control_u control_v control_w control_x control_y control_z decimal delete divide down end escape execute f1 f10 f11 f12 f13 f14 f15 f16 f17 f18 f19 f2 f20 f21 f22 f23 f24 f3 f4 f5 f6 f7 f8 f9 help home insert lbutton left mbutton menu multiply next none numlock numpad0 numpad1 numpad2 numpad3 numpad4 numpad5 numpad6 numpad7 numpad8 numpad9 numpad_add numpad_begin numpad_decimal numpad_delete numpad_divide numpad_down numpad_end numpad_enter numpad_equal numpad_f1 numpad_f2 numpad_f3 numpad_f4 numpad_home numpad_insert numpad_left numpad_multiply numpad_next numpad_pagedown numpad_pageup numpad_prior numpad_right numpad_separator numpad_space numpad_subtract numpad_tab numpad_up pagedown pageup pause print prior raw_control rbutton return right scroll select separator shift snapshot space special1 special10 special11 special12 special13 special14 special15 special16 special17 special18 special19 special2 special20 special3 special4 special5 special6 special7 special8 special9 start subtract tab up windows_left windows_menu windows_right')

STAGE_SIZE = (500.0, 400.0)
ORIGIN = (STAGE_SIZE[0]/2.0, STAGE_SIZE[1]/2.0)

FLAG_EVENT = object()


class Block(object):
    def __init__(self, cls, name):
        self.cls = cls
        self.name = name
        
        
all_blocks = {}