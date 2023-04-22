from ursina import *
from ursina.shaders import lit_with_shadows_shader
from ursina.lights import DirectionalLight

from simulators.ursina.ursina_mesh import create_sphere

shader = lit_with_shadows_shader
shader.default_input = {
    'texture_scale': Vec2(1, 1),
    'texture_offset': Vec2(0, 0),
    'shadow_color': Vec4(0.1, 0.1, 0.1, .5),
}

Entity.default_shader = shader

app = Ursina()

moon = Entity(model=create_sphere(0.5, 32), texture="../textures/moon.png", y=1, color=color.light_gray)
earth = Entity(model=create_sphere(0.5, 32), texture='../textures/earth.png', y=1, x=1, z=3)
e_pos = earth.position

sun = DirectionalLight(shadow_map_resolution=(1024, 1024), position=[e_pos[0], e_pos[1] + 1, e_pos[2] + 1])
sun.look_at(moon)
sun._light.show_frustum()


# light = PointLight(parent=earth, intensity=10, range=10, color=color.white)


def update():
    moon.x += (held_keys['d'] - held_keys['a']) * time.dt
    moon.y += (held_keys['e'] - held_keys['q']) * time.dt
    moon.z += (held_keys['w'] - held_keys['s']) * time.dt
    sun.update_bounds()


# scene.fog_density = (100, 500)
# scene.fog_color = color.orange
# scene.fog_density = (10, 50)
Sky(color=color.light_gray, texture="../textures/cosmic1.png")
EditorCamera()

app.run()
