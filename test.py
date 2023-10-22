from ursina import *
import panda3d.bullet as blt

app = Ursina(borderless=False)

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
ground = Entity(model='plane', texture='grass', scale=(200, 1, 200))
shape = blt.BulletBoxShape(Vec3(100.0, 1.0, 100.0))
collision_node = blt.BulletRigidBodyNode('Rigidbody')
collision_node.addShape(shape)
ground_np = render.attachNewNode(collision_node)
ground_np.setPos(0, -2, 0)
world.attachRigidBody(collision_node)
ground.parent = ground_np
ground.y = 1

def spawn_cube():
    # Cube
    cube = Entity(model='cube', texture='brick')
    shape2 = blt.BulletBoxShape(Vec3(.5, .5, .5))
    node = blt.BulletRigidBodyNode('Rigidbody')
    node.setMass(1)
    node.addShape(shape2)
    np = render.attachNewNode(node)
    np.setPos(0, 50, 0)
    world.attachRigidBody(node)
    cube.parent = np

def update():
    world.doPhysics(time.dt)

def input(key):
    if key == 'space up':
        spawn_cube()

Sky()

EditorCamera()

app.run()