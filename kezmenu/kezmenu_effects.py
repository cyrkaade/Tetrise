import pygame

VALID_EFFECTS = ('enlarge-font-on-focus','raise-line-padding-on-focus','raise-col-padding-on-focus')

class KezMenuEffectAble(object):
    
    def __init__(self):
        self._effects = {}

    def enableEffect(self, name, **kwargs):
        if name not in VALID_EFFECTS:
            raise KeyError("KezMenu don't know an effect of type %s" % name)
        self.__getattribute__('_effectinit_%s' % name.replace("-","_"))(name, **kwargs)

    def disableEffect(self, name):
        try:
            del self._effects[name]
            self.__getattribute__('_effectdisable_%s' % name.replace("-","_"))()
        except KeyError:
            pass
        except AttributeError:
            pass

    def _updateEffects(self, time_passed):
        for name,params in self._effects.items():
            self.__getattribute__('_effectupdate_%s' % name.replace("-","_"))(time_passed)

    # ******* Effects *******

    def _effectinit_enlarge_font_on_focus(self, name, **kwargs):
        self._effects[name] = kwargs
        if 'font' not in kwargs:
            raise TypeError("enlarge_font_on_focus: font parameter is required")
        if 'size' not in kwargs:
            raise TypeError("enlarge_font_on_focus: size parameter is required")
        if 'enlarge_time' not in kwargs:
            kwargs['enlarge_time'] = .5
        if 'enlarge_factor' not in kwargs:
            kwargs['enlarge_factor'] = 2.
        kwargs['raise_font_ps'] = kwargs['enlarge_factor']/kwargs['enlarge_time'] # pixel-per-second
        for o in self.options:
            o['font'] = pygame.font.Font(kwargs['font'], kwargs['size'])
            o['font_current_size'] = kwargs['size']
            o['raise_font_factor'] = 1.

    def _effectupdate_enlarge_font_on_focus(self, time_passed):
        data = self._effects['enlarge-font-on-focus']
        fps = data['raise_font_ps']
        i = 0
        final_size = data['size'] * data['enlarge_factor']
        for o in self.options:
            if i==self.option:
                # Raise me
                if o['font_current_size']<final_size:
                    o['raise_font_factor']+=fps*time_passed
                elif o['font_current_size']>final_size:
                    o['raise_font_factor']=data['enlarge_factor']
            elif o['raise_font_factor']!=1.:
                # decrease
                if o['raise_font_factor']>1.:
                    o['raise_font_factor']-=fps*time_passed
                elif o['raise_font_factor']<1.:
                    o['raise_font_factor'] = 1.

            new_size = int(data['size'] * o['raise_font_factor'])
            if new_size!=o['font_current_size']:
                o['font'] = pygame.font.Font(data['font'], new_size)
                o['font_current_size'] = new_size
            i+=1

    def _effectdisable_enlarge_font_on_focus(self):
        self.font = self._font


    def _effectinit_raise_line_padding_on_focus(self, name, **kwargs):
        self._effects[name] = kwargs
        if 'enlarge_time' not in kwargs:
            kwargs['enlarge_time'] = .5
        if 'padding' not in kwargs:
            kwargs['padding'] = 10
        kwargs['padding_pps'] = kwargs['padding']/kwargs['enlarge_time'] # pixel-per-second
        # Now, every menu voices need additional infos
        for o in self.options:
            o['padding_line']=0.

    def _effectupdate_raise_line_padding_on_focus(self, time_passed):
        data = self._effects['raise-line-padding-on-focus']
        pps = data['padding_pps']
        i = 0
        for o in self.options:
            if i==self.option:
                # Raise me
                if o['padding_line']<data['padding']:
                    o['padding_line']+=pps*time_passed
                elif o['padding_line']>data['padding']:
                    o['padding_line'] = data['padding']
            elif o['padding_line']:
                if o['padding_line']>0:
                    o['padding_line']-=pps*time_passed
                elif o['padding_line']<0:
                    o['padding_line'] = 0
            i+=1

    def _effectdisable_raise_line_padding_on_focus(self):
        """Delete all line paddings"""
        for o in self.options:
            del o['padding_line']


    def _effectinit_raise_col_padding_on_focus(self, name, **kwargs):
        self._effects[name] = kwargs
        if not kwargs.has_key('enlarge_time'):
            kwargs['enlarge_time'] = .5
        if not kwargs.has_key('padding'):
            kwargs['padding'] = 10
        kwargs['padding_pps'] = kwargs['padding']/kwargs['enlarge_time'] # pixel-per-second
        # Now, every menu voices need additional infos
        for o in self.options:
            o['padding_col']=0.

    def _effectupdate_raise_col_padding_on_focus(self, time_passed):
        data = self._effects['raise-col-padding-on-focus']
        pps = data['padding_pps']
        i = 0
        for o in self.options:
            if i==self.option:
                # Raise me
                if o['padding_col']<data['padding']:
                    o['padding_col']+=pps*time_passed
                elif o['padding_col']>data['padding']:
                    o['padding_col'] = data['padding']
            elif o['padding_col']:
                if o['padding_col']>0:
                    o['padding_col']-=pps*time_passed
                elif o['padding_col']<0:
                    o['padding_col'] = 0
            i+=1

    def _effectdisable_raise_col_padding_on_focus(self):
        for o in self.options:
            del o['padding_col']

