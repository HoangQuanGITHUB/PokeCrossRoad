from ursina import *

app=Ursina()
cube = Entity(model="cube", collider="box", texture="acacia_log", position=(0, 0, 3), ignore=True, parent=camera)

def update():

    #torch_light.rotation_y = lerp(torch_light.rotation_y, mouse.velocity.x, time.dt*5)
    cube.rotation_y = lerp(cube.rotation_y, mouse.velocity.x, time.dt*5)
    #camera.rotation_z = lerp(camera.rotation_z, mouse.velocity.x, time.dt*5)

app.run()