from ursina import *
from ursina.shaders import *
from direct.filter.CommonFilters import CommonFilters

app = Ursina(development_mode=False ,show_ursina_splash=True)
Audio('theme.mp3',loop=True)

shader=lit_with_shadows_shader
filter=CommonFilters(app.win,app.cam)
poke=Entity(model='poke',shader=shader,y=1.2,z=-10)
start_point=poke.position
road=Entity(shader=shader)
for z in range(3):
    Entity(model='road',shader=shader,z=z*25,parent=road,color=color.white)
road.combine()

Sky(texture='sky_sunset')
filter.setCartoonInk()
filter.setMSAA(16)
filter.setBloom(intensity=.2)

camera_pivot=Entity()
camera.parent=camera_pivot
camera.position=(0,1,-30)
camera_pivot.rotation_y=-30 
camera_pivot.rotation_x=20

def update():
    if held_keys['w']:
        poke.rotation_y=lerp(poke.rotation_y,0,time.dt*10)
    elif held_keys['s']:
        poke.rotation_y=lerp(poke.rotation_y,180,time.dt*10)
    elif held_keys['a']:
        poke.rotation_y=lerp(poke.rotation_y,-90,time.dt*10)
    elif held_keys['d']:
        poke.rotation_y=lerp(poke.rotation_y,90,time.dt*10)
    if (held_keys['w'] or held_keys['s'] or held_keys['a'] or held_keys['d']) and (poke.x > -15.3379 and poke.x < 22.9091):
        poke.position+=poke.forward*time.dt*5
    elif poke.x<=-15.3379:
        poke.x+=time.dt
    elif poke.x>=22.9091:
        poke.x-=time.dt
    road.z=floor((poke.z-start_point.z)/29)*25
    camera_pivot.position=lerp(camera_pivot.position,poke.position,time.dt*5)
Draggable
class Setting(Entity):
    def __init__(self, **kwargs):
        super().__init__(model='quad',radius=.1,**kwargs)
settings=None
def openSetting():
    global settings
    settings=Setting()

def input(key):
    if key=='q':
        openSetting()

pivot = Entity()
light=DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, 90, 45))

app.run()