from ursina import *

app = Ursina()

player = Entity(model='wireframe_cube', color=color.lime)
player.forward_indicator = Entity(parent=player, model=Cone(mode='line'), rotation_x=90, z=.5, color=color.orange)
def input(key):
    if key == 'w':
        player.rotation_y = 0
    if key == 'd':
        player.rotation_y = 90
    if key == 's':
        player.rotation_y = 180
    if key == 'a':
        player.rotation_y = 270


def lerp_angle(start_angle, end_angle, t):
    start_angle = start_angle % 360
    end_angle = end_angle % 360
    angle_diff = (end_angle - start_angle + 180) % 360 - 180
    result_angle = start_angle + t * angle_diff
    result_angle = (result_angle + 360) % 360
    return result_angle

graphics = duplicate(player, parent=scene)
def update():
    graphics.position = player.position
    graphics.rotation_y = lerp_angle(graphics.rotation_y, player.rotation_y, time.dt * 5)

EditorCamera()

app.run()