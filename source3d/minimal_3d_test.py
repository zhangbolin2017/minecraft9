from ursina import AmbientLight, DirectionalLight, Entity, Text, Ursina, Vec3, camera, color, time, window


app = Ursina()

window.title = "Minecraft9 Minimal 3D Test"
window.borderless = False
window.color = color.rgba(18/255.0, 24/255.0, 38/255.0, 1.0)

ground = Entity(
    model="plane",
    scale=(18, 1, 18),
    color=color.rgba(70/255.0, 90/255.0, 70/255.0, 1.0),
    rotation_x=0,
)

center_cube = Entity(
    model="cube",
    position=(0, 1, 0),
    scale=2,
    color=color.azure,
)

left_cube = Entity(
    model="cube",
    position=(-4, 1, 3),
    scale=2,
    color=color.orange,
)

right_cube = Entity(
    model="cube",
    position=(4, 1, 2),
    scale=2,
    color=color.lime,
)

back_cube = Entity(
    model="cube",
    position=(0, 1, 6),
    scale=2,
    color=color.red,
)

AmbientLight(color=color.rgba(160/255.0, 160/255.0, 160/255.0, 1.0))
sun = DirectionalLight()
sun.look_at(Vec3(1, -1, -1))

camera.position = (12, 10, -20)
camera.look_at(Vec3(0, 1, 2))

Text(
    text=(
        "Minimal 3D Test\n"
        "You should see a dark background,\n"
        "a green floor, and 4 colored cubes.\n"
        "The blue cube rotates slowly."
    ),
    x=-0.86,
    y=0.45,
    scale=1.0,
    color=color.white,
)


def update():
    center_cube.rotation_y += 35 * time.dt


if __name__ == "__main__":
    app.run()
