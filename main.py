from ursina import *
from ursina.shaders import *
from direct.filter.CommonFilters import CommonFilters
from random import randint

app = Ursina(development_mode=False ,show_ursina_splash=True)
Audio('theme.mp3',loop=True)

shader=lit_with_shadows_shader
filter=CommonFilters(app.win,app.cam)
poke=Entity(model='poke',shader=shader,y=1.2,z=-10,collider='box')
poker=Entity(parent=poke)
start_point=poke.position
road=Entity(shader=shader)
current_level=0
for z in range(3):
    Entity(model='road',shader=shader,z=z*19.024458,parent=road,color=color.white)
road.combine()

Sky(texture='sky_sunset')
filter.setCartoonInk(2)
camera_pivot=Entity()
camera.parent=camera_pivot
camera.position=(0,1,-30)
camera_pivot.rotation_y=-30 
camera_pivot.rotation_x=20
moving=False
def lerp_angle(start_angle, end_angle, t):
    start_angle = start_angle % 360
    end_angle = end_angle % 360
    angle_diff = (end_angle - start_angle + 180) % 360 - 180
    result_angle = start_angle + t * angle_diff
    result_angle = (result_angle + 360) % 360
    return result_angle

def update():
    global moving, current_level
    moving=False
    if held_keys['w'] and not moving and not stop:
        poke.rotation_y=lerp_angle(poke.rotation_y,0,time.dt*10)
        moving=True
    if held_keys['s'] and not moving and not stop:
        poke.rotation_y=lerp_angle(poke.rotation_y,180,time.dt*10)
        moving=True
    if held_keys['a'] and not moving and not stop:
        poke.rotation_y=lerp_angle(poke.rotation_y,-90,time.dt*10)
        moving=True
    if held_keys['d'] and not moving and not stop:
        poke.rotation_y=lerp_angle(poke.rotation_y,90,time.dt*10)
        moving=True
    if moving and (poke.x > -15.3379 and poke.x < 22.9091):
        poke.position+=poke.forward*time.dt*5
    elif poke.x<=-15.3379:
        poke.x+=time.dt
    elif poke.x>=22.9091:
        poke.x-=time.dt
    road.z=floor((poke.z-start_point.z)/19.024458)*19.024458
    current_level=floor((poke.z-start_point.z)/19.024458)
    camera_pivot.position=lerp(camera_pivot.position,poke.position,time.dt*5)

class Car(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, model='Camaro',scale=2,y=.5,shader=lit_with_shadows_shader,**kwargs)
        self.choice=randint(0,1)
        self.collider='box'
        if self.choice>0:
            self.rotation_y=90
            self.z=-3+(current_level)*19.024458
            self.x=-20
        else:
            self.rotation_y=-90
            self.z=3+(current_level)*19.024458
            self.x=20
        self.speed=5
        self.color=color.random_color()
    def update(self):
        self.position+=self.forward*self.speed*time.dt
        if self.x < -30 or self.x > 30:
            destroy(self)
        if self.intersects(poke):
            exit()

class Setting(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad',parent=camera.ui,**kwargs)
        self.scale=(1,.5)
        self.color=color.rgb(94,94,94)
        self.MSAAsetting=Slider(text='MSAA',min=0,max=32,step=1,parent=self,scale=(1,2),x=-.4,y=.4)
        self.MSAAsetting.on_value_changed=self.changeMSAA
        self.bloomsetting=Slider(text='Bloom',min=0,max=1,parent=self,scale=(1,2),x=-.4,y=.2,dynamic=True)
        self.bloomsetting.on_value_changed=self.changebloom
        self.togglelight=Slider(text='Lights',min=0,max=1,step=1,parent=self,scale=(1,2),x=-.4,y=0,default=1)
        self.togglelight.on_value_changed=self.toggleLight
        self.changegamma=Slider(text='Adjust Gamma',min=0,max=1,parent=self,scale=(1,2),x=-.3,y=-.2,dynamic=True,default=1)
        self.changegamma.on_value_changed=self.changeGamma
    def changeMSAA(self):
        filter.delMSAA()
        filter.setMSAA(self.MSAAsetting.value)
    def changebloom(self):
        filter.delBloom()
        filter.setBloom(intensity=self.bloomsetting.value)
    def changeGamma(self):
        filter.delGammaAdjust()
        filter.setGammaAdjust(self.changegamma.value)
    def toggleLight(self):
        global light
        if self.togglelight.value>0:
            self.togglelight.knob.text_entity.text='On'
            render.setLight(light._light_np)
        else:
            self.togglelight.knob.text_entity.text='Off'
            render.clearLight(light._light_np)
    def update(self):
        if self.togglelight.value>0:
            self.togglelight.knob.text_entity.text='On'
        else:
            self.togglelight.knob.text_entity.text='Off'
class TaskManager(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
    @every((current_level+1)*1)
    def onesec(self):
        exec('Car()')
TaskManager()
settings=Setting()
settings.disable()
stop=False
def toggleSetting():
    global settings, stop
    if settings.enabled:
        settings.disable()
        stop=False
    else:
        settings.enable()
        stop=True
def input(key):
    if key=='q':
        toggleSetting()
pivot=Entity()

light=DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, 90, 45))
light.shadow_map_resolution = (1024,1024)

app.run()