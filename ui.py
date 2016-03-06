from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
import wx
import os
import sys
from pytch import *
from pytch.types import STAGE_SIZE, ORIGIN
from math import radians, cos, sin
import threading

wxkeys ={323:'help',1:'category_arrow',307:'alt',382:'numpad_end',310:'pause',309:'menu',195:'special3',194:'special2',193:'special1',199:'special7',198:'special6',197:'special5',196:'special4',379:'numpad_down',201:'special9',200:'special8',376:'numpad_left',392:'numpad_divide',363:'f24',393:'windows_left',384:'numpad_insert',322:'insert',320:'execute',338:'decimal',321:'snapshot',316:'right',381:'numpad_next',8:'back',371:'numpad_f1',373:'numpad_f3',372:'numpad_f2',374:'numpad_f4',301:'lbutton',313:'home',378:'numpad_right',32:'space',362:'f23',361:'f22',360:'f21',359:'f20',367:'pagedown',311:'capital',319:'print',209:'special17',2:'category_paging',308:'raw_control',212:'special20',337:'subtract',23:'control_w',390:'numpad_subtract',21:'control_u',20:'control_t',368:'numpad_space',388:'numpad_add',17:'control_q',16:'control_p',306:'shift',380:'numpad_pageup',25:'control_y',395:'windows_menu',7:'control_g',366:'prior',5:'control_e',4:'control_d',336:'separator',2:'control_b',1:'control_a',15:'control_o',14:'control_n',380:'numpad_prior',354:'f15',11:'control_k',10:'control_j',9:'control_i',8:'control_h',211:'special19',4:'category_jump',339:'divide',304:'mbutton',387:'numpad_multiply',317:'down',208:'special16',207:'special15',206:'special14',205:'special13',204:'special12',203:'special11',202:'special10',303:'cancel',386:'numpad_equal',383:'numpad_begin',318:'select',210:'special18',326:'numpad2',327:'numpad3',324:'numpad0',325:'numpad1',330:'numpad6',331:'numpad7',328:'numpad4',329:'numpad5',332:'numpad8',333:'numpad9',335:'add',367:'next',375:'numpad_home',300:'start',377:'numpad_up',302:'rbutton',22:'control_v',8:'category_tab',7:'category_navigation',19:'control_s',16:'category_cut',18:'control_r',0:'none',389:'numpad_separator',366:'pageup',315:'up',357:'f18',358:'f19',351:'f12',352:'f13',349:'f10',350:'f11',355:'f16',356:'f17',353:'f14',127:'delete',308:'control',340:'f1',341:'f2',342:'f3',343:'f4',344:'f5',345:'f6',346:'f7',347:'f8',348:'f9',27:'escape',26:'control_z',9:'tab',381:'numpad_pagedown',13:u'return',364:'numlock',24:'control_x',391:'numpad_decimal',370:'numpad_enter',6:'control_f',394:'windows_right',3:'control_c',334:'multiply',312:'end',13:'control_m',12:'control_l',305:'clear',308:'command',369:'numpad_tab',365:'scroll',385:'numpad_delete',314:'left'}

USE_BUFFER = ('wxMSW' in wx.PlatformInfo) # use buffered drawing on Windows
if sys.platform == 'win32':
    MEDIA = r'C:\Program Files (x86)\Scratch\Media'
elif sys.platform == 'darwin':
    MEDIA = '/Applications/Scratch 1.4/Media/'
else:
    exit('Set MEDIA to a scratch media directory here')


def load_image(path):
    return wx.Image(os.path.join(MEDIA, path))
    
def create_crosshair_path(gc, size):
    cross = size//2
    path = gc.CreatePath()
    path.MoveToPoint(-cross, 0)
    path.AddLineToPoint(cross, 0)
    path.MoveToPoint(0, -cross)
    path.AddLineToPoint(0, cross)
    path.CloseSubpath()
    return path


class Stage(wx.Panel):
    '''This class is the view portal of the stage. It handles rendering of the 
    whole scene whenever a paint event occurs.
    
    It will also need to 
    '''
    def __init__(self, parent):
        super(Stage, self).__init__(parent, size=STAGE_SIZE)
        self.Bind(wx.EVT_PAINT, self._on_paint)
        if USE_BUFFER:
            self.Bind(wx.EVT_SIZE, self._on_size)
        self.Bind(wx.EVT_ERASE_BACKGROUND, self._on_erase)

    def _on_erase(self, evt):
        pass
            
    def _on_size(self, evt):
        # When there is a size event then recreate the buffer to match
        # the new size of the window.
        self._init_buffer()
        evt.Skip()
        
    def _init_buffer(self):
        sz = self.GetClientSize()
        sz.width = max(1, sz.width)
        sz.height = max(1, sz.height)
        self._buffer = wx.EmptyBitmap(sz.width, sz.height, 32)

        dc = wx.MemoryDC(self._buffer)
        dc.SetBackground(wx.Brush(self.GetBackgroundColour()))
        dc.Clear()
        gc = wx.GraphicsContext.Create(dc)
        self._draw(gc)

    def _on_paint(self, evt):
        if USE_BUFFER:
            # The buffer already contains our drawing, so no need to
            # do anything else but create the buffered DC.  When this
            # method exits and dc is collected then the buffer will be
            # blitted to the paint DC automagically
            dc = wx.BufferedPaintDC(self, self._buffer)
        else:
            # Otherwise we need to draw our content to the paint DC at
            # this time.
            dc = wx.PaintDC(self)
            gc = wx.GraphicsContext.Create(dc)
            self._draw(gc)
            
    def _draw(self, gc):
        gc.AntiAliasMode = wx.ANTIALIAS_NONE

        # create a cross hair to spot the middle of the stage, this is to help
        # figure out what is going on with rotations and translations
        crosshair = create_crosshair_path(gc, 20)
        gc.PushState()
        gc.SetPen(wx.Pen('navy', 1))
        gc.Translate(ORIGIN[0], ORIGIN[1])
        gc.StrokePath(crosshair)
        gc.PopState()
        for actor in runner.actors:
            image = load_image(actor.costume)
            sz = image.GetSize()
            x, y, rotate = actor.x_position(), -actor.y_position(), None
            if actor.turn_mode == TurnMode.can_rotate:
                rotate = radians(actor.direction()-90.0)
            elif actor.turn_mode == TurnMode.only_face_left_right and actor.direction() < 0.0:
                image = image.Mirror(True)

            bmp = gc.CreateBitmapFromImage(image)
            gc.PushState()
            gc.Translate(x + ORIGIN[0], y + ORIGIN[1])
            if rotate is not None:
                gc.Rotate(rotate)
            gc.DrawBitmap(bmp, - sz[0]/2, -sz[1]/2 , *sz)
            gc.PopState()
            
            
class RHSPanel(wx.Panel):
    def __init__(self, parent):
        super(RHSPanel, self).__init__(parent)

        self.Sizer = sizer = wx.BoxSizer(wx.VERTICAL)
        
        tb = wx.ToolBar(self, style=wx.TB_HORIZONTAL | wx.NO_BORDER | wx.TB_FLAT)
        tb.AddSimpleTool(wx.ID_ANY, wx.Bitmap('res/flag.png'), shortHelpString='Start green flag scripts')
        tb.AddSimpleTool(wx.ID_ANY, wx.Bitmap('res/stop.png'), shortHelpString='Stop everything')
        self.stage = Stage(self)
        sizer.Add(tb, 0, wx.EXPAND)
        sizer.Add(self.stage, 0, wx.EXPAND)
        self.actor_selector = wx.StaticText(self, label='Select actors here')
        sizer.Add(self.actor_selector, 1, wx.EXPAND)

class MainWindow(wx.Frame):
    def __init__(self):
        super(MainWindow, self).__init__(None, title='Pytch', size=(800, 600))
        splitter = wx.SplitterWindow(self, style=wx.SP_LIVE_UPDATE)
        rhs_panel = RHSPanel(splitter)
        editor = wx.StaticText(splitter, label='editor goes here')
        splitter.SplitVertically(editor, rhs_panel, -500)
        
        self.stage = rhs_panel.stage
        self.timer = wx.Timer(self)
        self.timer.Start(100)
        self.Bind(wx.EVT_TIMER, self._on_timer)
        self.Bind(wx.EVT_KEY_DOWN, self._on_key)
        #flag.Bind(wx.EVT_BUTTON, self._on_flag)
        #stop.Bind(wx.EVT_BUTTON, self._on_stop_all)
        self.thread = threading.Thread(target=runner.main_loop)
        self.thread.daemon = True
        self.thread.start()
        
    def _on_flag(self, e):
        runner.on_flag()
        
    def _on_stop_all(self, e):
        runner.stop_all()

    def _on_key(self, e):
        try:
            key = Key(wxkeys[e.GetKeyCode()])
        except KeyError:
            key = chr(e.GetKeyCode())
        runner.on_key(key)

    def _on_timer(self, e):
        self.stage.Refresh()

if __name__ == '__main__':
    import doctest
    if doctest.testmod()[0] != 0:
        sys.exit()
    #import app
    from pytch.runner import Runner
    runner = Runner()
    runner.load_actor('examples/demo1.py')
    app = wx.App()
    frame = MainWindow()
    frame.Show()
    frame.Refresh()
    app.MainLoop()