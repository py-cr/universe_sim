# -*- coding:utf-8 -*-
# title           :水滴
# description     :水滴
# author          :Python超人
# date            :2023-08-02
# link            :https://gitcode.net/pythoncr/
# python_version  :3.8
# ==============================================================================
from objs.obj import Obj


class WaterDrop(Obj):
    """
    水滴
    来源：https://www.cgmodel.com/model/500318.html
    """

    def __init__(self, name="水滴", mass=5.97237e24,
                 init_position=[0, 0, 0],
                 init_velocity=[0, 0, 0],
                 texture="drops.png", size_scale=1.0, distance_scale=1.0,
                 ignore_mass=False, density=1e3, color=(7, 0, 162),
                 trail_color=None, show_name=False,
                 model="drops.obj", rotation=(0, 0, 0),
                 parent=None, gravity_only_for=[]):
        params = {
            "name": name,
            "mass": mass,
            "init_position": init_position,
            "init_velocity": init_velocity,
            "density": density,
            "color": color,
            "texture": texture,
            "size_scale": size_scale,
            "distance_scale": distance_scale,
            "ignore_mass": ignore_mass,
            "trail_color": trail_color,
            "show_name": show_name,
            "parent": parent,
            "rotation": rotation,
            "gravity_only_for": gravity_only_for,
            "model": model
        }
        super().__init__(**params)

from ursina.prefabs.primitives import Shader

matcap_shader = Shader(name='matcap_shader', language=Shader.GLSL, vertex = '''#version 140
uniform mat4 p3d_ModelViewProjectionMatrix;
uniform mat4 p3d_ModelMatrix;
uniform mat4 p3d_ModelViewMatrix;
uniform mat3 p3d_NormalMatrix;
in vec4 p3d_Vertex;
in vec3 p3d_Normal;

out vec3 eye;
out vec3 view_normal;
// reflect alternative:
// r = e - 2. * dot( n, e ) * n;

void main() {
    gl_Position = p3d_ModelViewProjectionMatrix * p3d_Vertex;

    eye = normalize(vec3(p3d_ModelViewMatrix * vec4(p3d_Vertex.xyz, 1.0)));
    view_normal = normalize( p3d_NormalMatrix * p3d_Normal );
}
''',
fragment='''
#version 130
uniform sampler2D p3d_Texture0;
uniform vec4 p3d_ColorScale;

in vec3 eye;
in vec3 view_normal;
out vec4 fragColor;

void main() {

    vec3 r = reflect( eye, view_normal );
    float m = 2. * sqrt( pow( r.x, 2. ) + pow( r.y, 2. ) + pow( r.z + 1., 2. ) );
    vec2 vN = r.xy / m + .5;

    vec3 base = texture2D( p3d_Texture0, vN ).rgb;
    // vec3 base = texture2D( p3d_Texture0, uv ).rgb;
    fragColor = vec4( base, 1. ) * p3d_ColorScale;
}

''',
)

if __name__ == '__main__':


    shader = matcap_shader

    water_drop = WaterDrop(
        # texture="drops_normal.png"
        # texture="drops_uvw.png"
        texture="drops.png"
    )
    water_drop.init_velocity = [0, 0, -10]
    print(water_drop)


    def on_ready():
        water_drop.planet.rotation_x = 90
        water_drop.planet.shader = shader,


    water_drop.show_demo(size_scale=1000000, on_ready_fun=on_ready)
