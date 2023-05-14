__version__ = 1.0
__description__ = "Tetrose - best tetris clone"
import pygame
import warnings

from .kezmenu_effects import KezMenuEffectAble, VALID_EFFECTS

class deprecated(object):
    
    def __init__(self, msg):
        self._msg = msg
        self._printed = False
    
    def __call__(self, func):
        if not self._printed:
            def wrapped_func(*args):
                warnings.warn(self._msg % func.__name__, DeprecationWarning, stacklevel=3)
                func(*args)
            self._printed = True
            return wrapped_func
        return func

class KezMenu(KezMenuEffectAble):

    def __init__(self, *options):
        KezMenuEffectAble.__init__(self)
        self.options = [{'label': x[0], 'callable': x[1]} for x in options]
        self.x = 0
        self.y = 0
        self.screen_topleft_offset = (0,0)
        self.option = 0
        self.width = 0
        self.height = 0
        self.color = (0, 0, 0, 0)
        self.focus_color = (255, 0, 0, 255)
        self.mouse_enabled = True
        self.mouse_focus = False
        try:
            self._font = None
            self.font = pygame.font.Font(None, 32)
            self._fixSize()
        except:
            pass

    def _fixSize(self):
        self.height = 0
        for o in self.options:
            text = o['label']
            font = o['font']
            ren = font.render(text, 1, (0, 0, 0))
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            self.height+=font.get_height()

    def draw(self, surface):
        offset = 0
        i = 0
        ol, ot = self.screen_topleft_offset
        first = self.options and self.options[0]
        last = self.options and self.options[-1]
        for o in self.options:
            indent = o.get('padding_col',0)
            if o!=first and o.get('padding_line',0):
                offset+=o['padding_line']
            
            font = o.get('font',self._font)
            if i==self.option and self.focus_color:
                clr = self.focus_color
            else:
                clr = self.color
            text = o['label']
            ren = font.render(text, 1, clr)
            if ren.get_width() > self.width:
                self.width = ren.get_width()
            o['label_rect'] = pygame.Rect( (ol+self.x + indent, ot+self.y + offset), (ren.get_width(),ren.get_height()) )
            surface.blit(ren, (self.x + indent, self.y + offset))
            offset+=font.get_height()
            if o!=last and o.get('padding_line',0):
                offset+=o['padding_line']

            i+=1

    def update(self, events, time_passed=None):
        for e in events:
            if e.type == pygame.KEYDOWN:
                if e.key == pygame.K_DOWN:
                    self.option += 1
                if e.key == pygame.K_UP:
                    self.option -= 1
                if e.key == pygame.K_RETURN or e.key == pygame.K_SPACE:
                    self.options[self.option]['callable']()
            elif e.type == pygame.MOUSEBUTTONDOWN:
                lb, cb, rb = pygame.mouse.get_pressed()
                if lb and self.mouse_focus:
                    self.options[self.option]['callable']()
        if self.option > len(self.options)-1:
            self.option = len(self.options)-1
        elif self.option < 0:
            self.option = 0
        if self.mouse_enabled:
            self._checkMousePositionForFocus()
        if time_passed:
            self._updateEffects(time_passed)

    def _checkMousePositionForFocus(self):
        i = 0
        mouse_pos = pygame.mouse.get_pos()
        ml,mt = self.position
        for o in self.options:
            rect = o.get('label_rect')
            if rect:
                if rect.collidepoint(mouse_pos):
                    self.option = i
                    self.mouse_focus = True
                    break           
            i+=1
        else:
            self.mouse_focus = False

    def _setPosition(self, position):
        x,y = position
        self.x = x
        self.y = y
    position = property(lambda self: (self.x,self.y), _setPosition, doc="""The menu position inside the container""")

    def _setFont(self, font):
        self._font = font
        for o in self.options:
            o['font'] = font
        self._fixSize()
    font = property(lambda self: self._font, _setFont, doc="""Font used by the menu""")

    def center_at(self, x, y):
        self.x = x-(self.width/2)
        self.y = y-(self.height/2)


def runTests():
    import tests
