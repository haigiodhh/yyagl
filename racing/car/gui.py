from panda3d.core import TextNode, LVector3f
from direct.gui.DirectSlider import DirectSlider
from direct.gui.OnscreenText import OnscreenText
from direct.gui.OnscreenImage import OnscreenImage
from yyagl.gameobject import Gui
from yyagl.engine.font import FontMgr


class CarParameter(object):

    def __init__(self, attr, init_val, pos, val_range, callback):
        self.__callback = callback
        self.__lab = OnscreenText(
            text=attr, pos=pos, align=TextNode.ARight, fg=(1, 1, 1, 1),
            parent=eng.base.a2dTopLeft, scale=.06)
        _pos = LVector3f(pos[0], 1, pos[1]) + (.3, 0, .01)
        self.__slider = DirectSlider(
            pos=_pos, value=init_val, range=val_range, command=self.__set_attr,
            parent=eng.base.a2dTopLeft, scale=.24)
        _pos = LVector3f(pos[0], pos[1], 1) + (.6, 0, 0)
        self.__val = OnscreenText(pos=_pos, align=TextNode.ALeft,
                                  fg=(1, 1, 1, 1),
                                  parent=eng.base.a2dTopLeft, scale=.06)
        self.toggle()

    def toggle(self):
        widgets = [self.__slider, self.__lab, self.__val]
        map(lambda wdg: (wdg.show if wdg.isHidden() else wdg.hide)(), widgets)

    @property
    def is_visible(self):
        widgets = [self.__slider, self.__lab, self.__val]
        return any(not wdg.is_hidden() for wdg in widgets)

    def __set_attr(self):
        self.__callback(self.__slider['value'])
        self.__val.setText(str(round(self.__slider['value'], 2)))

    def destroy(self):
        map(lambda wdg: wdg.destroy(), [self.__slider, self.__lab, self.__val])


class CarGui(Gui):

    def apply_damage(self, reset=False):
        pass


class CarPlayerGui(CarGui):

    def __init__(self, mdt, cargui_props):
        self.cargui_props = cargui_props
        CarGui.__init__(self, mdt)
        self.set_pars()
        self.set_panel()

    def set_pars(self):
        self.__max_speed_par = CarParameter(
            'max_speed', self.mdt.phys.max_speed, (.5, -.04), (10.0, 200.0),
            lambda val: setattr(self.mdt.phys, 'max_speed', val))
        self.__mass_par = CarParameter(
            'mass', self.mdt.phys.mass, (.5, -.12), (100, 2000),
            self.mdt.gfx.nodepath.node().setMass)
        self.__steering_min_speed = CarParameter(
            'steering_min_speed', self.mdt.phys.steering_min_speed, (.5, -.2),
            (10.0, 100.0),
            lambda val: setattr(self.mdt.phys, 'steering_min_speed', val))
        self.__steering_max_speed = CarParameter(
            'steering_max_speed', self.mdt.phys.steering_max_speed, (.5, -.28),
            (1.0, 50.0),
            lambda val: setattr(self.mdt.phys, 'steering_max_speed', val))
        self.__steering_clamp = CarParameter(
            'steering_clamp', self.mdt.phys.steering_clamp, (.5, -.36),
            (1, 100),
            lambda val: setattr(self.mdt.phys, 'steering_clamp', val))
        self.__steering_inc = CarParameter(
            'steering_inc', self.mdt.phys.steering_inc, (.5, -.44), (1, 200),
            lambda val: setattr(self.mdt.phys, 'steering_inc', val))
        self.__steering_dec = CarParameter(
            'steering_dec', self.mdt.phys.steering_dec, (.5, -.52), (1, 200),
            lambda val: setattr(self.mdt.phys, 'steering_dec', val))
        self.__engine_acc_frc = CarParameter(
            'engine_acc_frc', self.mdt.phys.engine_acc_frc, (.5, -.6),
            (100, 10000),
            lambda val: setattr(self.mdt.phys, 'engine_acc_frc', val))
        self.__engine_dec_frc = CarParameter(
            'engine_dec_frc', self.mdt.phys.engine_dec_frc, (.5, -.68),
            (-10000, -100),
            lambda val: setattr(self.mdt.phys, 'engine_dec_frc', val))
        self.__brake_frc = CarParameter(
            'brake_frc', self.mdt.phys.brake_frc, (.5, -.76),
            (1, 1000),
            lambda val: setattr(self.mdt.phys, 'brake_frc', val))
        self.__pitch_control = CarParameter(
            'pitch_control', self.mdt.phys.pitch_control, (.5, -.84),
            (-10, 10), self.mdt.phys.vehicle.setPitchControl)
        self.__suspension_compression = CarParameter(
            'suspension_compression', self.mdt.phys.suspension_compression,
            (.5, -.92), (-1, 10),
            self.mdt.phys.vehicle.getTuning().setSuspensionCompression)
        self.__suspension_damping = CarParameter(
            'suspension_damping', self.mdt.phys.suspension_damping,
            (.5, -1.0), (-1, 10),
            self.mdt.phys.vehicle.getTuning().setSuspensionDamping)
        self.__max_suspension_force = CarParameter(
            'max_suspension_force', self.mdt.phys.max_suspension_force,
            (.5, -1.08), (1, 15000),
            lambda val: map(lambda whl: whl.setMaxSuspensionForce(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__max_suspension_travel_cm = CarParameter(
            'max_suspension_travel_cm', self.mdt.phys.max_suspension_travel_cm,
            (.5, -1.16), (1, 2000),
            lambda val: map(lambda whl: whl.setMaxSuspensionTravelCm(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__skid_info = CarParameter(
            'skid_info', self.mdt.phys.skid_info,
            (.5, -1.24), (-10, 10),
            lambda val: map(lambda whl: whl.setSkidInfo(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__suspension_stiffness = CarParameter(
            'suspension_stiffness', self.mdt.phys.suspension_stiffness,
            (.5, -1.32), (0, 100),
            lambda val: map(lambda whl: whl.setSuspensionStiffness(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__wheels_damping_relaxation = CarParameter(
            'wheels_damping_relaxation',
            self.mdt.phys.wheels_damping_relaxation, (.5, -1.4), (-1, 10),
            lambda val: map(lambda whl: whl.setWheelsDampingRelaxation(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__wheels_damping_compression = CarParameter(
            'wheels_damping_compression',
            self.mdt.phys.wheels_damping_compression, (.5, -1.48), (-1, 10),
            lambda val: map(lambda whl: whl.setWheelsDampingCompression(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__friction_slip = CarParameter(
            'friction_slip', self.mdt.phys.friction_slip, (.5, -1.56),
            (-1, 10),
            lambda val: map(lambda whl: whl.setFrictionSlip(val),
                            self.mdt.phys.vehicle.get_wheels()))
        self.__roll_influence = CarParameter(
            'roll_influence', self.mdt.phys.roll_influence,
            (.5, -1.64), (-1, 10),
            lambda val: map(lambda whl: whl.setRollInfluence(val),
                            self.mdt.phys.vehicle.get_wheels()))

        def set_cam_x(val):
            vec = self.mdt.logic.camera.cam_vec
            self.mdt.logic.camera.cam_vec = (val, vec[1], vec[2])
        self.__cam_x = CarParameter(
            'camera_x', self.mdt.logic.camera.cam_vec[0],
            (.5, -1.72), (-1, 1), set_cam_x)

        def set_cam_y(val):
            vec = self.mdt.logic.camera.cam_vec
            self.mdt.logic.camera.cam_vec = (vec[0], val, vec[2])
        self.__cam_y = CarParameter(
            'camera_y', self.mdt.logic.camera.cam_vec[1],
            (.5, -1.8), (-1, 1), set_cam_y)

        def set_cam_z(val):
            vec = self.mdt.logic.camera.cam_vec
            self.mdt.logic.camera.cam_vec = (vec[0], vec[1], val)
        self.__cam_z = CarParameter(
            'camera_z', self.mdt.logic.camera.cam_vec[2],
            (.5, -1.88), (-1, 1), set_cam_z)

        self.__pars = [
            self.__max_speed_par, self.__mass_par, self.__steering_min_speed,
            self.__steering_max_speed, self.__steering_clamp,
            self.__steering_inc, self.__steering_dec, self.__engine_acc_frc,
            self.__engine_dec_frc, self.__brake_frc, self.__pitch_control,
            self.__suspension_compression, self.__suspension_damping,
            self.__max_suspension_force, self.__max_suspension_travel_cm,
            self.__skid_info, self.__suspension_stiffness,
            self.__wheels_damping_relaxation,
            self.__wheels_damping_compression,
            self.__friction_slip, self.__roll_influence,
            self.__cam_x, self.__cam_y, self.__cam_z]

    def set_panel(self):
        pars = {'scale': .065, 'parent': eng.base.a2dTopRight,
                'fg': self.cargui_props.color_main, 'align': TextNode.A_left,
                'font': FontMgr().load_font(self.cargui_props.font)}
        self.speed_txt = OnscreenText(pos=(-.24, -.1), **pars)
        self.lap_txt = OnscreenText(
            text='1/' + str(self.cargui_props.laps), pos=(-.24, -.2), **pars)
        self.time_txt = OnscreenText(pos=(-.24, -.3), **pars)
        self.best_txt = OnscreenText(pos=(-.24, -.4), **pars)
        self.ranking_txt = OnscreenText(pos=(-.24, -.5), **pars)
        self.damages_txt = OnscreenText(pos=(-.24, -.6), **pars)
        self.damages_txt['text'] = '-'
        self.damages_txt['fg'] = self.cargui_props.color
        pars = {'scale': .05, 'parent': eng.base.a2dTopRight,
                'fg': self.cargui_props.color, 'align': TextNode.A_right,
                'font': FontMgr().load_font(self.cargui_props.font)}
        self.speed_lab = OnscreenText(_('speed:'), pos=(-.3, -.1), **pars)
        self.lap_lab = OnscreenText(
            text=_('lap:'), pos=(-.3, -.2), **pars)
        self.time_lab = OnscreenText(_('time:'), pos=(-.3, -.3), **pars)
        self.best_lab = OnscreenText(_('best lap:'), pos=(-.3, -.4), **pars)
        self.ranking_lab = OnscreenText(_('ranking:'), pos=(-.3, -.5), **pars)
        self.damages_lab = OnscreenText(_('damages:'), pos=(-.3, -.6), **pars)
        self.weapon_lab = OnscreenText(_('weapon:'), pos=(-.3, -.7), **pars)

    def set_weapon(self, wpn):
        self.weapon_img = OnscreenImage(
            'assets/images/weapons/%s.png' % wpn,
            scale=.05, parent=eng.base.a2dTopRight, pos=(-.2, 1, -.69))
        self.weapon_img.set_transparency(True)

    def unset_weapon(self):
        self.weapon_img.destroy()

    def apply_damage(self, reset=False):
        col = self.cargui_props.color
        if reset:
            self.damages_txt['text'] = '-'
            self.damages_txt['fg'] = col
        else:
            if self.damages_txt['text'] == '-':
                self.damages_txt['text'] = _('low')
                yellow = (col[0], col[1] - .25, col[2] - .5, col[3])
                self.damages_txt['fg'] = yellow
            elif self.damages_txt['text'] == _('low'):
                self.damages_txt['text'] = _('hi')
                red = (col[0], col[1] - .5, col[2] - .5, col[3])
                self.damages_txt['fg'] = red

    def toggle(self):
        map(lambda par: par.toggle(), self.__pars)
        if self.__max_speed_par.is_visible:
            eng.show_cursor()
        else:
            eng.hide_cursor()

    def destroy(self):
        labels = [self.speed_txt, self.time_txt, self.lap_txt,
                  self.best_txt, self.speed_lab, self.time_lab, self.lap_lab,
                  self.best_lab, self.damages_txt, self.damages_lab,
                  self.ranking_txt, self.ranking_lab, self.weapon_lab,
                  self.weapon_img]
        map(lambda wdg: wdg.destroy(), self.__pars + labels)
        Gui.destroy(self)
