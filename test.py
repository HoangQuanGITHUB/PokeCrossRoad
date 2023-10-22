from ursina import *

app = Ursina(borderless = False)

import panda3d.bullet as blt

debugNode = blt.BulletDebugNode('Debug')
debugNode.showWireframe(True)
debugNode.showConstraints(True)
debugNode.showBoundingBoxes(False)
debugNode.showNormals(False)
debugNP = render.attachNewNode(debugNode)
debugNP.show()

world = blt.BulletWorld()
world.setGravity(Vec3(0, -9.81, 0))
world.setDebugNode(debugNP.node())

# Ground
ground = Entity(model = 'plane', texture = 'grass', scale = (200, 1, 200))

shape = blt.BulletBoxShape(Vec3(100.0, 0.100, 100.0))

collision_node = blt.BulletRigidBodyNode('Rigidbody')
collision_node.addShape(shape)

ground_np = render.attachNewNode(collision_node)
ground_np.setPos(0, -2, 0)
world.attachRigidBody(collision_node)
ground.parent = ground_np

def spawn_cube():
    cube = Entity(model = 'cube', texture = 'brick')

    shape = blt.BulletBoxShape(Vec3(.5, .5, .5))

    collision_node = blt.BulletRigidBodyNode('Rigidbody')
    collision_node.setMass(1)
    collision_node.addShape(shape)

    cube_np = render.attachNewNode(collision_node)
    cube_np.setPos(0, 50, 0)
    world.attachRigidBody(collision_node)
    cube.parent = cube_np


spawnButton_1 = Button(model = 'cube', color = color.green, parent = scene)
spawnButton_1.on_click = spawn_cube

def update():
    world.doPhysics(time.dt)

Sky()

EditorCamera()

app.run()