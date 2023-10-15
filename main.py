from ursina import *
from ursina.shaders import lit_with_shadows_shader
from direct.filter.CommonFilters import CommonFilters
app = Ursina(development_mode=False)

filter=CommonFilters(app.win,app.cam)

Audio('theme.mp3',loop=True)

poke=Entity(model='poke',shader=lit_with_shadows_shader,y=1.2)
for z in range(10):
    Entity(model='road',shader=lit_with_shadows_shader,z=z*25)

filter.setCartoonInk()
filter.setMSAA(32)
filter.setBloom(intensity=.1)

camera_pivot=Entity()
camera.parent=camera_pivot
camera.position=(0,.5,-30)
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
    camera_pivot.position=lerp(camera_pivot.position,poke.position,time.dt*5)

pivot = Entity()
light=DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, 90, 45))
def input(key):
    if key=='q':
        light.disable()
    if key=='e':
        light.enable()

app.run()