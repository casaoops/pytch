from __future__ import print_function
from __future__ import division
from __future__ import unicode_literals
from flufl.enum import Enum
from collections import defaultdict
import six
import sys
import fibers
import time
from .actor import Actor, actor_methods
from .types import FLAG_EVENT

class ScriptFiber(object):
    def __init__(self, actor, handler):
        self.fiber = None
        self.handler = handler
        self.actor = actor
        self.target = None
        self.next = None
        
    @property
    def started(self):
        return self.fiber is not None
        
    @property
    def finished(self):
        return self.fiber and not self.fiber.is_alive()
        
    def start(self):
        self.fiber = fibers.Fiber(self.handler)
        self.fiber.switch()
        
    def run_to_next_switch(self):
        if isinstance(self.next, Exception):
            fn, args, kwargs = self.fiber.throw(self.next)
        else:
            fn, args, kwargs = self.fiber.switch(self.next)
        print(fn, args, kwargs)
        try:
            self.next = getattr(self.actor, fn)(*args, **kwargs)
        except Exception as e:
            self.next = e

class Runner(object):
    def __init__(self):
        self._fibers = []
        self._main_fiber=None
        self.actors = []
        
    def load_actor(self, path):
        globs = self.create_actor_method_forwarders()
        globs.update(self.create_event_binders())
        locals = {}
        execfile(path, globs, locals)
        #print('\n'.join(repr(x) for x in globs.items()))
        #print('!'*100)
        #print('\n'.join(repr(x) for x in locals.items()))
        name, actor = [(name, x) for name, x in locals.items() if isinstance(x, Actor)][0]
        actor.name = name
        actor.event_handlers = globs['event_handlers']
        self.actors.append(actor)
                    
    def _on_event(self, event):
        '''Run any event handlers bound to the given event.'''
        for actor in self.actors:
            for handler in actor.event_handlers[event]:
                script = ScriptFiber(actor, handler)
                self._fibers.append(script)

    def main_loop(self):
        self._main_fiber = fibers.current()
        while 1:
            if self._fibers:
                s = self._fibers.pop(0)
                if not s.started:
                    s.start()
                    self._fibers.append(s)
                elif s.finished:
                    # script has ended, remove it from the list
                    self._fibers.pop(s)
                else:
                    s.run_to_next_switch()
                    self._fibers.append(s)
            self._on_idle()
        
        
    def exec_actor_method(self, name, args, kwargs):
        return self._main_fiber.switch((name, args, kwargs))
        
    def _on_idle(self):
        '''Called from main_loop periodically.
        
        If main_loop is run as a separate thread then this should sleep a bit to 
        prevent scripts executing too quickly.
        '''
        time.sleep(0.5)
            
    def on_flag(self):
        self._on_event(FLAG_EVENT)

    def on_key(self, key):
        self._on_event(key)

    def stop_all(self):
        # TODO do we need a more graceful shutdown here? what happens to fibers
        #      that are just GC'd?
        self._fibers[:] = []        

    def create_actor_method_forwarders(self):
        '''Create a namespace with functions for interacting with the current actor.
        
        These functions all have the form fn(*args, **kargs), and switch fiber to 
        the script runner fiber.
        '''
        def create_method_fn(method):
            def method_fn(*args, **kwargs):
                return self.exec_actor_method(method.__name__, args, kwargs)
            method_fn.__name__ = method.__name__
            return method_fn
        res = {}
        for category, methods in actor_methods.items():
            for method in methods:
                res[method.__name__] = create_method_fn(method)
        return res        
        
    def create_event_binders(self):
        '''Create a namespace for the event handling decorators.
        '''
        event_handlers = defaultdict(list)
        res = {}
        res['event_handlers'] = event_handlers
        def when_key_pressed(key):
            def handler(f):
                event_handlers[key].append(f)
                return f
            return handler

        def when_flag_clicked():
            def handler(f):
                event_handlers[FLAG_EVENT].append(f)
                return f
            return handler
        res['when_key_pressed'] = when_key_pressed
        res['when_flag_clicked'] = when_flag_clicked
        return res





            