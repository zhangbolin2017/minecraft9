from ursina import *
app = Ursina()

# Triangle 1: CCW
verts1 = [Vec3(-2, 0, 0), Vec3(-1, 0, 0), Vec3(-1, 1, 0)]
m1 = Mesh(vertices=verts1, colors=[color.red]*3)
e1 = Entity(model=m1, position=(0,0,0))

# Triangle 2: CW
verts2 = [Vec3(1, 0, 0), Vec3(1, 1, 0), Vec3(2, 0, 0)]
m2 = Mesh(vertices=verts2, colors=[color.green]*3)
e2 = Entity(model=m2, position=(0,0,0))

camera.position = (0, 0.5, -5)

def update():
    pass

import threading
import time
def close():
    time.sleep(2)
    application.quit()
threading.Thread(target=close).start()

app.run()
