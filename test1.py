from ursina import *

app=Ursina()
Entity(model='Assets/poke')
pivot=Entity()
light=DirectionalLight(parent=pivot, y=2, z=3, shadows=True, rotation=(45, -45, 45))
EditorCamera()

app.run()