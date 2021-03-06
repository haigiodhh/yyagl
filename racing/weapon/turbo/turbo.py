from yyagl.gameobject import GameObject
from .gfx import TurboGfx
from .audio import TurboAudio
from .logic import TurboLogic


class TurboFacade(object):

    def attach_obs(self, meth):
        return self.logic.attach(meth)

    def detach_obs(self, meth):
        return self.logic.detach(meth)

    def fire(self):
        return self.logic.fire()


class Turbo(GameObject, TurboFacade):
    gfx_cls = TurboGfx
    audio_cls = TurboAudio
    logic_cls = TurboLogic

    def __init__(self, car, path):
        init_lst = [
            [('gfx', self.gfx_cls, [self, car.gfx.nodepath, path])],
            [('audio', self.audio_cls, [self])],
            [('logic', self.logic_cls, [self, car])]]
        GameObject.__init__(self, init_lst)
