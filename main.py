from ursina import *
from ursina.networking import *
from ursina.shaders import *
from direct.filter.CommonFilters import CommonFilters
from random import randint

app = Ursina(development_mode=False)
Audio('Assets/theme.wav',loop=True)
shader=lit_with_shadows_shader
filter=CommonFilters(app.win,app.cam)
playerdata={}
mp=False
peer = RPCPeer()
@rpc(peer)
def message(connection, time_received, msg: str):
    pass
@rpc(peer)
def on_connect(connection, time_connected):
	print_on_screen(f"{connection.address} joined the room!")
@rpc(peer)
def on_disconnect(connection, time_disconnected):
	print_on_screen(f"{connection.address} left the room!")

class Menu(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities,**kwargs)
        application.time_scale=0
        self.parent=camera.ui
        self.title=Entity(parent=self,model='quad',texture='title',y=.2,scale=1)
        self.sp=Button(text='Singleplayer',scale=(.5,0.25),color=color.white,parent=self)
        self.sp.text_entity.color=color.black
        self.sp.on_click=self.startsp
        self.mp=Button(text='Multiplayer (Not available yet)',scale=(.5,0.25),color=color.white,y=-.3,parent=self)
        self.mp.text_entity.color=color.black
    def startsp(self):
        application.time_scale=1
        destroy(self)
    def startmp(self):
        global mp
        mp=True
        application.time_scale=1
        destroy(self)
invoke(lambda:Menu(),delay=1.5)
poke=Entity(model='Assets/poke',shader=shader,y=1.2,z=-10,collider='box')
start_point=poke.position
road=Entity(shader=shader)
current_level=0
old_level=0
for z in range(-1,4):
    Entity(model='Assets/road',shader=shader,z=z*19.024458,parent=road,color=color.white)
road.combine()
filter.setCartoonInk(1.5)
camera_pivot=Entity()
camera.parent=camera_pivot
camera.position=(18, 20, -23)
camera.rotation_y=-37.5
camera.rotation_x=32.963
moving=False

def update():
    global moving, current_level, old_level
    if mp:
        peer.update()
    moving=False
    if held_keys['w'] and not moving:
        poke.rotation_y=lerp_angle(poke.rotation_y,0,time.dt*10)
        moving=True
    if held_keys['s'] and not moving:
        poke.rotation_y=lerp_angle(poke.rotation_y,180,time.dt*10)
        moving=True
    if held_keys['a'] and not moving:
        poke.rotation_y=lerp_angle(poke.rotation_y,-90,time.dt*10)
        moving=True
    if held_keys['d'] and not moving:
        poke.rotation_y=lerp_angle(poke.rotation_y,90,time.dt*10)
        moving=True
    if moving and (poke.x > -15.3379 and poke.x < 22.9091 and poke.z>-11):
        poke.position+=poke.forward*time.dt*(7*(1+current_level/100))
    elif poke.x<=-15.3379:
        poke.x+=time.dt
    elif poke.x>=22.9091:
        poke.x-=time.dt
    elif poke.z<-11:
        poke.z+=time.dt
    if old_level != current_level:
        exec(f'Car({current_level})')
    current_level=floor((poke.z-start_point.z)/19.024458)
    if current_level>=0:
        road.z=floor((poke.z-start_point.z)/19.024458)*19.024458
    else:
        current_level=0
    camera_pivot.position=lerp(camera_pivot.position,poke.position,time.dt*5)
    old_level=current_level
def restart_light():
    render.clearLight(light._light_np)
    render.setLight(light._light_np)

class Car(Entity):
    def __init__(self, level=0,add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, model='Assets/car',shader=shader,**kwargs)
        self.level=level
        self.choice=randint(0,1)
        self.collider='box'
        if self.choice>0:
            self.rotation_y=90
            self.z=-3+(current_level)*19.024458
            self.x=-30
        else:
            self.rotation_y=-90
            self.z=3+(current_level)*19.024458
            self.x=30
        self.speed=(10+(current_level/10))*(1+current_level/10)
    def update(self):
        global current_level
        self.position+=self.forward*self.speed*time.dt
        if self.x < -30 or self.x > 30:
            destroy(self)
        if self.level!=current_level:
            destroy(self)
        if self.intersects(poke):
            poke.z=-10
            poke.x=0
            current_level=0
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
        self.changegamma=Slider(text='Gamma',min=0,max=1,parent=self,scale=(1,2),x=-.375,y=-.2,dynamic=True,default=1)
        self.changegamma.on_value_changed=self.changeGamma
        self.smreschange=Slider(text='Shadow map resolution',min=0,max=4096,parent=self,scale=(1,2),x=-.19,y=-.4,default=1024,step=512)
        self.smreschange.on_value_changed=self.shadow_map_change
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
    def shadow_map_change(self):
        light.shadow_map_resolution=(self.smreschange.value,self.smreschange.value)
        restart_light()
    def update(self):
        if self.togglelight.value>0:
            self.togglelight.knob.text_entity.text='On'
        else:
            self.togglelight.knob.text_entity.text='Off'
class TaskManager(Entity):
    def __init__(self, add_to_scene_entities=True, **kwargs):
        super().__init__(add_to_scene_entities, **kwargs)
    def update(self):
        
        peer.update()

        score.text=f'{current_level}'
        pivot.position=poke.position
    @every(1/(current_level+1))
    def cars(self):
        exec(f'Car({current_level})')
TaskManager()
score=Text(text=f'{current_level}',y=.5,scale=3)
settings=Setting()
settings.disable()
def toggleSetting():
    global settings
    if settings.enabled:
        settings.disable()
    else:
        settings.enable()
def input(key):
    if key=='q':
        toggleSetting()

pivot=Entity()
light=DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
light._light_np=light.attachNewNode(light._light)

Sky(texture='sky_sunset')

app.run()